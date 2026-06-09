# Meta-prompt: Generování zadání Česká AI Olympiáda 2026
## Šablona pro tvorbu nových zadání ve stejné filozofii jako AIO_SZ-01-UK a AIO_SZ-02-UK

---

## Jak tento prompt použít

Zkopíruj celý blok níže do svého nástroje (ChatGPT, Claude, Gemini, Copilot…) a vyplň proměnné v sekci `[PARAMETRY ZADÁNÍ]`. Zbytek promptu popisuje filozofii, strukturu a konkrétní požadavky, které musí každé zadání splňovat.

---

---

## PROMPT (začátek — kopíruj od zde)

Jsi expert na tvorbu vzdělávacích soutěžních zadání pro středoškoláky v oblasti umělé inteligence. Připravíš kompletní zadání pro krajské kolo soutěže Česká AI Olympiáda 2026, linie AI Startup, podle následujících parametrů a filozofie.

---

### [PARAMETRY ZADÁNÍ] — vyplň před použitím

```
KÓD ZADÁNÍ:         AIO_[ZKRATKA_KRAJE]-02-[KRAJ_KÓD]
                    Příklad: AIO_JZ-02-PK (Jihozápad, Plzeňský kraj)

KRAJ:               [název kraje]
TÉMA:               [hlavní téma — musí odpovídat RIS3 smart specializaci kraje]
                    Příklady: chytrá mobilita, průmysl 4.0, digitální zemědělství,
                    cestovní ruch a kultura, zdravotnictví a péče o seniory,
                    vodní hospodářství, biotechnologie, lesnictví a dřevozpracování

ODBORNÝ PARTNER:    [název organizace v porotě — regionální nebo oborový expert]

ZÁKAZNÍK (hint):    [kdo by mohl být primárním zákazníkem produktu — neomezující]
                    Příklad: zemědělský poradce, správce parku, nemocniční manažer

PROMĚNNÁ 1 (max):   [co chceme maximalizovat — název sloupce + popis]
                    Příklad: vynos_kg_ha — výnos plodiny na hektar

PROMĚNNÁ 2 (min):   [co chceme minimalizovat — název sloupce + popis]
                    Příklad: riziko_sucha_0_100 — riziko výpadku úrody suchem

NAPĚTÍ MEZI NIMI:   [jak spolu proměnné soupeří — pedagogické jádro]
                    Příklad: Intenzivní hnojení → výnos ↑, ale riziko sucha ↑
                             Zavlažování → obojí klesá, ale náklady rostou

4 TŘÍDY OBRAZU:     [4 vizuálně rozlišitelné třídy pro klasifikaci z ortofota nebo jiného
                    obrazového zdroje — každá musí být jasně odlišná]
                    Příklad pro zemědělství:
                    0: zdrava_plodina — sytě zelená, hustá textura
                    1: stres_sucho — hnědnoucí okraje, světlá textura
                    2: zaburenena_plocha — různobarevná, nerovnoměrná
                    3: sklizena_puda — holá hnědá plocha po sklizni

KATALOG OPATŘENÍ:   [3 kategorie × 5 opatření = 15 celkem]
                    Kategorie musí odpovídat tématu. Každé opatření má:
                    - cena (Kč nebo mil. Kč)
                    - doba implementace (roky)
                    - dopad na proměnnou 1 (delta)
                    - dopad na proměnnou 2 (delta)
                    Jedno opatření musí být "velká vize" — vysoká cena, dlouhá implementace,
                    největší dopad (analogie vodíku v energetice).

REÁLNÉ PROJEKTY:    [2–3 reálné projekty nebo iniciativy v kraji relevantní k tématu]
                    Tyto projekty budou zmíněny v kontextu zadání pro autenticitu.

ZDROJE DAT:         [2–4 veřejné datové zdroje relevantní k tématu]
                    Příklady: ČHMÚ, ČSÚ, ČÚZK ortofoto, data.gov.cz, EAGRI,
                    Sentinel-2 Copernicus, PVGIS, ERÚ, ŘSD, SŽDC...
```

---

### FILOZOFIE A POŽADAVKY — dodržuj přesně

#### 1. Kontext zadání — otevřený, ne direktivní

