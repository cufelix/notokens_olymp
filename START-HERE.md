# START HERE — kickoff prompt pro Claude Code (hackathon)

Repo: **https://github.com/cufelix/notokens_olymp** · tým **notokens** · zadání **AIO_PHA-02-PHA**.

## Jak to použít
1. Naklonuj repo a otevři Claude Code v té složce: `claude` (CLAUDE.md se načte sám).
2. **Zkopíruj prompt níž** a vlož ho jako první zprávu. Uprav jen `[MOJE TRAŤ]`.
3. Pokud používáš HF nástroje, nastav `export HF_TOKEN=hf_xxx` (viz `SETUP.md`).

## Co je v repu (rychlý přehled)
- **`HACKATHON-PLAN.md`** — řídící 4h plán, 3 tratě (🅐 ML / 🅑 demo / 🅒 pitch), hodina po hodině.
- **`TEAMFLOW.md`** — kontrakty mezi tratěmi + git/branch/merge postup (jak se to spojí).
- `BRIEF.md` (co hodnotí porota) · `CONCEPT-VoltPlan.md` (koncept V2G) · `DATA-MAP.md` · `HARDWARE.md` · `SETUP.md`.
- `src/` — `profile_data.py`, `train_demand.py`, `match.py`, `app.py`. `pitch/DECK.md` — 8 slidů. `zadani/` — zadání.
- **Core data JSOU v repu:** `data/core-dataset.zip` (42 MB) → rozbal `unzip data/core-dataset.zip -d data/participants/`.
  (Optional ~1,6 GB jen z Google Drive — viz `data/README.md`.)

---

## ⬇️ PASTE-READY PROMPT (zkopíruj celé)

```
Jsme na hackathonu České AI Olympiáda 2026 (tým notokens, krajské Praha, zadání
AIO_PHA-02-PHA). Máme 4 hodiny a 3 lidi. Pracuješ v tomhle repu
(github.com/cufelix/notokens_olymp). Já jsem na trati: [MOJE TRAŤ: 🅐 ML / 🅑 demo / 🅒 pitch].

KROK 1 — zorientuj se a synchronizuj se mnou. Přečti `HACKATHON-PLAN.md`, `BRIEF.md`,
`CONCEPT-VoltPlan.md`, `DATA-MAP.md`, `HARDWARE.md`, `TEAMFLOW.md`. Pak mi v 5 bodech řekni:
(1) co je úkol, (2) naše cesta (Linie A: predikce → řízené nabíjení + V2G), (3) na čem mám
podle plánu na mojí trati makat teď, (4) co je kritická cesta týmu + jaký kontrakt dodávám/
dostávám (viz TEAMFLOW), (5) na co si dát pozor. Nezačínej kódit, dokud mi tohle neřekneš.

KROK 2 — setup + akce podle mojí tratě. Data UŽ JSOU v repu jako zip, nejdřív rozbal:
  `unzip data/core-dataset.zip -d data/participants/`  (→ data/participants/core/*.csv)
  `uv venv --python 3.11 && uv pip install -r requirements.txt`
Pak podle tratě:
- 🅐 ML → `python src/profile_data.py` (zkontroluj auto-detekci cílů + leakage, vypíše se),
  pak `python src/train_demand.py` → dej mi MAE vs baseline + P@50 a soubor
  `submissions/predictions_validation.csv` (kontrakt pro demo). Pak rozpracuj `src/v2g.py`
  (heuristika řízené nabíjení + V2G nad hourly_* — náš diferenciátor).
- 🅑 demo → `src/app.py` (mapa z `predictions_validation.csv` + časový graf zátěž/rezerva
  s/bez V2G). Dokud nemáš reálné predikce, jeď na mocku. Pak screenshot + 30s záznam jako zálohu.
- 🅒 pitch → `pitch/DECK.md` (8 slidů), doplň `[DOPLNIT]` čísly od 🅐, najdi 1 zahraniční V2G
  trend a obhaj Prahu (slide 6), 1 A4. Dokud nemáš čísla, jeď na placeholderech.

PRAVIDLA (drž se jich striktně):
- Řídí se `HACKATHON-PLAN.md`. Nestav nic mimo scope (žádné MILP, n8n se jen popisuje).
- Anti-leakage: `target_*_2030_synthetic` ani sloupce z nich odvozené NIKDY jako featura.
- Sandbox, ne soutěž: validuj `zones_validation` / vlastním holdoutem, žádné odevzdání predikcí.
- Velká CSV (hourly = 2,29 M řádků, 261 MB): polars/duckdb lazy, float32, nečíst celé do kontextu.
- Hardware: Intel Lunar Lake, žádná CUDA → trénink na CPU. NPU jen inference.
- Rychlost > dokonalost, ale vždy drž baseline a měř proti němu (porota to chce na slide 3).
- Git dle `TEAMFLOW.md`: vlastní feature branch (`feat/ml|demo|pitch`), commit malé a často,
  PR → main jakmile máš kus co ostatní potřebují, po zelené CI merge. NIKDY přímo na main.
- Před PR/odevzdáním: codex review (`codex exec --sandbox read-only`) na model + anti-leakage.
- Po prozkoumání dat doplň reálná čísla do `DATA-MAP.md` (paměť mezi sessions).

Začni KROKEM 1.
```

---

## Varianty podle tratě (co dáš do `[MOJE TRAŤ]`)
- **🅐 ML** → predikce (`train_demand.py`) → číslo vs baseline → pak V2G heuristika (`v2g.py`).
- **🅑 demo** → `src/app.py` Streamlit (mapa + časový graf řízené nabíjení/V2G) + screenshot/záznam jako záloha.
- **🅒 pitch** → `pitch/DECK.md` do Gammy, doplň čísla od 🅐, najdi 1 zahraniční V2G trend pro Prahu, 1 A4.
