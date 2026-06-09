# VoltPlán — vítězný koncept + architektura
## Česká AI Olympiáda 2026 · AI Startup · AIO_PHA-02-PHA (Praha)

> **Jedna platforma, která spojuje všechny tři linie zadání do jednoho rozhodnutí:**
> *predikuj* poptávku → *doporuč* typ → *ochraň* síť — se vestavěnou spravedlností a živým demem.

---

## 0 · Shrnutí na jednu obrazovku

**Co to je.** VoltPlán je předplatitelská rozhodovací platforma pro Hl. m. Prahu, Operátora ICT a městské části. Jako jediné řešení odpovídá na všechny tři otázky úlohy v jednom propojeném kroku:

1. **KDE** bude poptávka po veřejném dobíjení v roce 2030 — s pásmem scénářů, ne jedním číslem *(Linie A)*
2. **JAKÝ TYP** dobíječky do dané čtvrti patří podle jejího profilu *(Linie B)*
3. **KOLIK a kde přesně** postavit, aby se **žádná trafostanice nepřetížila** ve večerní špičce a vešlo se to do rozpočtu *(Linie C)*

…a to vše s **vestavěnou férovostí** pro husté čtvrti bez vlastního stání (cold-start jako funkce, ne odstavec).

**Proč právě tohle vyhrává tabulku 40 / 40 / 20.** Zadání samo říká: *„nejsilnější řešení obvykle propojí předpověď poptávky s chytrým doporučením."* VoltPlán propojí rovnou všechny tři linie + vrstvu důvěry pod nimi + živý what-if explorer nad nimi:

- **Technika (40):** běžící AI ve třech vrstvách, každá s **doloženým překonáním baseline**, čištění + leakage check, interpretace přes SHAP, cold-start zabudovaný do modelu.
- **Byznys (40):** konkrétní instituce, ceník v Kč, opakovaný příjem, datová smyčka v n8n (kterou umíš reálně ukázat), návratnost vyčíslená přes ušetřená přetížení a mrtvé dobíječky, škálování město-agnostické.
- **Prezentace/etika/relevance (20):** živé demo s posuvníky, 4 etické oblasti s konkrétními mechanismy, napojení na Klimatický plán / Generel / Smart Prague + PRE / IPR, komunikace nejistoty přes pásma a scénáře.

---

## 1 · Hlavní myšlenka: tři linie jako jedna pipeline

Většina týmů udělá jednu linii (jen predikci, nebo jen recommender). VoltPlán je řetězec, kde výstup jedné vrstvy je vstupem další — proto dává odpověď, kterou triviální tabulka nedá:

- **A předpoví poptávku** → tím dostane B i C reálné číslo, se kterým počítají.
- **B doporučí typ** → tím dostane C katalog možností + váhu férovosti pro každou zónu.
- **C optimalizuje umístění** pod tvrdým omezením rezervy sítě → tím vznikne plán, který je *zároveň* poptávkou opodstatněný, typově vhodný a síťově bezpečný.