Kontext popíše region a téma pomocí **4 otevřených otázek**, na které neexistují jednoduché odpovědi. Kontext NESMÍ říkat "vaším úkolem je vyřešit X" — studenti si produkt navrhují sami. Zmínit alespoň 1–2 reálné projekty nebo iniciativy z kraje pro autenticitu.

Závěr kontextu: *"Vaším úkolem je navrhnout AI produkt nebo datovou službu, která tyto otázky pomáhá řešit — pro konkrétního zákazníka, s reálnou hodnotou a promyšlenou etikou. Inspirujte se přiloženými daty, ale nebojte se jít vlastní cestou."*

#### 2. Datová sada — povinná struktura

Vygeneruj nebo popiš 4 soubory:

**01_historicka_data_[tema]_[roky].csv**
- Min. 60 řádků (6 lokalit × 10+ let nebo 10 lokalit × 6+ let)
- Sloupce: rok, lokalita/obec, vstupy (3–5 sloupců), výstupy (proměnná 1 a 2 + 1–2 vedlejší)
- Data musí mít realistický trend a variabilitu napříč lokalitami
- Čistá data bez chyb

**02_katalog_opatreni_[tema].csv**
- 15 opatření ve 3 kategoriích (5+5+5)
- Záměrně obsahuje 3–5 typů chyb: text místo čísla, chybné jednotky, prázdné buňky, nekonzistentní formát
- Studenti musí data vyčistit — to je pedagogický záměr, ale v zadání se to NEZMIŇUJE jako "záměrné" — jen upozornění ⚠️

**03_scenare_projekce_[roky].csv**
- 7 scénářů × 6 lokalit × 10 let = 420 řádků
- Vstupy vyplněné s náběhovou křivkou (lineární náběh přes dobu implementace opatření)
- Výstupní sloupce (proměnná 1 a 2) PRÁZDNÉ — studenti je predikují pomocí Simple ML
- Záměrně obsahuje ~5 % chybných řádků

**04_simpleml_komplet_[tema].csv**
- Historická data (výstupy vyplněné) + scénáře (výstupy prázdné)
- Připraveno přímo pro Simple ML for Sheets: "Predict missing values"
- Min. 60 vyplněných řádků pro trénink (varování Simple ML je 50+)

**Zásady datové variability:**
- Hodnota proměnné 1 musí v různých scénářích a lokalitách pokrývat alespoň 40% rozsah svého maxima
- Hodnota proměnné 2 musí reagovat opačně nebo s zpožděním na změny proměnné 1
- Scénář "velká vize" musí mít náběh ≥ 6 let a nejvyšší hodnoty obou proměnných po implementaci

**Obrazový dataset:**
- 4 třídy, 80 trénovacích + 25 testovacích snímků každá = 420 celkem
- 64×64 px, JPEG
- Každá třída musí být vizuálně jednoznačně odlišitelná (barva, textura, tvar)
- NESMÍ obsahovat třídy, jejichž vhodnost závisí na kontextu (orientace, sezóna) — každá třída musí mít jednoznačnou relevanci
- Třída 1 (inventura/stav) — co již existuje
- Třída 0 (vhodné) — priorita pro intervenci
- Třída 2 (nevhodné) — jednoznačně problematické, ne jen "záleží na podmínkách"
- Třída 3 (velký potenciál) — přehlížená příležitost, vizuálně výrazná

#### 3. Tři linie řešení

Každá linie musí:
- Mít jasný přístup (tabulková / obrazová / kombinovaná data)
- NEJMENOVAT konkrétní nástroj přímo v názvu linie — nástroje jdou do poznámky
- Mít formulaci "Využijte poskytnutý dataset, případně doplňte vlastní data z [zdroj]"
- Končit kurzívou: "*Doporučené nástroje najdete v konzultačních kartách [T1/T2/B1].*"

**Linie 1 — Tabulková data:** prediktivní model na historických datech, porovnání scénářů, plánovací nástroj
**Linie 2 — Kombinovaný přístup:** klasifikace obrazu → odvození vstupní proměnné → predikce výstupu
**Linie 3 — Obrazová data:** klasifikátor 4 tříd, test přesnosti, inventurní produkt

#### 4. Technické úrovně

Tabulka: No-code / Low-code / Code s příklady nástrojů.

