# VoltPlán — Technická dokumentace

**Česká AI Olympiáda 2026 · AI Startup · krajské kolo Praha · zadání AIO_PHA-02-PHA**
**Tým notokens** · *„Praha v pohybu a pod proudem"*

> **VoltPlán** je B2G datová služba, která pomocí AI vyhodnotí pro **každou zónu Prahy**, kde má
> smysl stavět dobíjecí stanice — tak, aby město neutopilo peníze v prázdných dobíječkách a aby
> nová zátěž nepřetížila lokální síť. Propojuje **mobilitu** (kde a kolik se bude nabíjet)
> s **energetikou** (kde síť unese zátěž), což je podle zadání nejsilnější možná cesta.

---

## 1 · Problém a zákazník

Klimatický plán hl. m. Prahy do 2030 cílí na **až 10 000 veřejných dobíjecích stanic** (Generel
HMP střední scénář: ~180 000 EV a min. 4 500 stanic). Investice jde do miliard. Z oborových dat
ale **~30 % veřejných dobíječek končí podvyužitých** — postavených bez datové analýzy poptávky a
kapacity sítě. To je mrtvý kapitál a zároveň riziko: nová rychlonabíjecí zátěž ve večerní špičce
může lokálně přetížit transformační stanici (TS).

| | |
|---|---|
| **Zákazník (instituce)** | Hl. m. Praha / městská část / **Operátor ICT (Golemio)** / **distributor (PRE)** / energetická komunita |
| **Konkrétní role** | plánovač mobility na magistrátu, **energetik distributora** |
| **Co ho pálí** | kam z omezeného rozpočtu umístit stanice, aby se využily a síť je unesla |
| **Dnešní stav ho stojí** | desítky milionů Kč v podvyužitých stanicích + riziko lokálního přetížení |

VoltPlán dává odpověď, kterou tabulka „hodně lidí → velký hub" nedá: **kde se vyplatí stavět
s ohledem na poptávku 2030 × rezervu sítě × mezeru v pokrytí × férovost.**

---

## 2 · Data: reálné vs. modelové, a jak jsme je čistili

Jednotkou je **zóna odvozená od transformační stanice (TS)**. Pracujeme s bohatým datasetem
Linie A (Nabíjení a síť).

| Soubor | Obsah | Řádků | Použití |
|---|---|---|---|
| `zones_train.csv` | profil zóny: reálné + odvozené vstupy + modelové cíle 2030 | 2 378 | **trénink** |
| `zones_validation.csv` | menší slice (stejné sloupce) | 517 | **holdout — poctivá validace** |
| `stations_by_zone_real.csv` | reálné stanice MPO přiřazené k zónám | 855 | obvody, stávající nabídka |
| `grid_capacity_and_reserve_2025.csv` | výkon TS, špička, limit, **rezerva** | 3 408 | grid headroom |
| `candidate_solutions.csv` | katalog 6 typů dobíjecího řešení | 6 | doporučený typ (porty, kW) |
| `future_scenarios.csv` | konzervativní/střední/ambiciózní růst EV | 4 | **pásmo nejistoty 2030** |
| `hourly_*` | 4 reprezentativní týdny po hodinách (zátěž, overload) | 2,29 M | časový kontext (lazy) |

**Kontrola dat (součást úlohy):**
- **Reálné (`_real`)** = měřené/registrované (ČSÚ, RÚIAN, IPR, MPO, PRE mapová vrstva).
  **Odvozené (`_derived`)** = indexy z reálných vstupů. **Syntetické (`_synthetic`)** = modelové,
  **nikoli měření PRE**. Toto rozlišení řídí anti-leakage (§4).
- Velká CSV čteme přes **polars (lazy), `float32`**, nikdy celá do paměti — `hourly_*` má 2,29 M řádků.
- Ošetřeny chybějící hodnoty (`ignore_errors`, `infer_schema_length=10000`), různý zápis obcí
  (`„Praha 4 - Chodov"` → `Praha 4`), duplicitní záznamy stanic agregovány na zónu.
- **Poctivý limit dat**: většina dnešních veřejných bodů je pomalá (≤ 22 kW), veřejné dobíjení je
  doplňkové → pracujeme s **pásmem scénářů**, ne s jedním zaručeným číslem (§7).

---

## 3 · AI jádro — dva běžící modely + skóre

VoltPlán **není jednorázová analýza zakončená grafem**. Jsou to dva natrénované modely, které
v produktu trvale pracují a přepočítají se, jak přicházejí nová data.

### 3.1 Predikce poptávky (regrese) — *hlavní AI signál*
- **Model:** LightGBM regrese (`n_estimators=600`, `lr=0.03`, `num_leaves=31`), CPU.
- **Cíl:** `estimated_ev_count_2030_synthetic` — predikovaná poptávka po nabíjení v zóně 2030.
- **Featury:** **60** reálných/odvozených/2025-kapacitních sloupců (zástavba, byty bez stání,
  landuse, parking, veřejné osvětlení, MHD, silnice, **rezerva sítě 2025**, indexy rezidenčnosti
  a citlivosti sítě). Bohatý profil, ne jeden údaj.