```
                ┌─────────────────────────────────────────────┐
                │   RAW DATA  (9 core CSV + optional 1,6 GB)    │
                │   reálné (R) · odvozené (O) · syntetické (S)  │
                └───────────────────────┬─────────────────────┘
                                        │
                ┌───────────────────────▼─────────────────────┐
   VRSTVA 0     │  TRUST LAYER — kvalita dat + leakage guard    │
   (důvěra)     │  čištění · dedup · imputace · kontrola úniku  │
                │  → confidence známka A/B/C pro každou zónu    │
                └───────────────────────┬─────────────────────┘
                                        │ čistá data + známka spolehlivosti
                ┌───────────────────────▼─────────────────────┐
   LINIE A      │  DEMAND ENGINE — predikce poptávky 2030       │
   (KDE)        │  LightGBM regrese (denní kWh, špička kW)      │
                │  + quantile heads P10/P50/P90  + riziko       │
                │  přetížení · 3 scénáře z future_scenarios     │
                │  → poptávka per zóna, per scénář, s pásmem    │
                └───────────────────────┬─────────────────────┘
                                        │ d[z] = poptávka zóny
                ┌───────────────────────▼─────────────────────┐
   LINIE B      │  MATCHING ENGINE — jaký typ kam               │
   (JAKÝ TYP)   │  content-based recommender: profil zóny →     │
                │  skóre 6 typů z candidate_solutions           │
                │  + EQUITY váha (byty bez stání, okraj, 0 nabídka) │
                │  + SHAP zdůvodnění  → mapa mezer              │
                └───────────────────────┬─────────────────────┘
                                        │ w[z] = váha férovosti, vhodné typy
                ┌───────────────────────▼─────────────────────┐
   LINIE C      │  GRID OPTIMIZER — kolik a kde, bez přetížení  │
   (OCHRANA)    │  MILP (PuLP / OR-Tools)                       │
                │  omezení: rezerva každé TS ve špičce + rozpočet │
                │  + equity floor (min. pokrytí v každé MČ)     │
                │  cíl: max vážené pokryté poptávky             │
                │  → finální plán + metrika „zabráněná přetížení" │
                └───────────────────────┬─────────────────────┘
                                        │ plán výstavby per scénář
                ┌───────────────────────▼─────────────────────┐
   SERVING      │  WHAT-IF EXPLORER (Streamlit) + API           │
                │  mapa · posuvníky: růst EV, rozpočet,         │
                │  řízené nabíjení on/off, váha férovosti       │
                │  exporty: žebříček CSV, mapa mezer,           │
                │           sample_submission pro test zóny     │
                └───────────────────────┬─────────────────────┘
                                        │
                ┌───────────────────────▼─────────────────────┐
   SMYČKA       │  DATA REFRESH (n8n na VPS, měsíčně)           │
                │  stanice MPO · registrace EV · obsazenost PRE │
                │  · žádosti o připojení → Trust Layer → retrain │
                └─────────────────────────────────────────────┘
```

> Tahle „smyčka" je tvůj nejsilnější byznys argument: služba **běží a zlepšuje se opakovaně**, ne jednorázová studie. A protože n8n na svém VPS reálně provozuješ, můžeš workflow v pitchi ukázat živě.

---

## 2 · Architektura po vrstvách

Pro každou vrstvu: **co dělá · technika · klíčové featury/vstupy · výstup · jak porazí baseline · které soubory.**

### VRSTVA 0 · Trust Layer (kvalita dat + leakage)
- **Co dělá.** Než cokoliv predikuješ, vyčistí reálné zdroje (chybějící hodnoty, duplicity, různý zápis), zkontroluje **leakage** a každé zóně přidělí známku spolehlivosti A/B/C podle úplnosti dat + šířky predikčního intervalu.
- **Technika.** pandas pro čištění; pravidla pro imputaci (medián per typ zóny, ne globální); leakage check = flag featur s podezřele vysokou korelací k `target_*_2030_synthetic` a featur, které by v čase predikce nebyly dostupné; outlier detection (IQR / isolation forest).
- **Výstup.** Vyčištěný dataset + `data_quality_report` + `confidence_grade` per zóna.
- **Baseline.** Naivní model na syrových datech → ukážeš, že po vyčištění a odstranění leakage se validace chová spolehlivěji a test nemá přehnaně sebejisté predikce; **předveď jeden zachycený případ leakage** (to porotu přesvědčí).
- **Soubory.** Všechny; důraz na `optional/real_sources/` (nepořádek) a varování zadání o syntetických cílech.
- **Bonus body.** Pokrývá technickou 40 (čištění, validace, leakage) **a** etiku oblast 1+4 (odpovědnost, nejistota) **a** zviditelní cold-start (oblast 3 — explicitně označí datově chudé zóny).

