# AIO_PHA-02-PHA — AKTUALIZOVANÉ ZADÁNÍ (2026-06-09)

> ⚠ Toto je nejnovější verze zadání (nahrazuje `zadani_AIO_PHA-02-PHA.md`). Text byl vložen
> z kopie a má místy OCR/copy artefakty (přerušená slova). Čistý zhuštěný výklad = `../BRIEF.md`.
> Hlavní změny: téma = mobilita+energetika, V2G „nejhlubší příležitost", sandbox (ne soutěž),
> 4 linie A–D, bonus za vlastní úhel + zahraniční trend na Prahu.

---

ČESKÁ AI OLYMPIÁDA 2026 · AI STARTUP · KRAJSKÉ KOLO
**Praha v pohybu a pod proudem** — Mobilita a energetika se ve městě potkávají. Najděte, kde
jim AI pomůže nejvíc — bez přetížené sítě, rozpočtu i ulic.

| Pole | Hodnota |
|---|---|
| Kód zadání | AIO_PHA-02-PHA |
| Kraj | Hlavní město Praha |
| Téma | Udržitelná mobilita a energetika (RIS3 — Chytré město) |
| Typ úlohy | Predikce · doporučování (matching) · optimalizace — podle zvolené cesty |
| Partner krajského kola | Magistrát hlavního města Prahy |
| Datový a odborný ekosystém | Operátor ICT / Golemio · Smart Prague · PRE · IPR Praha |
| Zákazník (hint) | Hl. m. Praha / MČ / Operátor ICT / distributor / energetická komunita |
| Formát | Tým 3 studentů · Pitch 3 min + 2 min dotazů · 4 konzultační karty |

nvias, z.s. · info@nvias.org · CC BY-NC-SA 4.0

## 1 · Kontext
Praha mění, jak se po ní lidé/zboží pohybují i jak se vyrábí a spotřebovává energie.
Elektromobilů přibývá, večerní špička jde na hranu. Doprava a energetika se prolínají.
Klimatický plán hl. m. Prahy do 2030 spojuje dopravu a energetiku — 69 opatření v 5 oblastech
(energetika, budovy, doprava, cirkulární ekonomika, adaptace). Chybí jednoduché nástroje, které
z dat rychle ukážou, kde a co pomůže nejvíc. Tady pomáhá AI.

**Čtyři otázky bez snadné odpovědi**
1. Jak pohnout rostoucím počtem lidí a aut tak, aby ubylo zácp, emisí i ztraceného času — ne jen přidávat pruhy a parkoviště?
2. Jak přibývajícím EV nabídnout, kde a kdy nabít, aniž se ve špičce přetíží lokální síť?
3. Kdy poslat člověka na P+R a do tramvaje místo auta — a kdy je auto baterie/zdroj, který může vrátit energii síti/čtvrti (V2G)? Komu má služba sloužit a kdo ji zaplatí, aby běžela i za 5 let?

**Reálná data, ze kterých vycházíme**
- ČR: přes 59 000 EV (2026); veřejná síť ~7 574 bodů, +19 % za 2025.
- Klimatický plán Prahy 2030: 10 000 veřejných stanic; −18 % fosilních paliv; MHD +150 mil. cestujících; rozšiřování zón placeného stání a zpoplatnění vjezdu; OZE (až 23 000 budov se solár./kogen. zdroji) + Pražské společenství pro obnovitelnou energii.
- Generel rozvoje dobíjecí infrastruktury HMP (2/2021, střední): ~180 000 EV a ≥4 500 stanic do 2030.
- Pilot Smart Prague + PRE: platforma sbírá obsazenost, počet uživatelů, odběr kWh, dobu nabíjení.
- Poctivá poznámka: většina veřejných bodů je pomalá (≤22 kW), veřejné dobíjení bývá doplňkové. Pracujte s pásmem scénářů.

