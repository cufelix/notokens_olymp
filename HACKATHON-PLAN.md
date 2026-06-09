# ⏱ 4HODINOVÝ PLÁN — co reálně postavit (governs, ne 4týdenní roadmapa)

> Máme **4 hodiny** na všechno včetně pitche. VoltPlán je plná vize; tady je co se z něj
> reálně stihne. **Pravidlo: radši 1 běžící model + skvělý pitch než 3 rozbité linie.**
> Odevzdej s rezervou — **submit v 3:45**, ne v 4:00.

## Bodová matematika (proč tahle priorita)
- **Byznys 40 + Prezentace/etika 20 = 60 bodů ≈ hlavně SLIDY.** Z VoltPlánu (`CONCEPT-VoltPlan.md`
  §4 byznys, §5 etika, §6 pitch) máš 80 % textu hotového. **Nejvyšší body/minutu.**
- **Technika 40** = potřebuje JEDEN běžící model s **doloženým překonáním baseline**. Bez běžícího
  modelu = 0 z techniky. Všechno ostatní (MILP optimizer, n8n, quantily, SHAP, TabPFN) = bonus.

## Naše cesta = Linie A (nabíjení + síť + **V2G**). Jedna čistá běžící linie stačí.
Zadání: V2G = „nejhlubší příležitost", propojení mobility+energetiky = nejsilnější. Je to
**sandbox, ne soutěž** → žádné odevzdání predikcí, validuješ si sám (holdout / `zones_validation`).

## Co stavíme (MUST) vs co jen POPÍŠEME v pitchi (CUT) — 3 lidi
| | Stav |
|---|---|
| **Predikce poptávky/zátěže (LightGBM)** | ✅ POSTAVIT. + baseline + interpretace. Jádro, de-risk první. |
| **V2G / řízené nabíjení (diferenciátor)** | ✅ POSTAVIT lehce: heuristika nad `hourly_*` (rezerva+overload) → posun nabíjení do hodin s rezervou + V2G plní rezervu. Headline „X zabráněných přetížení / Y kWh flexibility". |
| **Mapa mezer / matching typů** | 🟡 JEN když zbude čas (`src/match.py`). Jinak popsat. |
| **n8n datová smyčka** | ❌ Jen popsat (pilíř 2 „stačí promyslet" — zadání to dovoluje). |
| **Demo** | ✅ Streamlit: mapa predikce + **časový graf řízené nabíjení/V2G vs špička**. screenshot/záznam jako záloha. |
| **Byznys + etika + pitch + zahraniční trend** | ✅ Slidy — vlastní track od minuty 0. |

## Rozdělení na 3 tratě (paralelně od 0:00)
**🅐 ML/MODEL** (technika 40) · **🅑 DEMO/DATA** (demo + viz) · **🅒 PITCH/BYZNYS** (byznys 40 + etika 20)

### 🅐 ML — vlastník čísla + V2G
- **0:00–0:25** setup + `python src/profile_data.py` → cíle, leakage. Vyber hlavní cíl (kWh nebo špička).
- **0:25–1:30** `python src/train_demand.py` → **MAE/RMSE vs baseline + P@50 = ČÍSLO na slide 3**
  + predikce na validaci pro demo. **Hotové první — de-risk. Pošli číslo 🅒 hned.**
- **1:30–3:00** **V2G/řízené nabíjení** nad `hourly_*` (rezerva+overload_flag): heuristika posunu
  nabíjení do hodin s rezervou + V2G plní špičku → metrika **„X zabráněných přetížení / Y kWh vráceno síti"**.
  To je náš diferenciátor (mobilita×energetika). Předej 🅑 časový profil.
- **3:00–4:00** čísla + feature-importance + V2G metrika 🅒 do slidů, technické shrnutí 1 A4, nácvik.

### 🅑 DEMO/DATA — vlastník ukázky
- **0:00–0:50** prostředí, pomoc 🅐 s daty, mapové sloupce (lat/lon, MČ).
- **0:50–2:30** `src/app.py` Streamlit: mapa obarvená predikcí + **časový graf zátěž vs rezerva
  s/bez řízeného nabíjení+V2G** (to je „aha" moment ukázky).
- **2:30–3:00** **screenshot + 30s screen-record jako zálohu** (demo na place může spadnout).
- **3:00–4:00** vizuály do decku (mapa, V2G graf, baseline vs model), pomoc s nácvikem.

### 🅒 PITCH/BYZNYS — vlastník decku (běží nezávisle na kódu)
- **0:00–1:45** deck z `pitch/DECK.md`: slide 1 problém+zákazník (energ. komunita/distributor),
  5 byznys (ceník + sdílení výnosu z flexibility), 6 **váš úhel + zahraniční V2G trend na Prahu**,
  7 etika (cold-start), 8 tým. **Najdi 1 zahraniční příklad** (Utrecht V2G / Octopus dynam. tarify).
- **1:45–3:00** slide 2 data, 3 AI model (placeholdery na čísla), 4 výsledky+demo; technické shrnutí 1 A4.
- **3:00–3:45** doplnit čísla + V2G metriku od 🅐, sjednotit vizuál, **vést nácvik 3 min**.
- **3:45–4:00** **ODEVZDÁNÍ** na platform.aiolympiada.cz (kód/odkaz, datové výstupy, deck, A4).

## Tvrdá pravidla pod tlakem
- **Anti-leakage hned:** nikdy `target_*_2030_synthetic` ani sloupce z nich odvozené jako featura
  (`src/train_demand.py` je auto-vyhazuje). Jeden zachycený leakage = dobrý bod do pitche.
- **Číslo > krása.** MAE proti baseline na slide 3 vyhrává techniku. Bez něj nic.
- **V2G heuristika nemusí být MILP** — i greedy posun do hodin s rezervou je „optimalizace" a dá headline.
- **Sandbox, ne soutěž:** žádné odevzdání predikcí, validuj si sám (holdout / `zones_validation`).
- **n8n jen popsat.** Sběr dat v čase obhájíš v pitchi (pilíř 2).
- **Demo má zálohu.** Screenshot/záznam. Běžící jednoduchost > efektní pád.
- **sklearnex/TabPFN/quantily = jen když jsi napřed.** Na 2 400 řádků LightGBM stačí.

## Připravené skripty (spustíš jak dorazí data)
- `src/profile_data.py` — schéma + řádky + leakage guard.
- `src/train_demand.py` — adaptivní (auto-detekce cílů/featur), LightGBM + baseline + predikce na validaci.
- `src/match.py` — mapa mezer / matching typů (volitelné).
- `src/app.py` — Streamlit demo (mapa + V2G časový graf).
- **TODO na místě:** `src/v2g.py` — heuristika řízeného nabíjení + V2G nad `hourly_*` (diferenciátor).