### LINIE A · Demand Engine (predikce — KDE)
- **Co dělá.** Pro každou zónu předpoví denní `kWh`, špičkový `kW` a riziko přetížení v roce 2030, ve třech scénářích, s pásmem P10/P50/P90.
- **Technika.** `LightGBM` (gradient boosting) — jeden regresor na kWh, jeden na špičkový kW, jeden klasifikátor/regresor na riziko přetížení. Nejistota přes **quantile regression** (`objective='quantile'`, alpha 0,1 / 0,5 / 0,9) → poctivá pásma levně. Scénář aplikuješ jako násobitel z `future_scenarios.csv` (konzervativní/střední/ambiciózní + řízená/neřízená špička).
- **Klíčové featury.** populace, `flats_*`, `building_*`, `landuse_*`, `parking_*`, `public_lighting_poles_real`, `charging_*_2026_real` (současná nabídka), `pid_stops_real`, `major_road_segments_real`, odvozené indexy (rezidenčnost, chybějící stání, citlivost sítě), `nn_area_sqm_real`. **Používej poměry, ne jen absolutní hodnoty** (např. byty bez stání / všechny byty) — model pak generalizuje líp a porazí populační baseline.
- **Trend.** Scénáře řeší „ne dnešek, ale za 3 roky" — zóna s málo EV ale rychlým růstem vyjde jinak než nasycená.
- **Výstup.** `d[z]` = poptávka per zóna/scénář s pásmem + riziko přetížení.
- **Jak porazí baseline.** Reportuj na `zones_validation.csv`:
  - **MAE/RMSE** vs. (a) průměr (predikuj trénovací průměr všude) a (b) lineární model `poptávka ∝ populace`.
  - **Precision@50 / Recall@50** — kolik z reálně 50 nejpoptávanějších zón model trefí do svých top 50, oproti seřazení podle populace.
  - **Kalibrace pásma** — podíl skutečných hodnot mezi P10–P90 ≈ 80 %.
- **Soubory.** `zones_train/validation` (cíle), `future_scenarios`.

### LINIE B · Matching Engine (doporučení — JAKÝ TYP)
- **Co dělá.** Pro profil každé zóny seřadí 6 typů řešení z `candidate_solutions.csv` podle vhodnosti a vyrobí celoměstskou **mapu mezer** (potřeba vs. současná nabídka).
- **Technika.** Kombinace dvou přístupů: (1) klasifikátor trénovaný na syntetickém cíli „doporučený typ" + (2) content-based skóre = jak profil zóny sedí „ideálnímu profilu" každého typu. Příklady logiky: husté sídliště bez stání + volná rezerva + hodně stožárů VO → vysoké skóre pro **pomalé nabíjení na stožárech / AC street**; tranzitní/retail uzel s vysokou průjezdnou poptávkou → **rychlý DC hub**.
- **EQUITY váha (klíč k etice 3).** Priorita zóny × `equity_weight` — vyšší pro vysoký podíl bytů bez stání, okrajovou polohu, nulovou současnou nabídku, nižší příjmový proxy. Pásmo se rozšíří pro řídké zóny (z confidence známky Trust Layeru).
- **Výstup.** Per zóna seřazené typy + **SHAP zdůvodnění** (které featury rozhodly) + `w[z]` pro optimalizér + mapa mezer.
- **Jak porazí baseline.** Baseline = „doporuč nejčastější typ všude" / „hodně aut → DC hub". Reportuj accuracy/F1 oproti syntetickému cíli **a ukaž konkrétní zóny, kde se model liší od naivního pravidla a proč** (přes SHAP) — to je přesně to „méně očekávané, ale sedící umístění", které zadání chce vidět.
- **Soubory.** `candidate_solutions`, featury zón + cíl typu, `stations_by_zone_real` (současná nabídka → mezera).

### LINIE C · Grid Optimizer (ochrana sítě — KOLIK a KDE)
- **Co dělá.** Z předpovězené poptávky, doporučených typů a rezervy každé trafostanice vyřeší, kolik bodů jakého typu postavit v které zóně, aby se **maximalizovalo vážené pokrytí poptávky** při **nulovém přetížení** a v rámci rozpočtu.
- **Technika.** **MILP** (PuLP + CBC, nebo OR-Tools). Pro ~500 zón × 6 typů je instance malá a řeší se rychle.

  **Rozhodovací proměnné:** `x[z,t] ∈ ℤ≥0` — počet bodů typu *t* v zóně *z*.

  **Parametry:** `d[z]` poptávka (z A); `cap[t]` denní kapacita bodu (z candidate_solutions); `pk[t]` příspěvek ke špičce v kW; `cost[t]` investiční náklad; `R[s]` odběrová rezerva TS *s* (`reserve_capacity_kw`); `w[z]` váha férovosti (z B); `B` rozpočet; `σ` koeficient současnosti ve večerní špičce (řízené nabíjení → `σ↓` uvolní kapacitu).

  **Účelová funkce:** `max Σ_z w[z]·served[z]`, kde `served[z] ≤ d[z]` a `served[z] ≤ Σ_t x[z,t]·cap[t]`.

  **Omezení:**
  1. **Síť (klíčové):** pro každou TS *s*: `Σ_{z∈s} Σ_t x[z,t]·pk[t]·σ ≤ R[s]`
  2. **Rozpočet:** `Σ_z Σ_t x[z,t]·cost[t] ≤ B`
  3. **Equity floor (volitelné, silné):** pro každou MČ *m*: `Σ_{z∈m} served[z] ≥ floor_m`
