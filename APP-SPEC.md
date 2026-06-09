# VoltPlán — APP SPEC (TO JE TEN PLÁN) · AIO_PHA-02-PHA

> ⭐ **Toto je řídící dokument produktu.** Nahrazuje předchozí rozptyl (V2G/dynamic-pricing
> byly explorace) — **vybraná cesta = JEDEN problém: kde mají dobíječky smysl.**
> Druhý Claude staví přesně podle „Build order" níž. Máme **~2 hodiny**.

## Produkt jednou větou
**VoltPlán** = **B2G SaaS aplikace, která městu vyhodnotí, KDE má smysl stavět dobíječky** —
AI natrénovaná z dat skóruje každou zónu Prahy (poptávka 2030 + kapacita sítě + mezera v
pokrytí + férovost). Město tím **neutopí peníze v prázdných dobíječkách**.

| | |
|---|---|
| **Zákazník** | Hl. m. Praha / městská část / Operátor ICT (B2G) |
| **Hodnota** | ~30 % veřejných dobíječek končí podvyužitých = zmařené miliony. VoltPlán řekne, kam investovat first. |
| **Byznys model** | **roční licence** (SaaS) — město/MČ platí za přístup + aktualizace |
| **AI** | LightGBM natrénovaný z `zones_train.csv` → suitability skóre per zóna |
| **Proč je to AI, ne tabulka** | učí se z bohatého profilu (zástavba, byty bez stání, síť, tranzit, trend EV), ukáže i méně očekávané sedící lokace |

## Co AI dělá (jádro techniky — 40 bodů)
**Vstup:** profil zóny (populace, byty bez stání, landuse, parking, stožáry VO, tranzit, současná
nabídka, rezerva sítě…). **Trénink:** `zones_train.csv` (2 378 zón, cíl `target_*_2030_synthetic`).
**Výstup per zóna:** `suitability_score 0–100` složené z:
- **predicted_demand** (LightGBM regrese poptávky/zátěže 2030) — *hlavní AI signál*
- **grid_headroom** (z `grid_capacity_and_reserve_2025` — kde síť unese)
- **coverage_gap** (poptávka − současné stanice z `stations_by_zone_real`)
- **equity_weight** (byty bez stání / okrajové zóny — férovost + etika)

→ Anti-leakage: `target_*_2030_synthetic` NIKDY jako featura. Validace: vlastní holdout / `zones_validation` (sandbox, ne soutěž).

## Kontrakt mezi modelem a aplikací (KLÍČOVÉ — domluvte HNED)
Model 🅐 vyrobí `submissions/app_zone_scores.csv`, aplikace 🅑 čte JEN tohle:
```
grid_zone_id, district, center_lat, center_lon,
predicted_demand_2030, grid_headroom, current_stations, coverage_gap,
equity_weight, suitability_score, recommended_type, top_reasons
```
🅑 může začít hned na **mocku se stejnými sloupci**, než 🅐 dodá reál → swap.

---

## FEATURY (ověřené proti trhu: EVpin, StreetLight, NCSU EVSE Map, ILIT, EV-Planner, Driivz)

