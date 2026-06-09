# notokens — VoltPlán · Česká AI Olympiáda 2026 (AIO_PHA-02-PHA)

Tým **notokens**, krajské kolo Praha — AI Startup. Téma: **udržitelná mobilita a energetika**.
Stavíme **VoltPlán** (Linie A): predikce poptávky/zátěže → **řízené nabíjení + V2G** (auto jako
zdroj pro síť/čtvrť) → chytré umístění. Propojení mobility a energetiky = nejsilnější cesta.
Data jsou **sandbox** (ne soutěž o skóre) — validujeme vlastním holdoutem.

## Start (4 hodiny, 3 lidi)
1. Přečti **`HACKATHON-PLAN.md`** — řídící plán + rozdělení na 3 tratě (🅐 ML / 🅑 demo / 🅒 pitch).
2. Orientace: `BRIEF.md` (co hodnotí porota) → `CONCEPT-VoltPlan.md` (architektura) →
   `HARDWARE.md` (HW/trénink) → `DATA-MAP.md` (data) → `SETUP.md` (prostředí).
3. Až dorazí data → rozbal do `data/participants/` a:
   ```bash
   uv venv --python 3.11 && source .venv/bin/activate
   uv pip install -r requirements.txt
   python src/profile_data.py      # schéma + leakage guard
   python src/train_demand.py      # LightGBM + baseline + predikce na validaci
   streamlit run src/app.py        # demo (mapa + V2G časový graf)
   ```

## Struktura
- `src/` — `profile_data.py`, `train_demand.py` (Linie A), `match.py` (Linie B), `app.py` (demo)
- `pitch/DECK.md` — 8 slidů (text z VoltPlánu, `[DOPLNIT]` na čísla)
- `submissions/` — predikce ve formátu `sample_submission.csv`
- `zadani/` — zadání + meta-prompty · `data/` — **negitované** (1,85 GB, `.gitignore`)

> Hardware: Intel Core Ultra 7 258V (Lunar Lake), 32 GB, žádná CUDA → trénink na CPU
> (LightGBM/sklearn + sklearnex). Detaily `HARDWARE.md`.
