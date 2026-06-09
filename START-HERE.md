# START HERE — kickoff prompt pro Claude Code (hackathon)

Repo: **https://github.com/cufelix/notokens_olymp** · tým **notokens** · zadání **AIO_PHA-02-PHA**.

## Jak to použít
1. Naklonuj repo a otevři Claude Code v té složce: `claude` (CLAUDE.md se načte sám).
2. **Zkopíruj prompt níž** a vlož ho jako první zprávu. Uprav jen `[MOJE TRAŤ]`.
3. Pokud používáš HF nástroje, nastav `export HF_TOKEN=hf_xxx` (viz `SETUP.md`).

## Co je v repu (rychlý přehled)
- **`APP-SPEC.md`** — ⭐ ŘÍDÍCÍ PLÁN: produkt (B2G app „kde mají dobíječky smysl"), featury, AI kontrakt, build order.
- `BRIEF.md` (co hodnotí porota) · `TEAMFLOW.md` (kontrakty + git) · `DATA-MAP.md` · `HARDWARE.md` · `SETUP.md` · `zadani/`.
- `src/` — `profile_data.py`, `train_demand.py`, `match.py`, `app.py`. *(starší V2G/CONCEPT-VoltPlan = explorace, neřídí.)*
- **Core data JSOU v repu:** `data/core-dataset.zip` → rozbal `unzip data/core-dataset.zip -d data/participants/`.

---

## ⬇️ PASTE-READY PROMPT (zkopíruj celé)

```
Jsme na hackathonu České AI Olympiáda 2026 (tým notokens, krajské Praha, zadání
AIO_PHA-02-PHA). Máme ~2 hodiny a 3 lidi. Repo: github.com/cufelix/notokens_olymp.
Vybraný produkt: VoltPlán = B2G aplikace, která městu vyhodnotí, KDE má smysl stavět
dobíječky (AI suitability scoring zón z datasetu), roční licence. Já jsem na trati:
[MOJE TRAŤ: 🅐 MODEL / 🅑 APP / 🅒 PITCH].

KROK 1 — zorientuj se a synchronizuj se mnou. Přečti `APP-SPEC.md` (řídící!), `BRIEF.md`,
`DATA-MAP.md`, `TEAMFLOW.md`. Pak mi v 5 bodech řekni: (1) co je produkt, (2) co AI dělá
(suitability skóre per zóna), (3) na čem mám na mojí trati makat teď podle „Build order",
(4) jaký kontrakt dodávám/dostávám (`submissions/app_zone_scores.csv`), (5) na co pozor.
Nezačínej kódit, dokud mi tohle neřekneš.

KROK 2 — setup + akce podle mojí tratě. Nejdřív rozbal data:
  `unzip data/core-dataset.zip -d data/participants/`
  `uv venv --python 3.11 && uv pip install -r requirements.txt`
Pak podle tratě (detail v APP-SPEC „Build order" a „Rozdělení"):
- 🅐 MODEL → `python src/profile_data.py`, pak rozšiř `train_demand.py`: LightGBM predikce
  poptávky → spočítej suitability_score (poptávka+grid_headroom+coverage_gap+equity) →
  zapiš `submissions/app_zone_scores.csv` (kontrakt). Dej mi MAE vs baseline + že skóre dává smysl.
- 🅑 APP → hned vytvoř MOCK `submissions/app_zone_scores.csv` (správné sloupce), pak `src/app.py`
  Streamlit: heatmapa skóre, filtr po obvodech, markery s popupem, žebříček TOP-N, export, live
  statistika (MVP featury 1–6). Až 🅐 dodá reál, swap. Pak screenshot + 30s záznam jako zálohu.
- 🅒 PITCH → business plan (roční licence, ROI pro město), pitch deck (problém→řešení→zákazník
  B2G→byznys→etika), pozicování vs EVpin/StreetLight (viz APP-SPEC research). Čísla od 🅐 na konci.

PRAVIDLA (drž se jich striktně):
- Řídí se `APP-SPEC.md`. JEDEN problém = umístění dobíječek. Nestav V2G/dynamic-pricing (to byla explorace).
- Anti-leakage: `target_*_2030_synthetic` ani sloupce z nich odvozené NIKDY jako featura.
- Sandbox, ne soutěž: validuj `zones_validation` / vlastním holdoutem, žádné odevzdání predikcí.
- Velká CSV (hourly = 2,29 M řádků, 261 MB): polars/duckdb lazy, nečíst celé do kontextu.
- Trénink na CPU (LightGBM). Rychlost > dokonalost, ale drž baseline a měř (porota chce „opravdová AI ne pravidlo").
- Kontrakt model↔app = `submissions/app_zone_scores.csv` — domluvte sloupce HNED, 🅑 jede na mocku.
- Git dle `TEAMFLOW.md`: vlastní branch (`feat/model|app|pitch`), PR po zelené CI, NIKDY přímo na main.
- Čísla v byznysu musí být obhajitelná (porota = energetik z PRE) — žádné ROI 750x ani 240 kWh/auto.

Začni KROKEM 1.
```

---

## Varianty podle tratě (co dáš do `[MOJE TRAŤ]`)
- **🅐 ML** → predikce (`train_demand.py`) → číslo vs baseline → pak V2G heuristika (`v2g.py`).
- **🅑 demo** → `src/app.py` Streamlit (mapa + časový graf řízené nabíjení/V2G) + screenshot/záznam jako záloha.
- **🅒 pitch** → `pitch/DECK.md` do Gammy, doplň čísla od 🅐, najdi 1 zahraniční V2G trend pro Prahu, 1 A4.