> Vaším úkolem je navrhnout AI produkt nebo datovou službu, která **některou** z otázek řeší —
> pro konkrétního zákazníka, s reálnou hodnotou a etikou. Přiložená data jsou **sandbox**, ne
> zadání samo. Inspirujte se, ale nebojte se jít vlastní cestou.

## 2 · Data
**Bohatý dataset = jen pro Linii A** (nabíjení a síť), ~251 MB, `participants` (Google Drive).
Všechny zóny mají vyplněné modelové cíle — data slouží ke stavbě/validaci/interpretaci, **NE k
soutěži o skóre**. Chceš-li poctivě validovat, část dat si odlož stranou (holdout).

| Soubor | Řádků |
|---|---|
| zones_train.csv | 2 378 |
| zones_validation.csv | 517 |
| stations_by_zone_real.csv | 855 |
| grid_capacity_and_reserve_2025.csv | 3 408 |
| hourly_grid_and_charging_history_2025.csv | 2 290 176 |
| candidate_solutions.csv | 6 |
| future_scenarios.csv | 3 |

Původ sloupců: `_real` (R) / `_derived` (O, výpočet z reálných) / `_synthetic` (S, modelová).
`target_*_2030_synthetic` = denní kWh, špičkový kW, riziko přetížení (modelové cíle).

**Otevřená pražská data (linie B/C/D — přines/doplň vlastní):** Golemio (platby v zónách stání —
jen nerezidenti; real-time parkování; dojezdy Waze 400+ úseků; cyklosčítače; polohy PID; GTFS),
ŘSD/NDIC + městské kamery (obraz), opendata.praha.eu.

⚠ Zkontrolujte data (chybějící hodnoty, různý zápis, duplicity). Syntetické = modelová, ne měření PRE.
Parkovací platby pokrývají jen nerezidenty → samy neukazují skutečnou obsazenost.

## 3 · Linie řešení (jen inspirace, ne menu)
Nejsilnější řešení obvykle propojí mobilitu a energetiku. Lze kombinovat / jít vlastní cestou.

- **Linie A — Nabíjení a síť (auto jako spotřebič i ZDROJ):** predikce poptávky + kapacity v čase →
  nejen KAM přidat body, ale hlavně KDY a JAK nabíjet, aby auta síť nezatěžovala, ale pomáhala jí —
  **řízené nabíjení a obousměrné nabíjení (V2G)**. Bohatý dataset (rezerva, hodinová zátěž, overload).
  *„Auto u nabíječky není jen spotřebič — podle doby stání může vrátit energii (V2G). To je nejhlubší
  příležitost tohoto zadání."* Hodí se: regrese/stromy + optimalizace rozložení v čase. Karty: T1, T2.
- **Linie B — Místo v centru:** předpověz a naveď řidiče na volné parkovací/nabíjecí místo, omez
  kroužení → míň zácp/emisí/zátěže sítě. Mapa mezer. Hodí se: predikce obsazenosti, content-based
  recommender/navigace. Karty: T1, B2.
- **Linie C — Přesun od auta (multimodalita):** recommender kombinace auto×P+R×MHD×kolo×sdílená +
  predikce poptávky po MHD (cíl +150 mil. cestujících 2030). Hodí se: recommender volby dopravy.
- **Linie D (obraz):** z dopravních kamer odhad obsazenosti parkování / hustoty provozu — náhrada
  chybějících senzorů. Hodí se: klasifikace/detekce obrazu (Teachable Machine). Karta: T1.

**Čekáme i kreativitu — jděte vlastní cestou.** Kombinujte, nebo přijďte s vlastním řešením
(vlastní úhel/data/zákazník). Najděte zahraniční trend a obhajte, proč by v Praze (ne)fungoval.
Porota originální a propojenou cestu ocení. **Jedna čistá, běžící linie může stačit.**

**Tři pilíře každého řešení:** 1) běžící AI algoritmus (ne jednorázový výpočet), 2) sběr a údržba
dat v čase (stačí promyslet+obhájit), 3) kontinuální hodnota (monetizace předplatné/služba).

