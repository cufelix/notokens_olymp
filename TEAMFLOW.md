# TEAMFLOW — jak na sebe matchnout ML + demo + pitch a jak commitovat

> 3 lidi, 4 hodiny, jeden cíl. Klíč: **tratě se propojují přes sdílené KONTRAKTY
> (soubor/číslo), ne přes „zeptej se mě".** Každý ví, co dodá a co dostane.

## 1 · Kontrakty mezi tratěmi (lepidlo)
| Od → Komu | Co přesně (kontrakt) |
|---|---|
| **🅐 ML → 🅑 demo** | soubor `submissions/predictions_validation.csv` se sloupci `grid_zone_id, pred_<cíl>, true_<cíl>`. Demo čte JEN tenhle soubor + `lat/lon` ze `zones_validation.csv`. Nezávisí na vnitřku modelu. *(už generuje `train_demand.py`)* |
| **🅐 ML → 🅒 pitch** | 3 čísla na slide 3: `MAE LightGBM`, `MAE baseline`, `% zlepšení` + `P@50`. V2G metrika na slide 4: „X zabráněných přetížení / Y kWh vráceno". To jsou ty `[DOPLNIT]` v `pitch/DECK.md`. |
| **🅑 demo → 🅒 pitch** | screenshot + 30s záznam mapy a V2G grafu → slide 4. |

→ Dokud kontrakt drží (názvy sloupců, formát souboru), může každý makat **nezávisle**.

## 2 · Branche — `main` je svatý
```
main  ←  feat/ml (train_demand, v2g.py)
      ←  feat/demo (app.py)
      ←  feat/pitch (pitch/)
```
- Každá trať = vlastní branch, sahá na **jiné soubory** → merge konflikty skoro nehrozí.
  **Dělte si soubory, ne řádky.**
- **Nikdy přímo na main** (kromě triviálního fixu). Vyhnete se přepsání práce.

## 3 · Kdy commitovat / pushovat / mergovat
- **Commit malé a často** — ~20–30 min, nebo když něco funguje. Malé commity = lehké revertování.
- **Push na svůj branch kdykoli** (záloha + viditelnost).
- **PR → main, jakmile máš funkční kus, co ostatní potřebují** (hlavně ML `predictions_validation.csv`).
  Po zelené CI **hned merge**. „Merge small, merge often."
- Po merge ostatní udělají `git checkout main && git pull`.

Flow na člověka:
```bash
git checkout -b feat/ml
git add -p && git commit -m "trénink: LightGBM + baseline"   # malé commity
git push -u origin feat/ml
gh pr create --base main --title "..."     # když to ostatní potřebují
gh pr merge --merge                        # po zelené CI
git checkout main && git pull              # ostatní stáhnou
```

## 4 · Sync body (krátký stand-up, ~1 min)
- **0:30** 🅐 má číslo vs baseline (de-risk) → pošle čísla 🅒, predikce 🅑.
- **2:00** 🅑 demo běží na REÁLNÝCH predikcích (ne mock).
- **3:15** **dry-run celého pitche s živým demem** — tady se odhalí nesoulad, zbývá 30 min na opravu.
- **3:45** odevzdání.

## 5 · Integrátor (důležité)
Jeden člověk (ideálně 🅑 — demo konzumuje výstupy obou) je **integrátor**: po každém merge stáhne
main a ověří, že čísla v decku == výstup modelu == co ukazuje demo. **Integrace je něčí úkol,
ne „samo se to spojí".**

## 6 · Tři pravidla, co vás zachrání
1. **Kontrakt drží i když model ne** — domluvte názvy sloupců `predictions_validation.csv` HNED na začátku.
2. **Mock než přijde reál** — 🅑 i 🅒 můžou jet na vymyšlených číslech/predikcích, dokud 🅐 nedodá; pak swapnou.
3. **3:15 dry-run je posvátný** — radši horší řešení odprezentované sladěně než skvělé v chaosu.
