ČESKÁ AI OLYMPIÁDA 2026
AI STARTUP · KRAJSKÉ KOLO

Dobíjet tam, kde lidé žijí —
a nepřetížit přitom síť

Chytré rozmístění a kapacitní plánování dobíjecí infrastruktury pro
elektromobilitu v Praze.

Kód zadání

AIO_PHA-02-PHA

Kraj

Téma

Hlavní město Praha

Čistá mobilita a chytré město (RIS3)

Typ úlohy

Predikce + párování (matching)

Odborný partner

Operátor ICT / Smart Prague · PRE · IPR Praha

Zákazník (hint)

Hl. m. Praha / městská část / Operátor ICT

nvias, z.s. · info@nvias.org · CC BY-NC-SA 4.0

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

1 · Kontext: proč to řešíme

Praha se zavázala k čisté mobilitě a počet elektromobilů v jejích ulicích rychle roste —
Česko vstoupilo do roku 2026 s více než 59 000 elektromobily a veřejná dobíjecí síť za rok
2025 povyrostla o 19 %. Pro velkou část Pražanů, kteří bydlí v bytech bez vlastní garáže
nebo vyhrazeného stání, je ale „kde a kdy nabít“ tou hlavní praktickou překážkou přechodu
na elektromobil. A kvůli dobíjení, když po práci večer začnou nabíjet desítky aut ve stejné
čtvrti, lokální distribuční síť jde do špičky.

Praha tuto výzvu aktivně řeší. Klimatický plán hl. m. Prahy do roku 2030 cílí na 10 000
veřejných dobíjecích stanic; městský Generel rozvoje dobíjecí infrastruktury počítá ve
středním scénáři s přibližně 180 000 elektromobily v Praze v roce 2030 a potřebou alespoň
4 500 stanic. Město už také pilotně sbírá data — v projektu Smart Prague s PRE datová
platforma získává ze stanic obsazenost, počet uživatelů, odběr energie i dobu nabíjení, a
osvědčují se i dobíječky na stožárech veřejného osvětlení. Co zatím chybí, není snaha ani
plán — chybí jednoduchý, přímočarý nástroj, který městu a městským částem napoví, kam a
jakého typu dobíjecí body přidat nejdřív, aby pomohly nejvíce lidem a přitom nezatížily síť.
Pro tento problém můžeme využít AI.

Čtyři otázky bez snadné odpovědi

1.  Jak poznáme, kde bude poptávka po veřejném dobíjení největší za tři roky — ne dnes,
ale až aut přibude — a jak odlišíme čtvrť, která dobíječku skutečně využije, od té, kde
zůstane prázdná?

2.  Jak rozmístit dobíjení tak, aby pomohlo i lidem bez vlastního stání v hustých sídlištích a

vnitřním městě — a nejen řidičům u nákupních center a tranzitních tahů?

3.  Kde se vyplatí pomalé noční nabíjení u domu a kde rychlý hub — a jak přitom nepřetížit

lokální trafostanici v podvečerní špičce?

4.  Komu má taková služba sloužit a kdo za ni zaplatí, aby běžela a zlepšovala se i za pět

let — ne jen jako jednorázová analýza?

Reálná data, ze kterých vycházíme

•  ČR: přes 59 000 elektromobilů (vstup do 2026); veřejná síť 7 574 bodů (z toho 967

≥ 150 kW), růst +19 % za 2025.

•  Praha — cíle: 10 000 veřejných stanic do 2030 (Klimatický plán); Generel (2/2021,

střední scénář): ~180 000 EV a ≥ 4 500 stanic do 2030.

•  Pilot: Smart Prague + PRE — platforma sbírá ze stanic obsazenost, počet

uživatelů, odběr kWh a dobu nabíjení.

Poctivá poznámka o nejistotě: poptávka v roce 2030 závisí na cenách, dotacích i
chování a je nejistá; většina dnešních veřejných bodů je pomalá (≤ 22 kW) a veřejné
dobíjení bývá doplňkové. Predikce na pět let proto pracuje s pásmem scénářů, ne s
jedním „zaručeným“ číslem.

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

2

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

