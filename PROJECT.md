# aiolympiada — projektový descriptor pro agenty

> Čte ho agent (i z jiného adresáře) aby věděl co projekt dělá a co v něm je.
> Prózu níž udržuj ručně; inventář dole regeneruje `refresh-project-map`.

## Co to dělá
**Hackathon — Česká AI Olympiáda 2026, linie AI Startup, krajské kolo Praha**
(zadání `AIO_PHA-02-PHA`). Téma (aktualizováno 2026-06-09): **udržitelná mobilita a
energetika**. Naše cesta = predikce poptávky/zátěže + **řízené nabíjení a V2G** (auto jako
zdroj pro síť/čtvrť) + chytré umístění. Cíl = vyhrát krajské kolo.

**Orientace:** `HACKATHON-PLAN.md` (4h plán) → `BRIEF.md` (úkol + co hodnotí porota) →
`CONCEPT-VoltPlan.md` (koncept + update banner) → `HARDWARE.md` (HW/trénink) → `DATA-MAP.md`
(data) → `SETUP.md` (prostředí). Plné zadání + meta-prompty v `zadani/`.

## Koncept: VoltPlán (aktualizováno 2026-06-09)
Téma rozšířeno na **mobilitu + energetiku**. Naše cesta = **Linie A**: predikce → **řízené
nabíjení + V2G** („nejhlubší příležitost") → umístění. Vrstvy: Trust → Demand (LightGBM) →
Matching → Grid/V2G → demo → smyčka. **Sandbox, ne soutěž** (žádné test zóny/submission,
vlastní holdout). Zákazník i energetická komunita/distributor. Plný plán `CONCEPT-VoltPlan.md`.

## Stav / poznámky
- 2026-06-09: setup hotový — brief, **koncept VoltPlán**, hardware guide, data-mapa, requirements,
  HF MCP + plugin, profilovací skelet. **Data zatím nedorazila** (`participants/` core ~251 MB +
  optional ~1,6 GB → `data/`).
- **Hardware:** Intel Core Ultra 7 258V (Lunar Lake), 32 GB, NPU, žádná CUDA → trénink na CPU
  (LightGBM/sklearn + sklearnex), NPU jen inference. Velká data: polars/duckdb lazy.
- HuggingFace: MCP zapnutý (`.mcp.json`, `${HF_TOKEN}`); plugin `huggingface-skills`; TabPFN jako
  tabular FM alternativa. Predikce → `submissions/`, skripty → `src/`.
- Klíčové pasti: jednorázová analýza, triviální zrcadlení, data leakage, chybějící cold-start,
  chybějící živé demo (= 0 bodů technika). Viz `BRIEF.md`.

<!-- AUTO:INVENTORY (generuje refresh-project-map — needituj ručně) -->
**Stack:** Python

**Adresáře:** `.github`, `.streamlit`, `data`, `pitch`, `pitch-deck`, `src`, `submissions`, `video`, `zadani`

**Soubory:** `.mcp.json`, `.mcp.json.disabled`, `APP-SPEC.md`, `BRIEF.md`, `BUSINESS-MODEL-DETAIL.md`, `CLAUDE.md`, `CONCEPT-VoltPlan.md`, `DATA-MAP.md`, `DYNAMIC-PRICING.md`, `FINISH-PROMPT.md`, `HACKATHON-PLAN.md`, `HARDWARE.md`, `MENTOR-SESSION-PREP.md`, `PITCH-ONE-PAGE.md`, `PITCH-ONE-PAGE.txt`, `PREMIUM_GUIDE.md`, `README.md`, `READY.md`, `RUN.md`, `SETUP.md`, `START-HERE.md`, `TEAMFLOW.md`, `TECHNICAL-SUMMARY.md`, `requirements.txt`

_Refreshed: 2026-06-09 · `refresh-project-map`_
<!-- /AUTO:INVENTORY -->