### 3.2 Doporučení typu stanice (klasifikace) — *recommender*
- **Model:** LightGBM klasifikátor → jeden ze **6 typů** z `candidate_solutions.csv`
  (`residential_ac_small/medium`, `destination_dc50`, `fast_hub_150`, `mixed_mobility_hub`,
  `none_monitor`). Z typu se doplní počet portů a výkon kW.

### 3.3 Suitability skóre 0–100 — *kompozit, který propojuje mobilitu a energetiku*

```
suitability = 100 × ( 0.40 · poptávka_2030      (LightGBM)
                    + 0.30 · coverage_gap        (poptávka − stávající stanice)
                    + 0.15 · grid_headroom       (rezerva TS 2025)
                    + 0.15 · equity_weight )     (domácnosti bez vlastního stání)
```

Každá složka je z reálných dat nebo z modelu, normalizovaná přes celé město. Skóre je **plně
interpretovatelné** — appka u každé zóny ukáže `top_reasons` („vysoká poptávka; málo stávajících
stanic; volná síť; mnoho bytů bez stání").

### 3.4 Výstupní kontrakt
Modely vyrobí jediný soubor `submissions/app_zone_scores.csv` (16 sloupců), který appka čte:
`grid_zone_id, district, center_lat/lon, population, predicted_demand_2030, grid_headroom,
current_stations, coverage_gap, equity_weight, suitability_score, recommended_type,
recommended_ports, recommended_total_kw, top_reasons`.

**Skórujeme všech 2 895 zón = celá Praha, 22 správních obvodů** (sandbox umožňuje skórovat vše;
metriky měříme jen na odděleném holdoutu — §4).

---

## 4 · Proč je to opravdová AI (ne tabulka) + anti-leakage

### Že to není triviální pravidlo
Porovnáváme proti **populační baseline** („víc lidí → víc nabíjení", což zvládne tabulka):

| Model | MAE (EV/den) | RMSE | Precision@50 |
|---|---|---|---|
| **LightGBM (náš)** | **4,63** | 7,67 | **0,84** |
| baseline ∝ populace | 5,66 | 7,98 | 0,84 |
| baseline = průměr | 29,47 | 38,34 | 0,08 |

→ Model má **MAE o 18,1 % nižší** než triviální populační pravidlo a najde i **méně očekávané, ale
sedící** zóny (malá populace, ale tranzit + volná síť + žádné stanice), které pravidlo mine.
**Recommender typu stanice: 83,8 % přesnost** na holdoutu.

### Anti-leakage (kontrolováno kódem)
Sdílená funkce `feature_cols` automaticky **vyřazuje z featur** vše, co je cíl nebo z cíle
odvozené: `target_*`, `_2030_synthetic` (tedy i `estimated_ev_count_2030`), `recommended_*`,
`risk_overload`, ID sloupce a textové sloupce. V kódu je **runtime `assert not leaky`**.
Modely se učí z 60 reálných/2025 featur, **nikdy z budoucích cílů**.

### Poctivá validace
Trénujeme na `zones_train`, **metriky měříme jen na odděleném `zones_validation`** (holdout).
Predikce na trénovacích zónách (pro mapu celého města) jsou označené jako in-sample; **čísla
v dokumentaci a v appce pocházejí výhradně z holdoutu.** Žádné odevzdání na skryté labely —
data jsou sandbox.

---

## 5 · Běžící produkt (živá ukázka)

Streamlit dashboard `src/app_premium.py` nad výstupem modelu — **navržený pro městského úředníka**:

- **3 přepínatelné heatmapy** celé Prahy (model-driven): ① vhodnost (suitability), ② projektovaná
  spotřeba 2030, ③ potřeba nových stanic 2030; hlavní vrstva = souvislý heat **zelená → červená**.
- **Filtr po obvodech** (Praha 1–22), min. skóre, slider „kolik nových stanic plánuješ" →
  **očíslované špendlíky = KAM stavět**.
- Vrstva **„všechny potřebné stanice 2030"** obarvená dle typu stanice (AC/DC/hub).
- **Detailní popup „proč"** u každé zóny, **žebříček TOP-N**, **export CSV/GeoJSON**.
- **Rozpočtový optimalizátor** („mám X mil. Kč → kam pro max pokrytí poptávky").
- Tab **Model & metodika**: živé metriky, anti-leakage, etika.

Stack: **Python · LightGBM · scikit-learn · polars · Streamlit · folium**. Trénink ~2 min na CPU
(Intel Lunar Lake, bez CUDA).

---

## 6 · Byznys: kontinuální služba, ne studie

| Otázka | VoltPlán |
|---|---|
| **Zákazník** | Magistrát HMP / MČ / Operátor ICT / **PRE** / energetická komunita |
| **Opakovaná hodnota** | skóre se **přepočítává**, jak přibývají EV, stanice a mění se rezerva sítě — ne jednorázový výpočet |
| **Sběr dat v čase** | napojení na pilot **PRE/Smart Prague** (obsazenost, kWh, doba nabíjení) a **Golemio** (parkování, doprava); registr EV; aktualizace profilu zóny |
| **Monetizace** | **roční licence (SaaS)** ~300 tis. Kč/rok pro město/MČ; vyšší tarif pro distributora |
| **Návratnost** | cílení místo plošného rozmístění sníží podíl podvyužitých stanic z ~30 % na ~10 % → z rozpočtu např. 60 mil. Kč **uchrání ~12 mil. Kč**; licence se vrátí už při jediné nepostavené prázdné stanici |
| **Škálování** | další města (Brno, Plzeň, Ostrava) stejným pipeline; další infrastruktura (P+R, sdílená mobilita, energetické komunity) |

Čísla jsou **konzervativní a obhajitelná** — žádné spekulativní násobky. Náklady stanic vychází
z reálu ČR (veřejná AC ~0,2–0,4 mil. Kč, DC rychlo ~1–2 mil. Kč).

---

## 7 · AI etika — všechny 4 oblasti

1. **Chybná predikce a odpovědnost.** Výstup je **podpora rozhodnutí, ne automat** — člověk
   (úředník) rozhoduje. Kvalitu měříme na holdoutu a model lze **přetrénovat**, jak dorazí reálná
   data o obsazenosti z pilotu PRE → chyba se pozná (skutečné využití vs. predikce) a opraví.
2. **Soukromí.** Pracujeme **výhradně se zónovými agregáty** (TS-oblast, ČSÚ/RÚIAN), **žádná data
   o jednotlivcích**, žádné individuální trasy či platby. Profil zóny nelze rozklíčovat na osobu.
3. **Spravedlnost / cold-start.** Spirálu „málo dat v okrajové čtvrti → horší doporučení → žádná
   infrastruktura → lidé nepřejdou → dál chybí data" **aktivně lámeme**: složka `equity_weight`
   (index domácností bez vlastního stání) **zvyšuje skóre okrajových a méně bohatých čtvrtí**.
   Content-based featury (profil zóny), ne collaborative, takže **řídké zóny nejsou znevýhodněné**.
4. **Komunikace nejistoty.** Predikce 2030 **prezentujeme jako pásmo scénářů**
   (`future_scenarios.csv`: konzervativní / střední / ambiciózní), ne jako jedno „zaručené" číslo.
   U řídkých zón hlásíme nižší jistotu. Město tak nedělá přehnaně sebejistá rozhodnutí.

---

## 8 · Náš úhel + zahraniční inspirace na Prahu

Nejzřejmější řešení je „kam dát velký hub". My místo toho skórujeme **každou zónu** kompozitem,
který **propojuje mobilitu a energetiku** — poptávka × rezerva sítě × mezera × férovost. To je ten
průnik, který zadání označuje za nejsilnější.

**Zahraniční trend lokalizovaný na Prahu:** ve světě vznikají *EV charging suitability /
grid-aware siting* nástroje (např. NCSU EVSE suitability map s vrstvou **grid headroom**,
StreetLight a Justice40 **equity** vrstvy, EV-Planner multikriteriální optimalizace). Přenášíme
jejich tři diferenciátory — **AI suitability scoring, vrstva kapacity sítě, equity analýza** — na
pražská data a cíle (Klimatický plán 2030, Smart Prague/PRE pilot, Generel HMP). V Praze to sedí
o to víc, že **rezerva TS je úzké hrdlo** a podíl bytů bez vlastního stání je vysoký.

---

## 9 · Shrnutí pro porotu

| Kritérium (váha) | Jak ho plníme |
|---|---|
| **Technické (40)** | 2 běžící modely (regrese + recommender), MAE −18,1 % vs baseline, P@50 0,84, recommender 83,8 %, kontrolovaný anti-leakage, interpretace „proč", cold-start v modelu |
| **Byznys (40)** | jasný zákazník (HMP/PRE), roční licence, sběr dat v čase (PRE/Golemio), obhajitelná návratnost, škálování na další města |
| **Prezentace + etika + region (20)** | běžící živé demo, **všechny 4 etické oblasti**, napojení na Klimatický plán/Smart Prague/IPR, vlastní úhel + zahraniční inspirace, pásmo nejistoty |

**Reprodukce:** `python src/generate_scores.py` → `streamlit run src/app_premium.py`.

`AIO_PHA-02-PHA · Česká AI Olympiáda 2026 · tým notokens · data = sandbox (reálná + modelová)`
