# 🚀 RUN CHECKLIST — VoltPlán spuštění

**Hackathon: 4 hodiny, 3 tratě paralelně. Zde je co spouštět když dorazí data.**

---

## PREREQUISITE (0:00–0:10)

### 1️⃣ Stáhnout data
```bash
# 1. Otevři https://drive.google.com/drive/folders/[ID z zadání]
# 2. Stáhni participants_data (~251 MB) a optional (~1.6 GB pokud chceš, ale nepovinné)
# 3. Rozbal do: data/participants/
```

**Check:**
```bash
ls data/participants/
# Měl bys vidět: zones_train.csv, zones_validation.csv, 
#                hourly_grid_and_charging_history_2025.csv, atd.
```

### 2️⃣ Setup prostředí
```bash
# (Pokud jsi to nedělal)
uv venv --python 3.11
source .venv/bin/activate       # Linux/Mac
# nebo .venv\Scripts\activate  # Windows

uv pip install -r requirements.txt
```

---

## KRITICKÁ CESTA (0:10–3:00)

### TRACK 🅐 (ML/MODEL) — vlastník čísla na slide 3
```bash
# 0:10–0:30 — explorece dat + leakage guard
python src/profile_data.py

# Doplň výsledky do DATA-MAP.md (paměť mezi sessions)
# Kontrola: jsou tam target_*_2030_synthetic sloupce?
```

```bash
# 0:30–1:30 — TRÉNINK (❗ daj si pozor na leakage!)
python src/train_demand.py

# Výstupy:
#   • submissions/predictions_validation.csv ← (pro demo + mapu)
#   • Console output: MAE, RMSE, Precision@50, baseline srovnání
#
# 📌 DOPLNIT NA SLIDE 3:
#   - MAE LightGBM: [číslo z konsole]
#   - MAE baseline: [číslo z konsole]
#   - Improvement: [%]
#   - Precision@50: [číslo]
```

### TRACK 🅑 (DEMO) — vlastník ukázky
```bash
# Čekej na předchozí (submissions/predictions_validation.csv)

# 1:30–2:30 — Web
streamlit run src/app.py

# Měl by se otevřít browser s:
#   • Mapou Prahy obarvená predikcí
#   • Tabulkou top 20 zón
#
# 📷 SCREENSHOT / VIDEO:
#   • otevřít screenshot nástroj: flameshot (Linux) / Print Screen (Win)
#   • nebo screen-record: ffmpeg -f x11grab ... (Linux) / Quicktime (Mac) / Xbox app (Win)
#   • ulož do: submissions/demo_screenshot.png + demo_video.mp4 (záloha)
```

### TRACK 🅒 (V2G + PITCH) — vlastník metriky na slide 4
```bash
# Běží paralelně s 🅐/🅑

# V2G heuristika
python src/v2g.py

# Výstupy:
#   • submissions/v2g_metrics.csv
#   • Console: overload_prevented_pct, v2g_kwh_returned, atd.
#
# 📌 DOPLNIT NA SLIDE 4:
#   - Přetížení zabráněno: [%]
#   - V2G vráceno síti: [kWh]
```

---

## SECUNDÁRNÍ (2:30–3:00) — pokud zbyde čas

```bash
# Linie B: matching typů + mapa mezer (v2g.py a train_demand.py mají prioritu!)
python src/match.py
# → submissions/matching.csv (zóna → doporučený typ + equity váha)
```

---

## ODEVZDÁNÍ (3:00–3:45)

### Připrav artefakty
```bash
ls submissions/
# Měl bys vidět:
#   ✅ predictions_validation.csv      (z train_demand.py)
#   ✅ v2g_metrics.csv                 (z v2g.py)
#   ✅ demo_screenshot.png             (z app.py)
#   ✅ matching.csv                    (z match.py, pokud jsi měl čas)
```

### Slide doplnění
1. **Slide 2** — Data: reálné vs. modelové
   - Odkaz na sandbox dataset
   - Zmínka o leakage guard (`.py` to kontroluje)
2. **Slide 3** — AI model + ČÍSLA
   - MAE: [DOPLNIT z train_demand.py consolu]
   - Precision@50: [DOPLNIT]
3. **Slide 4** — Výsledky + V2G DEMO
   - [DEMO SCREENSHOT nebo VIDEO z app.py]
   - Metrika V2G: [z v2g.py]
4. **Slide 6** — Zahraniční trend
   - "Utrecht We Drive Solar" — konkrétní čísla
5. Slide 7 — Etika: TECHNICAL-SUMMARY.md má body

### Finálně
```bash
# Odevzdej na platform.aiolympiada.cz:
#   1. Pitch Deck (PDF/PPTX)
#   2. Video (MP4, pokud máš; nebo screenshot)
#   3. Technické shrnutí (TECHNICAL-SUMMARY.md → PDF)
#   4. Odkaz na kód (GitHub repo)
#   5. Data outputs (submissions/*.csv)
```

---

## TROUBLESHOOTING

| Problém | Řešení |
|---|---|
| `Nenalezen zones_train.csv` | Rozbal data do `data/participants/` (viz PREREQUISITE) |
| `Leakage: target_* v features` | `train_demand.py` je vyhazuje automaticky; Check console |
| App spadne bez dat | Nejdřív spusť `train_demand.py`, pak `streamlit run app.py` |
| V2G metriky jsou dummy | Bez `hourly_grid_and_charging_history_2025.csv` vrací fallback čísla |
| Tréning je pomalý | CPU bez CUDA je normální (~2 min); Polars lazy je OK pro 2.29M řádků |

---

## 📋 Quick Reference

```bash
# All-in-one (když jsou data ready):
python src/profile_data.py && \
python src/train_demand.py && \
python src/v2g.py && \
python src/match.py && \
streamlit run src/app.py

# Jen train (nejdůležitější):
python src/train_demand.py

# Jen demo (když máš predikce):
streamlit run src/app.py
```

---

**Status:** ✅ Vše je připraveno. Čekáme na data. Jakmile je stáhneš, spusť si `python src/profile_data.py` a pojď na vývojáře s konkrétními čísly!
