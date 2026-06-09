# VoltPlán — Technické shrnutí (1 A4)

**Česká AI Olympiáda 2026 · AI Startup · AIO_PHA-02-PHA · tým notokens**

## Problém
Klimatický plán Prahy cílí na **až 10 000 dobíjecích stanic do 2030** (investice v miliardách).
Z oborových dat ~**30 % veřejných stanic končí podvyužitých** — staví se bez analýzy poptávky a
kapacity sítě. **VoltPlán** = B2G datová služba, která AI ohodnotí **každou zónu Prahy**, kde má
stanice smysl — propojuje **mobilitu** (poptávka) a **energetiku** (rezerva sítě).

**Zákazník:** Magistrát HMP / MČ / Operátor ICT (Golemio) / distributor (PRE) / energetická komunita.

## Řešení — dva běžící AI modely + skóre
1. **Regrese (LightGBM):** predikce poptávky po nabíjení 2030 z profilu zóny (60 featur:
   zástavba, byty bez stání, landuse, MHD, silnice, rezerva TS 2025…).
2. **Klasifikace (LightGBM):** doporučený typ stanice (6 typů z `candidate_solutions`).
3. **Suitability 0–100** = 0,40·poptávka + 0,30·mezera_pokrytí + 0,15·rezerva_sítě + 0,15·férovost.

Skóruje **celá Praha (2 895 zón, 22 obvodů)**. Výstup: `app_zone_scores.csv` → živé Streamlit demo
(heatmapy, filtr obvodů, „kam stavět N stanic", popup „proč", rozpočtový optimalizátor, export).

## Klíčové metriky (na odděleném holdoutu 517 zón)
| Metrika | Hodnota | Význam |
|---|---|---|
| **MAE** | **4,63 EV/den** | o **18,1 %** lépe než triviální populační baseline (5,66) |
| **Precision@50** | **0,84** | správně určená většina TOP-50 zón |
| **Recommender accuracy** | **83,8 %** | přesnost doporučení typu stanice |
| **Anti-leakage** | ✅ kontrolováno kódem | cíle `target_*` / `_2030_synthetic` ≠ featury |

## Proč je to opravdová AI (ne tabulka)
„Hodně lidí → velký hub" zvládne tabulka. Náš model bije populační pravidlo a najde i **méně
očekávané, ale sedící** zóny (malá populace, ale tranzit + volná síť + žádné stanice). Skóre je
**plně interpretovatelné** — appka u každé zóny ukáže důvody.

## Anti-leakage & validace
Sdílená `feature_cols` vyřazuje `target_*`, `_2030_synthetic`, `recommended_*`, `risk_overload`,
ID a textové sloupce (+ runtime `assert`). Trénink na `zones_train`, **metriky jen na holdoutu**
`zones_validation`. Sandbox — žádné odevzdání skrytých labelů.

## Byznys
**Roční licence (SaaS)** ~300 tis. Kč/rok. Cílení sníží podíl podvyužitých stanic z ~30 % na ~10 %
→ z rozpočtu 60 mil. Kč **uchrání ~12 mil. Kč**; licence se vrátí už při jediné nepostavené prázdné
stanici. **Sběr dat v čase:** pilot PRE/Smart Prague + Golemio. **Škálování:** Brno, Plzeň, Ostrava.

## Etika (4 oblasti)
1. **Odpovědnost:** podpora rozhodnutí, ne automat; přetrénovatelné z reálných dat.
2. **Soukromí:** jen zónové agregáty, žádní jednotlivci.
3. **Cold-start / spravedlnost:** `equity_weight` zvyšuje skóre okrajových čtvrtí; content-based →
   řídké zóny nejsou znevýhodněné.
4. **Nejistota:** predikce 2030 jako **pásmo scénářů** (konzervativní/střední/ambiciózní), ne 1 číslo.

## Náš úhel + zahraniční inspirace
Skórujeme **každou zónu** kompozitem mobilita × energetika (ne jen „kde hub"). Inspirace: EV
suitability mapy s **grid-headroom** vrstvou (NCSU), **equity** vrstvy (StreetLight/Justice40),
multikriteriální optimalizace (EV-Planner) — přeneseno na pražská data a Klimatický plán 2030.

## Stack & reprodukce
Python · LightGBM · scikit-learn · polars · Streamlit · folium · CPU (~2 min).
`python src/generate_scores.py` → `streamlit run src/app_premium.py`.

`notokens · 2026-06-09 · data = sandbox (reálná + modelová)`
