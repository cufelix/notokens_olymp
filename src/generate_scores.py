"""generate_scores.py — VoltPlán suitability scoring (kontrakt pro aplikaci).

Vyrobí `submissions/app_zone_scores.csv` — JEDINÝ soubor, který appka čte. Skóre
NEvychází z natvrdo zadaných čísel, ale z natrénovaného LightGBM + reálných dat o síti,
stanicích a férovosti. Sandbox: trénuje na zones_train, skóruje zones_validation (holdout).

Suitability (0–100) = vážená kombinace:
  predicted_demand_2030  (LightGBM, hlavní AI signál)   váha 0.40
  coverage_gap           (poptávka vs. stávající stanice) váha 0.30
  grid_headroom          (rezerva sítě, kde unese)        váha 0.15
  equity_weight          (domácnosti bez vlastního stání) váha 0.15

ANTI-LEAKAGE: cíle target_*_2030_synthetic a sloupce z nich odvozené NEJSOU featury
(viz feature_cols z train_demand). Skóruje se na holdoutu, ne na tréninku.

    python src/generate_scores.py
"""
from __future__ import annotations

import pathlib
import pickle

import numpy as np
import polars as pl

from train_demand import DROP_HINTS, ID_HINTS, feature_cols  # sdílená anti-leakage logika

ROOT = pathlib.Path(__file__).resolve().parent.parent
_PART = ROOT / "data" / "participants"
DATA = _PART / "core" if (_PART / "core").exists() else _PART
SUB = ROOT / "submissions"

TARGET = "estimated_ev_count_2030_synthetic"  # poptávka 2030 = hlavní AI signál
WEIGHTS = {"demand": 0.40, "gap": 0.30, "grid": 0.15, "equity": 0.15}


def load(name: str) -> pl.DataFrame:
    hits = list(DATA.rglob(name))
    if not hits:
        raise SystemExit(f"Nenalezen {name} v {DATA} — rozbal data (viz DATA-MAP.md)")
    return pl.read_csv(hits[0], infer_schema_length=10_000, ignore_errors=True)


def minmax(a: np.ndarray) -> np.ndarray:
    lo, hi = float(np.nanmin(a)), float(np.nanmax(a))
    if hi - lo < 1e-9:
        return np.zeros_like(a, dtype=float)
    return (a - lo) / (hi - lo)


# Přibližné centroidy 22 správních obvodů Prahy (zóny nemají obvod → GIS aproximace).
DISTRICT_CENTROIDS = {
    "Praha 1": (50.088, 14.420), "Praha 2": (50.075, 14.435), "Praha 3": (50.082, 14.450),
    "Praha 4": (50.040, 14.450), "Praha 5": (50.070, 14.380), "Praha 6": (50.100, 14.380),
    "Praha 7": (50.105, 14.430), "Praha 8": (50.115, 14.460), "Praha 9": (50.110, 14.500),
    "Praha 10": (50.065, 14.480), "Praha 11": (50.030, 14.500), "Praha 12": (50.000, 14.430),
    "Praha 13": (50.050, 14.340), "Praha 14": (50.105, 14.540), "Praha 15": (50.050, 14.530),
    "Praha 16": (49.980, 14.360), "Praha 17": (50.055, 14.310), "Praha 18": (50.135, 14.510),
    "Praha 19": (50.130, 14.545), "Praha 20": (50.120, 14.600), "Praha 21": (50.080, 14.660),
    "Praha 22": (50.020, 14.560),
}


def district_map(val: pl.DataFrame) -> pl.Series:
    """Přiřadí obvod každé zóně podle nejbližšího centroidu správního obvodu (aproximace)."""
    names = list(DISTRICT_CENTROIDS)
    cen = np.array([DISTRICT_CENTROIDS[n] for n in names])  # (22, 2)
    lat = val.get_column("center_lat_real").to_numpy()
    lon = val.get_column("center_lon_real").to_numpy()
    pts = np.column_stack([lat, lon])  # (N, 2)
    d2 = ((pts[:, None, :] - cen[None, :, :]) ** 2).sum(axis=2)  # (N, 22)
    labels = [names[int(i)] for i in d2.argmin(axis=1)]
    return pl.Series("district", labels)


REC_TARGET = "target_recommended_solution_synthetic"


def recommend_type(train: pl.DataFrame, val: pl.DataFrame, feats: list[str]) -> tuple[list[str], float]:
    """Doporučený typ stanice = LightGBM klasifikátor (recommender) na anti-leakage featurách.

    Trénuje na zones_train, predikuje na zones_validation, vrací i accuracy vs ground truth.
    """
    import lightgbm as lgb

    ytr = train.get_column(REC_TARGET).to_list()
    classes = sorted(set(ytr))
    cmap = {c: i for i, c in enumerate(classes)}
    ytr_i = np.array([cmap[c] for c in ytr])

    clf = lgb.LGBMClassifier(
        n_estimators=400, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, random_state=42, verbose=-1,
    )
    clf.fit(train.select(feats).to_numpy(), ytr_i)
    pred_i = clf.predict(val.select(feats).to_numpy())
    pred = [classes[int(i)] for i in pred_i]

    acc = float("nan")
    if REC_TARGET in val.columns:
        yva = val.get_column(REC_TARGET).to_list()
        acc = float(np.mean([p == t for p, t in zip(pred, yva)]))
    return pred, acc