Vaším úkolem je navrhnout AI produkt nebo datovou službu, která tyto otázky pomáhá
řešit — pro konkrétního zákazníka, s reálnou hodnotou a promyšlenou etikou. Inspirujte
se přiloženými daty, ale nebojte se jít vlastní cestou.

2 · Datová sada

Dostáváte složku participants s povinnou částí core (9 CSV, přibližně 251 MB) a rozšiřující
částí optional (přibližně 1,6 GB). Jednotkou je zóna odvozená od veřejného identifikátoru
oblasti transformační stanice (TS). Train a validation obsahují cíle, test je bez cílů. Soukromé
testovací labely zůstávají pořadateli a účastníkům se nepředávají.

Soubor

zones_train.csv

zones_validation.csv

Obsah

Trénovací zóny: reálné a odvozené vstupy +
syntetické cíle pro rok 2030

Validační zóny se stejnými vstupy a cíli pro
lokální vyhodnocení

zones_test.csv

Testovací zóny bez cílových sloupců

stations_by_zone_real.csv

grid_capacity_and_reserve_2025.csv

Reálné záznamy stanic MPO přiřazené k
oblastem přes grid_zone_id

Modelový výkon TS, základní špička, provozní
limit a odběrová rezerva

Řádků

2 378

517

513

855

3 408

hourly_grid_and_charging_history_2025.
csv

Čtyři reprezentativní týdny: zatížení, rezerva,
počasí a nabíjení po hodinách

2 290 176

candidate_solutions.csv

Katalog šesti typů dobíjecího řešení

future_scenarios.csv

Konzervativní, střední a ambiciózní scénář
rozvoje EV

6

3

sample_submission.csv

Přesný formát predikcí pro testovací zóny

513

Datový slovník (reálné R / odvozené O / syntetické S)

Přípona sloupce určuje původ: *_real vychází z otevřených dat, *_derived je výpočet z
reálných vstupů a *_synthetic je reprodukovatelná modelová hodnota.

zones_train.csv · zones_validation.csv · zones_test.csv

Sloupec / skupina

grid_zone_id, split

Význam

soutěžní ID zóny a geografické rozdělení train /
validation / test

transformer_station_id_real,
parent_substation_id_real

identifikátory z veřejné mapové vrstvy PRE; nejde o
ověřený pasport zařízení

center_lon_real, center_lat_real,
nn_area_sqm_real

poloha a plocha oblasti NN

R/O/S

O

R

R

generation_connectability_clas
s_real,
connection_requests_*_real

population_census_2021_real,
flats_*_real, building_*_real

veřejné indikátory připojitelnosti výroben a stav žádostí  R

obyvatelstvo, byty a zástavba z ČSÚ, RÚIAN a IPR

R

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

3

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

Sloupec / skupina

Význam

landuse_*_real, parking_*_real,
public_lighting_poles_real

charging_*_2026_real,
pid_stops_real,
major_road_segments_real

stations_by_zone_real.csv

*_derived

využití území, parkování a veřejné osvětlení

současná dobíjecí nabídka, MHD a silniční dostupnost  R

relační mapa MPO stanice × grid_zone_id: poloha,
provozovatel, body, výkon a typ nabíjení

index rezidenčnosti, cílové aktivity, chybějícího
soukromého stání a citlivosti sítě

target_*_2030_synthetic

denní kWh, špičkový kW, riziko přetížení a doporučený
typ / počet bodů / výkon

grid_capacity_and_reserve_2025.csv · hourly_grid_and_charging_history_2025.csv

Sloupec / skupina

Význam

rated_capacity_kw_synthetic

modelový jmenovitý činný výkon oblasti TS

base_peak_load_kw_2025_synt
hetic

operating_limit_kw_2025_synth
etic,
reserve_capacity_kw_2025_synt
hetic

timestamp_utc,
representative_season,
day_of_week, hour

temperature_c_real,
relative_humidity_pct_real,
precipitation_mm_real

base_load_kw_synthetic,
ev_charging_load_kw_synthetic
, total_load_kw_synthetic

charging_sessions_synthetic,
charging_energy_kwh_syntheti
c, occupied_ports_synthetic

available_capacity_after_ev_kw
_synthetic,
overload_flag_synthetic

modelová špička odběru bez nové poptávky EV

