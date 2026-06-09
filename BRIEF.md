# BRIEF — AIO_PHA-02-PHA (Česká AI Olympiáda 2026, AI Startup, krajské Praha)

> **AKTUALIZOVÁNO 2026-06-09 dle nového zadání.** Téma se rozšířilo z „kam dát dobíječky"
> na **udržitelnou mobilitu A energetiku**. Zdroj pravdy = `zadani/zadani_AIO_PHA-02-PHA_UPDATED.md`
> (starší `zadani_AIO_PHA-02-PHA.md` je neaktuální). Meta-prompty v `zadani/` = co porota odměňuje.

## Úkol jednou větou
Navrhni **běžící AI produkt / datovou službu**, která řeší **některou** otázku na průniku
**mobility a energetiky** v Praze — pro konkrétního zákazníka, s reálnou hodnotou a etikou.
Data jsou **sandbox (odrazový můstek), ne zadání samo.** Jedna čistá běžící linie stačí.

- **Téma:** Udržitelná mobilita a energetika (RIS3 Chytré město). Partner: **Magistrát HMP**.
  Ekosystém: Operátor ICT / **Golemio**, Smart Prague, **PRE**, IPR Praha.
- **Typ úlohy:** predikce · doporučování (matching) · optimalizace — dle zvolené cesty.
- **Zákazník:** Hl. m. Praha / MČ / Operátor ICT / **distributor** / **energetická komunita**
  (Pražské společenství pro OZE).

## ⚡ Naše cesta: Linie A povýšená na V2G — `CONCEPT-VoltPlan.md`
Zadání říká: *„Auto u nabíječky není jen spotřebič — podle doby stání může vrátit energii
do sítě nebo čtvrti (V2G). To je **nejhlubší příležitost** tohoto zadání."* a *„nejsilnější
řešení obvykle propojí mobilitu a energetiku."*
→ VoltPlán = predikce poptávky + **řízené nabíjení (KDY/JAK) + V2G (auto jako zdroj pro síť/čtvrť)**
+ chytré umístění. Propojuje mobilitu (kde/kdy stojí auta) s energetikou (rezerva sítě, flexibilita).
Zákazník = **energetická komunita / distributor** (sdílení výnosu z flexibility) vedle města.

## Čtyři linie (NEjsou menu — inspirace; lze kombinovat / jít vlastní cestou)
- **A — Nabíjení a síť (auto jako spotřebič i ZDROJ):** predikce poptávky + kapacity v čase →
  KDY a JAK nabíjet (řízené nabíjení) + **V2G**. Bohatý dataset (rezerva, hodinová zátěž, overload).
- **B — Místo v centru:** predikce obsazenosti + navádění na volné parkovací/nabíjecí místo →
  míň kroužení → míň zácp/emisí/zátěže sítě. Mapa mezer. (Golemio parking/Waze data.)
- **C — Přesun od auta (multimodalita):** recommender kombinace auto×P+R×MHD×kolo×sdílená +
  predikce poptávky po MHD (cíl +150 mil. cestujících 2030). (Golemio PID/GTFS.)
- **D — Obraz z kamer:** z dopravních kamer odhad obsazenosti parkování / hustoty provozu,
  náhrada chybějících senzorů. Klasifikace/detekce obrazu. (ŘSD/městské kamery.)

## Tři pilíře, které MUSÍ splnit každé řešení
1. **Běžící AI algoritmus** — model trvale pracuje (predikce / recommender / **optimalizace**), NE jednorázový výpočet.
2. **Sběr a údržba dat v čase** — jak služba žije zítra. Stačí promyslet + obhájit v pitchi.
3. **Kontinuální hodnota** — běží opakovaně → monetizace předplatné/služba (u V2G i sdílení výnosu z flexibility).

## ⚑ Co porota REÁLNĚ hodnotí (failure modes — vyhnout se = výhra)
- **Jedna čistá běžící linie stačí** — radši hloubka než tři rozbité linie.
- **„Opravdová AI, ne triviální pravidlo/tabulka."** „Hodně aut → velký hub" zvládne tabulka.
  Ukaž **méně očekávané, ale sedící** řešení (serendipity) a vysvětli, KDY model platí a kdy ne.
- **Propojení mobility a energetiky = nejsilnější** (V2G, řízené nabíjení, poslat člověka MHD).
- **Vlastní úhel + zahraniční trend lokalizovaný na Prahu** boduje ve 20% kategorii. Najdi 1 trend
  ze světa (V2G, dynamické tarify, navádění na parkování, „město krátkých vzdáleností") a obhaj Prahu.
- **Cold-start = body 2×** (technika + etika): málo dat o okrajových čtvrtích → spirála.
- **Sandbox, ne soutěž o skóre.** Data slouží ke stavbě/validaci/interpretaci. **Validuj si sám**
  (odlož část stranou — holdout). Žádné odevzdání predikcí na skryté labely.
- **Reálné vs. modelové:** `_real`/`_derived`/`_synthetic`. Cíle `target_*_2030_synthetic` jsou
  modelové, ne měření PRE → nikdy jako featura (leakage). Kontrola dat je součást úlohy.
- **Živá ukázka běžícího modelu povinná** — UI obal bez běžící AI = **0 bodů** za techniku.
- **Nejistota:** predikce 2030 → pásmo scénářů, ne jedno „zaručené" číslo.

## Hodnoticí kritéria (40 / 40 / 20)
- **Technické (40):** běžící AI (predikce/recommender/**optimalizace**); kvalita dat + čištění;
  **že je to opravdová AI, ne triviální pravidlo**; interpretace; cold-start.
- **Byznys (40):** jasný zákazník (instituce); opakovaný příjem; sběr dat v čase; návratnost; škálování.
- **Prezentace + etika + relevance (20):** srozumitelný pitch + ukázka; 4 etické oblasti;
  **chytré propojení mobility a energetiky; zahraniční inspirace lokalizovaná na Prahu**; nejistota.

## 4 etické oblasti (absence = 0 bodů v etice)
1. Chybná predikce a odpovědnost. 2. Soukromí (data o pohybu/parkování/nabíjení).
3. **Spravedlnost / cold-start** (spirála chudších čtvrtí). 4. Komunikace nejistoty.

## Odevzdání + Pitch (doporučeně)
Platforma `platform.aiolympiada.cz`: odkaz na běžící řešení/kód, datové výstupy, pitch deck, 1 A4.
**Deck ~8 slidů**, **3 min + 2 min Q&A**. Checklist (nově): 1) Problém+zákazník 2) Data (reálné vs.
modelové + čištění) 3) AI model **+ proč je to opravdu AI a jak poznáš že funguje** 4) Výsledky+demo
5) Byznys (opak. příjem, sběr dat, škálování) 6) **Váš úhel + zahraniční inspirace na Prahu**
7) Etika (cold-start) 8) Tým.

---
`AIO_PHA-02-PHA | Česká AI Olympiáda 2026 | nvias, z.s. | CC BY-NC-SA 4.0` — data modelová, sandbox.