- **Výstup.** Finální plán `x[z,t]` per scénář + **metrika „zabráněná přetížení"**.
- **Jak porazí baseline.** Baseline = greedy „stav největší huby tam, kde je nejvíc aut, ignoruj síť". Spočítáš, kolik TS by greedy přetížil (`Σ přidaná špička > R[s]`). Headline na slidu: **„Náš plán: 0 přetížených trafostanic. Naivní plán za stejný rozpočet: X přetížených — a obslouží méně poptávky."**
- **Soubory.** `grid_capacity_and_reserve_2025` (rezerva per TS), `candidate_solutions` (kapacita/výkon/cena), výstup A, `future_scenarios` (σ řízené/neřízené).

### SERVING · What-if Explorer + API
- **Co dělá.** Interaktivní mapa, kde plánovač posune posuvník (růst EV %, roční rozpočet, řízené nabíjení on/off, váha férovosti) a živě vidí, jak se mění doporučená výstavba, rezerva sítě, pokrytí a férovost.
- **Technika.** **Streamlit** (nejnižší riziko, že demo nepoběží) s mapou přes `pydeck`/`folium`/`plotly`. Volitelně polish front ve **v0/Lovable** nad `FastAPI` backendem. Hostuj na svém **VPS přes Caddy**.
- **Výstup.** Živá ukázka pro 3min pitch + exporty: žebříček CSV, mapa mezer, **`sample_submission.csv`** ve formátu pro test zóny (datový výstup k odevzdání).
- **Proč to boduje.** Zadání explicitně odměňuje živou ukázku a dělá nejistotu hmatatelnou (přepínání scénářů = etika 4).

### SMYČKA · Data refresh (n8n na VPS)
- **Co dělá.** Měsíčně stáhne seznam stanic MPO, proxy registrací EV (ČSÚ), feed obsazenosti z pilotu PRE a nové žádosti o připojení → pustí Trust Layer → přetrénuje modely → nasadí.
- **Proč to boduje.** Reálný „sběr a údržba dat v čase" (pilíř 2) — a umíš ho ukázat, protože n8n provozuješ.

---

## 3 · Jak DOLOŽIT překonání baseline (nejdůležitější pro 40 bodů techniky)

Tohle je místo, kde se vyhrává nebo prohrává. Měj připravené **konkrétní číslo** na slidu č. 3 pitche.

| Vrstva | Triviální baseline | Metrika | Co ukázat |
|---|---|---|---|
| A · poptávka | průměr + `∝ populace` | MAE/RMSE, Precision@50, kalibrace P10–P90 | „MAE o Y % nižší než populační model; trefíme 80 % skutečně nejpoptávanějších zón do top 50" |
| B · typ | „nejčastější typ všude" | accuracy/F1 + případové studie | konkrétní zóny, kde se lišíme od naivního pravidla, + SHAP proč |
| C · plán | greedy „huby u nejvíc aut" | zabráněná přetížení + obsloužená poptávka / Kč | „0 vs. X přetížení, +Z % obsloužené poptávky za stejný rozpočet" |

> Dokud tahle čísla reálně nespustíš na `zones_validation.csv`, jsou to hypotézy. Mít je černé na bílém je **úkol číslo jedna** (viz roadmapa, týden 1).

---

## 4 · Byznys model (konkrétní čísla)

**Zákazník (instituce) + role.** Primárně **Operátor ICT / Hl. m. Praha** (celoměstská licence) a **městské části** (per-district předplatné). Konkrétní role uvnitř: plánovač mobility (chce mapu mezer a prioritizaci), energetik distributora PRE (chce modul ochrany sítě — Linii C).

**Problém a kolik dnešní stav stojí.** Bez nástroje se buduje „od oka": dobíječky končí prázdné (mrtvá investice), nebo se přehlédne čtvrť s velkou potřebou, a večerní špička hrozí přetížením lokální trafostanice. Každá z těchto chyb je drahá:
- instalace veřejného **AC** bodu ≈ desítky až nízké stovky tisíc Kč,
- **DC rychlý** bod ≈ stovky tisíc až jednotky milionů Kč,
- posílení trafostanice / sítě ≈ jednotky až desítky milionů Kč.

