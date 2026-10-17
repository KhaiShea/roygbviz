"""Small example figures for the README, in light and dark. python examples/readme_figs.py [outdir]"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from plotnine import *  # noqa: F401,F403
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.argv = [sys.argv[0], "/tmp/_mega_unused"]  # mega.py reads argv for its own output folder
import mega  # noqa: E402
import roygbviz as rv  # noqa: E402

out = Path(__file__).resolve().parent.parent / "assets" / "examples"
out.mkdir(parents=True, exist_ok=True)
W, H, DPI = 5.6, 3.5, 160


def levels_fig():
    names = ["STT", "teal", "violet"]
    d = pd.DataFrame([(n, k, 1) for n in names for k in range(5)], columns=["colour", "level", "v"])
    d["colour"] = pd.Categorical(d["colour"], names[::-1])
    d["cell"] = d["colour"].astype(str) + d["level"].astype(str)
    cols = {f"{n}{k}": c for n in names for k, c in enumerate(rv.levels(n, 5))}
    return (ggplot(d, aes("level", "colour", fill="cell")) + geom_tile(colour=mega.S["N"]["bg"], size=3)
            + scale_fill_manual(values=cols) + mega.noleg()
            + scale_x_continuous(breaks=range(5), labels=["deep", "", "default", "", "soft"], expand=(0, 0))
            + theme(panel_grid_major=element_blank(), axis_ticks=element_blank())
            + labs(title="Levels", subtitle="Five steps per colour, default in the middle", x="", y=""))


def div_fig():
    rng = np.random.default_rng(5)
    a = rng.normal(0, 1, (6, 6)); m = np.clip(np.round((a + a.T) / 2, 1), -1, 1); np.fill_diagonal(m, 1)
    names = ["Whisper", "Parakeet", "Kokoro", "Piper", "Llama", "Qwen"]
    d = pd.DataFrame([(names[i], names[j], m[i, j]) for i in range(6) for j in range(6)], columns=["x", "y", "v"])
    d["x"] = pd.Categorical(d["x"], names); d["y"] = pd.Categorical(d["y"], names[::-1])
    return (ggplot(d, aes("x", "y", fill="v")) + geom_tile(colour=mega.S["N"]["bg"], size=2)
            + rv.scale_fill_roygbviz_div(limits=(-1, 1)) + theme(panel_grid_major=element_blank(), axis_text_x=element_text(rotation=35, ha="right"))
            + labs(title="Diverging", subtitle="Cold (TTS colour), white, hot (STT colour)", x="", y="", fill=""))


FIGS = {
    "quickstart": mega.line, "stages": mega.stacked, "levels": levels_fig, "diverging": div_fig,
    "shading": mega.st_density, "boxes": mega.st_box,
}

for mode in ("light", "dark", "cream"):
    mega.S["P"] = rv.use(mode); mega.S["N"] = mega.S["P"].neutrals
    for name, fn in FIGS.items():
        fn().save(out / f"{name}_{mode}.png", width=W, height=H, dpi=DPI, verbose=False)
    # sizes: two base sizes side by side
    ims = []
    for bs in (9, 14):
        rv.use(mode, base_size=bs)
        g = mega._base(f"Base size {bs}", "Text and strokes scale together", base_size=bs)
        f = out / f"_s{bs}.png"; g.save(f, width=W / 1.3, height=H / 1.3, dpi=DPI, verbose=False); ims.append(Image.open(f))
        f.unlink()
    sheet = Image.new("RGB", (ims[0].width + ims[1].width, max(i.height for i in ims)), mega.S["N"]["bg"])
    sheet.paste(ims[0], (0, 0)); sheet.paste(ims[1], (ims[0].width, 0)); sheet.save(out / f"sizes_{mode}.png")
    rv.use(mode)
print("done")