def reasons(row: dict) -> str:
    r = []
    if row["demand_n"] >= 0.6:
        r.append("vysoká predikovaná poptávka 2030")
    if row["gap_n"] >= 0.6:
        r.append("málo stávajících stanic vůči poptávce")
    if row["grid_n"] >= 0.6:
        r.append("volná kapacita sítě")
    elif row["grid_n"] <= 0.25:
        r.append("⚠ omezená rezerva sítě")
    if row["equity_n"] >= 0.6:
        r.append("mnoho domácností bez vlastního stání")
    if not r:
        r.append("průměrný profil zóny")
    return "; ".join(r[:3])


def main() -> None:
    train = load("zones_train.csv")
    val = load("zones_validation.csv")
    solutions = load("candidate_solutions.csv")

    # --- 1) LightGBM: predikce poptávky (anti-leakage feature_cols) ---
    feats = feature_cols(train, TARGET)
    print(f"Featur (po anti-leakage): {len(feats)}")
    leaky = [c for c in feats if any(h in c.lower() for h in DROP_HINTS)]
    assert not leaky, f"LEAKAGE: {leaky}"

    Xtr = train.select(feats).to_numpy()
    ytr = train.get_column(TARGET).to_numpy()
    Xva = val.select(feats).to_numpy()

    import lightgbm as lgb

    model = lgb.LGBMRegressor(
        n_estimators=600, learning_rate=0.03, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8, random_state=42, verbose=-1,
    )
    model.fit(Xtr, ytr)
    pred = np.clip(model.predict(Xva), 0, None)

    SUB.mkdir(exist_ok=True)
    with open(SUB / "lgbm_model.pkl", "wb") as f:
        pickle.dump(model, f)

    # --- 2) komponenty suitability z reálných dat ---
    grid = val.get_column("reserve_margin_pct_2025_synthetic").to_numpy().astype(float)
    cur_points = val.get_column("charging_points_2026_real").to_numpy().astype(float)
    equity = val.get_column("no_private_parking_index_derived").to_numpy().astype(float)

    demand_n = minmax(pred)
    grid_n = minmax(grid)
    equity_n = minmax(equity)
    # coverage gap = relativní neuspokojená poptávka (poptávka − stávající nabídka)
    coverage_gap = np.clip(demand_n - minmax(cur_points), 0, None)
    gap_n = minmax(coverage_gap)

    suitability = 100.0 * (
        WEIGHTS["demand"] * demand_n
        + WEIGHTS["gap"] * gap_n
        + WEIGHTS["grid"] * grid_n
        + WEIGHTS["equity"] * equity_n
    )

    rec_type, rec_acc = recommend_type(train, val, feats)
    print(f"Recommender (typ stanice) accuracy na validaci: {rec_acc:.1%}")

    # --- 3) sestav kontrakt ---
    out = pl.DataFrame({
        "grid_zone_id": val.get_column("grid_zone_id"),
        "center_lat": val.get_column("center_lat_real"),
        "center_lon": val.get_column("center_lon_real"),
        "population": val.get_column("population_census_2021_real"),
        "predicted_demand_2030": np.round(pred, 1),
        "grid_headroom": np.round(grid, 1),
        "current_stations": val.get_column("charging_stations_2026_real"),
        "current_points": cur_points.astype(int),
        "coverage_gap": np.round(coverage_gap, 3),
        "equity_weight": np.round(equity, 3),
        "suitability_score": np.round(suitability, 1),
        "recommended_type": rec_type,
        # pomocné normalizované složky pro "proč"
        "demand_n": np.round(demand_n, 3),
        "gap_n": np.round(gap_n, 3),
        "grid_n": np.round(grid_n, 3),
        "equity_n": np.round(equity_n, 3),
    })
    out = out.with_columns(district_map(val))
    out = out.with_columns(
        pl.struct(["demand_n", "gap_n", "grid_n", "equity_n"])
        .map_elements(reasons, return_dtype=pl.Utf8)
        .alias("top_reasons")
    )

    # join počet portů/výkon z candidate_solutions k doporučenému typu
    sol = solutions.select([
        pl.col("solution_type").alias("recommended_type"),
        pl.col("ports").alias("recommended_ports"),
        pl.col("total_power_kw").alias("recommended_total_kw"),
    ])
    out = out.join(sol, on="recommended_type", how="left")

    cols = [
        "grid_zone_id", "district", "center_lat", "center_lon", "population",
        "predicted_demand_2030", "grid_headroom", "current_stations", "current_points",
        "coverage_gap", "equity_weight", "suitability_score", "recommended_type",
        "recommended_ports", "recommended_total_kw", "top_reasons",
    ]
    out = out.select(cols).sort("suitability_score", descending=True)
    out.write_csv(SUB / "app_zone_scores.csv")

    # thin kompat soubor pro starší appky (app.py / app_complete.py)
    out.select([
        pl.col("grid_zone_id"),
        pl.col("predicted_demand_2030").alias("estimated_ev_count_2030_synthetic"),
        pl.col("recommended_type").alias("target_recommended_solution_synthetic"),
        pl.col("recommended_ports").alias("target_recommended_ports_synthetic"),
        pl.col("recommended_total_kw").alias("target_recommended_total_kw_synthetic"),
    ]).write_csv(SUB / "sample_submission.csv")

    print(f"\n>>> {SUB / 'app_zone_scores.csv'}  ({out.height} zón)")
    print(out.select(["grid_zone_id", "district", "suitability_score",
                      "predicted_demand_2030", "grid_headroom", "current_stations",
                      "recommended_type", "top_reasons"]).head(8))
    print("\nDistribuce obvodů (top 10):")
    print(out.group_by("district").len().sort("len", descending=True).head(10))


if __name__ == "__main__":
    main()
