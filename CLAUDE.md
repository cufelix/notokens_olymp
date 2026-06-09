# aiolympiada — Česká AI Olympiáda 2026, AI Startup (krajské Praha)

**Hackathon projekt.** Soutěžíme se zadáním **AIO_PHA-02-PHA**: AI služba pro chytré
rozmístění a kapacitní plánování EV dobíjení v Praze. Cíl = vyhrát krajské kolo.

> ⏱ **~2 HODINY** (3 lidi). 🎯 **VYBRANÝ PRODUKT = `APP-SPEC.md`** — B2G aplikace, která
> městu vyhodnotí **KDE mají dobíječky smysl** (AI suitability scoring zón), roční licence.
> **Toto je THE plán. Stav podle `APP-SPEC.md` → „Build order".** Starší V2G/dynamic-pricing/
> CONCEPT-VoltPlan byly explorace — dnes řešíme JEDEN problém (umístění), ne všechno.

## Než cokoli uděláš — přečti v tomto pořadí
1. **`APP-SPEC.md`** — ⭐ ŘÍDÍCÍ: produkt, featury, AI kontrakt, rozdělení, build order.
2. **`BRIEF.md`** — co porota reálně hodnotí. `zadani/` — plné zadání.
3. *(kontext, neřídí už):* `CONCEPT-VoltPlan.md` — starší širší koncept (3 linie jako 1 pipeline:
   Trust Layer → Demand → Matching → Grid Optimizer → demo → datová smyčka). Toto stavíme.
3. **`HARDWARE.md`** — na čem to běží (Intel Lunar Lake, NPU, 32GB) + jak trénovat + stack.
4. **`DATA-MAP.md`** — inventář dat + ingest playbook. Data zatím nedorazila → slot připravený.
5. **`SETUP.md`** — prostředí (uv, HF token/MCP/plugin). Detaily zadání: `zadani/`.

## Pevná fakta (ať je neztratíme)
- Jednotka = zóna (`grid_zone_id`, odvozeno z TS). Predikujeme **513 test zón bez cílů** → formát `sample_submission.csv`.
- Cíle = `target_*_2030_synthetic` (denní kWh, špička kW, riziko přetížení, doporučený typ/počet/výkon). **Nikdy jako featura → leakage.**
- Dvě proměnné v napětí: max pokrytí poptávky × min přetížení sítě.
- Hodnocení **40 (technika) / 40 (byznys) / 20 (prezentace+etika+region)**.
- **Živá ukázka běžícího modelu povinná** — bez ní 0 bodů za techniku.

## Pravidla práce (hackathon mód)
- **Rychlost > dokonalost**, ale vždy drž **baseline a měř proti němu** (porota to explicitně chce).
- **Hardware:** Intel Lunar Lake, **žádná CUDA**. Trénink = **CPU** (LightGBM/sklearn + **sklearnex**).
  NPU/OpenVINO = jen inference. Nehledej GPU trénink. Viz `HARDWARE.md`.
- Velká CSV (hourly = 2,29 M řádků, optional 1,6 GB): **polars/duckdb lazy**, `float32`, nikdy
  `read_csv` celé ani číst do kontextu. Skelet: `src/profile_data.py`.
- Po prozkoumání dat **doplň skutečná čísla do `DATA-MAP.md`** — slouží jako paměť mezi sessions.
- Anti-leakage a cold-start ber jako prioritu — skórují dvakrát (technika + etika).
- Predikce → `submissions/`, tréninkové skripty → `src/`, experimenty → `notebooks/`.

## Workflow
1. Data dorazí → rozbal do `data/participants/`, spusť ingest playbook z `DATA-MAP.md`, doplň mapu.
2. Baseline → feature engineering (s anti-leakage) → model (regrese A) + recommender (B) → mapa mezer.
3. Lehké UI (vibe-coding) nad modelem pro živé demo.
4. Pitch (8 slidů) + technické shrnutí 1 A4 dle checklistu v `BRIEF.md`.
5. Před odevzdáním: **Codex review** (`codex exec --sandbox read-only`) na model i anti-leakage.

## Infra
- Native memory řeš jen pro durable rozhodnutí o tomhle projektu. Code facts → rg/Read.
- **HF MCP zapnutý** (`.mcp.json`, čte `${HF_TOKEN}`) — model/dataset/paper search. ruflo off.
- HF skilly: `claude plugin install huggingface-skills@claude-plugins-official` (trackio, datasets,
  gradio, local-models). TabPFN (HF tabular FM) jako silná alternativa modelu — viz `HARDWARE.md`.
