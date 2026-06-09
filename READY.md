# ✅ READINESS CHECKLIST — VoltPlán development ready

Commit: `ccb7918`

---

## ✅ Kód je HOTOVÝ (v `src/`)

| File | Status | Co dělá | Čas na spuštění |
|---|---|---|---|
| `profile_data.py` | ✅ Hotovo | Explorece dat + leakage guard | ~1 min |
| `train_demand.py` | ✅ Hotovo | LightGBM predikce + baseline | ~2 min |
| **`v2g.py`** | ✅ **NOVÉ** | V2G heuristika + metriky | ~1 min |
| `match.py` | ✅ Hotovo | Content-based recommender (Linie B) | ~1 min |
| `app.py` | ✅ Hotovo | Streamlit demo (mapa + top zóny) | ~1 min |

---

## ✅ Dokumentace je HOTOVÁ

| File | Status | Důvod |
|---|---|---|
| `HACKATHON-PLAN.md` | ✅ | 4hodinový plán (3 tratě paralelně) |
| `BRIEF.md` | ✅ | Zhuštěný úkol + co porota chce |
| `CONCEPT-VoltPlan.md` | ✅ | Architektura + byznys model |
| `DYNAMIC-PRICING.md` | ✅ **NOVÉ** | Klíč: ekonomické řízení (řidič se ROZHODUJE) |
| `TECHNICAL-SUMMARY.md` | ✅ | 1 A4 pro odevzdání |
| `RUN.md` | ✅ | Konkrétní příkazy (0:00–3:45) |
| `pitch/DECK.md` | ✅ | 8 slidů (slide 4 aktualizován — dynamic pricing) |

---

## ⏳ CO ZBÝVÁ (čeká na DATA)

### Data dorazí → SPUSŤ (10:00–1:30)

1. **0:10–0:30:** `python src/profile_data.py` → zkontroluj leakage
2. **0:30–1:30:** `python src/train_demand.py` → MAE/Precision@50 **na slide 3**
3. **1:30–2:30:** `python src/v2g.py` → V2G metriky **na slide 4**
4. **2:30–3:00:** `streamlit run src/app.py` + screenshot → **slide 4 demo**

### Pitch doplnění (2:30–3:45)

- Slide 2: Zdroj datasetu (sandbox)
- Slide 3: **[DOPLNIT čísla]** ← z `train_demand.py`
- Slide 4: **[DOPLNIT metriky]** + **[DEMO]** ← z `v2g.py` + `app.py`
- Slide 6: Utrecht V2G reference ✅ (hotovo, jen verify)
- Slide 7: Etika (cold-start z `TECHNICAL-SUMMARY.md`)

### Odevzdání (3:45–4:00)

1. Pitch deck (PDF)
2. Technické shrnutí (→ PDF z `TECHNICAL-SUMMARY.md`)
3. Video/screenshot (z demodu)
4. GitHub repo link
5. Data outputs (`submissions/*.csv`)

---

## 🎯 Kritické cesty (failure points)

| Risk | Jak se to nedělá | Jak se to dělá |
|---|---|---|
| **Bez dat** | Nic | Stáhni z Google Drive do `data/participants/` |
| **Leakage v modelu** | `train_demand.py` má to kontrolovat; pokud selže → oprav DROP_HINTS | Check `profile_data.py` output; leakage guard v `train_demand.py` je auto |
| **Bez čísla na slide 3** | Padáš z techniky (0 bodů) | Spusť `train_demand.py`, přepíši MAE vs baseline |
| **Bez V2G demo** | "Není vidět diferenciátor" | `streamlit run src/app.py` + screenshot (máš fallback dummy čísla) |
| **Bez technical summary** | Chybí povinné odevzdání | `TECHNICAL-SUMMARY.md` je připraveno; stačí PDF |

---

## 📝 Quick copy-paste (až budou data)

```bash
cd /home/felix/projects/ai-olypm-notokens
source .venv/bin/activate

# Explorece
python src/profile_data.py

# Trénink + V2G + demo (paralelně v terminálu 1–3)
python src/train_demand.py           # Terminál 1: MAE, Precision@50
python src/v2g.py                    # Terminál 2: V2G metriky
streamlit run src/app.py             # Terminál 3: demo (browser)

# Volitelně
python src/match.py                  # Pokud zbyde čas

# Screenshot
# (use system tool: flameshot, screenshot, etc.)
```

---

## ✅ Status FINÁL

- ✅ Kód: HOTOVÝ
- ✅ Dokumentace: HOTOVÁ
- ✅ Plán: JASNÝ (RUN.md)
- ✅ Commit: Uloženo
- ⏳ Data: Čekáme
- ➡️ **NEXT:** Stáhni data, spusť `python src/profile_data.py`, pak jdi na vývojáře!

---

**Pokud vše padne:** fallback dummy čísla v `v2g.py` a `train_demand.py` ti dají "playing field" i bez plných dat.

**Pohod! ⚡**