Callout "Co je a co není AI řešení" musí obsahovat:
- Vibe-coding (Lovable, v0, Bolt, Replit Agent) je výslovně vítán pro UI vrstvu
- Pod UI musí být skutečná AI komponenta (klasifikátor, prediktivní model, LLM API, Colab kód)
- V pitchi musí tým AI komponentu demonstrovat — jinak 0 bodů za Technické řešení

#### 5. Tipy na technické řešení

4 konkrétní přístupy přizpůsobené tématu:
- Predikce / regrese (na datech tohoto tématu)
- Klasifikace obrazu (4 třídy tohoto tématu)
- Segmentace / clustering (relevantní pro toto téma)
- Optimalizace (mixu opatření / zdrojů / parametrů)

Závěrečný tip: *"Čím jednodušší AI, tím důležitější je ji dobře interpretovat."*

#### 6. Byznys záměr

Standardní tabulka 5 otázek (Zákazník / Problém / Řešení / Cena / Škálovatelnost). Neměnit.

#### 7. AI etika — povinná, bez konzultační karty

4 otázky přizpůsobené tématu — musí pokrývat:
- Chybnou predikci a odpovědnost
- Přístup k datům a soukromí
- Spravedlnost (kdo má a kdo nemá přístup k benefitům)
- Komunikaci nejistoty zákazníkovi

Závěrečný callout: *"Absence etiky = 0 bodů v kategorii AI etika."*

#### 8. Konzultační karty

4 karty celkem — 2× technická + 2× byznys. Bez časového omezení kdy je musí použít.

#### 9. Průběžné odevzdání

Standardní sekce — neměnit. Odkaz na platform.aiolympiada.cz.

#### 10. Co odevzdáváte

- Pitch deck: max. 8 slidů, tabulka s checklistem (Slide | Obsah | Co porota sleduje)
- Živá prezentace: 3 min pitch + 2 min dotazy — NE video jako povinný výstup
- Technické shrnutí: 1 A4

#### 11. Hodnotící kritéria

Vždy: Technické řešení 40 % / Byznys & pitch 40 % / AI etika 20 %. Třetí sloupec upřesnit pro toto téma a partnera v porotě.

#### 12. Inspirační zdroje

4–6 odkazů: odborný partner, PVGIS nebo jiný datový nástroj, ERÚ nebo jiný registr, národní platforma (ECUK, ČHMÚ, ŘSD…), ČÚZK Geoprohlížeč (ortofoto), případně tematická asociace.

---

### FORMÁTOVÁNÍ

- Výstup v Markdown
- Zápatí každého dokumentu: `[KÓD ZADÁNÍ] | Česká AI Olympiáda 2026 | nvias, z.s. | info@nvias.org | CC BY-NC-SA 4.0`
- Disclaimer na konci: `Data jsou modelová. [název reálných projektů] jsou reálné — viz inspirační zdroje.`
- Kód zadání v záhlaví: `## Krajské kolo | [kraj] | [KÓD]`

---

### ČEHO SE VYVAROVAT

❌ Nezmiňuj ECUK ani energetiku — to je specifické pro AIO_SZ-02-UK
❌ Nepiš "ECUK řeší každý den ručně" ani podobné popisy rutiny partnera
❌ Nepiš "záměrné chyby" v datech — jen ⚠️ zkontrolujte data
❌ Nezdůrazňuj konkrétní nástroj v názvu linie (Simple ML, Teachable Machine)
❌ Nezahrn sedlové střechy bez orientace do třídy "nevhodné" — nebo jakoukoli třídu, jejíž klasifikace závisí na kontextu (orientace, sezóna, stáří)
❌ Nepiš "video jako povinný výstup" — tým prezentuje živě
❌ Nepiš časový limit pro konzultační karty (60 min před koncem apod.)
❌ Nevkládej větu o postupu týmů do finále (to závisí na aktuálním harmonogramu)
❌ Neuváděj jen jednu cílovou proměnnou — vždy musí být dvě v napětí

---

### KONTROLNÍ SEZNAM PŘED ODEVZDÁNÍM ZADÁNÍ

Před finalizací ověř, že zadání splňuje:

