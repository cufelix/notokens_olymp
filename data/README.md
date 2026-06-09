# data/

## Core dataset (pro Linii A) — JE V REPU
`core-dataset.zip` (42 MB) obsahuje 7 CSV (~263 MB rozbaleno). Rozbal:
```bash
unzip core-dataset.zip -d participants/      # → participants/core/*.csv
```
Obsah: `zones_train.csv` (2 378), `zones_validation.csv` (517), `stations_by_zone_real.csv` (855),
`grid_capacity_and_reserve_2025.csv` (3 408), `hourly_grid_and_charging_history_2025.csv` (2 290 176),
`candidate_solutions.csv` (6), `future_scenarios.csv` (3).

⚠ **Rozbalené CSV se NEcommitují** (`.gitignore` — `hourly_*` má 261 MB, GitHub blokuje >100 MB).
Zip jde do repa (42 MB < limit), CSV si každý rozbalí lokálně.

## Optional dataset (~1,6 GB) — NENÍ v repu
Příliš velký pro git. Stáhni z **Google Drive** (odkaz v zadání) a rozbal do `participants/optional/`.
Sahej po něm jen když core nestačí (detailní real_sources, 15min grid sample).

## Pak
`python src/profile_data.py` → `python src/train_demand.py`. Viz `../DATA-MAP.md`.
