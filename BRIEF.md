# BRIEF — AIO_PHA-02-PHA (Česká AI Olympiáda 2026, AI Startup, krajské Praha)

> Zhuštěné zadání pro rychlou orientaci. Zdroj pravdy = `zadani/zadani_AIO_PHA-02-PHA.md`
> (+ PDF). **Meta-prompty** (`zadani/meta_prompt_v1.md`, `v2.md`) jsou šablona, podle
> které zadání vzniklo → prozrazují, **co porota odměňuje a co sráží** → viz „Co porota
> reálně hodnotí" níž. To je naše tajná zbraň.

## Úkol jednou větou
Postav **běžící AI službu** pro Prahu, která **předpoví poptávku po veřejném dobíjení
EV v roce 2030 po zónách** a **doporučí, kam a jaký typ dobíječky přidat**, aniž by
přetížila lokální distribuční síť ve špičce.

- **Jednotka:** zóna odvozená z oblasti transformační stanice (TS), `grid_zone_id`.
- **Typ úlohy:** predikce (regrese) **+** párování/recommender (zóna ↔ typ řešení).
- **Zákazník:** Hl. m. Praha / městská část / Operátor ICT (Smart Prague). Partner: PRE, IPR.
- **Cíl predikce (test):** 513 testovacích zón **bez cílů** → odevzdat ve formátu
  `sample_submission.csv`. Privátní labely zůstávají pořadateli.

## Cílové proměnné (target_*_2030_synthetic)
denní kWh · špičkový kW · **riziko přetížení** · doporučený **typ / počet bodů / výkon**.
→ Dvě proměnné v napětí: **maximalizuj pokrytí poptávky**, **minimalizuj přetížení sítě**.
Optimum bývá uprostřed (pomalé noční u domu vs. rychlý hub vs. kapacita trafa).

## Tři linie (NEjsou menu — inspirace, lze kombinovat; nejsilnější je propojí)
- **A — Předvídat poptávku:** regrese / stromy → plán rozmístění a kapacit ve scénářích.
- **B — Spárovat zónu s řešením:** content-based recommender (podobnost profilů) + **mapa mezer**.
- **C — Hlídat síť:** optimalizace / clustering nad predikcí, aby se síť nepřetížila ve špičce.

## Tři pilíře, které MUSÍ splnit každé řešení (jinak propadák)
1. **Běžící AI algoritmus** — model trvale pracuje v produktu, NE jednorázový výpočet.
2. **Sběr a údržba dat v čase** — jak profil zóny vzniká a aktualizuje se (nové stanice,
   registrace EV, obsazenost z pilotu PRE, kapacita sítě). Stačí promyslet + obhájit v pitchi.
3. **Kontinuální hodnota** — běží a dává hodnotu opakovaně → monetizace = předplatné/služba.

---

## ⚑ Co porota REÁLNĚ hodnotí (vytěženo z meta-promptů — failure modes)
Toto jsou přesně ty pasti, na které je zadání designované. Vyhnout se jim = výhra.

- **Jednorázová analýza = smrt.** Nejčastější selhání: krásná data-analýza + jeden návrh a
  konec. Musí být **běžící algoritmus + plán sběru dat + opakovaný příjem**. (princip 0.3)
- **Triviální zrcadlení = nula hodnoty.** „Hodně aut → velký hub" zvládne tabulka. Musíme
  ukázat **méně očekávané, ale sedící** umístění (serendipity). (0.5)
- **Překonej baseline a DOLOŽ to.** Slide 3 pitche to explicitně chce: *jak měříte kvalitu,
  že výstup překonává baseline/náhodu.* → vždy si drž triviální baseline a měř proti němu.
- **Bohatší profil než jeden údaj.** Ne jen počet aut: typ zástavby, podíl bytů bez stání,
  kapacita sítě, tranzit, chování v čase.
- **Trend, ne dnešek.** Zóna s málo EV dnes, ale rychle rostoucí poptávkou ≠ nasycená zóna.
- **Cold-start = body 2×.** Málo dat o okrajových/chudších čtvrtích → horší doporučení →
  sebenaplňující spirála. Ošetřit to skóruje v **Technickém řešení i v Etice** zároveň.
