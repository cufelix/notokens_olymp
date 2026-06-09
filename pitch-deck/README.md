# VoltPlán — pitch deck

Plně editovatelný `.pptx` generovaný z kódu (PptxGenJS, stejný workflow jako `~/projects/misa`).

## Generování
```bash
cd pitch-deck
NODE_PATH=~/projects/misa/node_modules node build.js   # → VoltPlan-pitch.pptx
```
(Závislosti `pptxgenjs`, `react`, `react-dom`, `sharp`, `react-icons` se berou z misa
`node_modules` přes `NODE_PATH`. Případně `npm i` lokálně.)

## Struktura (10 slidů, dle checklistu v `BRIEF.md`)
1. Titul · 2. Problém & zákazník · 3. Řešení · 4. Data · 5. AI model (jádro techniky) ·
6. Výsledky & živé demo · 7. Byznys · 8. Náš úhel & světový trend · 9. Etika · 10. Tým

## Čísla v decku = reálné výstupy modelu
Pochází z `src/train_demand.py` + `src/generate_scores.py` (stav 2026-06-09):
- LightGBM, 60 anti-leakage featur, trénink 2 378 zón / holdout 517 zón
- MAE o 17 % nižší než populační baseline; P@50 = 0,84; recommender typu 83,8 %
- Top lokace TS_3820 (Praha 13), suitability 91,1 / 100
Po přetrénování modelu čísla v `build.js` zkontroluj/aktualizuj.

## TODO až bude demo hotové (branding + screenshoty)
- **Slide 6** — nahradit placeholder `[ SCREENSHOT ŽIVÉHO DEMA ]` reálným screenshotem
  appky (mapa + popup). Vlož přes `s.addImage({ path: "assets/demo.png", ... })`.
- **Slide 10** — doplnit jména členů týmu k rolím.
- **Byznys (slide 7)** — částky licence/ROI jsou zatím ilustrativní; doplnit konkrétní
  čísla, až je tým odsouhlasí.
- Případně doladit paletu/logo (branding) dle finálního vzhledu appky.
