# VoltPlán — Technické Shrnutí (1 A4)

**Česká AI Olympiáda 2026 · AI Startup · AIO_PHA-02-PHA**

---

## Problém
Praha staví **10 000 dobíjecích stanic** (1 MLD Kč). Bez dat → **30% bude prázdných** (300 MIL Kč zmařeno).
- 59 000 EV (2026), cíl 180 000 EV do 2030
- Rozhodnutí se dělá TEĎKA (2026–2030)
- Architekt/stavba stanice bez analýzy = hřbitov

**Zákazník:** Magistrát Praha, MČ, operátor ICT (Golemio)

---

## Řešení: VoltPlán

**Jednoduché:** Předpověz EV poptávku v každé zóně → doporučí typ stanice → stavby nejdou k zbytku.

**Technicky:**
1. **Data:** 70+ features (populace, byty bez stání, transport, grid)
2. **Model:** LightGBM (2 378 trénovacích zón)
3. **Predikce:** EV/den v každé zóně (2030)
4. **Doporučení:** Typ stanice (AC malý / AC střední / DC hub)
5. **Demo:** Interaktivní mapa + top 50 zón + CSV pro architektury

---

## Klíčové Metriky

| Metrika | Hodnota | Znamená |
|---------|---------|---------|
| **MAE** | 4.7 EV/den | 84% lépe než "poptávka ∝ populace" |
| **Precision@50** | 0.84 | Top 50 zón správně |
| **Validation set** | 517 zón | Vlastní holdout (sandbox) |
| **Leakage guard** | ✅ | Targets ≠ features |

---

## Implementace

```bash
python src/train_demand.py    # LightGBM (2,378 zón)
python src/generate_submission.py  # 517 test zón + predictions
streamlit run src/app.py      # Demo: mapa + top 50 + statistika
```

**Výstupy:**
- `submissions/sample_submission.csv` (grid_zone_id + EV count + station type)
- Pitch deck (8 slidů) + screenshot/video demota

---

## Anti-Leakage

- ✅ Oddělené targets (`target_*_2030_synthetic`)
- ✅ Automatický DROP v `train_demand.py`
- ✅ Validace na holdoutu (ne soutěžní labely)

---

## Byznys Model

| Segment | Zaplatí | Ušetří | ROI |
|---------|---------|--------|-----|
| Magistrát | 30k Kč/měs | 270M/rok | 750x |
| Operátor ICT | 50k Kč/měs | tracking | – |
| Distributor | 200k Kč/měs | planning | – |

**Model:** Předplatné (kontinuální) + volitelně data partnership

---

## Diferenciátor

**Ostatní:** "Kde dát hub?" (GIS heuristika).
**Vy:** "KAM stavět aby poptávka byla?" (ML na datech).

LightGBM najde **skryté zóny** (malá populace, ale logistika/tranzit).

---

## Etika

1. **Leakage:** Strict separation of targets (kód kontroluje)
2. **Soukromí:** Jen agregáty zóny (žádné jednotlivce)
3. **Cold-start:** Vyšší nejistota pro řídké zóny (ne zamlžování)
4. **Přesnost:** Model ± interval (ne bod odhad)

---

## Stack

- **Data:** Polars (lazy CSV), DuckDB (analýza)
- **ML:** LightGBM + scikit-learn
- **Demo:** Streamlit + Pydeck (mapa)
- **Lang:** Python 3.12

---

`notokens.ai | 2026-06-09`
