"""Draw the palette sheet: python examples/swatches.py [outfile]"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import roygbviz as rv

out = sys.argv[1] if len(sys.argv) > 1 else "assets/palette.png"
W, H = 12.0, 12.6
fig = plt.figure(figsize=(W, H), facecolor="#FAF6EF")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
font = {"family": rv.mpl.pick_font()}
serif = {"family": rv.config.pick_serif()}
ink, soft = "#1B2A41", "#756F61"
ax.text(0.5, 0.5, "Roygbviz palette", fontsize=22, weight="bold", color=ink, va="center", **serif)
ax.text(0.5, 0.95, "Twelve colours from one rainbow (nine models, three stages), five lightness levels each, in light and dark.",
        fontsize=10, color=soft, va="center", **font)


def block(y, mode):
    p = rv.get_palette(mode)
    n = p.neutrals
    ax.add_patch(Rectangle((0.3, y), W - 0.6, 5.05, color=n["bg"], lw=0))
    ax.add_patch(Rectangle((0.3, y), W - 0.6, 5.05, fill=False, ec="#D9D1BF", lw=0.8))
    ax.text(0.6, y + 0.35, f"{mode.title()} mode", fontsize=12, weight="bold", color=n["text"], va="center", **serif)
    cols = [("STT", p.groups["STT"])] + [(r, p.roles[r]) for r in ("red", "orange", "yellow")] \
        + [("TTS", p.groups["TTS"])] + [(r, p.roles[r]) for r in ("green", "teal", "blue")] \
        + [("LLM", p.groups["LLM"])] + [(r, p.roles[r]) for r in ("indigo", "violet", "pink")]
    for i, (r, base) in enumerate(cols):
        x = 0.6 + i * 0.9
        stage = r in ("STT", "LLM", "TTS")
        ax.text(x, y + 0.85, r.upper() if stage else r.title(), fontsize=8, weight="bold" if stage else "normal",
                color=n["text"] if stage else n["muted"], va="center", **font)
        for k, hx in enumerate(p.levels(r, 5)):
            ax.add_patch(Rectangle((x, y + 1.05 + k * 0.42), 0.82, 0.38, color=hx, lw=0))
        ax.text(x, y + 3.25, base, fontsize=6, color=n["muted"], va="center", **font)
    ax.text(0.6, y + 3.65, "Ramps", fontsize=8, color=n["muted"], va="center", **font)
    for j, (name, cols) in enumerate((("blue", p.sequential("blue", 12)), ("violet", p.sequential("violet", 12)),
                                      ("spectrum", p.sequential("spectrum", 12)), ("diverging", p.diverging(12)))):
        for k, hx in enumerate(cols):
            ax.add_patch(Rectangle((0.6 + j * 2.65 + k * 0.2, y + 3.85), 0.2, 0.4, color=hx, lw=0))
        ax.text(0.6 + j * 2.65, y + 4.4, name, fontsize=7.5, color=n["muted"], va="center", **font)
    for k, key in enumerate(("bg", "grid", "rule", "muted", "text_2", "text")):
        ax.add_patch(Rectangle((0.6 + k * 1.25, y + 4.6), 1.15, 0.3, color=n[key], ec="#D9D1BF", lw=0.5))
        ax.text(0.6 + k * 1.25 + 0.05, y + 4.75, key, fontsize=6.5, va="center",
                color=n["text"] if key in ("bg", "grid") else n["bg"], **font)


block(1.35, "light")
block(6.75, "dark")
ax.text(0.5, 12.25, "Hand-out order: " + ", ".join(rv.palettes._SERIES_ORDER), fontsize=8,
        color=soft, va="center", **font)
fig.savefig(out, dpi=130, facecolor=fig.get_facecolor())
print("wrote", out)
