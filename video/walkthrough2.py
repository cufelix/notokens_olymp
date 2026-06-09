#!/usr/bin/env python3
"""Silent, smooth feature tour of VoltPlán for a pitch-background loop.

Drives the real UI (sidebar layer toggles, tabs, in-map heatmap layers) with
gentle smooth scrolling. Emits video/timeline2.json (scene starts + labels).
"""
import json, time, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
URL = "http://localhost:8766/"
W, H = 1440, 900

# scene: (id, label, hold_seconds)
LABELS = {
    "intro":  "VoltPlán — skóruje celou Prahu: 2 895 zón, 22 obvodů",
    "heat":   "Hlavní heatmapa vhodnosti · zelená → červená",
    "layers": "Přepínatelné vrstvy: vhodnost / spotřeba 2030 / potřeba stanic",
    "grid":   "Vrstva rizika sítě — kde by síť novou zátěž neunesla",
    "need":   "Všechny potřebné stanice 2030, obarvené dle typu",
    "top":    "TOP doporučené lokality + typ, počet portů a výkon",
    "why":    "Vysvětlitelnost — proč model lokalitu vybral",
    "budget": "Rozpočtový optimalizátor — nejvíc pokrytí za daný rozpočet",
    "value":  "Hodnota pro město — zabráněná promrhaná investice",
    "model":  "Pod kapotou — LightGBM, anti-leakage, metriky",
    "ethics": "Etika, nejistota a rozložení suitability skóre",
}

def smooth_to(page, text, block="center"):
    page.evaluate("""([t,b]) => {
      const els=[...document.querySelectorAll('h1,h2,h3,h4,p,div,span,label')];
      const el=els.find(e=>e.textContent && e.textContent.trim().startsWith(t));
      if(el) el.scrollIntoView({behavior:'smooth', block:b});
    }""", [text, block])

def click_tab(page, name):
    page.get_by_role("tab", name=name).click()
    page.wait_for_timeout(1800)

def click_label(page, text):
    try:
        page.get_by_text(text, exact=False).first.click(timeout=4000)
        return True
    except Exception:
        return False

def try_map_layer(page, label):
    """Best-effort: switch the folium LayerControl radio inside the st_folium iframe."""
    try:
        for fr in page.frames:
            try:
                ctrl = fr.locator(".leaflet-control-layers")
                if ctrl.count() == 0:
                    continue
                ctrl.first.hover(timeout=1500)
                page.wait_for_timeout(500)
                lab = fr.get_by_text(label, exact=False)
                if lab.count() > 0:
                    lab.first.click(timeout=2000)
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": W, "height": H},
        device_scale_factor=2,
        record_video_dir=str(ROOT / "raw2"),
        record_video_size={"width": W, "height": H},
    )
    page = ctx.new_page()
    t_rec = time.time()   # recording is now active; anchor for trim offset
    page.goto(URL, wait_until="networkidle")
    page.add_style_tag(content="html{scroll-behavior:smooth;}")
    page.wait_for_timeout(7000)
    try:
        page.get_by_role("tab", name="1 · Kde stavět (mapa)").wait_for(timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(1500)

    t0 = time.time()
    tl = []
    def mark(scene_id):
        tl.append({"id": scene_id, "start": round(time.time() - t0, 2)})

    # 1 — intro / KPIs
    page.evaluate("window.scrollTo({top:0,behavior:'smooth'})")
    mark("intro"); page.wait_for_timeout(4200)

    # 2 — main heatmap
    smooth_to(page, "Heatmapy Prahy"); page.wait_for_timeout(1200)
    mark("heat"); page.wait_for_timeout(5200)

    # 3 — switch in-map heatmap layers (best effort)
    mark("layers")
    if try_map_layer(page, "spotřeb"):
        page.wait_for_timeout(3200)
    if try_map_layer(page, "potřeb"):
        page.wait_for_timeout(3200)
    try_map_layer(page, "vhodnost")
    page.wait_for_timeout(2600)

    # 4 — grid-risk layer toggle
    click_label(page, "Zvýraznit nízkou rezervu sítě")
    page.wait_for_timeout(2200)
    smooth_to(page, "Heatmapy Prahy"); page.wait_for_timeout(1000)
    mark("grid"); page.wait_for_timeout(4800)

    # 5 — all-needed-stations-by-type layer toggle (new feature; loads a few s)
    click_label(page, "Zobrazit VŠECHNY potřebné stanice 2030")
    page.wait_for_timeout(4000)
    smooth_to(page, "Heatmapy Prahy"); page.wait_for_timeout(1000)
    mark("need"); page.wait_for_timeout(5200)
    # turn both layers back off to declutter
    click_label(page, "Zobrazit VŠECHNY potřebné stanice 2030"); page.wait_for_timeout(1500)
    click_label(page, "Zvýraznit nízkou rezervu sítě"); page.wait_for_timeout(1800)

    # 6 — TOP recommendations table
    smooth_to(page, "TOP"); page.wait_for_timeout(1000)
    mark("top"); page.wait_for_timeout(5200)

    # 7 — why / explainability
    smooth_to(page, "Proč model"); page.wait_for_timeout(1000)
    mark("why"); page.wait_for_timeout(5000)

    # 8 — budget optimizer
    click_tab(page, "2 · Za kolik (rozpočet)")
    smooth_to(page, "Rozpočtový optimalizátor"); page.wait_for_timeout(1000)
    mark("budget"); page.wait_for_timeout(5200)

    # 9 — value for city
    smooth_to(page, "Hodnota pro město"); page.wait_for_timeout(1000)
    mark("value"); page.wait_for_timeout(5000)

    # 10 — model tab
    click_tab(page, "3 · Jak to ví (model)")
    smooth_to(page, "Jak model funguje"); page.wait_for_timeout(1000)
    mark("model"); page.wait_for_timeout(5200)

    # 11 — ethics + distribution
    smooth_to(page, "Etika"); page.wait_for_timeout(1000)
    mark("ethics"); page.wait_for_timeout(5000)
    smooth_to(page, "Rozložení suitability"); page.wait_for_timeout(3500)

    total = time.time() - t0
    page.wait_for_timeout(500)
    ctx.close()
    browser.close()

video_file = sorted((ROOT / "raw2").glob("*.webm"))[-1]
out = {"video": str(video_file), "total": round(total, 2),
       "offset": round(t0 - t_rec, 2),
       "labels": LABELS, "scenes": tl}
json.dump(out, open(ROOT / "timeline2.json", "w"), indent=2, ensure_ascii=False)
print("VIDEO:", video_file)
print("TOTAL:", round(total, 2))
print("SCENES:", [s["id"] for s in tl])
