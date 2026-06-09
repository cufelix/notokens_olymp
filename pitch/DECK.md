# VoltPlán — pitch deck (8 slidů) · AIO_PHA-02-PHA

> Text předepsaný z `CONCEPT-VoltPlan.md`. `[DOPLNIT]` = čísla od tracku 🅐/🅑 na místě.
> 3 min mluvení + 2 min Q&A. Slide 3 je nejdůležitější (číslo vs baseline).
> Stavěj v čem jsi rychlý: Slides / Canva / Gamma / Marp z tohohle .md. Drž navy/cyan.

---
## Slide 1 — Problém a zákazník
**Headline:** Praha chce 10 000 dobíječek do 2030. Kam je dát, aby nezůstaly prázdné a nepřetížily síť?
- Zákazník: **Hl. m. Praha / městská část / Operátor ICT** (+ role: plánovač mobility, energetik PRE).
- Co je pálí: dobíječky „od oka" → prázdné (mrtvá investice) NEBO přehlédnutá čtvrť; večerní špička hrozí přetížením trafa.
- Kotva: 59 000 EV (2026), +19 % síť za 2025, Generel: ~180 000 EV / ≥4 500 stanic do 2030.

## Slide 2 — Data (reálné vs. modelové)
- 9 core CSV (~251 MB) + 1,6 GB optional; jednotka = **zóna** (oblast trafostanice).
- Původ značíme: `_real` (ČSÚ, RÚIAN, PRE, IPR, ČHMÚ…) / `_derived` / `_synthetic` (cíle 2030).
- **Trust Layer:** čištění, dedup, **kontrola leakage** → ukázat **1 zachycený leakage případ**.
- Confidence známka A/B/C per zóna (úplnost dat) — propojeno s cold-startem.

## Slide 3 — AI model + JAK MĚŘÍME KVALITU ⭐ (nejdůležitější)
- **Demand Engine = LightGBM** (vlastní natrénovaný model), featury = poměry (byty bez stání/celkem, hustota…), ne absolutní čísla.
- **Doložené překonání baseline na zones_validation.csv:**
  - MAE LightGBM **[DOPLNIT]** vs populační baseline **[DOPLNIT]** → o **[DOPLNIT] %** lépe.
  - **Precision@50 = [DOPLNIT]** (trefíme nejpoptávanější zóny do top 50).
- Nejistota: scénáře konzervativní/střední/ambiciózní (ne jedno „zaručené" číslo).

## Slide 4 — Výsledky a živá ukázka
- **[ŽIVÉ DEMO / záloha screenshot]** — mapa Prahy obarvená predikovanou poptávkou + top zóny.
- **Matching:** profil zóny → doporučený typ (AC street / DC hub / stožár VO…) + **mapa mezer**.
- Příklad „méně očekávané, ale sedící" umístění: **[DOPLNIT konkrétní zónu z dat]**.

## Slide 5 — Byznys model (kontinuální služba)
- Předplatné MČ ~**19 000 Kč/měs** · celoměstská licence ~**900 000 Kč/rok** · modul Ochrana sítě (PRE) ~**500 000 Kč/rok**.
- **Opakovaný příjem** + **sběr dat v čase** (nové stanice, registrace EV, obsazenost z pilotu PRE → retrain). Smyčka přes n8n.
- Návratnost: zabráníme byť 1 mrtvé dobíječce / 1 předčasnému posílení trafa ročně → zaplatí se mnohonásobně. **Služba = investice, ne výdaj.**

## Slide 6 — Etika (4 oblasti, zabudované)
1. Chybná predikce → confidence známka + člověk v kličce + čtvrtletní back-testing.
2. Soukromí → jen agregáty na úrovni zóny (práh min. domácností), žádná individuální data.
3. **Spravedlnost / cold-start (těžiště):** equity váha + nafouknutá nejistota pro řídké zóny → lámeme sebenaplňující spirálu chudších čtvrtí. Metrika „fairness gap".
4. Nejistota → pásma + scénáře, rozhodnutí robustní napříč scénáři.

## Slide 7 — Škálování
- Featury **město-agnostické** (poměry/hustoty) → Brno, Plzeň, Ostrava jen nasypou open data.
- Jiná infrastruktura: P+R, sdílená mobilita, depa elektrobusů. Síťový efekt sdíleného modelu.

## Slide 8 — Tým a shrnutí
- Tým: **[DOPLNIT jména/role]**. Proč my: **[DOPLNIT — VPS/n8n provozujeme reálně apod.]**.
- One-liner: *„VoltPlán: predikuj → doporuč → ochraň síť — jedna služba, vestavěná férovost, běžící model."*

---
**K odevzdání:** tenhle deck (PDF) · technické shrnutí 1 A4 · `submissions/sample_submission.csv` · odkaz na kód/demo.
**Q&A připrav:** jak měříte kvalitu (baseline), jak řešíte leakage, jak cold-start, kdo platí a proč.
