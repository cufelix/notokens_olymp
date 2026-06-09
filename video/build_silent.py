#!/usr/bin/env python3
"""Build the silent, smooth, loop-friendly pitch-background video from
   the timeline2 recording: dark matte + brand bar + persistent lower-thirds.
   No audio. No fade-to-black (clean for looping)."""
import json, subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
TL = json.load(open(ROOT / "timeline2.json"))
RAW = pathlib.Path(TL["video"])
TOTAL = TL["total"]
LABELS = TL["labels"]
SCENES = TL["scenes"]
ASSETS = ROOT / "assets2"
ASSETS.mkdir(exist_ok=True)

# prefer the measured pre-roll (webm has trailing padding that inflates duration)
OFFSET = TL.get("offset")
if OFFSET is None:
    rawdur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(RAW)]).decode().strip())
    OFFSET = max(0.0, rawdur - TOTAL)
END = TOTAL

FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"

# brand bar (always on)
brand = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
d = ImageDraw.Draw(brand)
d.text((160, 8), "VoltPlán", font=ImageFont.truetype(FB, 30), fill=(237, 234, 227, 255))
d.text((318, 14), "Česká AI Olympiáda 2026 · AIO_PHA-02-PHA · plánování EV infrastruktury",
       font=ImageFont.truetype(FR, 20), fill=(143, 185, 172, 255))
brand.save(ASSETS / "brand.png")

def make_lt(text, path):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB, 28)
    w = dr.textlength(text, font=f)
    dr.rounded_rectangle([160, 980, 220 + w, 1040], radius=10, fill=(10, 21, 18, 210))
    dr.rectangle([160, 980, 166, 1040], fill=(31, 111, 92, 255))
    dr.text((192, 994), text, font=f, fill=(255, 255, 255, 255))
    img.save(path)

for s in SCENES:
    make_lt(LABELS[s["id"]], ASSETS / f"lt_{s['id']}.png")

# scene windows: start[i] .. start[i+1] (last -> END)
wins = []
for i, s in enumerate(SCENES):
    a = s["start"]
    b = SCENES[i + 1]["start"] if i + 1 < len(SCENES) else END
    wins.append((s["id"], a, b))

inputs = ["-i", str(RAW), "-i", str(ASSETS / "brand.png")]
idx = 2
lt_idx = {}
for s in SCENES:
    inputs += ["-i", str(ASSETS / f"lt_{s['id']}.png")]
    lt_idx[s["id"]] = idx
    idx += 1

g = (
    f"color=c=0x0E1A16:s=1920x1080:d={END:.2f}[bg];"
    f"[0:v]trim=start={OFFSET:.3f},setpts=PTS-STARTPTS,scale=1600:1000,fps=30[app];"
    "[bg][app]overlay=160:34[mt];"
    "[mt]drawbox=x=158:y=32:w=1604:h=1004:color=0x1F6F5C@0.85:t=3[v0];"
    "[v0][1:v]overlay=0:0[vb];"
)
prev = "vb"
for i, (sid, a, b) in enumerate(wins):
    out = f"vl{i}"
    g += (f"[{prev}][{lt_idx[sid]}:v]overlay=0:0:"
          f"enable='between(t,{a:.2f},{b:.2f})'[{out}];")
    prev = out
# tiny fade-in only on very first frames (no fade-out -> clean loop)
g += f"[{prev}]fade=t=in:st=0:d=0.5[vout]"

cmd = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", g,
    "-map", "[vout]", "-an", "-t", f"{END:.2f}",
    "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-preset", "medium",
    "-r", "30", "-movflags", "+faststart",
    str(ROOT / "VoltPlan-pitch-loop.mp4"),
]
print(f"OFFSET={OFFSET:.2f} END={END:.2f} scenes={len(SCENES)}")
subprocess.run(cmd, check=True)
print("DONE -> video/VoltPlan-pitch-loop.mp4")
