# HARDWARE & TRÉNINK — jak to zvládnout na hackathonovém notebooku

> **Notebook:** Intel **Core Ultra 7 258V** (Lunar Lake) · 8 jader (4P+4E) · Intel **Arc 140V** iGPU
> · **NPU** (~47 TOPS) · **32 GB** RAM (LPDDR5X). **Žádná NVIDIA / CUDA.**
> (Pozn.: vývojový Mac M4/16GB je jiný stroj — setup je cross-platform, ale cíl je ten Intel.)

## TL;DR — co reálně platí (ověřeno research + websearch 2026-06-09)
1. **Trénink tabulkových modelů = CPU.** LightGBM/XGBoost/CatBoost i scikit-learn trénují
   na CPU rychle. Na ~2 400 trénovacích zón je to **otázka sekund až minut**, ne hodin.
2. **NPU a OpenVINO = INFERENCE, ne trénink.** NPU je na energeticky úsporné spouštění
   hotových modelů (hlavně LLM). Pro náš trénink ho **nepoužiješ**. Využití jen volitelně:
   běžící lokální LLM na demu / generování textových zdůvodnění (viz dole).
3. **Intel akcelerace zdarma:** `scikit-learn-intelex` (**sklearnex**) přes oneDAL zrychlí
   sklearn algoritmy **10–100×** přímo na tomto Intel CPU. Dvě řádky:
   ```python
   from sklearnex import patch_sklearn; patch_sklearn()   # PŘED importem sklearn
   from sklearn.ensemble import RandomForestRegressor      # už zrychlené
   ```
   (x86-only → na Apple Mac se přeskočí, na Intel notebooku naběhne — viz requirements markery.)
4. **Velká data NEjsou problém na 32 GB**, když nepoužiješ naivní `pandas.read_csv` celé:
   - **Polars** (lazy) nebo **DuckDB** na `hourly_…csv` (2,29 M řádků) i `optional/` (1,6 GB).
   - Vynucuj `float32`/kategorie místo `float64` → poloviční paměť.
   - Core (251 MB) se vejde do RAM v pohodě i v pandas, ale poměrové featury dělej v polars.

## Trénink „vlastního modelu" — co to konkrétně znamená pro nás
„Vlastní model" = **vlastní natrénovaný gradient boosting / recommender na poskytnutých
datech**, ne stahování foundation modelu. To je zároveň **vítězný přístup pro tabulková data**.
Plán dle VoltPlánu (`CONCEPT-VoltPlan.md`):
- **Linie A (poptávka):** LightGBM regrese + **quantile** heads (P10/P50/P90) — vlastní trénink.
- **Linie B (typ):** sklearn klasifikátor + content-based skóre, SHAP zdůvodnění.
- **Linie C (síť):** MILP (PuLP/OR-Tools) — optimalizace, ne ML trénink.

### Volitelný silný tah: TabPFN (HuggingFace) jako „vlastní model 2.0"
**TabPFN v2** = pretrénovaný tabular transformer z HuggingFace, který **na malých datech
(< ~10 k řádků) běžně přebije laděný gradient boosting bez vlastního tréninku** a běží na CPU.
Náš train má ~2 378 řádků → **přesně jeho doména.** Skvělý do pitche: „použili jsme moderní
tabular foundation model a porovnali s LightGBM baseline". Zkus jako alternativu/ensemble k A.
```bash
pip install tabpfn         # CPU varianta; model se stáhne z HF Hub
```
> Pozor na limity TabPFN (počet featur/řádků) — drž LightGBM jako spolehlivou baseline.

## HuggingFace — k čemu reálně v TOMTO projektu (ne cargo cult)
- **HF MCP server** (přidán do `.mcp.json`): hledání modelů/datasetů/papers z Claude Code.
- **`huggingface-skills` plugin:** `datasets` (efektivní načítání), **`trackio`** (lehké
  trackování experimentů — porovnání model vs. baseline, což je PŘESNĚ kritérium poroty),
  `gradio` (alternativa Streamlitu na demo), `local-models` (lokální LLM přes NPU/OpenVINO).
- **TabPFN** (viz výš) — tabular foundation model z HF Hub.
- Kde HF NEpomůže: samotná optimalizace sítě (Linie C) a MILP — to je čistá matematika.

## Doporučený běhový stack (shrnutí)
| Úloha | Nástroj | Pozn. |
|---|---|---|
| Velká CSV / featury | **polars** (lazy) + **duckdb** | float32, kategorie; nečíst celé do RAM |
| Gradient boosting | **LightGBM** (+ quantile) | CPU, rychlé, SHAP |
| sklearn algoritmy | **scikit-learn** + **sklearnex** | 10–100× na Intel CPU |
| (volitelně) tabular FM | **TabPFN** (HF) | malá data → silný |
| Optimalizace sítě | **PuLP (CBC)** / OR-Tools | malý MILP |
| Interpretace | **SHAP** | zdůvodnění do pitche |
| Demo | **Streamlit** (+pydeck) | nízké riziko; HF Gradio jako alt |
| Experimenty | **trackio** (HF) | baseline vs. model — body poroty |
| (volitelně) lokální LLM | **OpenVINO** na NPU | jen inference, ne nutné |

→ Setup prostředí: `SETUP.md`. Inženýrský plán: `CONCEPT-VoltPlan.md`. Data: `DATA-MAP.md`.