*(Čísla ber jako obhajitelné odhady — před pitchem ověř přes reálné zakázky MPO/PRE.)*

**Monetizace (opakovaný příjem).**
- Předplatné **městské části**: ~**19 000 Kč/měsíc** (≈ 228 000 Kč/rok) za přístup pro danou MČ.
- **Celoměstská licence** (Operátor ICT / MHMP): ~**900 000 Kč/rok** — všechny zóny, prioritní scénáře, API, datový refresh.
- Volitelný modul **„Ochrana sítě"** pro PRE (Linie C): ~**500 000 Kč/rok**.

**Návratnost.** Když VoltPlán zabrání **byť jedné** chybné dobíječce nebo **jednomu** předčasnému posílení trafa ročně, zaplatí se mnohonásobně. Měkké přínosy: rychlejší přechod na EV → nižší emise a hluk, lepší ovzduší a image čtvrti, lépe využité veřejné investice. **Služba = investice, ne výdaj.**

**Škálovatelnost.** Featury jsou navržené **město-agnosticky** (poměry a hustoty, ne pražská specifika) → Brno, Plzeň, Ostrava jen nasypou svá open data. Jiná infrastruktura: P+R, sdílená mobilita, depa elektrobusů. Síťový efekt: každé nové město zlepší sdílený base model.

---

## 5 · Etika — 4 oblasti zabudované do produktu (ne odstavec navíc)

1. **Chybná predikce a odpovědnost.** Každé doporučení nese **confidence známku A/B/C**; před jakoukoli stavbou je **člověk v kličce** (plánovač schvaluje, optimalizér jen navrhuje) + audit log. **Čtvrtletní back-testing**: porovnáš predikované vs. skutečné využití nově postavených dobíječek, čímž chybu odhalíš a model rekalibruješ.
2. **Přístup k datům a soukromí.** Pracuješ **jen s agregáty na úrovni zóny** (s prahem minimálního počtu domácností, aby nešlo nikoho re-identifikovat), žádná individuální data o session ani pohybu. Soulad s GDPR; agreguje se obsazenost, ne jednotlivé nabíjecí události.
3. **Spravedlnost (cold-start) — těžiště.** Spirálu „málo dat → horší doporučení → nevznikne dobíječka → nevznikají data" lámeš třemi mechanismy: (a) **equity váha + equity floor** přímo v optimalizéru, (b) **nafouknutá nejistota** pro řídké zóny místo tichých nul, (c) **aktivní sběr signálu** z datově chudých zón (občanské žádosti, dočasné měřáky). Sleduješ metriku **„fairness gap"** v čase.
4. **Komunikace nejistoty.** Nikdy jedno číslo — vždy **pásmo P10/P50/P90 a tři scénáře**. Explorer dělá nejistotu hmatatelnou (přepneš scénář, mapa se změní). Rozhodnutí rámuješ jako **robustní napříč scénáři** (co obstojí i v konzervativním vývoji), ne jako sázku na střední odhad.

---

## 6 · Pitch deck — 8 slidů namapováno 1:1 na checklist zadání

1. **Problém a zákazník** — Operátor ICT / MČ; co je pálí (prázdné dobíječky, přetížení, pomalý přechod) + kolik to stojí.
2. **Data** — co je reálné vs. modelové; jak Trust Layer čistí + jeden zachycený leakage případ.
3. **AI model / engine + jak měříš kvalitu** — tři vrstvy A/B/C; **tabulka čísel proti baseline** (sekce 3). *Nejdůležitější slide.*
4. **Výsledky a živá ukázka** — what-if explorer, posuvníky, mapa mezer, „0 vs. X přetížení".
5. **Byznys model** — ceník v Kč, opakovaný příjem, datová smyčka v n8n (sběr dat v čase).
6. **Etika** — 4 oblasti, zvlášť fairness gap + confidence známky.
7. **Škálování** — Brno/Plzeň/Ostrava + P+R / sdílená mobilita; síťový efekt.
8. **Tým a shrnutí** — kdo jste a proč to dává smysl.

Plus: **technické shrnutí na 1 A4** (architektura + metriky) a **datové výstupy** (`sample_submission.csv`). Živě: **3 min + 2 min Q&A**, video nepovinné.

