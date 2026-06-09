"""train_demand.py — Linie A: predikce poptávky/zátěže + baseline + interpretace.

SANDBOX (ne soutěž): žádný skrytý test set, žádné odevzdání predikcí. Validuješ si SÁM —
trénuješ na zones_train.csv, ověřuješ na zones_validation.csv (nebo vlastním holdoutu).

ADAPTIVNÍ: nezná přesné názvy sloupců předem. Sám:
  1. najde cílové sloupce (target_* / *_2030_synthetic),
  2. vyhodí leakage (cíle + sloupce z nich odvozené + ID),
  3. natrénuje LightGBM na vybraný cíl,
  4. změří MAE/RMSE proti baseline (průměr + ∝ populace) + Precision@50 na validaci,
  5. uloží predikce na validační zóny do submissions/predictions_validation.csv (pro demo/mapu).

Spuštění (po rozbalení dat do data/participants/):
    python src/train_demand.py                 # auto-vybere první cíl
    python src/train_demand.py --target target_daily_kwh_2030_synthetic
    python src/train_demand.py --list          # jen vypíše cíle a skončí

⚠ Na místě zkontroluj auto-detekci (vypisuje se) — když sedí, jedeš; když ne, dej --target
  a uprav DROP_HINTS dle reálných názvů.
"""
from __future__ import annotations
import argparse
import pathlib
import sys
import numpy as np
import polars as pl

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "participants"
SUB = ROOT / "submissions"

ID_HINTS = ("grid_zone_id", "transformer_station_id", "parent_substation_id", "split", "_id")
# featury, které jsou de-facto cíl/odvozené z cíle → leakage. Uprav podle reálných názvů.
DROP_HINTS = ("target_", "_2030_synthetic", "recommended_", "risk_overload")


def find_file(name: str) -> pathlib.Path:
    hits = list(DATA.rglob(name))
    if not hits:
        sys.exit(f"Nenalezen {name} v {DATA} — rozbal data, viz DATA-MAP.md")
    return hits[0]


def load(name: str) -> pl.DataFrame:
    return pl.read_csv(find_file(name), infer_schema_length=10_000, ignore_errors=True)


def target_cols(df: pl.DataFrame) -> list[str]:
    return [c for c in df.columns if "target_" in c or c.endswith("_2030_synthetic")]


def feature_cols(df: pl.DataFrame, target: str) -> list[str]:
    out = []
    for c in df.columns:
        cl = c.lower()
        if c == target:
            continue
        if any(h in cl for h in DROP_HINTS):      # leakage guard
            continue
        if any(h in cl for h in ID_HINTS):
            continue
        if df.schema[c] in (pl.Utf8, pl.Categorical, pl.Boolean):
            continue                               # MVP: jen numerika (kategorie přidej když je čas)
        out.append(c)
    return out


def population_col(df: pl.DataFrame) -> str | None:
    for c in df.columns:
        if "population" in c.lower() or "obyvatel" in c.lower():
            return c
    return None


def precision_at_k(y_true: np.ndarray, y_pred: np.ndarray, k: int = 50) -> float:
    k = min(k, len(y_true))
    top_true = set(np.argsort(y_true)[-k:])
    top_pred = set(np.argsort(y_pred)[-k:])
    return len(top_true & top_pred) / k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    train = load("zones_train.csv")
    val = load("zones_validation.csv")   # sandbox: vlastní ověření (žádný skrytý test set)

    targets = target_cols(train)
    if not targets:
        sys.exit("Nenašel jsem cílové sloupce (target_* / *_2030_synthetic) — zkontroluj data.")
    print("Cílové sloupce:", *targets, sep="\n  ")
    if args.list:
        return
    target = args.target or targets[0]
    print(f"\n>>> Trénuju na cíli: {target}")

    feats = feature_cols(train, target)
    print(f"Featur: {len(feats)} (leakage sloupce vyhozené). Prvních 12: {feats[:12]}")

    Xtr, ytr = train.select(feats).to_numpy(), train.get_column(target).to_numpy()
    Xva, yva = val.select(feats).to_numpy(), val.get_column(target).to_numpy()

    try:
        import lightgbm as lgb
    except ImportError:
        sys.exit("Chybí lightgbm → uv pip install -r requirements.txt")

    model = lgb.LGBMRegressor(n_estimators=600, learning_rate=0.03, num_leaves=31,
                              subsample=0.8, colsample_bytree=0.8, random_state=42)
    model.fit(Xtr, ytr, eval_set=[(Xva, yva)],
              callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)])
    pred = model.predict(Xva)

    def mae(a, b): return float(np.mean(np.abs(a - b)))
    def rmse(a, b): return float(np.sqrt(np.mean((a - b) ** 2)))

    # baseline 1: průměr trénovacího cíle všude
    b_mean = np.full_like(yva, ytr.mean(), dtype=float)
    # baseline 2: ∝ populace (přeškálovaná na průměr cíle) — „triviální pravidlo" k překonání
    popc = population_col(val)
    if popc:
        pv = val.get_column(popc).to_numpy().astype(float)
        b_pop = pv / pv.mean() * ytr.mean()
    else:
        b_pop = b_mean

    print("\n================ VÝSLEDKY (validace) ================")
    print(f"{'model':<16}{'MAE':>12}{'RMSE':>12}{'P@50':>8}")
    for name, p in [("LightGBM", pred), ("baseline-průměr", b_mean), ("baseline-populace", b_pop)]:
        print(f"{name:<16}{mae(yva, p):>12.3f}{rmse(yva, p):>12.3f}{precision_at_k(yva, p):>8.2f}")
    impr = (mae(yva, b_pop) - mae(yva, pred)) / mae(yva, b_pop) * 100
    print(f"\n>>> NA SLIDE 3: LightGBM má MAE o {impr:.1f} % nižší než populační (triviální) baseline,"
          f" P@50={precision_at_k(yva, pred):.2f} → 'opravdová AI, ne pravidlo'.")
    print("=====================================================")

    # predikce na validační zóny → pro demo/mapu a interpretaci (NE odevzdání)
    SUB.mkdir(exist_ok=True)
    zid = next((c for c in val.columns if "grid_zone_id" in c.lower()), val.columns[0])
    out = pl.DataFrame({zid: val.get_column(zid), f"pred_{target}": pred, f"true_{target}": yva})
    out_path = SUB / "predictions_validation.csv"
    out.write_csv(out_path)
    print(f"\nPredikce (validace) → {out_path}  ({out.height} zón) — pro demo/mapu.")
    print("Tip: feature importance pro interpretaci → model.feature_importances_ (viz notebooks/).")


if __name__ == "__main__":
    main()