modelový provozní limit a rezerva před novým
nabíjením

časové znaky čtyř reprezentativních týdnů roku 2025

R/O

agregované desetiminutové měření ČHMÚ

R

modelová základní, nabíjecí a celková hodinová zátěž

S

agregovaná modelová historie veřejného nabíjení

modelová zbývající kapacita a překročení provozního
limitu

Pomocné soubory a optional data

Soubor / složka

Obsah

candidate_solutions.csv

typ řešení, počet bodů, výkon a modelová denní
kapacita

future_scenarios.csv

násobitele poptávky a řízené / neřízené špičky

optional/real_sources/

detailní PRE proxy, IPR, RÚIAN, ČSÚ, MPO, PID
GTFS, ČHMÚ a MHMP; přibližně 1,6 GB

optional/synthetic/quarter_hour
_grid_sample_2025.csv

300 zón, zimní a letní týden v 15minutovém kroku; 403
200 řádků

R/O/S

R

R

O

S

R/O/S

S

S

S

S

S

R/O/S

S

S

R

S

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

4

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

Soubor / složka

Obsah

docs/data_dictionary.csv

úplný strojově čitelný slovník všech sloupců

R/O/S

O

⚠  Než data použijete, zkontrolujte je. Reálné zdroje mohou obsahovat chybějící
hodnoty, různý zápis nebo opakované záznamy. Syntetické sloupce jsou modelová data,
nikoli měření PRE. Čištění, kontrola leakage a obhajoba feature engineeringu jsou
součástí úlohy.

Disclaimer (reálné vs. odvozené vs. syntetické). Reálné jsou veřejné prostorové podklady a
jejich agregace (PRE, ČSÚ, RÚIAN, IPR, MPO, PID, ČHMÚ a MHMP). Odvozené sloupce vznikají
výpočtem z těchto dat. Syntetické jsou výkon TS, zatížení, odběrová rezerva, historie nabíjení a cíle pro rok
2030. Veřejná vrstva PRE popisuje indikativní připojitelnost výroben, nikoli garantovanou kapacitu pro
odběr EV; realizace vždy vyžaduje technické posouzení distributora.

3 · Linie řešení (inspirace)

Následující linie nejsou povinné cesty ani menu — jsou to vodítka, kudy se dá vydat. Můžete
je kombinovat nebo jít vlastní cestou; nejsilnější řešení obvykle propojí předpověď poptávky
s chytrým doporučením.

Linie A — Předvídat poptávku (kde a kolik)

Model předpovídá poptávku po dobíjení v mikrozónách v čase a z ní odvodí plán rozmístění
a kapacit ve scénářích (opatrný vs. ambiciózní růst EV). Využijte poskytnutý dataset,
případně doplňte vlastní data z opendata.praha.eu.

Hodí se: regrese / rozhodovací stromy. Karty: Technická karta 1 a 2.

Linie B — Spárovat zónu s řešením (jaký typ kam)

Doporučovací engine páruje mikrozónu s vhodným typem dobíjecího řešení podle profilu
(poptávka, citlivost sítě, charakter zástavby, tranzit) a vykreslí mapu mezer — kde pokrytí
chybí. Využijte poskytnutý dataset, případně doplňte vlastní data z opendata.praha.eu.

Hodí se: content-based recommender (podobnost profilů). Karty: Technická karta 1 a 2.

Linie C — Hlídat síť (kdy a jak nabíjet)

Model navrhuje mix typů a rozložení nabíjení v čase tak, aby se lokální síť nepřetížila ve
špičce. Využijte poskytnutý dataset, případně doplňte vlastní data z opendata.praha.eu.

Hodí se: optimalizace / clustering nad predikcí. Karty: Technická karta 1 a Byznys karta 2.

Co musí splňovat každé řešení

Pilíř

Co to znamená

1 · Běžící AI algoritmus

Model, který v produktu trvale pracuje (prediktivní model nebo
doporučovací engine) — ne jednorázový výpočet nad daty.

2 · Sběr a údržba dat v
čase

Z čeho služba žije zítra: jak vzniká a aktualizuje se profil zóny, jak se
sledují nové stanice, registrace EV, obsazenost a kapacita sítě. Stačí
promyslet, popsat a obhájit v pitchi — nemusí být postaveno.

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

