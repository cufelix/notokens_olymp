# VoltPlán — pitch deck

Plně editovatelný `.pptx` generovaný z kódu (PptxGenJS, stejný workflow jako `~/projects/misa`).

## Generování
```bash
cd pitch-deck
NODE_PATH=~/projects/misa/node_modules node build.js   # → VoltPlan-pitch.pptx
```
(Závislosti `pptxgenjs`, `react`, `react-dom`, `sharp`, `react-icons` se berou z misa
`node_modules` přes `NODE_PATH`. Případně `npm i` lokálně.)

## Struktura (12 slidů, dle checklistu v `BRIEF.md`)
1. Titul · 2. Problém & zákazník · 3. Řešení · 4. Data · 5. Datová pipeline (scraping & sběr dat v čase) ·
6. AI model (jádro techniky) · 7. Výsledky & živé demo · 8. Byznys · 9. Náš úhel & světový trend ·
10. Etika (4 oblasti) · 11. Etika zabudovaná v produktu (mechanismy) · 12. Tým

> Pozn.: konektory na slide 5 (Golemio, ČHMÚ, PRE, ČSÚ, OSM…) a kadence scrapingu jsou
> ilustrativní návrh pipeline — sedí na reálné pražské zdroje, ale samotný scraper zatím neběží.

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