- [ ] Kód zadání ve správném formátu (AIO_XX-02-XX)
- [ ] Glossář obsahuje všechny zkratky použité v textu
- [ ] Kontext má 4 otevřené otázky, ne direktivy
- [ ] Dataset 04 má min. 60 vyplněných řádků pro trénink Simple ML
- [ ] Obě cílové proměnné jsou jasně definovány a jejich napětí vysvětleno v Tipu
- [ ] Třída 2 (nevhodné) je jednoznačně nevhodná bez závislosti na orientaci/kontextu
- [ ] Každá linie říká "Využijte poskytnutý dataset, případně vlastní data z [zdroj]"
- [ ] Callout o AI komponentě obsahuje vibe-coding guidance
- [ ] Etika má 4 otázky přizpůsobené tématu
- [ ] Pitch checklist je tabulka 8 slidů
- [ ] Odevzdání je "Živá prezentace", ne "Video"
- [ ] Hodnotící kritéria jsou 40/40/20
- [ ] Zápatí obsahuje kód zadání a CC BY-NC-SA 4.0

## PROMPT (konec)

---

## Příklady vyplněných parametrů pro různá témata

### Příklad A — Plzeňský kraj: Průmysl 4.0 a prediktivní maintenance

```
KÓD ZADÁNÍ:         AIO_JZ-02-PK
KRAJ:               Plzeňský kraj
TÉMA:               Prediktivní údržba průmyslových strojů (Industry 4.0)
ODBORNÝ PARTNER:    Škoda Auto DigiLab nebo DTSP (Digitální technologická a servisní platforma)
PROMĚNNÁ 1 (max):   dostupnost_stroje_procent — % času, kdy stroj funguje bez výpadku
PROMĚNNÁ 2 (min):   riziko_havarie_0_100 — riziko neplánovaného výpadku
NAPĚTÍ:             Agresivní provoz → dostupnost ↑ krátkodobě, riziko ↑. Preventivní servis → dostupnost ↓ krátkodobě, riziko ↓↓.
4 TŘÍDY OBRAZU:     vibrace_normalni / predhavarie / po_oprave / vadny_dil (z termokamer nebo foto součástek)
```

### Příklad B — Jihočeský kraj: Chytré zemědělství a sucho

```
KÓD ZADÁNÍ:         AIO_JC-02-JC
KRAJ:               Jihočeský kraj
TÉMA:               Predikce sucha a optimalizace zavlažování
ODBORNÝ PARTNER:    Jihočeská univerzita v Českých Budějovicích, zemědělský výzkum
PROMĚNNÁ 1 (max):   vynos_t_ha — výnos plodiny v tunách na hektar
PROMĚNNÁ 2 (min):   stres_index_0_100 — vodní stres plodiny (z NDVI nebo modelů)
NAPĚTÍ:             Intenzivní hnojení → výnos ↑, stres při suchu ↑. Zavlažování → obojí zlepší, ale náklady ↑.
4 TŘÍDY OBRAZU:     zdrava_plodina / vodni_stres / zaburenena / sklizena_puda (Sentinel-2 nebo ortofoto)
```

### Příklad C — Karlovarský kraj: Cestovní ruch a přírodní dědictví

```
KÓD ZADÁNÍ:         AIO_SZ-02-KK
KRAJ:               Karlovarský kraj
TÉMA:               AI pro udržitelný cestovní ruch a monitoring stavu lázní
ODBORNÝ PARTNER:    Destinační agentura Karlovarského kraje nebo Karlovarská krajská nemocnice
PROMĚNNÁ 1 (max):   spokojenost_navstevniku_0_100 — hodnocení zážitku
PROMĚNNÁ 2 (min):   zatizeni_lokality_0_100 — přetížení infrastruktury, dopad na přírodu
NAPĚTÍ:             Marketingová kampaň → spokojenost ↑, zatížení ↑↑. Kapacitní opatření → zatížení ↓, náklady ↑.
4 TŘÍDY OBRAZU:     udrzovana_plocha / preoplnena_zona / zarostla_stezka / historicky_objekt (z drone nebo ortofoto)
```

---

*Tento meta-prompt byl vytvořen pro interní potřeby nvias, z.s. v rámci projektu Česká AI Olympiáda 2026.*
*Aktualizovat při změnách filozofie soutěže nebo platformy.*
