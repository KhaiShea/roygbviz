"""Logo options for the README and the GitHub social preview. python examples/logo.py [outdir]

Writes SVG (text as paths, transparent) and PNG for light and dark, for three options:
  a: coloured wordmark   b: twelve dots + wordmark   c: rainbow bars + wordmark
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

import roygbviz as rv
from roygbviz.config import pick_serif

out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/logo")
out.mkdir(parents=True, exist_ok=True)
plt.rcParams["svg.fonttype"] = "path"

ROW = ["STT", "red", "orange", "yellow", "TTS", "green", "teal", "blue", "LLM", "indigo", "violet", "pink"]
LETTERS = ["red", "orange", "yellow", "green", "blue", "violet", "indigo", "pink"]  # r o y g b v i z


def canvas(w, h, n, bg):
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(bg)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    return fig, ax


def wordmark(ax, x, y, size, cols, ink, colour_all=True):
    """Draw 'roygbviz' letter by letter so each can have its own colour."""
    from matplotlib.textpath import TextPath
    from matplotlib.patches import PathPatch
    from matplotlib.transforms import Affine2D
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(family=pick_serif(), weight="bold")
    cx = x
    for ch, col in zip("roygbviz", cols):
        tp = TextPath((0, 0), ch, size=size, prop=fp)
        ax.add_patch(PathPatch(tp, transform=Affine2D().translate(cx, y) + ax.transData, fc=col if colour_all else ink, ec="none"))
        cx += tp.get_extents().width + size * 0.075
    return cx - x


def width_of(text, size):
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(family=pick_serif(), weight="bold")
    return sum(TextPath((0, 0), c, size=size, prop=fp).get_extents().width + size * .075 for c in text) - size * .075


def build(opt, mode, w=8, h=3.2, transparent=True):
    p = rv.use(mode); n = p.neutrals
    bg = "none" if transparent else n["bg"]
    fig, ax = canvas(w, h, 0, bg)
    col = lambda k: p.roles.get(k) or p.groups[k]
    ink = n["text"]
    if opt == "a":
        s = 1.35
        tw = width_of("roygbviz", s)
        wordmark(ax, (w - tw) / 2, h / 2 - .35, s, [col(k) for k in LETTERS], ink)
        ax.text(w / 2, .5, "a rainbow theme for plotnine", ha="center", va="center", color=n["text_2"], fontsize=13, family=rv.config.pick_font())
    elif opt == "b":
        r_big, r_small, gap = .21, .15, .52
        xs0 = (w - gap * 11) / 2
        for i, k in enumerate(ROW):
            ax.add_patch(Circle((xs0 + i * gap, h * .70), r_big if k in ("STT", "TTS", "LLM") else r_small, fc=col(k), ec="none"))
        s = .95
        tw = width_of("roygbviz", s)
        wordmark(ax, (w - tw) / 2, h * .22, s, [ink] * 8, ink, colour_all=False)
    elif opt == "c":
        heights = [.55, .8, 1.1, .9, 1.35, 1.0, 1.55, 1.2, 1.7, 1.4, 1.85, 1.6]
        bw, gap = .3, .09
        x0 = (w - (12 * bw + 11 * gap)) / 2
        for i, (k, hh) in enumerate(zip(ROW, heights)):
            ax.add_patch(FancyBboxPatch((x0 + i * (bw + gap), h * .56), bw, hh * .45, boxstyle="round,pad=0,rounding_size=.05", fc=rv.shade(k), ec=col(k), lw=1.6))
        s = .8
        tw = width_of("roygbviz", s)
        wordmark(ax, (w - tw) / 2, h * .2, s, [ink] * 8, ink, colour_all=False)
    return fig


if __name__ == "__main__":
    for opt in "b":
        for mode in ("light", "dark"):
            fig = build(opt, mode)
            fig.savefig(out / f"logo_{opt}_{mode}.svg", transparent=True)
            fig.savefig(out / f"logo_{opt}_{mode}.png", transparent=True, dpi=200)
            plt.close(fig)
            # social preview: 1280 x 640 with the page colour behind
            fig = build(opt, mode, w=8, h=4, transparent=False)
            fig.savefig(out / f"social_{opt}_{mode}.png", dpi=160, facecolor=fig.get_facecolor())
            plt.close(fig)
    print("done")
