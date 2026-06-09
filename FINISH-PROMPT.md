# FINISH PROMPT — pro druhého Clauda (dotáhnout do finále)

> Zkopíruj blok níž druhému Claudovi v repu `notokens_olymp`. On dotáhne, vyladí design,
> ověří že to FAKT běží a model je reálný, a připraví na odevzdání.

```
Jsme na hackathonu (Česká AI Olympiáda 2026, tým notokens, zadání AIO_PHA-02-PHA).
Repo github.com/cufelix/notokens_olymp. Zbývá ~1–2 h. Tvůj úkol: DOTÁHNOUT řešení
do finále — ne přestavět, ale dokončit, ověřit a vyleštit. Pracuj na branchi
`feat/finish`, commituj malé a často, PR na main po zelené CI.

PRODUKT (řídí `APP-SPEC.md`): VoltPlán = B2G aplikace, která městu vyhodnotí, KDE mají
dobíječky smysl — AI skóruje zóny Prahy (suitability = poptávka + kapacita sítě + mezera
v pokrytí + férovost). Zákazník = Magistrát/MČ, roční licence.

STAV: kolega (Felix) postavil hodně lokálně a pushnul to: src/app.py, src/app_complete.py,
src/app_premium.py (enterprise dashboard), src/generate_submission.py, natrénovaný model
submissions/lgbm_model.pkl. Na to navazuješ.

KROK 1 — ZORIENTUJ SE A NIC NEROZBIJ. Přečti `APP-SPEC.md`, `BRIEF.md`, `TEAMFLOW.md`.
Projdi všechny 3 appky (app.py, app_complete.py, app_premium.py) a `generate_submission.py`,
`train_demand.py`. Pak mi řekni: (a) která appka je nejdál a má jít do dema, (b) co reálně
běží vs co je rozbité/placeholder, (c) tvůj plán dotažení. Nezačínej měnit, dokud to neřekneš.

KROK 2 — OVĚŘ, ŽE TO FAKT FUNGUJE (priorita č.1, tady se vyhrává/prohrává):
- Rozbal data: `unzip data/core-dataset.zip -d data/participants/`, prostředí `uv pip install -r requirements.txt`
  (chybí-li balík jako streamlit-folium/plotly/folium, doinstaluj).
- Spusť trénink i scoring end-to-end. Ověř, že MODEL JE REÁLNÝ:
  * že lgbm_model.pkl je fakt natrénovaný z dat (ne prázdný/dummy),
  * že předpovědi vychází z modelu, ne z natvrdo zadaných čísel,
  * ANTI-LEAKAGE: `target_*_2030_synthetic` ani sloupce z nich odvozené NESMÍ být featura. Zkontroluj featury.
  * Změř kvalitu: MAE/RMSE vs baseline (průměr + ∝ populace) + Precision@50 → musí PŘEKONAT baseline.
- Spusť vybranou appku (`streamlit run src/app_premium.py`) a proklikej: načte data? mapa/heatmapa
  jede? filtr po obvodech? popupy? export? Čísla v UI MUSÍ sedět s výstupem modelu (ne fake).
- Oprav, co je rozbité. Když něco nesedí nebo je dummy, NAHLAS mi to a oprav na reálné.

KROK 3 — DESIGN (udělej to fakt hezké, porota to vidí). Načti a řiď se design skilly z
map-scraper (jsou napsané dobře, použij je):
  ~/projects/map-scraper/.ai/skills/frontend-design.md
  ~/projects/map-scraper/.ai/skills/impeccable-color.md
  ~/projects/map-scraper/.ai/skills/impeccable-typography.md
  ~/projects/map-scraper/.ai/skills/impeccable-spatial.md
  ~/projects/map-scraper/.ai/skills/design-motion-principles.md
  ~/projects/map-scraper/.ai/skills/taste-minimalist.md
  a skill `design-review` (~/projects/map-scraper/.claude/skills/design-review) pusť na výsledek.
Cíl: čistý, profesionální, důvěryhodný dashboard pro městského úředníka (ne „AI hračka").
Konzistentní paleta, typografie, mezery; jasná hierarchie; čitelná mapa; smysluplné KPI.
Po úpravě udělej screenshot. CHYBÍ-li ti nějaká schopnost/skill, použij `find-skills`
(globální skill) a najdi/doinstaluj vhodný — nečekej na mě.

KROK 4 — FINALIZACE:
- Jedna appka jako finální demo (ostatní nech, ale README/APP-SPEC ať říká, která to je).
- Smaž junk: `.~lock.*.md#` (LibreOffice zámky) + přidej `*.~lock.*#` do `.gitignore`.
- `generate_submission.py` cílí na „513 test zón / sample_submission" = STARÁ logika (sandbox
  nemá test set). Přepiš na scoring všech zón / validaci, nebo aspoň přejmenuj, ať to neplete.
- Ověř, že byznys čísla (licence, ROI) jsou OBHAJITELNÁ — žádné ROI 750x, žádné 240 kWh z auta.
  Porota = energetik z PRE. Nereálná čísla sraž na střízlivá.
- Před PR: codex review `codex exec --sandbox read-only "zkontroluj anti-leakage v train_demand.py
  a generate_submission.py a že predikce vychází z modelu"` → reportuj mi VŠECHNY nálezy.
- Screenshot + 30s záznam dema jako záloha (kdyby na pódiu spadlo).

PRAVIDLA: polars/duckdb lazy na hourly_* (261 MB), CPU trénink, drž baseline a měř. Sandbox =
vlastní validace, ne odevzdání predikcí. Git: feat/finish branch, PR po zelené CI, ne přímo na main.

Začni KROKEM 1.
```
