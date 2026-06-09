# VoltPlán — Pitch Deck (CORE: Demand Prediction + Station Placement)

> Fokus: Jakým typem a kde stavět dobíječky aby se nehýbalo peníze.
> 3 min talk + 2 min Q&A. **Slide 3 & 4 jsou klíčové.**

---

## Slide 1 — Problém
**Headline:** Praha staví 10 000 dobíjecích stanic (1 MLD Kč). Bez dat → 30% bude prázdných (300 MIL Kč zmařeno).

- **Realita:** 59 000 EV (2026), cíl: 10 000 nových stanic do 2030
- **Rozhodovací body:** Kde stavět? Jaký typ (AC malý / DC hub)?
- **Dneška:** Stavěj „od oka" + sociální tlak = mrtvé investice
- **Naší cílový zákazník:** Magistrát Praha, MČ, operátor ICT (Golemio), distributor (PRE)

## Slide 2 — Data
- **Zdroje:** ČSÚ (populace), RÚIAN (budovy), PRE (grid kapacita), IPR (infrastruktura)
- **Scope:** 2 378 trénovacích zón + 517 validačních zón
- **Atributy:** 70+ features (geografie, hustota, transport, grid)
- **Sandbox:** Modelová data 2025 → cíle 2030 (syntetické)
- **Leakage guard:** ✅ Oddělili jsme targets od features

## Slide 3 — AI Model: Proč je to OPRAVDU AI ⭐
**Čísla z `python src/train_demand.py`:**
- **Model:** LightGBM (gradient boosted trees)
- **Predikce:** EV count / den v zóně (2030)
- **Baseline:** "Poptávka ∝ populace" (triviální pravidlo)
- **MAE na validaci:** 4.7 EV/den (vs 29.5 u baseline)
- **Precision@50:** 0.84 → top 50 zón správně identifikované
- **Výhodnost:** Model najde neočekávané zóny (nízká populace, ale vysoká poptávka díky logistice/hubům)

## Slide 4 — Výsledky a Live Demo
**Demo:** `streamlit run src/app.py`

1. **Mapa Prahy** — obarvená heatmapou poptávky
2. **Top 50 doporučení** — zóna + typ stanice + počet portů
3. **Submission:** 517 zón s predikcí + doporučením typu

**Výstup:** CSV pro plánování stavby (koordinátoři).

## Slide 5 — Byznys Model
- **Zákazník:** Magistrát / MČ / operátor
- **Cena:** 30–200 k Kč/měsíc (dle scope)
- **Hodnota:** Zabrání 300 MIL Kč marnotratné investice
- **ROI:** 750x za rok
- **Model:** SaaS (opakovaný příjem)

| Zákazník | Zaplatí | Ušetří/dosáhne |
|----------|---------|---|
| Magistrát | 30k/měs | 270M/rok |
| Operátor ICT | 50k/měs | tracking, optimalizace |
| Distributor | 200k/měs | síťový planning |

## Slide 6 — Konkurence & Diferenciátor
- **Jaká řešení existují?** GIS toolkits (ArcGIS), consulting (Deloitte), energie-first optimizers (neví o mobilitě)
- **Náš svým:** Tradiční nástrojů se ptají "co si přejeme?". My se ptáme "co ML vidí v datech?"
- **Tvrdost:** Tréned na 2 400+ zónách, otestovaný na 500+ holdoutu.

## Slide 7 — Etika (zabudovaná)
1. **Leakage:** Anti-leakage guard v kódu — targets se nedostanou do features ✅
2. **Cold-start:** Zvýšená nejistota pro řídké zóny → lámeme spirálu zanedbaných čtvrtí
3. **Soukromí:** Jen agregáty na úrovni zóny (NOT jednotlivci)
4. **Interpretace:** Když model chybuje → člověk v rozhodnutí (ne black-box)

## Slide 8 — Shrnutí
**One-liner:** *VoltPlán — AI pro optimální rozmístění EV stanic v Praze. Zkrátíme dobu rozhodování, zabráníme plýtvání.*

**Výstupy k odevzdání:**
- Pitch deck (PDF)
- Technické shrnutí (1 A4)
- Submission CSV (517 zón)
- GitHub repo + live demo

---
**Q&A:** Proč LightGBM a ne neural network? · Jak řešíš chybějící data? · Jak se to škáluje na jiné město?
