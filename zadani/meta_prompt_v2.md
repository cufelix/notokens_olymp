# Meta-prompt: Generování zadání Česká AI Olympiáda 2026 (v2)
## Šablona pro tvorbu nových zadání ve filozofii AIO_SZ-01-UK, AIO_SZ-02-UK a AIO_SZ-02-KV

> **Co je nového ve v2:** Doplněn oddíl **„0. Kritický pohled — principy kvality"**, který zobecňuje poznatky z tvorby zadání AIO_SZ-02-KV (recommender pro propojení žáků, škol a firem). Obrazový dataset už není povinný — volí se technika podle problému. Byznys je nově kontinuální služba, ne jednorázová analýza. Přidána disciplína „reálná vs. modelová data" a nárok na kvalitu výstupu („překonej triviální baseline").

---

## Jak tento prompt použít

Zkopíruj celý blok níže do svého nástroje (ChatGPT, Claude, Gemini, Copilot…) a vyplň proměnné v sekci `[PARAMETRY ZADÁNÍ]`. **Nejdřív si přečti oddíl 0 — je to kritický filtr, kterým má projít každé zadání bez ohledu na téma.**

---

## PROMPT (začátek — kopíruj od zde)

Jsi expert na tvorbu vzdělávacích soutěžních zadání pro středoškoláky v oblasti umělé inteligence. Připravíš kompletní zadání pro krajské kolo soutěže Česká AI Olympiáda 2026, linie AI Startup, podle následujících parametrů a filozofie.

---

### 0. KRITICKÝ POHLED — principy kvality (čti první, platí pro každé zadání)

Tyto principy jsou nadřazené konkrétní struktuře níže. Když je struktura a princip v rozporu, vyhrává princip.

**0.1 Technika podle problému, ne problém podle techniky.**
Nešroubuj do zadání AI techniku jen proto, že „tam má být". Klasifikace obrazu, predikce, recommender, clustering — vyber to, co sedí na *jádro* problému, ne to, co vyplní tabulku tří linií.
- Problém typu „propojit / doporučit / spárovat" (žák↔obor, škola↔firma, pacient↔péče) → **recommender / matching**.
- Problém typu „naplánovat / odhadnout dopad" → **predikce / regrese / optimalizace**.
- Klasifikaci obrazu nasazuj jen tehdy, když je obraz skutečně jádrem úlohy, ne jako ozdobu. Test: kdyby porota smazala obrazovou linii, dává zbytek pořád smysl? Pokud ano, obraz tam možná nepatří.

**0.2 Linie jsou inspirace, ne menu.**
Tři linie prezentuj jako *ukázky možných směrů*, ne jako cesty k výběru. Tým může linie kombinovat nebo jít vlastní cestou. Formulace: „Následující linie nejsou povinné cesty ani menu — jsou to vodítka, kudy se dá vydat."

**0.3 Výstup je kontinuální byznys, ne jednorázová analýza.**
Nejčastější selhání: tým (i AI generující vzorové řešení) udělá krásnou datovou analýzu + návrh jednoho řešení a skončí. To je málo. Každé řešení musí splňovat tři pilíře:
1. **Běžící AI algoritmus** — model, který v produktu trvale pracuje (prediktivní model nebo recommendation engine), ne jednorázový výpočet.
2. **Návrh sběru a údržby dat v čase** — z čeho služba žije zítra: jak vzniká a vyvíjí se profil uživatele, jak se monitorují firmy / dění / pobídky v regionu. **Nemusí být postaveno — stačí promyslet, popsat a obhájit v pitchi.** (Vědomě tím zvyšujeme komplexitu v *myšlení*, ne v implementaci.)
3. **Kontinuální hodnota** — produkt běží a dává hodnotu opakovaně; tomu odpovídá i monetizace (předplatné / služba).

**0.4 Reálná vs. modelová data — disciplína a poctivost.**
Kotvi zadání reálnými veřejnými daty kraje (výroční zprávy, ČSÚ, krajské analýzy, oborové portály, dataportály). Ale:
- **Reálné je jen to, co reálně existuje** (názvy, počty, trendy z veřejných zdrojů). U každého sloupce/datové sekce **označ „reálné" vs. „modelové"**.
- **Nepředstírej data, která nikdo nezměřil.** Cílové „outcome" proměnné (zůstal v kraji, pracuje v oboru, uplatnil se) v ČR na úrovni jednotlivce veřejně neexistují → musí zůstat **modelové** a sloužit jen k ověření v rámci soutěže.
- Modelové proměnné smíš *informovaně doladit* reálným trendem (např. poptávku trendem odvětví), ale nevydávej je za oficiální statistiku.

**0.5 Kvalita výstupu musí překonat triviální baseline.**
Doporučení/predikce nesmí jen zrcadlit vstup. „Mám rád IT → studuj IT" zvládne i fulltext — to není AI hodnota. Do zadání zařaď nárok (formou otázek, ne návodů):
- Překoná řešení triviální shodu? Ukáže i **neočekávaný, ale sedící** výstup (serendipity)?
- Pracuje s **bohatším profilem** než jeden deklarovaný údaj (chování, koníčky, signály v čase)?
- Zohledňuje **trend**, ne jen aktuální stav (obor/jev, který dnes sedí, ale upadá, vs. nižší shoda s rostoucím trendem)?

**0.6 Tón vůči odbornému partnerovi a regionu.**
Nikdy nepiš „nikdo to neumí / neřeší", „spoléhá se na náhodu" apod. Partner a region problém zpravidla **aktivně řeší** — chybí jen jednoduchý, přímočarý nástroj, a tam pomáhá AI. Popis rutiny partnera nikdy nehodnoť jako selhání.

**0.7 Poctivost k nejistotě.**
Když je cílová proměnná těžko predikovatelná nebo data mají metodické limity, **napiš to**. Veď tým k práci s trendem a nejistotou, ne s jedním „zaručeným" číslem. Těžší predikce je příležitost mluvit o nejistotě — porota to ocení víc než „přesný" model bez vysvětlení.

**0.8 Self-test zadání.**
Před finalizací si sám zkus vypracovat vzorové řešení podle vlastního zadání a hledej failure modes (triviální zrcadlení, jednorázová analýza, generické výstupy z generických dat). Pokud do nich spadne tvoje vzorové řešení, spadne do nich i tým — uprav zadání.

---

### [PARAMETRY ZADÁNÍ] — vyplň před použitím

```
KÓD ZADÁNÍ:         AIO_[ZKRATKA_KRAJE]-02-[KRAJ_KÓD]
                    Příklad: AIO_JZ-02-PK (Jihozápad, Plzeňský kraj)

KRAJ:               [název kraje]
TÉMA:               [hlavní téma — musí odpovídat RIS3 smart specializaci kraje]

TYP ÚLOHY:          [vyber podle jádra problému — viz princip 0.1]
                    A) PREDIKCE/PLÁNOVÁNÍ  — historická data → model → scénáře
                    B) RECOMMENDER/MATCHING — profily → podobnost → doporučení/párování
                    C) OBRAZOVÁ KLASIFIKACE — jen když je obraz jádrem úlohy
                    (typy lze kombinovat; obraz NENÍ povinný)

ODBORNÝ PARTNER:    [regionální nebo oborový expert v porotě]

ZÁKAZNÍK (hint):    [primární zákazník — neomezující; preferuj OBECNOU instituci:
                    kraj / město / ORP / rozvojová agentura, vedle konkrétních rolí]

PROMĚNNÁ 1 (max):   [co maximalizovat — název sloupce + popis]
PROMĚNNÁ 2 (min):   [co minimalizovat — název sloupce + popis]
NAPĚTÍ MEZI NIMI:   [jak spolu soupeří — pedagogické jádro; optimum bývá uprostřed]

REÁLNÉ KOTVY:       [2–4 veřejné zdroje, ze kterých vezmeš REÁLNÁ data:
                    výroční zprávy kraje, ČSÚ, krajské analýzy, oborové portály,
                    dataportály (např. DATA ZAPAD), ČÚZK ortofoto…]

MODELOVÉ PROMĚNNÉ:  [co nikdo nezměřil a zůstane modelové — typicky outcome
                    na úrovni jednotlivce; uveď, že slouží jen k ověření]

(pokud TYP = C nebo obsahuje obraz)
4 TŘÍDY OBRAZU:     [4 vizuálně jednoznačně odlišitelné třídy — žádná závislá
                    na kontextu/orientaci/sezóně]
```

---

### FILOZOFIE A POŽADAVKY — dodržuj přesně

#### 1. Kontext zadání — první v dokumentu, otevřený, ne direktivní

Kontext umísti **hned na začátek** (před linie i data) — logika „nejdřív proč, pak jak". Popíše region a téma pomocí **4 otevřených otázek** bez jednoduchých odpovědí. Zmíní 1–2 reálné iniciativy partnera/kraje (tón dle principu 0.6 — partner problém aktivně řeší). Doporučeně přidej **rámeček „reálná data"** s doloženými čísly a zdroji a poctivou poznámkou o nejistotě (princip 0.7).

Závěr kontextu: *„Vaším úkolem je navrhnout AI produkt nebo datovou službu, která tyto otázky pomáhá řešit — pro konkrétního zákazníka, s reálnou hodnotou a promyšlenou etikou. Inspirujte se přiloženými daty, ale nebojte se jít vlastní cestou."*

#### 2. Datová sada — povinná struktura a disciplína reálné/modelové

Vždy doprovoď datový slovník označením **reálné / modelové** u každého sloupce (princip 0.4).

**Vždy (typ A i B):**
- **01_historicka_data_[tema]_[roky].csv** — min. 60 řádků (lokality × roky), vstupy + obě cílové proměnné, realistický trend a variabilita, čistá data.
- **0X_simpleml_komplet_[tema].csv** — historická data připravená pro Simple ML (min. 50+ řádků pro trénink).

**Pro recommender/matching (typ B) navíc:**
- **katalog položek** (obory, služby, lokality…) — profil na společných osách + reálné kotvy (počty, trendy). Profilové osy bývají modelové, počty/trendy reálné.
- **profily uživatelů** — vstupní vektory + (modelové) outcome pro ověření. Zabuduj **cold-start**: o malých/okrajových jednotkách méně dat → horší doporučení (to je zároveň etické téma, viz 0.5 a sekce 7).
- **reálná mapa vazeb** (např. obor × škola × okres) z veřejných dat — silná kotva pro matching/mapu mezer.

**Volitelně (typ C / když je obraz jádrem):**
- 4 třídy, ~80 train + 25 test na třídu, 64×64 px JPEG, každá třída jednoznačně odlišitelná, žádná závislá na kontextu/orientaci/sezóně.

**Záměrné chyby k čištění:** 2 soubory obsahují 3–5 typů chyb (text místo čísla, jednotky, desetinná čárka, prázdné buňky, duplicita). V zadání se to NEoznačuje jako „záměrné" — jen ⚠️ „zkontrolujte data".

**Zásady variability a učitelnosti (ověř kódem):**
- Cílová proměnná pokrývá v datech alespoň ~40 % rozsahu; proměnná 2 reaguje opačně/zpožděně (napětí).
- **Ověř, že úloha je naučitelná**: jednoduchý model/recommender musí prokazatelně **překonat náhodu/baseline** (princip 0.5, 0.8). Plochá predikce = špatný režim nebo málo variability — oprav před finalizací.

#### 3. Linie řešení — jako inspirace (princip 0.2)

Uveď je výslovně jako ukázky směrů, ne jako volbu. Každá linie: jasný přístup, žádný konkrétní nástroj v názvu, formulace „Využijte poskytnutý dataset, případně doplňte vlastní data z [zdroj]", odkaz na karty kurzívou.

**Pod linie zařaď tabulku „Co musí splňovat každé řešení" se třemi pilíři z principu 0.3** (běžící AI / návrh sběru dat / kontinuální hodnota).

#### 4. Technické úrovně + „Co je a co není AI řešení"

Tabulka No-code / Low-code / Code. Callout musí obsahovat: vibe-coding (Lovable, v0, Bolt, Replit Agent) vítán pro UI vrstvu; pod UI musí být skutečná AI komponenta; v pitchi nutno demonstrovat — jinak 0 bodů za Technické řešení. **Přidej větu, že jednorázová analýza nestačí** (princip 0.3).

#### 5. Tipy na technické řešení

4 přístupy dle typu úlohy (predikce/regrese; recommender — podobnost/vzdálenost/top-N; matching/mapa mezer; clustering; optimalizace; případně klasifikace obrazu). U recommenderu zmiň **content-based vs. collaborative** a proč na malých datech vyhrává content-based (cold-start). Závěrečný tip: *„Čím jednodušší AI, tím důležitější je ji dobře interpretovat."*

#### 5b. Rámeček „Co dělá [doporučení/predikci] dobrou" (princip 0.5)

Samostatný vizuální rámeček (obecný nárok na kvalitu, ne součást jedné linie) se 3 otázkami: překoná triviální baseline / pracuje s bohatším profilem / zohledňuje trend, ne jen aktuální stav. **Otázky, ne návody.**

#### 6. Byznys záměr — kontinuální služba (princip 0.3)

Tabulka otázek rozšířená oproti staré verzi: Zákazník (preferuj obecnou **instituci**) / Problém / Řešení (co se děje opakovaně) / **Sběr dat v čase** / **Monetizace (opakovaný příjem)** / **Návratnost pro zákazníka** (udržení a přilákání talentů/hodnoty → silnější ekonomika regionu → vyšší příjmy a nižší náklady; služba = investice, ne výdaj) / Škálovatelnost.
Příklad byznys modelu uveď **jen jako inspiraci** („služba, kterou si instituce předplácí a která monitoruje trendy a doporučuje opatření"), ne jako jediné řešení.

#### 7. AI etika — povinná, bez konzultační karty

4 otázky dle tématu: chybná predikce a odpovědnost; přístup k datům a soukromí; **spravedlnost (cold-start: méně dat o okrajových jednotkách → horší výstup → riziko sebenaplňující spirály)**; komunikace nejistoty. Etika má vyrůstat z jádra úlohy, ne být přílepek. Callout: *„Absence etiky = 0 bodů v kategorii AI etika."*

#### 8.–11. Karty / Odevzdání / Pitch / Kritéria

4 karty (2 technické + 2 byznys), bez časového omezení. Průběžné odevzdání na platform.aiolympiada.cz. Pitch deck max. 8 slidů (tabulka checklist) — slide o AI modelu žádá i **jak měříte kvalitu (že výstup překonává baseline)**. Živá prezentace 3 + 2 min (video nepovinné). Technické shrnutí 1 A4. Kritéria vždy 40 / 40 / 20, třetí sloupec upřesnit pro téma a partnera.

#### 12. Inspirační zdroje

4–6 odkazů včetně reálných kotev z principu 0.4 (odborný partner, krajská analýza/výroční zpráva, ČSÚ, dataportál, oborový portál, ČÚZK ortofoto…).

---

### FORMÁTOVÁNÍ

- Výstup pro studenty: profesionální DOCX (branding navy/cyan), případně Markdown.
- Zápatí: `[KÓD ZADÁNÍ] | Česká AI Olympiáda 2026 | nvias, z.s. | info@nvias.org | CC BY-NC-SA 4.0`
- Disclaimer dle disciplíny reálné/modelové: `Reálné jsou [co]. Modelové jsou [co] a slouží jen k ověření v rámci soutěže.`
- Záhlaví: `Česká AI Olympiáda 2026 | AI Startup | [KÓD] | [kraj]`
- Kód zadání zachovej beze změny ve všech verzích dokumentu (footery i headery).

---

### ČEHO SE VYVAROVAT

❌ Šroubovat klasifikaci obrazu (nebo jakoukoli techniku) jen kvůli „třem liniím" — technika podle problému (0.1)
❌ Prezentovat linie jako menu k výběru — jsou to inspirace (0.2)
❌ Výstup = jednorázová analýza + návrh jednoho řešení — chybí běžící algoritmus, sběr dat a kontinuální hodnota (0.3)
❌ Vydávat modelové hodnoty za reálná data; předstírat outcome, který nikdo neměří (0.4)
❌ Doporučení/predikce, která jen zrcadlí vstup („mám rád X → X") (0.5)
❌ Psát „nikdo to neumí / spoléhá se na náhodu" o partnerovi či regionu (0.6)
❌ Tvrdit jedno „zaručené" číslo tam, kde jsou data nejistá nebo metodicky omezená (0.7)
❌ Finalizovat bez self-testu vzorovým řešením (0.8)
❌ Třída obrazu závislá na kontextu/orientaci/sezóně (pokud obraz vůbec použit)
❌ Jen jedna cílová proměnná — vždy dvě v napětí
❌ Video jako povinný výstup; časový limit na karty; věta o postupu do finále

---

### KONTROLNÍ SEZNAM PŘED ODEVZDÁNÍM ZADÁNÍ

- [ ] Technika sedí na jádro problému (ne šroubovaná kvůli liniím) — 0.1
- [ ] Linie podány jako inspirace, ne menu — 0.2
- [ ] Tabulka tří pilířů (běžící AI / sběr dat / kontinuální hodnota) je v zadání — 0.3
- [ ] Datový slovník značí u každého sloupce reálné/modelové; outcome je modelový — 0.4
- [ ] Rámeček „co dělá výstup dobrým" (překonej baseline, profil, trend) — 0.5
- [ ] Kontext zjemněn vůči partnerovi (problém se aktivně řeší, chybí nástroj) — 0.6
- [ ] Poctivá poznámka o nejistotě/limitech dat — 0.7
- [ ] Self-test: vzorové řešení nepadá do triviálního zrcadlení/jednorázovky — 0.8
- [ ] Kontext je první sekcí dokumentu
- [ ] Úloha je prokazatelně naučitelná (baseline překonán), data mají napětí a variabilitu
- [ ] Cold-start zabudován a propojen s etikou spravedlnosti
- [ ] Byznys je kontinuální (opakovaný příjem, sběr dat v čase, návratnost, obecná instituce)
- [ ] 2 soubory mají záměrné chyby (v textu jen ⚠️, ne „záměrné")
- [ ] Kód zadání správný formát; zápatí CC BY-NC-SA 4.0; kritéria 40/40/20

## PROMPT (konec)

---

## Příklady vyplněných parametrů

### Příklad — Karlovarský kraj: AI pro propojení studentů, škol a firem (recommender)
```
KÓD ZADÁNÍ:        AIO_SZ-02-KV
TÉMA:              Prevence odlivu talentů — propojení žák ↔ obor ↔ firma v kraji
TYP ÚLOHY:         B) RECOMMENDER/MATCHING (+ A predikce pro obce)
ODBORNÝ PARTNER:   Karlovarská agentura rozvoje podnikání (KARP)
ZÁKAZNÍK:          instituce (kraj/město/ORP/agentura), kariérní poradce, ředitel SŠ, HR firmy
PROMĚNNÁ 1 (max):  uplatnitelnost_v_kraji_procent (modelová)
PROMĚNNÁ 2 (min):  riziko_odlivu / odliv_talentu (modelová)
NAPĚTÍ:            úzká specializace ↑ krátkodobá uplatnitelnost, ale ↑ odliv při změně trhu;
                   obecné vzdělání ↑ rozhled, ale ↑ odchod na VŠ; optimum uprostřed, jiné dle obce
REÁLNÉ KOTVY:      Výroční zpráva o školství KK (obory, absolventi, nábor 2012–2024),
                   ČSÚ zaměstnanost CZ-NACE (trend odvětví), KARP/RSK analýza 2017, DATA ZAPAD
MODELOVÉ PROMĚNNÉ: profil zájmů žáka, poptávka po oboru (informovaná trendem),
                   uplatnitelnost, riziko odlivu, outcome žáka (zůstal/pracuje v oboru)
```

### Příklad — Plzeňský kraj: Průmysl 4.0 / prediktivní údržba (predikce)
```
KÓD ZADÁNÍ:        AIO_JZ-02-PK
TYP ÚLOHY:         A) PREDIKCE/PLÁNOVÁNÍ
PROMĚNNÁ 1 (max):  dostupnost_stroje_procent
PROMĚNNÁ 2 (min):  riziko_havarie_0_100
NAPĚTÍ:            agresivní provoz → dostupnost ↑ krátkodobě, riziko ↑; preventivní servis → opačně
REÁLNÉ KOTVY:      [krajské/oborové statistiky výroby, registr firem, ČSÚ CZ-NACE]
```

### Příklad — Jihočeský kraj: Chytré zemědělství a sucho (predikce + volitelně obraz)
```
KÓD ZADÁNÍ:        AIO_JC-02-JC
TYP ÚLOHY:         A) PREDIKCE (+ volitelně C obraz, jen pokud je ortofoto jádrem)
PROMĚNNÁ 1 (max):  vynos_t_ha
PROMĚNNÁ 2 (min):  stres_index_0_100
NAPĚTÍ:            intenzivní hnojení → výnos ↑, stres při suchu ↑; zavlažování → obojí ↓, náklady ↑
REÁLNÉ KOTVY:      ČHMÚ, ČSÚ, EAGRI, Sentinel-2 Copernicus
```

---

*Verze 2 — zobecněno o kritický pohled z tvorby AIO_SZ-02-KV (recommender, kontinuální byznys, reálná vs. modelová data, kvalita nad triviální baseline). Aktualizovat při změnách filozofie soutěže nebo platformy.*
*Interní materiál nvias, z.s. — projekt Česká AI Olympiáda 2026.*
