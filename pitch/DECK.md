# VoltPlán — pitch deck (~8 slidů) · AIO_PHA-02-PHA

> Aktualizováno 2026-06-09 dle nového zadání (mobilita+energetika, V2G, sandbox).
> `[DOPLNIT]` = čísla od tracku 🅐/🅑. 3 min mluvení + 2 min Q&A. Slide 3 nejdůležitější.
> Stavěj v Gammě (vlož tenhle markdown → samo nadesignuje). Drž navy/cyan.

---
## Slide 1 — Problém a zákazník
**Headline:** Praha propojuje dopravu a energetiku. Kde a KDY nabíjet, aby auta síti pomáhala, ne ji přetížila?
- Zákazník: **Hl. m. Praha / MČ / Operátor ICT / distributor (PRE) / energetická komunita** (Pražské společenství pro OZE).
- Co je pálí: večerní špička jde na hranu sítě; dobíječky „od oka" zůstávají prázdné; pomalý přechod na EV.
- Kotva: 59 000 EV (2026), Klimatický plán → 10 000 stanic do 2030, ~180 000 EV / ≥4 500 stanic (Generel).

## Slide 2 — Data (reálné vs. modelové)
- Bohatý sandbox dataset (zóny TS): `_real` (ČSÚ, RÚIAN, PRE, IPR) / `_derived` / `_synthetic` (cíle 2030).
- Klíč pro nás: `grid_capacity_and_reserve_2025` + `hourly_*` (zátěž, **rezerva, overload_flag** po hodinách).
- **Čištění + kontrola leakage** → ukázat **1 zachycený leakage případ** (cíle `_synthetic` nesmí do featur).
- Poctivost: data jsou modelová (sandbox), validujeme vlastním holdoutem, ne soutěží o skóre.

## Slide 3 — AI model: proč je to OPRAVDU AI a jak víme, že funguje ⭐
**Spusť:** `python src/train_demand.py` → čísla z consolu.
- **Predikce poptávky/zátěže = LightGBM** (vlastní model), featury = poměry (byty bez stání/celkem, hustota…).
- **Doložené překonání triviálního pravidla** (na validaci): MAE LightGBM **[DOPLNIT z consolu]** vs „∝ populace" **[DOPLNIT z consolu]**
  → o **[DOPLNIT] %** lépe; **Precision@50 = [DOPLNIT z consolu]**. Ne tabulka — model najde i méně očekávané zóny.
- Vysvětlíme **kdy model platí a kdy ne** (nejistota → pásmo scénářů).

## Slide 4 — Výsledky a živá ukázka (Dynamic pricing + V2G)
**Spusť:** `streamlit run src/app.py` + screenshot. Pak `python src/v2g.py` → čísla.
- **[ŽIVÉ DEMO / záloha screenshot]** — mapa Prahy obarvená predikovanou poptávkou.
- **Jak se to řídí (KLÍČ — ne direktivně!):**
  - Nízká reserve v síti (špička) → elektřina 15 Kč/kWh (drahá)
  - Vysoká reserve (mild) → elektřina 3 Kč/kWh (levná)
  - Řidič se SÁM rozhodne: "Za 3 Kč? Nabiju v noci!" (ekonomicky, ne povinně)
- **V2G kompenzace:** V špičce auto vrátí 240 kWh → dostane 400 Kč (profit, ne povinnost)
- **Výsledek:** Přetížení **[DOPLNIT] %** zabráněno / **[DOPLNIT] kWh** vráceno. Auto = zdroj, řidič = investor.

## Slide 5 — Byznys model (kontinuální služba)
- Zákazník instituce; **opakovaný příjem**: předplatné MČ/města + **sdílení výnosu z flexibility (V2G)** s energ. komunitou/distributorem.
- **Sběr dat v čase:** nové stanice, registrace EV, obsazenost z pilotu PRE/Golemio, kapacita sítě → retrain (n8n smyčka, popsaná).
- Návratnost: 1 zabráněné posílení trafa / 1 mrtvá dobíječka ročně → zaplatí se. **Služba = investice.** Škálování: Brno/Plzeň/Ostrava, energetické komunity.

## Slide 6 — Náš úhel + zahraniční inspirace lokalizovaná na Prahu
- **Trend ze světa:** **Utrecht „We Drive Solar" (2023): 60 % vozidel v pilotu schopno V2G; 5 MW flexibility/rok; energetická komunita = investor.**
- Proč sedí na Prahu: Pražské společenství pro OZE + pilot PRE (Smart Prague) + cíl 23 000 budov s OZE → V2G umožňuje komunitám být producentem, ne jen spotřebitelem.
- Čím se lišíme od nejzřejmějšího řešení: ostatní dělají „kam dát hub", my řešíme **KDY/JAK nabíjet a vrátit energii** = propojení mobility + energetiky.

## Slide 7 — Etika (4 oblasti, zabudované)
1. Chybná predikce → confidence + člověk v kličce + back-testing.
2. Soukromí → jen agregáty na úrovni zóny (práh domácností), žádná individuální data.
3. **Spravedlnost / cold-start (těžiště):** equity váha + nafouknutá nejistota pro řídké zóny → lámeme spirálu chudších čtvrtí.
4. Nejistota → pásma + scénáře, robustní rozhodnutí.

## Slide 8 — Tým a shrnutí
- Tým: **[DOPLNIT jména/role]**. Proč my: **[DOPLNIT]**.
- One-liner: *„VoltPlán: předpověz → řiď nabíjení → vrať energii (V2G). Auto jako zdroj pro síť i čtvrť."*

---
**K odevzdání:** deck (PDF) · technické shrnutí 1 A4 · datové výstupy (predikce) · odkaz na kód/demo.
**Q&A připrav:** proč je to AI ne pravidlo · jak řešíš leakage/cold-start · kdo platí · jak funguje V2G smyčka.