5

Co dělá doporučení (nebo predikci) dobrou

•  Překoná vaše řešení triviální shodu? „Hodně aut → velký hub“ zvládne i tabulka.

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

Ukáže váš model i méně očekávané, ale sedící umístění?

•  Pracuje s bohatším profilem než jediným údajem? Nejen počet aut, ale typ

Pilíř

zástavby, podíl bytů bez stání, kapacita sítě, tranzit, chování v čase.

Co to znamená

•  Zohledňuje trend, ne jen dnešek? Zóna s málo EV, ale rychle rostoucí poptávkou,

sedí jinak než zóna už nasycená.

3 · Kontinuální hodnota

Produkt běží a dává hodnotu opakovaně; tomu odpovídá i monetizace
(předplatné / služba).

4 · Technické úrovně a co je (a co není) AI řešení

Úroveň

No-code

Vhodné pro

Příklady

týmy bez programování — model i UI
poskládáte z nástrojů

Simple ML for Sheets, tabulkové nástroje

Low-code

rychlé UI + napojení na model přes API

Code

plná kontrola nad modelem i daty

vibe-coding (Lovable, v0, Bolt, Replit
Agent), Make

Python (scikit-learn, pandas), vlastní
recommender

Co se počítá jako AI řešení

•  Vibe-coding je vítán pro vrstvu rozhraní (jak to vypadá a ovládá se).

•  Pod rozhraním ale musí být skutečná AI komponenta — predikční model nebo

doporučovací engine, který se učí z dat.

•  Tu je nutné v pitchi předvést (živě nebo na záznamu). Bez toho je 0 bodů za

Technické řešení.

Porota chce vidět běžící model nebo engine

5 · Tipy na technické řešení

•  Matching / mapa mezer: spárování zón s řešeními plus vizualizace, kde pokrytí chybí

(poptávka vs. nabídka po zónách).

•  Clustering / optimalizace: shlukněte podobné zóny a hledejte rozmístění při

rozpočtovém a síťovém omezení.

Čím jednodušší AI, tím důležitější je ji dobře interpretovat.

6 · Byznys záměr: kontinuální služba

Cílem není jednorázová studie, ale produkt, který běží a opakovaně přináší hodnotu.
Promyslete:

Otázka

K zamyšlení

Zákazník (instituce)

Problém

Hl. m. Praha / městská část / Operátor ICT? Vedle nich konkrétní role:
energetik distributora, plánovač mobility.

Co konkrétně zákazníka pálí a kolik ho dnešní stav stojí (prázdné
dobíječky, stížnosti, pomalý přechod na EV)?

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

6

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

Otázka

K zamyšlení

Řešení (opakovaně)

Sběr dat v čase

Monetizace (opakovaný
příjem)

Návratnost pro zákazníka

Co služba dělá znovu a znovu — ne jednou, ale průběžně, jak se
mění data?

Jak data vznikají a aktualizují se: nové stanice, registrace EV,
obsazenost z pilotu PRE, odhady kapacity sítě.

Předplatné / služba — kolik a za co? Stačí navrhnout a obhájit.

Dostupné dobíjení → rychlejší přechod na EV → nižší emise a hluk,
lepší ovzduší i image čtvrti, lépe využité investice. Služba = investice,
ne výdaj.

Škálovatelnost

Další města (Brno, Plzeň, Ostrava)? Jiná infrastruktura (P+R, sdílená
mobilita)?

Příklad jen pro inspiraci: služba, kterou si město nebo městská část předplácí a která průběžně
sleduje růst EV, obsazenost stanic a kapacitu sítě a doporučuje, kam a jakého typu přidat další dobíjení.
Není to jediné správné řešení — jen ukázka.

7 · AI etika

Etika tu vyrůstá z jádra úlohy. Zpracujte všechny čtyři oblasti:

1.  Chybná predikce a odpovědnost. Co když model doporučí dobíječku tam, kde

zůstane prázdná (mrtvá investice), nebo přehlédne čtvrť s velkou potřebou? Kdo nese
odpovědnost a jak se chyba pozná a opraví?

2.  Přístup k datům a soukromí. Data o nabíjení a pohybu prozrazují, kde lidé bydlí a

