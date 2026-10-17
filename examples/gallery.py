"""Render the Roygbviz gallery: python examples/gallery.py [outdir]

All data is synthetic. Model names are placeholders for a cascaded speech pipeline (3 STT, 3 LLM, 3 TTS).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from plotnine import (aes, coord_flip, facet_wrap, scale_colour_manual, element_blank, element_text, geom_col, geom_line, geom_point, geom_text, geom_tile, ggplot,
                      labs, scale_fill_manual, scale_shape_manual, scale_x_continuous, scale_y_continuous, theme)

import roygbviz as rv

out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)

STT = ["Whisper", "Parakeet", "Conformer"]
LLM = ["Llama", "Qwen", "Gemma"]
TTS = ["Kokoro", "Piper", "XTTS"]
NINE = STT + LLM + TTS  # rainbow order: red..yellow (STT), green..blue (LLM), indigo..pink (TTS)
FAMILY = dict(**{m: "STT" for m in STT}, **{m: "LLM" for m in LLM}, **{m: "TTS" for m in TTS})


def model_colours():
    """Pin each model to one colour, handed out in rainbow order (red to pink)."""
    return dict(zip(NINE, PAL["p"].series(order="rainbow")))
SHAPES = {"STT": "o", "LLM": "s", "TTS": "^"}
N: dict = {}  # neutrals of the palette being drawn
PAL: dict = {}


def lines():
    x = np.arange(0, 13)
    names = NINE[:5]  # red, orange, yellow, green, teal
    floors = [3.1, 2.6, 2.1, 1.6, 1.1]  # descending, so the line ends read red at the top down to teal
    d = pd.concat([pd.DataFrame({"epoch": x, "loss": 2.2 * np.exp(-x / (3 + 0.5 * i)) + floors[i] - 0.5 + rng.normal(0, .015, len(x)),
                                 "model": m}) for i, m in enumerate(names)])
    d["model"] = pd.Categorical(d["model"], names)
    return (ggplot(d, aes("epoch", "loss", colour="model"))
            + geom_line(size=1.2)
            + rv.end_labels(d, "epoch", "loss", "model") + rv.room(0.32, breaks=[0, 4, 8, 12])
            + scale_colour_manual(values=model_colours())
            + theme(legend_position="none")
            + labs(title="Five runs, five colours", subtitle="Validation loss by epoch, labelled at the line end",
                   x="Epoch", y="", caption="Synthetic data"))


def nine():
    score = [91, 88, 84, 79, 82, 74, 91, 83, 72]  # same order as NINE (rainbow)
    d = pd.DataFrame({"model": NINE, "score": score})
    d["model"] = pd.Categorical(d["model"], NINE[::-1])  # flipped axis: first level at the bottom, so reverse
    d["label"] = d["score"].astype(str)
    return (ggplot(d, aes("model", "score", fill="model"))
            + geom_col(width=0.7, show_legend=False)
            + geom_text(aes(label="label"), ha="left", nudge_y=1.5, size=9, colour=N["text_2"])
            + coord_flip()
            + scale_fill_manual(values=model_colours())
            + scale_y_continuous(limits=(0, 104), expand=(0, 0))
            + rv.theme_roygbviz(grid="x")
            + labs(title="Nine models, nine colours", subtitle="Overall score (0 to 100), rainbow order from red to pink",
                   x="", y="", caption="Synthetic data"))


def stages():
    pipes = ["Cascade A", "Cascade B", "Cascade C", "Cascade D", "Cascade E"]
    base = rv.group_map()  # stage colours, a different kind of colour from the nine models
    ms = {"STT": [180, 210, 150, 240, 190], "LLM": [520, 410, 640, 380, 450], "TTS": [210, 160, 260, 190, 140]}
    rows = []
    for st, vals in ms.items():
        for p, v in zip(pipes, vals):
            rows.append((p, st, v))
    d = pd.DataFrame(rows, columns=["pipeline", "stage", "ms"])
    d["stage"] = pd.Categorical(d["stage"], ["TTS", "LLM", "STT"])
    d["pipeline"] = pd.Categorical(d["pipeline"], pipes[::-1])
    tot = d.groupby("pipeline", observed=True)["ms"].sum().reset_index()
    tot["label"] = tot["ms"].astype(str) + " ms"
    return (ggplot(d, aes("pipeline", "ms", fill="stage"))
            + geom_col(width=0.68, colour=N["bg"], size=1.1)
            + geom_text(aes("pipeline", "ms", label="label"), data=tot, inherit_aes=False, ha="left", nudge_y=14,
                        size=8.5, colour=N["text_2"])
            + coord_flip()
            + scale_fill_manual(values=base, breaks=["STT", "LLM", "TTS"])
            + scale_y_continuous(limits=(0, 1250), expand=(0, 0))
            + rv.theme_roygbviz(grid="x")
            + theme(legend_position="top", legend_title=element_blank())
            + labs(title="Where the time goes", subtitle="Latency per stage (ms), in the three stage colours", x="", y="", caption="Synthetic data"))


def levels_demo():
    """Lightness levels: one colour, five depths (deep to soft), e.g. for conditions or a dose-response."""
    cols = ["red", "green", "violet"]
    rows = []
    for c in cols:
        for k, hx in enumerate(rv.levels(c, 5)):
            rows.append((c.title(), f"L{k + 1}", 30 + 12 * k + rng.integers(-3, 4), hx))
    d = pd.DataFrame(rows, columns=["group", "level", "v", "hex"])
    d["group"] = pd.Categorical(d["group"], [c.title() for c in cols])
    d["key"] = d["group"].astype(str) + d["level"]
    vals = dict(zip(d["key"], d["hex"]))
    return (ggplot(d, aes("level", "v", fill="key"))
            + geom_col(width=0.75, show_legend=False)
            + scale_fill_manual(values=vals)
            + scale_y_continuous(expand=(0, 0, 0.05, 0))
            + facet_wrap("group", nrow=1)
            + theme(plot_subtitle=element_text(margin={"b": 16}))
            + labs(title="Levels of lightness", subtitle="Five steps per colour, deep to soft", x="", y="",
                   caption="Synthetic data"))


def scatter():
    lat = [310, 420, 520, 800, 650, 900, 1050, 880, 760]
    qual = [4.5, 4.3, 4.0, 4.6, 4.3, 3.9, 4.4, 4.0, 3.6]
    d = pd.DataFrame({"model": pd.Categorical(NINE, NINE), "latency": lat, "quality": qual,
                      "family": [FAMILY[m] for m in NINE]})
    return (ggplot(d, aes("latency", "quality", colour="model", shape="family"))
            + geom_point(size=4, show_legend=False)
            + geom_text(aes(label="model"), ha="left", nudge_x=24, size=8, colour=N["text"], show_legend=False)
            + scale_colour_manual(values=model_colours())
            + scale_shape_manual(values=SHAPES)
            + scale_x_continuous(limits=(200, 1250))
            + rv.theme_roygbviz(grid="xy")
            + labs(title="Quality vs latency", subtitle="Colour is the model, shape is the stage",
                   x="Latency (ms)", y="Quality (MOS)", caption="Synthetic data"))


def heat():
    n = 8
    m = np.clip(np.eye(n) * 0.75 + rng.random((n, n)) * 0.22, 0, 1)
    d = pd.DataFrame([(i, j, m[i, j]) for i in range(n) for j in range(n)], columns=["true", "pred", "p"])
    return (ggplot(d, aes("pred", "true", fill="p")) + geom_tile(colour=N["bg"], size=0.8)
            + rv.scale_fill_roygbviz_c("violet")
            + theme(panel_grid_major=element_blank())
            + labs(title="Confusion matrix", subtitle="Sequential, one colour, soft to deep", x="Predicted", y="True", fill="P"))


def diverging():
    d = pd.DataFrame([(a, b, v) for a, row in zip(STT, rng.normal(0, 1.4, (3, 3))) for b, v in zip(LLM, row)],
                     columns=["stt", "llm", "delta"])
    d["stt"] = pd.Categorical(d["stt"], STT[::-1]); d["llm"] = pd.Categorical(d["llm"], LLM)
    d["label"] = d["delta"].map(lambda v: f"{v:+.1f}")
    lim = float(d["delta"].abs().max())
    # pale tiles always get dark ink; saturated ends get white (light) or navy (dark)
    d["ink"] = np.where(d["delta"].abs() > 0.55 * lim, "hi", "lo")
    hi = "#FFFFFF" if PAL["mode"] == "light" else "#141A29"  # ink on the saturated ends
    return (ggplot(d, aes("llm", "stt", fill="delta")) + geom_tile(colour=N["bg"], size=1.2)
            + geom_text(aes(label="label", colour="ink"), size=9, show_legend=False)
            + scale_colour_manual(values={"hi": hi, "lo": "#1B2A41"})
            + rv.scale_fill_roygbviz_div()
            + labs(title="Change vs baseline", subtitle="-1 is the TTS colour, 0 is white, +1 is the STT colour", x="", y="", fill="pp"))


FNS = (lines, nine, stages, levels_demo, scatter, heat, diverging)
NAMES = tuple(f.__name__ for f in FNS)


def build(mode):
    p = rv.use(mode)
    N.clear(); N.update(p.neutrals); PAL.update(mode=mode, p=p)
    for name, fn in zip(NAMES, FNS):
        fn().save(out / f"_{mode}_{name}.png", width=5.4, height=4.0, dpi=110, verbose=False)
    return mode


if __name__ == "__main__":
    from PIL import Image
    for tag in [build("light"), build("dark"), build("cream")]:
        ims = [Image.open(out / f"_{tag}_{n}.png") for n in NAMES]
        w, h = ims[0].size
        sheet = Image.new("RGB", (w * 4, h * 2), ims[0].getpixel((3, 3)))
        for k, im in enumerate(ims):
            sheet.paste(im, ((k % 4) * w, (k // 4) * h))
        sheet.save(out / f"gallery_{tag}.png")
        for n in NAMES:
            (out / f"_{tag}_{n}.png").unlink()
        print("wrote", out / f"gallery_{tag}.png")
