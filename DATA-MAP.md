# DATA-MAP — datová sada AIO_PHA-02-PHA

> **Stav: data zatím NEDORAZILA.** Až přijde složka `participants/`, rozbal ji do
> `data/participants/` a spusť ingest playbook níž — pak tahle mapa ožije čísly.
> Inventář dole je z textu zadání (řádky, význam). Konvence původu: `*_real` (R, z
> otevřených dat), `*_derived` (O, výpočet z reálných), `*_synthetic` (S, modelová hodnota).

## Struktura složky
`participants/core/` — **povinná**, 9 CSV, ~251 MB · `participants/optional/` — ~1,6 GB.

## Core soubory (9)
| Soubor | Řádků | Co obsahuje |
|---|---|---|
| `zones_train.csv` | 2 378 | trénovací zóny: vstupy (R/O) + **cíle 2030 (S)** |
| `zones_validation.csv` | 517 | validační zóny, stejné vstupy + cíle (lokální eval) |
| `zones_test.csv` | 513 | testovací zóny **BEZ cílů** → tady predikujeme |
| `stations_by_zone_real.csv` | 855 | reálné MPO stanice ↔ `grid_zone_id` (poloha, provozovatel, výkon, typ) |
| `grid_capacity_and_reserve_2025.csv` | 3 408 | modelový výkon TS, špička, provozní limit, **odběrová rezerva** |
| `hourly_grid_and_charging_history_2025.csv` | **2 290 176** | 4 reprezent. týdny po hodinách: zátěž, rezerva, počasí (ČHMÚ R), nabíjení (S) |
| `candidate_solutions.csv` | 6 | katalog 6 typů dobíjecího řešení (počet bodů, výkon, denní kapacita) |
| `future_scenarios.csv` | 3 | scénáře růstu EV: konzervativní / střední / ambiciózní (násobitele poptávky, řízená/neřízená špička) |
| `sample_submission.csv` | 513 | **přesný formát predikcí** pro test zóny |

## Klíčové sloupce zón (zones_*.csv)
- `grid_zone_id`, `split` — ID zóny + train/validation/test.
- `transformer_station_id_real`, `parent_substation_id_real` — z mapové vrstvy PRE (ne pasport).
- `center_lon_real`, `center_lat_real`, `nn_area_sqm_real` — poloha + plocha NN oblasti.
- `generation_connectability_class_real`, `connection_requests_*_real` — připojitelnost / žádosti.
- `population_census_2021_real`, `flats_*_real`, `building_*_real` — ČSÚ/RÚIAN/IPR demografie a zástavba.
- `landuse_*_real`, `parking_*_real`, `public_lighting_poles_real` — využití území, parkování, **stožáry osvětlení** (dobíječka na stožáru je v Praze osvědčená).
- `charging_*_2026_real`, `pid_stops_real`, `major_road_segments_real` — současná nabídka, MHD, silnice.
- `*_derived` — indexy: rezidenčnost, cílové aktivity, chybějící soukromé stání, citlivost sítě.
- **`target_*_2030_synthetic`** — denní kWh, špičkový kW, riziko přetížení, doporučený typ/počet/výkon. **← cíle. NIKDY jako featura.**

## ⚠ Pozor (přímo ze zadání)
- Reálné zdroje: chybějící hodnoty, různý zápis, duplicity → **vyčistit**.
- Syntetické = modelová data, **ne měření PRE**.
- **Kontrola leakage je součást úlohy** — `*_synthetic` cíle a `*_derived` odvozené z cílů nesmí protéct do featur.
- PRE vrstva = indikativní připojitelnost výroben, **ne** garantovaná kapacita pro odběr EV.

## Optional (~1,6 GB) — sáhnout jen když core nestačí
- `optional/real_sources/` — detailní PRE proxy, IPR, RÚIAN, ČSÚ, MPO, PID GTFS, ČHMÚ, MHMP.
- `optional/synthetic/quarter_hour_grid_sample_2025.csv` — 300 zón, zima+léto, 15min krok, 403 200 řádků.
- `docs/data_dictionary.csv` — **úplný strojový slovník všech sloupců** (přečíst jako první!).

---

## Ingest playbook (až data dorazí) — NEčíst velké CSV celé do kontextu
```bash
cd ~/projects/aiolympiada
# 0) rozbal do data/participants/, pak:
find data/participants -name '*.csv' | xargs -I{} sh -c 'echo "== {} =="; wc -l "{}"'
# 1) slovník nejdřív
column -s, -t < data/participants/**/docs/data_dictionary.csv | less
# 2) hlavičky + pár řádků každého souboru (ne celý)
for f in data/participants/core/*.csv; do echo "== $f =="; head -3 "$f"; done
# 3) velký hourly soubor (2.29M řádků) profiluj, nečti:
head -1 data/participants/core/hourly_grid_and_charging_history_2025.csv
# rozsahy/typy přes python (pandas chunky nebo polars/duckdb):
python3 - <<'PY'
import polars as pl  # nebo: import duckdb
df = pl.scan_csv("data/participants/core/zones_train.csv")
print(df.collect_schema())
PY
```
- Na 2,29 M řádků a 1,6 GB optional použij **polars / duckdb** (lazy) + `float32`, ne pandas read_csv celé. Skelet hotový: `src/profile_data.py` (schéma + řádky + leakage guard). Trénink CPU + sklearnex — viz `HARDWARE.md`.
- Po prozkoumání **doplň skutečná čísla/rozsahy do téhle mapy** (sloupcové statistiky, podíl chybějících, distribuce cílů), ať je další session hned v obraze.
- Ulož profilovací skript do `src/profile_data.py`, predikce do `submissions/` ve formátu `sample_submission.csv`.