---

## 7 · Tech stack (napasováno na tvoje prostředí)

| Vrstva | Nástroj | Pozn. |
|---|---|---|
| Data / Trust | Python, pandas, scikit-learn | leakage check + confidence |
| A · predikce | LightGBM (quantile) | rychlé, interpretovatelné, SHAP |
| B · matching | scikit-learn + SHAP | recommender + zdůvodnění |
| C · optimalizace | PuLP (CBC) nebo OR-Tools | malý MILP, řeší se rychle |
| Serving / demo | **Streamlit** (+ pydeck/folium) | nízké riziko, běží na VPS přes Caddy |
| (volitelný front) | v0 / Lovable + FastAPI | jen polish, ne nutnost |
| Datová smyčka | **n8n** na VPS + Docker | „sběr dat v čase" — umíš ukázat živě |

> **Princip nasazení: funkční jednoduchost > rozbitá efektnost.** Streamlit demo, které poběží, porazí krásný front, který spadne. Bez předvedeného běžícího modelu = 0 bodů za techniku.

---

## 8 · Roadmapa stavby (de-risk → funkční demo brzy)

- **Týden 1 — Technické jádro (MVP důkaz).** Trust Layer (čištění + leakage + confidence) → Demand Engine (LightGBM + quantile) → **spustit baselines a mít ČÍSLO** (MAE proti průměru a populaci, Precision@50). Tohle je tvůj nejdůležitější výstup — hotové **první**.
- **Týden 2 — Matching + mapa mezer.** Recommender + SHAP zdůvodnění + equity vážení + vizuál mezer.
- **Týden 3 — Grid Optimizer.** PuLP MILP + metrika „zabráněná přetížení" + tři scénáře.
- **Týden 4 — Demo + byznys + pitch.** Streamlit explorer + n8n refresh (ukázat) + 8slidový deck + technické shrnutí 1 A4 + **nácvik 3min prezentace**.
- **Pravidlo.** Vždy měj běžící (i jednoduchou) verzi každé vrstvy, teprve pak vylepšuj.

---

## 9 · Rizika a co s nimi

| Riziko | Mitigace |
|---|---|
| Model neporazí baseline | poměrové featury, trend, feature selection, derived indexy; pokud ani tak, ukaž, kde model pomáhá v rankingu, ne jen v MAE |
| Demo nepoběží na pitchi | Streamlit lokálně + **záznam jako záloha**; jednoduchost > efektnost |
| Leakage zkreslí výsledky | Trust Layer hlídá korelaci featur s cílem, striktní train/val split, žádné `*_2030` jako vstup |
| MILP infeasible / nereálný | malá instance řeší CBC rychle; když infeasible, uvolni equity floor nebo zvyš rozpočet; fallback greedy s opravou přetížení |
| Byznys čísla zpochybněna | prezentuj jako **rozpětí + metoda**, ne jako jistota; odkaz na MPO/PRE ceníky |
| Etika působí formálně | ukaž **konkrétní mechanismus** (fairness gap, confidence známka), ne odstavec |

---

## 10 · Checklist před odevzdáním

1. ☐ Číslo proti baseline na `zones_validation.csv` (MAE + Precision@50)
2. ☐ Pásmo P10/P50/P90 + tři scénáře z `future_scenarios.csv`
3. ☐ Běžící demo (Streamlit) + záznam jako záloha
4. ☐ Metrika „zabráněná přetížení" z optimalizéru
5. ☐ Všechny 4 etické oblasti s konkrétním mechanismem, cold-start jako funkce
6. ☐ Konkrétní zákazník + ceník v Kč + ROI metrika
7. ☐ Škálování (Brno/Plzeň + jiná infrastruktura)
8. ☐ Datové výstupy ve formátu `sample_submission.csv`
9. ☐ Pitch 8 slidů + technické shrnutí 1 A4
10. ☐ Odevzdáno na platform.aiolympiada.cz

---

*Napojení na reálné cíle (relevance, 20 %): Klimatický plán HMP do 2030 (10 000 stanic) · Generel rozvoje dobíjecí infrastruktury HMP (~180 000 EV, ≥ 4 500 stanic) · pilot Smart Prague + PRE · IPR Praha · opendata.praha.eu · golemio.cz/data · czso.cz · MPO · premobilita.cz.*
