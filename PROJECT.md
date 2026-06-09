# aiolympiada — projektový descriptor pro agenty

> Čte ho agent (i z jiného adresáře) aby věděl co projekt dělá a co v něm je.
> Prózu níž udržuj ručně; inventář dole regeneruje `refresh-project-map`.

## Co to dělá
**Hackathon — Česká AI Olympiáda 2026, linie AI Startup, krajské kolo Praha**
(zadání `AIO_PHA-02-PHA`). Stavíme AI službu pro **chytré rozmístění a kapacitní
plánování EV dobíjení v Praze**: predikce poptávky 2030 po zónách + recommender typu
řešení + hlídání kapacity sítě. Cíl = vyhrát krajské kolo.

**Orientace:** `BRIEF.md` (úkol + co hodnotí porota) → `CONCEPT-VoltPlan.md` (náš vítězný
koncept + architektura) → `HARDWARE.md` (HW/trénink/stack) → `DATA-MAP.md` (data) →
`SETUP.md` (prostředí). Plné zadání + meta-prompty v `zadani/`.

## Koncept: VoltPlán
Předplatitelská rozhodovací platforma — 3 linie zadání jako 1 pipeline: Trust Layer →
Demand Engine (LightGBM quantile) → Matching Engine (recommender+equity+SHAP) → Grid
Optimizer (MILP) → What-if explorer (Streamlit) → datová smyčka (n8n). Plný plán v `CONCEPT-VoltPlan.md`.

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

**Adresáře:** `data`, `notebooks`, `pitch`, `src`, `submissions`, `zadani`

**Soubory:** `.mcp.json`, `.mcp.json.disabled`, `BRIEF.md`, `CLAUDE.md`, `CONCEPT-VoltPlan.md`, `DATA-MAP.md`, `HACKATHON-PLAN.md`, `HARDWARE.md`, `SETUP.md`, `requirements.txt`

_Refreshed: 2026-06-09 · `refresh-project-map`_
<!-- /AUTO:INVENTORY -->