## 4 · Technické úrovně
No-code (Simple ML for Sheets, Orange, Teachable Machine) · Low-code (vibe-coding Lovable/v0/Bolt/
Replit, Make) · Code (Python scikit-learn/pandas, vlastní recommender/optimalizace). Vibe-coding
vítán pro UI, ale pod ním musí být skutečná AI komponenta (predikce/recommender/optimalizace), kterou
**v pitchi předvedeš** — jinak 0 bodů za technické řešení. Jednorázová analýza zakončená grafem nestačí.

## 5 · Tipy + „co dělá predikci/doporučení dobrým"
Predikce/regrese; recommender (content-based vs collaborative — na malých datech vyhrává content-based,
cold-start); matching/mapa mezer; clustering/optimalizace; detekce z kamer. *Čím jednodušší AI, tím
důležitější je ji dobře interpretovat.* Dobré řešení: opravdová AI (ne triviální shoda „hodně aut →
velký hub"), bohatost profilu (víc než 1 údaj), zohlednění trendu (rostoucí vs nasycená zóna).

## 6 · Byznys (kontinuální služba)
Zákazník (instituce): Hl. m. Praha / MČ / Operátor ICT / distributor / energetická komunita (Pražské
společenství pro OZE). Problém (prázdné dobíječky, zácpy z kroužení, pomalý přechod na EV, přetížená
síť). Řešení opakovaně · sběr dat v čase (nové stanice, registrace EV, obsazenost PRE/Golemio, kapacita
sítě) · monetizace (předplatné; u V2G sdílení výnosu z flexibility) · návratnost · škálovatelnost
(Brno/Plzeň/Ostrava; P+R, sdílená mobilita, energetické komunity).

## 7 · AI etika (4 oblasti, absence = 0 bodů)
1. Chybná predikce a odpovědnost. 2. Přístup k datům a soukromí. 3. Spravedlnost (cold-start —
sebenaplňující spirála okrajových čtvrtí). 4. Komunikace nejistoty (predikce 2030 je nejistá).

## 8 · Karty
T1 Model a featury · T2 Data a cold-start · B1 Zákazník a monetizace · B2 Sběr dat a škálování.

## 9–10 · Odevzdání + Pitch
Průběžně na platform.aiolympiada.cz: odkaz na běžící řešení/kód, datové výstupy, pitch deck, 1 A4.
Deck ~8 slidů: 1) Problém+zákazník 2) Data (reálné vs modelové + čištění) 3) AI model — proč je to
opravdu AI a jak poznáš že funguje 4) Výsledky+ukázka 5) Byznys (opak. příjem, sběr dat, škálování)
6) Váš úhel + zahraniční inspirace na Prahu 7) Etika (cold-start) 8) Tým. Živě 3+2 min, video nepovinné.

## 11 · Kritéria (40/40/20)
- Technické 40: běžící AI (predikce/recommender/optimalizace); kvalita dat+čištění; **opravdová AI ne
  triviální pravidlo**; interpretace; cold-start.
- Byznys 40: jasný zákazník (instituce); opakovaný příjem; sběr dat v čase; návratnost; škálovatelnost.
- Prezentace/etika/relevance 20: srozumitelný pitch+ukázka; 4 etické oblasti; **chytré propojení
  mobility a energetiky; zahraniční inspirace lokalizovaná na Prahu**; komunikace nejistoty.

## 12 · Inspirační zdroje
Klimatický plán HMP 2030 (klima.praha.eu) · Plán udržitelné mobility Prahy (P+) „město krátkých
vzdáleností" · opendata.praha.eu, golemio.cz/data · smartprague.eu · czso.cz · premobilita.cz.
*Kam míří svět:* obousměrné nabíjení / auto jako zdroj, dynamické tarify a řízení poptávky, chytré
navádění na parkování, „město krátkých vzdáleností". Najdi 1 zahraniční trend a obhaj Prahu.
