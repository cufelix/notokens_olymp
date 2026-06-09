"""match.py — Linie B: spáruj zónu s typem dobíjecího řešení + mapa mezer + equity.

Content-based: profil zóny vs. "ideální profil" každého z typů z candidate_solutions.csv.
Skóre = podobnost + equity váha (byty bez stání, okraj, nulová současná nabídka).
ADAPTIVNÍ na názvy — na místě dolaď IDEAL_RULES dle reálných sloupců.

    python src/match.py        # zapíše submissions/matching.csv (zóna → top typ + skóre)
"""
from __future__ import annotations
import pathlib
import numpy as np
import polars as pl

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "participants"
SUB = ROOT / "submissions"


def find(name: str) -> pathlib.Path:
    hits = list(DATA.rglob(name))
    if not hits:
        raise SystemExit(f"Nenalezen {name} — rozbal data.")
    return hits[0]


def col(df: pl.DataFrame, *subs: str) -> str | None:
    for c in df.columns:
        if all(s in c.lower() for s in subs):
            return c
    return None


def main() -> None:
    zones = pl.read_csv(find("zones_test.csv"), ignore_errors=True)
    cand = pl.read_csv(find("candidate_solutions.csv"), ignore_errors=True)
    print("Typy řešení:", cand.shape, "\n", cand)

    zid = col(zones, "grid_zone_id") or zones.columns[0]

    # --- equity váha: vyšší pro zóny bez stání / okraj / bez nabídky (uprav názvy!) ---
    flats_no_park = col(zones, "flats", "no") or col(zones, "parking")  # byty bez stání proxy
    cur_charging = col(zones, "charging", "2026")                        # současná nabídka
    eq = np.ones(zones.height)
    if flats_no_park:
        v = zones.get_column(flats_no_park).fill_null(0).to_numpy().astype(float)
        eq *= 1 + (v - v.min()) / (v.max() - v.min() + 1e-9)            # 1..2
    if cur_charging:
        c = zones.get_column(cur_charging).fill_null(0).to_numpy().astype(float)
        eq *= np.where(c == 0, 1.5, 1.0)                                # nulová nabídka → priorita

    # --- content-based skóre (MVP heuristika; na místě nahraď reálnými osami profilu) ---
    # Příklad logiky: hustá rezidenční zóna + stožáry VO → pomalé AC/stožár; tranzit → DC hub.
    # Tady jen demonstrační: skóre = equity (placeholder), top typ = nejlevnější vhodný.
    # TODO na místě: spočítej podobnost profilu zóny k profilu každého typu z `cand`.
    type_name = cand.columns[0]
    top_type = cand.get_column(type_name)[0]

    out = pl.DataFrame({
        zid: zones.get_column(zid),
        "equity_weight": eq.round(3),
        "recommended_type": [top_type] * zones.height,  # TODO nahradit argmax skóre
    })
    SUB.mkdir(exist_ok=True)
    out.write_csv(SUB / "matching.csv")
    print(f"\nMatching → {SUB/'matching.csv'} ({out.height} zón)")
    print("⚠ TODO: dodělej reálné content-based skóre profil↔typ; teď je recommended_type placeholder.")


if __name__ == "__main__":
    main()
