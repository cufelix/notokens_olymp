# SETUP — prostředí na hackathonovém notebooku

> Cíl: Intel Core Ultra 7 258V (Lunar Lake), 32 GB, Windows/Linux. Funguje i na Macu
> (sklearnex se tam jen přeskočí). Vše přes **uv** (rychlé, izolované).

## 1. Python prostředí
```bash
cd ~/projects/aiolympiada       # nebo kamkoli projekt rozbalíš
uv venv --python 3.11           # 3.11 = nejširší kompatibilita ML balíků
source .venv/bin/activate       # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```
Ověření Intel akcelerace (na Intel notebooku):
```bash
python -c "from sklearnex import patch_sklearn; patch_sklearn(); print('sklearnex OK')"
```

## 2. Data
Až dorazí složka `participants/` → rozbal do `data/participants/`, pak spusť ingest
playbook z `DATA-MAP.md` (polars/duckdb, nečíst velké CSV celé). `data/` je v `.gitignore`.

## 3. HuggingFace
**Token:** založ na https://huggingface.co/settings/tokens (read stačí), pak:
```bash
export HF_TOKEN=hf_xxx           # do shellu / .env (NEcommituj)
huggingface-cli login            # nebo: hf auth login
```
**MCP server** je už nakonfigurovaný v `.mcp.json` (čte `${HF_TOKEN}`) → po startu
`claude` v tomhle adresáři máš HF model/dataset/paper search jako nástroje.

**Plugin se skilly** (datasets, trackio, gradio, local-models, llm/vision trainer):
```bash
claude plugin install huggingface-skills@claude-plugins-official
```
(oficiální Anthropic marketplace, zdroj github.com/huggingface/skills — ověřeno.)

## 4. (volitelně) NPU / lokální LLM přes OpenVINO
Jen pokud chceš na demu běžící lokální LLM (např. textová zdůvodnění). NENÍ nutné pro trénink.
```bash
uv pip install openvino openvino-genai
# model converted to OpenVINO IR, run device="NPU" nebo "GPU"
```

## 5. Struktura práce
- `src/` — profilovací + tréninkové skripty (`profile_data.py` je připravený skelet).
- `notebooks/` — explorace.
- `submissions/` — predikce ve formátu `sample_submission.csv`.
- Před odevzdáním: `codex exec --sandbox read-only` review na model + anti-leakage.

## Pasti specifické pro tenhle HW
- **Nehledej CUDA.** Žádná NVIDIA → LightGBM/sklearn jedou na CPU (a stačí to bohatě).
- **NPU netrénuje.** Je na inference; trénink tabulárních dat běží na CPU.
- **Paměť:** float32 + polars lazy; `hourly_…csv` (2,29 M řádků) nikdy celé do pandas.
