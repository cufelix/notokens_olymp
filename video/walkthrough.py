#!/usr/bin/env python3
"""Drive the VoltPlán Streamlit app and record a clean walkthrough video.

Each scene is held for its narration's duration (+ buffer) so the VO lines up.
Emits video/timeline.json with per-scene start offsets for caption sync.
"""
import json, time, subprocess, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
URL = "http://localhost:8765/"
W, H = 1440, 900
BUFFER = 1.0          # extra seconds per scene after the line ends
LEAD = 0.6            # settle time after an action before VO "starts"

def dur(mp3):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(ROOT / mp3)]).decode().strip()
    return float(out)

scenes = json.load(open(ROOT / "narration.json"))["scenes"]

def scroll_to(page, text):
    page.evaluate("""(t) => {
      const els = [...document.querySelectorAll('h1,h2,h3,h4,p,div')];
      const el = els.find(e => e.textContent && e.textContent.trim().startsWith(t));
      if (el) el.scrollIntoView({behavior:'smooth', block:'center'});
    }""", text)

def click_tab(page, label):
    page.get_by_role("tab", name=label).click()
    page.wait_for_timeout(1500)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": W, "height": H},
        device_scale_factor=2,
        record_video_dir=str(ROOT / "raw"),
        record_video_size={"width": W, "height": H},
    )
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    # let the map + folium tiles paint
    page.wait_for_timeout(7000)
    try:
        page.get_by_role("tab", name="1 · Kde stavět (mapa)").wait_for(timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(1500)

    t0 = time.time()
    timeline = []
    for s in scenes:
        a = s["action"]
        if a == "intro":
            page.evaluate("window.scrollTo({top:0, behavior:'smooth'})")
        elif a == "map":
            scroll_to(page, "Heatmapy Prahy")
        elif a == "top":
            scroll_to(page, "TOP")
        elif a == "why":
            scroll_to(page, "Proč model")
        elif a == "budget":
            click_tab(page, "2 · Za kolik (rozpočet)")
            scroll_to(page, "Rozpočtový optimalizátor")
        elif a == "value":
            scroll_to(page, "Hodnota pro město")
        elif a == "model":
            click_tab(page, "3 · Jak to ví (model)")
            scroll_to(page, "Jak model funguje")
        elif a == "outro":
            scroll_to(page, "Rozložení suitability")

        page.wait_for_timeout(int(LEAD * 1000))
        start = time.time() - t0
        d = dur(f"vo_{s['id']}.mp3")
        timeline.append({"id": s["id"], "start": round(start, 2), "vo": round(d, 2)})
        page.wait_for_timeout(int((d + BUFFER) * 1000))

    total = time.time() - t0
    page.wait_for_timeout(500)
    ctx.close()
    browser.close()

video_file = sorted((ROOT / "raw").glob("*.webm"))[-1]
json.dump({"video": str(video_file), "total": round(total, 2), "scenes": timeline},
          open(ROOT / "timeline.json", "w"), indent=2, ensure_ascii=False)
print("VIDEO:", video_file)
print("TOTAL:", round(total, 2))
