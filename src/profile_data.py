"""profile_data.py — bezpečné prozkoumání datasetu AIO_PHA-02-PHA.

Spusť až bude složka rozbalená v data/participants/. Nečte velké CSV celé do RAM —
používá polars lazy + duckdb. Výstup doplň ručně do DATA-MAP.md.

    python src/profile_data.py
"""
from __future__ import annotations
import pathlib
import polars as pl

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "participants"


def list_csvs() -> list[pathlib.Path]:
    return sorted(DATA.rglob("*.csv"))


def profile(path: pathlib.Path) -> None:
    """Schéma + počet řádků + null podíl, bez načtení celého souboru."""
    lf = pl.scan_csv(path, infer_schema_length=10_000)
    schema = lf.collect_schema()
    n = lf.select(pl.len()).collect().item()
    print(f"\n== {path.relative_to(DATA)} ==  rows={n:,}  cols={len(schema)}")
    for name, dtype in schema.items():
        print(f"   {name:<48} {dtype}")


def leakage_warning(train_csv: pathlib.Path) -> None:
    """Vypíše sloupce cílů (target_*_2030_synthetic) — NIKDY je nedávej do featur."""
    cols = pl.scan_csv(train_csv).collect_schema().names()
    targets = [c for c in cols if "target_" in c or c.endswith("_2030_synthetic")]
    print("\n⚠ CÍLE (leakage guard, nepoužívat jako featury):")
    for t in targets:
        print("   ", t)


if __name__ == "__main__":
    if not DATA.exists():
        raise SystemExit(f"Data nejsou rozbalená v {DATA} — viz DATA-MAP.md")
    csvs = list_csvs()
    print(f"Nalezeno {len(csvs)} CSV.")
    for p in csvs:
        try:
            profile(p)
        except Exception as e:  # noqa: BLE001
            print(f"   (chyba profilování {p.name}: {e})")
    train = next((p for p in csvs if p.name == "zones_train.csv"), None)
    if train:
        leakage_warning(train)
