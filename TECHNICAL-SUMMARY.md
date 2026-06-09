# VoltPlán — Technické shrnutí (1 A4)

**Česká AI Olympiáda 2026 · AI Startup · AIO_PHA-02-PHA**

---

## Problém
Praha má 59 000 EV (2026) a cíl 10 000 veřejných dobíjecích stanic do 2030. Večerní špička jde na hranu sítě; investice do dobíječek jsou neefektivní. Chybí nástroj, který říká: **KDY a JAK nabíjet, aby auta síť pomáhala.**

**Zákazník:** Energetická komunita / distributor (PRE) + Magistrát HMP.

---

## Řešení: VoltPlán (Linie A: V2G + řízené nabíjení)

**Architektura:** 3 vrstvy toku dat
1. **Trust Layer** — čištění dat, leakage guard (`_real`/`_synthetic`)
2. **Demand Engine** — LightGBM predikce poptávky 2030 (regrese)
3. **V2G + Grid** — heuristika řízení nabíjení + obousměrné nabíjení (auto vrací energii)

**Model:** LightGBM na 2 378 zónách (features: populace, byty bez stání, kapacita sítě, tranzit).

---

## Klíčové metriky (slide 3 + 4)

| Metrika | Číslo | Poznámka |
|---|---|---|
| **MAE vs baseline** | [DOPLNIT po trénování] | → Dokazuje AI (ne triviální pravidlo) |
| **Precision@50** | [DOPLNIT] | Top 50 zón s největší poptávkou |
| **Přetížení zabráněno (V2G)** | [DOPLNIT]% | Řízené nabíjení v hodinách s rezervou |
| **V2G vráceno síti** | [DOPLNIT] kWh | Flexibility zdroj: auta jako baterie |

---

## Implementace

**Kód:**
- `src/profile_data.py` — bezpečné exploraci, leakage guard
- `src/train_demand.py` — LightGBM + baseline + validace (`zones_validation.csv`)
- `src/v2g.py` — heuristika (shift nabíjení do mild hodin + V2G metrika)
- `src/match.py` — content-based recommender (Linie B, když zbyde čas)
- `src/app.py` — Streamlit: mapa + V2G timeline

**Data:** 2 378 zón + 2.29M hodinových záznamů (lazy evaluation).

**Validace:** Vlastní holdout (`zones_validation.csv`), ne skryté labely (sandbox).

---

## Anti-leakage & Cold-start

**Leakage:** Nikdy `target_*_2030_synthetic` či `recommended_*` do featur. `train_demand.py` je vyhazuje automaticky.

**Cold-start:** Equity váha v `match.py` — vyšší priorita pro zóny bez nabídky / byty bez stání.

---

## Byznys model

**Kontinuální služba** (3 pilíře):
1. **Běžící AI** — model aktualizuje se na nových datech (EV registrace, obsazenost).
2. **Sběr dat v čase** — n8n smyčka: PRE/Golemio → retrain měsíčně.
3. **Monetizace** — předplatné (MČ/město) + **sdílení výnosu z V2G flexibility** s energetickou komunitou.

**Návratnost:** 1 zabráněné posílení trafo / 1 mrtvá dobíječka ročně → zaplatí se.

---

## Zahraniční inspirace: Utrecht V2G

**"We Drive Solar"** (Amsterdam, 2023): 60% vozidel v pilotu schopno V2G. Ročně 5 MW flexibility → Energie. komunita = investor.

**Proč na Prahu:** Pražské společenství pro OZE + pilot PRE. V2G umožňuje lokálním energetickým komunitám být producenty, ne jen spotřebiteli.

---

## Etika (4 oblasti)

1. **Chybná predikce** → confidence skóre + backtesting + člověk v kličce
2. **Soukromí** → Jen agregáty na úrovni zóny (bez individuálních dat)
3. **Spravedlnost/cold-start** → Equity váha (priorita bez-nabídkových zón)
4. **Nejistota** → Pásma scénářů (konzervativní/střední/ambiciózní), ne jedno číslo

---

## Spuštění (4 hodiny)

```bash
# Setup
uv venv --python 3.11
uv pip install -r requirements.txt

# Když dorazí data
python src/profile_data.py          # 5 min — kontrola leakage
python src/train_demand.py          # 2 min — čísla (MAE, P@50)
python src/v2g.py                   # 1 min — V2G metriky
python src/match.py                 # 1 min — equity weighting
streamlit run src/app.py            # 1 min — demo + screenshot
```

**Výstupy:** `submissions/` (predikce, V2G metriky, matching) → doplnit do pitche.

---

## Diferenciátor

**Ostatní týmy** řeší: "Kam dát dobíječku?" (lokalizace).

**Vy řešíte:** "KDYŽ a JAK nabíjet aby síť nepřetížila a auta jí pomáhala?" (V2G + řízené nabíjení).

To je **nejhlubší příležitost zadání.**

---

`AIO_PHA-02-PHA | Česká AI Olympiáda 2026 | notokens | 2026-06-09`
