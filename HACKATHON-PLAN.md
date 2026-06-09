# ⏱ 4HODINOVÝ PLÁN — co reálně postavit (governs, ne 4týdenní roadmapa)

> Máme **4 hodiny** na všechno včetně pitche. VoltPlán je plná vize; tady je co se z něj
> reálně stihne. **Pravidlo: radši 1 běžící model + skvělý pitch než 3 rozbité linie.**
> Odevzdej s rezervou — **submit v 3:45**, ne v 4:00.

## Bodová matematika (proč tahle priorita)
- **Byznys 40 + Prezentace/etika 20 = 60 bodů ≈ hlavně SLIDY.** Z VoltPlánu (`CONCEPT-VoltPlan.md`
  §4 byznys, §5 etika, §6 pitch) máš 80 % textu hotového. **Nejvyšší body/minutu.**
- **Technika 40** = potřebuje JEDEN běžící model s **doloženým překonáním baseline**. Bez běžícího
  modelu = 0 z techniky. Všechno ostatní (MILP optimizer, n8n, quantily, SHAP, TabPFN) = bonus.

## Co stavíme (MUST) vs co jen POPÍŠEME v pitchi (CUT) — 3 lidi
| | Stav |
|---|---|
| **Linie A — Demand (LightGBM)** | ✅ POSTAVIT. Predikce + baseline + `sample_submission.csv`. Jádro. |
| **Linie B — Matching** | 🟡 JEN když A hotová do 1:30. Content-based profil→6 typů + equity + mapa mezer. Jinak popsat. |
| **Linie C — Grid check** | ❌ Nestavět (na 4h není čas). Popsat v pitchi (rezerva TS jako omezení). |
| **n8n datová smyčka** | ❌ Jen popsat (pilíř 2 „stačí promyslet" — zadání to dovoluje). |
| **Demo** | ✅ Streamlit mapa + predikce + mapa mezer. **screenshot/záznam jako záloha**. |
| **Byznys + etika + pitch** | ✅ Slidy z VoltPlánu — vlastní track, běží od minuty 0. |

## Rozdělení na 3 tratě (paralelně od 0:00)
**🅐 ML/MODEL** (technika 40) · **🅑 DEMO/DATA** (demo + viz) · **🅒 PITCH/BYZNYS** (byznys 40 + etika 20)

### 🅐 ML — vlastník čísla
- **0:00–0:25** setup + `python src/profile_data.py` → cíle, leakage. Vyber hlavní cíl.
- **0:25–1:30** `python src/train_demand.py` → **MAE/RMSE vs baseline + P@50 = ČÍSLO na slide 3**
  + `submissions/sample_submission.csv`. **Hotové první — de-risk. Pošli číslo 🅒 hned.**
- **1:30–2:45** Linie B matching (`src/match.py`) JEN když A sedí → předej 🅑 mapu mezer. Jinak rovnou k slidům.
- **2:45–4:00** čísla a feature-importance 🅒 do slidů, technické shrnutí 1 A4, nácvik.

### 🅑 DEMO/DATA — vlastník ukázky
- **0:00–0:50** prostředí, pomoc 🅐 s daty, mapové sloupce (lat/lon, MČ).
- **0:50–2:30** `src/app.py` Streamlit: mapa obarvená predikcí + top zóny (+ mapa mezer když je B).
- **2:30–3:00** **screenshot + 30s screen-record jako zálohu** (demo na place může spadnout).
- **3:00–4:00** vizuály do decku (mapa, graf baseline vs model), pomoc s nácvikem.

### 🅒 PITCH/BYZNYS — vlastník decku (běží nezávisle na kódu)
- **0:00–1:45** deck z `pitch/DECK.md` (VoltPlán §4 byznys, §5 etika, §6 pitch):
  slide 1 problém+zákazník, 5 byznys (ceník Kč), 6 etika (4 oblasti, cold-start), 7 škálování, 8 tým.
- **1:45–3:00** slide 2 data, 4 výsledky (placeholdery na čísla od 🅐); technické shrnutí 1 A4.
- **3:00–3:45** doplnit čísla od 🅐 (slide 3+4), sjednotit vizuál, **vést nácvik 3 min**.
- **3:45–4:00** **ODEVZDÁNÍ** na platform.aiolympiada.cz (kód/odkaz, `sample_submission.csv`, deck, A4).

## Tvrdá pravidla pod tlakem
- **Anti-leakage hned:** nikdy `target_*_2030_synthetic` ani sloupce z nich odvozené jako featura
  (`src/train_demand.py` je auto-vyhazuje). Jeden zachycený leakage = dobrý bod do pitche.
- **Číslo > krása.** MAE proti baseline na slide 3 vyhrává techniku. Bez něj nic.
- **Nestav optimizer ani n8n.** Popsané v pitchi stačí na byznys body.
- **Demo má zálohu.** Screenshot/záznam. Běžící jednoduchost > efektní pád.
- **sklearnex/TabPFN/quantily = jen když jsi napřed.** Na 2 400 řádků LightGBM stačí.

## Připravené skripty (spustíš jak dorazí data)
- `src/profile_data.py` — schéma + řádky + leakage guard.
- `src/train_demand.py` — adaptivní (auto-detekce cílů/featur), LightGBM + baseline + submission.
- `src/app.py` — minimální Streamlit demo (skelet).