### MVP — MUSÍ být do 2h (jádro demo)
1. **Mapa Prahy obarvená suitability skóre** (heatmapa) — zelená=stav, červená=ne. *(tvoje „heatmapa zátížení", rozšířená na skóre)*
2. **Filtrování po obvodech / MČ** — multiselect, mapa+statistiky se přepočtou. *(tvoje featura)*
3. **Dynamické značky + detailní popup** per zóna: skóre, predikovaná poptávka, headroom sítě, počet současných stanic, doporučený typ, **„proč" (top důvody)**. *(tvoje featura)*
4. **Žebříček TOP-N doporučených lokací** (seřazené tabulkou) — to je ten „output" pro město.
5. **Export dat** — CSV/GeoJSON download (žebříček + skóre). *(tvoje featura)*
6. **Live statistika** panel: počet zón, průměrné skóre, kolik lokací doporučeno, pokryto poptávky %. *(tvoje featura)*

### STRETCH — když zbude čas (každá = bod navíc)
7. **Scénářový slider** (růst EV konzervativní/střední/ambiciózní z `future_scenarios.csv`) → skóre se přepočítá *(trend = bod u poroty)*
8. **Grid-headroom overlay** (toggle) — zvýrazní zóny, kde síť neunese *(ověřeno NCSU: grid headroom layer)*
9. **Mapa mezer** — poptávka vs. současné stanice, podvyužité/nepokryté zóny *(ILIT: proximity to existing)*
10. **Equity / férovost vrstva** — priorita okrajových/chudších MČ *(StreetLight Justice40 + naše etika cold-start)*
11. **Doporučený typ dobíječky** (AC pomalá / DC rychlá / stožár VO) per zóna *(z `candidate_solutions.csv`)*
12. **Budget optimizer** — „mám X mil. Kč, kde maximalizovat pokrytí" *(EV-Planner multi-criteria)*
13. **ROI / návratnost** odhad per doporučená lokace *(Driivz: data-driven ROI)*
14. **„Proč tady" explainability** — feature importance / SHAP per zóna *(interpretace = bod u poroty)*
15. **Porovnání 2 zón/obvodů** side-by-side
16. **PDF report pro radnici** (export žebříčku + mapy)
17. **Confidence indikátor** (řídká data → nižší jistota) *(cold-start)*

> Trhem ověřeno (WebSearch + NotebookLM deep research): filtry (vzdálenost k existujícím,
> % domácností bez domácího nabíjení, populace, grid headroom), equity vrstvy, heatmapa poptávky,
> demand forecasting, utilization/ROI — vše má smysl.
> **NotebookLM verdikt:** must-have = GIS mapa + **vrstva kapacity sítě** + hustota dopravy +
> vlastnictví pozemků; diferenciátory = **AI suitability scoring**, **ROI predikce**, **equity
> analýza**, **validace reálnými daty o provozu**. → Náš `suitability_score` + grid_headroom +
> equity + interpretace „proč" trefuje přesně diferenciátory.

---

## Tech stack (jednoduchost > efektnost, ať to BĚŽÍ)
- **Model:** Python, **LightGBM** (+ scikit-learn), **polars** na data. Trénink CPU, ~2 min.
- **App:** **Streamlit** (nejnižší riziko) + mapa **pydeck**/**folium** (heatmapa, markery, popup).
  Volitelně polish ve v0/Lovable nad FastAPI — JEN když je čas.
- **Data:** už v repu (`data/core-dataset.zip` → `unzip ... -d data/participants/`).
- **Výstupy:** `submissions/app_zone_scores.csv` (kontrakt), exporty z appky.

---

## Rozdělení — 3 lidi, 2 hodiny
| | 🅐 MODEL & DATA | 🅑 APLIKACE (hlavně druhý Claude) | 🅒 BYZNYS & PITCH |
|---|---|---|---|
| **Vlastní** | suitability skóre | běžící appka + demo | licence/ROI + pitch |
| **0:00–0:20** | rozbal data, `profile_data.py`, zkontroluj sloupce | scaffold Streamlit + **mock `app_zone_scores.csv`** (stejné sloupce) → odblok | business plan: roční licence (cena), ROI pro město, zákazník B2G |
| **0:20–1:10** | uprav `train_demand.py` → vyrob **`app_zone_scores.csv`** (skóre+district+headroom+gap+typ) | MVP featury 1–6 z mocku | pitch deck (problém→řešení→zákazník→byznys→etika), research positioning vs EVpin/StreetLight |
| **1:10–1:40** | swap mock→reál, ověř čísla, feature importance pro „proč" | napoj reálné skóre, dolaď popup/heatmapu, **screenshot+záznam** | doplň čísla od 🅐, equity/etika slide, zahraniční tool jako důkaz trhu |
| **1:40–2:00** | pomoc 🅑/🅒, 1 A4 technické shrnutí | stretch featury (7–10) když čas | **dry-run pitche s živým demem**, odevzdání |

**Integrátor = 🅒** (po každém kroku ověří: skóre v modelu == co ukazuje mapa == čísla v pitchi).
Git: vlastní branch (`feat/model`, `feat/app`, `feat/pitch`), PR po zelené CI, ne přímo na main.

---

## BUILD ORDER pro druhého Clauda (vezmi odshora)
1. **Rozbal data** + prostředí: `unzip data/core-dataset.zip -d data/participants/`, `uv pip install -r requirements.txt`.
2. **Mock kontrakt:** vytvoř `submissions/app_zone_scores.csv` s pár řádky a správnými sloupci (viz Kontrakt) → appka se na něm rozjede.
3. **App MVP (`src/app.py`):** načti `app_zone_scores.csv` + lat/lon → mapa/heatmapa (pydeck) obarvená `suitability_score`, filtr po `district`, markery s popupem (skóre, poptávka, headroom, stanice, typ, „proč"), žebříček TOP-N, export CSV, panel live statistik.
4. **Model (`src/train_demand.py` rozšířit):** LightGBM na `zones_train` → `predicted_demand_2030`; přidej `grid_headroom`, `coverage_gap`, `equity_weight` → spočítej `suitability_score` (0–100, vážený součet, normalizuj) → zapiš reálný `app_zone_scores.csv`.
5. **Swap** mock za reál, ověř, že mapa dává smysl (vysoké skóre = hustá poptávka + volná síť + mezera).
6. **Stretch** (7–17) dle času. **Před PR:** codex review na anti-leakage.

> Pravidla: anti-leakage (`target_*` ne do featur), polars lazy na `hourly_*` (261 MB), CPU trénink,
> baseline drž a měř (porota chce „opravdová AI ne pravidlo"). Sandbox = vlastní validace, ne odevzdání.

---
`AIO_PHA-02-PHA | Česká AI Olympiáda 2026 | notokens` · research: EVpin, StreetLight, NCSU EVSE Suitability Map, ILIT, EV-Planner, Driivz.
