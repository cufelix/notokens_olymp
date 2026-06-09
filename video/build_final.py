#!/usr/bin/env python3
"""Assemble the cinematic VoltPlán walkthrough:
   trimmed app capture on a dark matte + PNG brand bar + lower-third labels
   + fades + VO synced to the recorded timeline.  (No drawtext: this ffmpeg
   lacks libfreetype, so text is rendered to transparent PNGs via Pillow.)
"""
import json, subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
TL = json.load(open(ROOT / "timeline.json"))
RAW = pathlib.Path(TL["video"])
TOTAL = TL["total"]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

rawdur = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "csv=p=0", str(RAW)]).decode().strip())
OFFSET = max(0.0, rawdur - TOTAL)
last = TL["scenes"][-1]
END = last["start"] + last["vo"] + 1.2

FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"

LABELS = {
    "intro": "VoltPlán — rozhodovací nástroj pro Magistrát HMP",
    "map":   "Suitability heatmapa · 513 zón Prahy",
    "top":   "TOP doporučené lokality + typ a výkon",
    "why":   "Vysvětlitelnost — proč model lokalitu vybral",
    "budget": "Rozpočtový optimalizátor",
    "value": "Hodnota pro město — zabráněná promrhaná investice",
    "model": "Pod kapotou — AI, anti-leakage, etika",
    "outro": "Z dat na rozhodnutí, kterému město věří",
}

# ---- brand bar (always on) ----
brand = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
d = ImageDraw.Draw(brand)
d.text((160, 8), "VoltPlán", font=ImageFont.truetype(FB, 30), fill=(237, 234, 227, 255))
d.text((318, 14), "Česká AI Olympiáda 2026 · AIO_PHA-02-PHA",
       font=ImageFont.truetype(FR, 20), fill=(143, 185, 172, 255))
brand.save(ASSETS / "brand.png")

# ---- per-scene lower-thirds ----
def make_lt(text, path):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    # rounded translucent bar bottom-left
    dr.rounded_rectangle([160, 980, 1760, 1040], radius=10, fill=(10, 21, 18, 205))
    dr.rectangle([160, 980, 166, 1040], fill=(31, 111, 92, 255))  # accent edge
    dr.text((192, 994), text, font=ImageFont.truetype(FB, 28), fill=(255, 255, 255, 255))
    img.save(path)

for s in TL["scenes"]:
    make_lt(LABELS[s["id"]], ASSETS / f"lt_{s['id']}.png")

# ---- ffmpeg inputs ----
inputs = ["-i", str(RAW), "-i", str(ASSETS / "brand.png")]
idx = 2
lt_idx = {}
for s in TL["scenes"]:
    inputs += ["-i", str(ASSETS / f"lt_{s['id']}.png")]
    lt_idx[s["id"]] = idx
    idx += 1
vo_start = idx
for s in TL["scenes"]:
    inputs += ["-i", str(ROOT / f"vo_{s['id']}.mp3")]
    idx += 1

# ---- video graph ----
g = (
    f"color=c=0x0E1A16:s=1920x1080:d={END:.2f}[bg];"
    f"[0:v]trim=start={OFFSET:.3f},setpts=PTS-STARTPTS,scale=1600:1000,fps=30[app];"
    "[bg][app]overlay=160:34[mt];"
    "[mt]drawbox=x=158:y=32:w=1604:h=1004:color=0x1F6F5C@0.85:t=3[v0];"
    "[v0][1:v]overlay=0:0[vb];"
)
prev = "vb"
for i, s in enumerate(TL["scenes"]):
    a = s["start"]
    b = s["start"] + s["vo"] + 0.8
    out = f"vl{i}"
    g += (f"[{prev}][{lt_idx[s['id']]}:v]overlay=0:0:"
          f"enable='between(t,{a:.2f},{b:.2f})'[{out}];")
    prev = out
g += f"[{prev}]fade=t=in:st=0:d=0.8,fade=t=out:st={END-1.0:.2f}:d=1.0[vout];"

# ---- audio graph ----
ap = []
for j, s in enumerate(TL["scenes"]):
    ii = vo_start + j
    delay = int(s["start"] * 1000)
    ap.append(f"[{ii}:a]adelay={delay}|{delay}[a{j}]")
g += ";".join(ap) + ";"
g += "".join(f"[a{j}]" for j in range(len(TL["scenes"])))
g += (f"amix=inputs={len(TL['scenes'])}:normalize=0,"
      f"apad,atrim=0:{END:.2f},aresample=44100[aout]")

cmd = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", g,
    "-map", "[vout]", "-map", "[aout]", "-t", f"{END:.2f}",
    "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-preset", "medium",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
    str(ROOT / "VoltPlan-demo.mp4"),
]
print(f"OFFSET={OFFSET:.2f} END={END:.2f}")
subprocess.run(cmd, check=True)
print("DONE -> video/VoltPlan-demo.mp4")