jezdí. Jak je chránit a co je ještě v pořádku agregovat?

3.  Spravedlnost (cold-start). O okrajových a méně bohatých čtvrtích máme málo dat →
model jim dává horší doporučení → dobíječky tam nevzniknou → lidé nepřejdou na EV
→ dál nevznikají data. Jak takovou sebenaplňující spirálu rozpoznat?

4.  Komunikace nejistoty. Predikce poptávky na rok 2030 je nejistá. Jak ji prezentovat

městu, aby nedělalo přehnaně sebejistá rozhodnutí?

Absence etiky = 0 bodů v kategorii AI etika.

8 · Karty nápovědy

Máte k dispozici čtyři karty — dvě technické a dvě byznysové. Čerpáte je u poroty nebo
mentora; nejsou nijak časově omezené.

Karta

K čemu slouží

Technická 1 — Model a featury  volba modelu, práce s trendem, jak doložit, že výstup překonává

baseline / náhodu

Technická 2 — Data a
cold-start

Byznys 1 — Zákazník a
monetizace

čištění dat, chybějící hodnoty, řídké profily okrajových zón, validace

kdo platí, opakovaný příjem, návratnost pro město / region

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

7

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

Karta

K čemu slouží

Byznys 2 — Sběr dat a
škálování

9 · Odevzdání

jak služba žije zítra, jak ji rozšířit na další města a typy infrastruktury

Průběžně odevzdávejte na platform.aiolympiada.cz. Odevzdejte: odkaz na běžící řešení nebo
kód, datové výstupy (predikce / doporučení), pitch deck a technické shrnutí na 1 A4.

10 · Pitch

Pitch deck má maximálně 8 slidů. Doporučený obsah (checklist):

1.  Problém a zákazník — kdo je zákazník a co ho pálí

2.  Data — co je reálné vs. modelové a jak jste data čistili

3.  AI model / engine — a hlavně jak měříte kvalitu — že výstup překonává baseline /

náhodu

4.  Výsledky a živá ukázka — co model doporučuje a jak to vypadá v praxi

5.  Byznys model — opakovaný příjem + sběr dat v čase

6.  Etika — čtyři oblasti, zvlášť spravedlnost / cold-start

7.  Škálování — kam dál (města, typy infrastruktury)

8.  Tým a shrnutí — kdo jste a proč to dává smysl

Živá prezentace: 3 minuty prezentace + 2 minuty na dotazy. Video je nepovinné. Technické
shrnutí odevzdejte na 1 A4.

11 · Hodnoticí kritéria (40 / 40 / 20)

Kategorie (váha)

Co porota hodnotí

Technické řešení — 40

běžící AI (predikce / recommender); kvalita dat a čištění; doložené
překonání baseline; interpretace výstupů; práce s cold-startem

Byznysový potenciál a hodnota
— 40

jasný zákazník (instituce); opakovaný příjem; sběr dat v čase;
návratnost pro město a region; škálovatelnost

Prezentace, etika a regionální
relevance — 20

srozumitelný pitch a ukázka; zpracování 4 etických oblastí;
napojení na reálné pražské cíle a partnera (Smart Prague / PRE /
IPR); komunikace nejistoty

12 · Inspirační zdroje

•  Klimatický plán hl. m. Prahy do 2030 — cíle čisté mobility a dobíjení.

•  Generel rozvoje dobíjecí infrastruktury HMP — scénáře počtu EV a stanic do 2030

(portál HMP / IPR).

•  opendata.praha.eu a golemio.cz/data — otevřená městská data (doprava, životní

prostředí).

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

8

Česká AI Olympiáda 2026  |  AI Startup  |  AIO_PHA-02-PHA  |  Praha

•  smartprague.eu — projekt dobíjecích stanic PRE a další chytrá řešení.

•  czso.cz — ČSÚ: obyvatelstvo a vozidla podle městských částí.

•  MPO — přehled veřejných dobíjecích stanic; premobilita.cz — mapa stanic PRE ke

stažení.

AIO_PHA-02-PHA  |  Česká AI Olympiáda 2026  |  nvias, z.s.  |  info@nvias.org  |  CC BY-NC-SA 4.0

9


