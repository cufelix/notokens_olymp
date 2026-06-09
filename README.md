# notokens — VoltWise · Česká AI Olympiáda 2026 (AIO_PHA-02-PHA)

Tým **notokens**, krajské kolo Praha — AI Startup. Téma: **udržitelná mobilita a energetika**.
Stavíme **VoltWise** (Linie A): predikce poptávky/zátěže → **řízené nabíjení + V2G** (auto jako
zdroj pro síť/čtvrť) → chytré umístění. Propojení mobility a energetiky = nejsilnější cesta.
Data jsou **sandbox** (ne soutěž o skóre) — validujeme vlastním holdoutem.

## Spuštění dema (THE app = `src/app_premium.py`)
```bash
# 1) data (rozbalí se do data/participants/core/)
unzip data/core-dataset.zip -d data/participants/

# 2) prostředí
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt folium streamlit-folium
brew install libomp                       # LightGBM na macOS potřebuje OpenMP
export DYLD_LIBRARY_PATH="$(brew --prefix libomp)/lib"   # macOS; na Intel/Linux netřeba

# 3) natrénuj model + vyrob kontrakt pro appku
python src/generate_scores.py             # -> submissions/app_zone_scores.csv + metrics.json

# 4) spusť dashboard (HLAVNÍ appka)
streamlit run src/app_premium.py
```

`generate_scores.py` natrénuje **LightGBM** (predikce poptávky 2030, anti-leakage) +
**LightGBM recommender** typu stanice, spočítá **suitability_score** (poptávka + rezerva sítě +
mezera v pokrytí + férovost) a zapíše jediný kontraktní soubor, který appka čte.

## Struktura
- `src/generate_scores.py` — ⭐ trénink modelů + suitability scoring → `app_zone_scores.csv`
- `src/app_premium.py` — ⭐ **HLAVNÍ dashboard** (mapa, filtr obvodů, TOP-N, rozpočet, metodika)
- `src/app.py`, `src/app_complete.py` — jednodušší/starší varianty dema (funkční, ale nehlavní)
- `src/train_demand.py` — samostatný trénink + baseline (MAE/P@50 do konzole)
- `src/generate_submission.py` — DEPRECATED (nahrazeno `generate_scores.py`)
- `submissions/` — `app_zone_scores.csv` (kontrakt), `metrics.json`, `lgbm_model.pkl`
- `zadani/` — zadání + meta-prompty · `data/` — **negitované** (`.gitignore`)

> Hardware: Intel Core Ultra 7 258V (Lunar Lake), 32 GB, žádná CUDA → trénink na CPU
> (LightGBM/sklearn + sklearnex). Detaily `HARDWARE.md`.