- **Reálné vs. modelové — poctivost.** Označovat původ dat (R/O/S, viz DATA-MAP). Nevydávat
  syntetické cíle za měření PRE. **Kontrola leakage je součást úlohy** (cíle 2030 jsou
  syntetické → nesmí protéct do featur).
- **Tón k partnerovi:** Praha problém **aktivně řeší**, chybí jen nástroj. Nikdy „nikdo to neumí".
- **Nejistota:** poptávka 2030 je nejistá → pracuj s **pásmem scénářů**, ne s jedním číslem.
- **Živá ukázka běžícího modelu je POVINNÁ.** Bez demonstrace AI komponenty = **0 bodů**
  za Technické řešení. Vibe-coding (Lovable/v0/Bolt/Replit) vítán na UI, ale pod ním musí
  být skutečný model/engine.

## Hodnoticí kritéria (40 / 40 / 20)
- **Technické (40):** běžící AI; kvalita dat + čištění; **doložené překonání baseline**;
  interpretace; práce s cold-startem.
- **Byznys (40):** jasný zákazník (instituce); **opakovaný příjem**; sběr dat v čase;
  návratnost pro město; škálovatelnost.
- **Prezentace + etika + regionální relevance (20):** srozumitelný pitch + ukázka;
  4 etické oblasti; napojení na reálné pražské cíle (Smart Prague / PRE / IPR); nejistota.

## 4 etické oblasti (povinné, absence = 0 bodů v etice)
1. Chybná predikce a odpovědnost (prázdná dobíječka = mrtvá investice / přehlédnutá čtvrť).
2. Přístup k datům a soukromí (nabíjení prozrazuje, kde lidé bydlí/jezdí).
3. **Spravedlnost / cold-start** (sebenaplňující spirála chudších čtvrtí).
4. Komunikace nejistoty (predikce 2030 → město nesmí dělat přehnaně sebejistá rozhodnutí).

## Odevzdání + Pitch
- Platforma `platform.aiolympiada.cz`: odkaz na běžící řešení/kód, datové výstupy
  (predikce/doporučení), pitch deck, technické shrnutí **1 A4**.
- **Pitch deck max 8 slidů**, **3 min prezentace + 2 min dotazy**, video nepovinné.
  Checklist: 1) Problém+zákazník 2) Data (reálné vs. modelové, čištění) 3) AI model **+ jak
  měříte kvalitu vs baseline** 4) Výsledky + živá ukázka 5) Byznys (opak. příjem + sběr dat)
  6) Etika (zvlášť cold-start) 7) Škálování 8) Tým+shrnutí.

## Náš koncept: VoltPlán → `CONCEPT-VoltPlan.md`
Tři linie spojené do **jedné pipeline**: Trust Layer (čištění+leakage+confidence) → Demand
Engine (LightGBM quantile, KDE) → Matching Engine (recommender+equity+SHAP, JAKÝ TYP) → Grid
Optimizer (MILP, KOLIK bez přetížení) → What-if explorer (Streamlit) → datová smyčka (n8n).
Hardware/stack/trénink: `HARDWARE.md`. Prostředí: `SETUP.md`.

## Doporučená strategie (náš plán)
1. **Nejdřív baseline** (průměr/medián, „víc aut → víc kW") a změřit ho — pak na něm stavět.
2. **Propojit linie A+B:** předpověď poptávky → recommender typu řešení → mapa mezer. To je
   explicitně označené jako nejsilnější řešení.
3. **Anti-leakage od začátku:** nikdy netrénovat na `target_*_2030_synthetic` jako featuře;
   pozor i na `*_derived` sloupce odvozené z cílů.
4. **Cold-start zabudovat** (fallback profil pro řídké zóny) → skóruje i v etice.
5. **Produkt = předplatná služba pro MČ/Operátor ICT**, ne studie. Připravit slide o sběru dat.
6. **Živé demo:** lehké UI (vibe-coding) nad skutečným modelem — mapa zón s doporučením.
7. Reálné kotvy do pitche: 59 000 EV (2026), cíl 10 000 stanic / ~4 500 do 2030, +19 % síť 2025.

---
`AIO_PHA-02-PHA | Česká AI Olympiáda 2026 | nvias, z.s. | CC BY-NC-SA 4.0` — zadání je modelové cvičení.
