# DATA-MAP — datová sada AIO_PHA-02-PHA (aktualizováno 2026-06-09)

> **Stav: data zatím NEDORAZILA.** Až přijde `participants/` (Google Drive, ~251 MB),
> rozbal do `data/participants/` a spusť ingest playbook níž.
> **DŮLEŽITÉ: je to SANDBOX, ne soutěž o skóre.** Všechny zóny mají vyplněné (modelové)
> cíle — data slouží ke stavbě/validaci/interpretaci produktu. **Validuj si sám: odlož
> část dat stranou (holdout).** Žádný skrytý test set, žádné odevzdání predikcí.
> Konvence původu: `*_real` (R) / `*_derived` (O, výpočet z reálných) / `*_synthetic` (S, modelová).

## Bohatý dataset = jen pro Linii A (nabíjení a síť + V2G)
Pro linie B/C/D si bereš **pražská otevřená data** (viz dole) nebo vlastní. Data nejsou povinná.

| Soubor | Řádků | Co obsahuje |
|---|---|---|
| `zones_train.csv` | 2 378 | zóny: reálné+odvozené vstupy + **modelové cíle 2030** |
| `zones_validation.csv` | 517 | menší slice zón (stejné sloupce) pro vlastní ověření |
| `stations_by_zone_real.csv` | 855 | reálné MPO stanice ↔ `grid_zone_id` |
| `grid_capacity_and_reserve_2025.csv` | 3 408 | modelový výkon TS, špička, provozní limit, **odběrová rezerva** |
| `hourly_grid_and_charging_history_2025.csv` | **2 290 176** | 4 týdny po hodinách: zátěž, rezerva, počasí, nabíjení, **overload_flag** |
| `candidate_solutions.csv` | 6 | katalog 6 typů dobíjecího řešení |
| `future_scenarios.csv` | 3 | scénáře růstu EV: konzervativní / střední / ambiciózní |

> ⚠ **ZMĚNA oproti staré verzi:** `zones_test.csv` a `sample_submission.csv` už NEEXISTUJÍ.
> Místo odevzdání predikcí si uděláš vlastní holdout z `zones_train.csv` + použiješ `zones_validation.csv`.

## Klíčové sloupce zón
- `grid_zone_id` (O), `transformer_station_id_real`, `parent_substation_id_real` (R, z PRE vrstvy).
- `center_lon/lat_real`, `nn_area_sqm_real` (R) — poloha + plocha NN oblasti.
- `population_census_2021_real`, `flats_*`, `building_*` (R) — ČSÚ/RÚIAN/IPR.
- `landuse_*`, `parking_*`, `public_lighting_poles_real` (R) — území, parkování, stožáry VO.
- `charging_*_2026_real`, `pid_stops_real`, `major_road_*` (R) — současná nabídka, MHD, silnice.
- `*_derived` (O) — indexy: rezidenčnost, citlivost sítě…
- **`target_*_2030_synthetic`** (S) — denní kWh, špičkový kW, riziko přetížení. **← cíle. NIKDY featura.**
- **Pro V2G/řízené nabíjení (Linie A jádro):** `grid_capacity_and_reserve_2025` (rezerva per TS) +
  `hourly_*` (zátěž+rezerva+overload po hodinách) — odtud KDY je v síti prostor a kdy hrozí přetížení.

## Pražská otevřená data (linie B/C/D — přines/doplň vlastní)
| Zdroj | Co | Pro linii |
|---|---|---|
| Golemio — platby v zónách stání (od 2017) | čas/délka/způsob platby (**jen nerezidenti!**) | B |
| Golemio — real-time parkování | P+R, on-street, komerční, ZTP | B |
| Golemio — dojezdy (Waze 400+ úseků), cyklosčítače | plynulost, kongesce, cyklo intenzity | B/C |
| Golemio — polohy vozidel PID (open API), PID GTFS | spoje, zpoždění, jízdní řády | C |
| ŘSD/NDIC + městské kamery (dopravniinfo.gov.cz) | obraz pro detekci obsazenosti/hustoty | D |
| opendata.praha.eu | obecná městská data | vše |

## ⚠ Pozor (ze zadání)
- Reálné zdroje: chybějící hodnoty, různý zápis, duplicity → **vyčistit**.
- Syntetické = modelová data, **ne měření PRE**. Leakage: `*_synthetic` cíle + odvozené z nich pryč z featur.
- **Parkovací platby = jen nerezidenti** → samy o sobě neukazují skutečnou obsazenost. Počítej s tím.

---
## Ingest playbook (až data dorazí) — NEčíst velké CSV celé do kontextu
```bash
cd ~/projects/aiolympiada
find data/participants -name '*.csv' -exec sh -c 'echo "== $1 =="; wc -l "$1"' _ {} \;
python src/profile_data.py        # schéma + řádky + leakage guard (cílové sloupce)
```
- Na 2,29 M řádků použij **polars/duckdb** (lazy) + `float32`. Trénink CPU + sklearnex → `HARDWARE.md`.
- **Vlastní validace:** odlož ~20 % `zones_train` stranou (nebo použij `zones_validation`) → měř proti baseline.
- Po prozkoumání **doplň reálná čísla/rozsahy sem** (statistiky, podíl chybějících, distribuce cílů, rezerva sítě).
