"""Mega test: every chart type and style, in light and dark. python examples/mega.py [outdir]

Shading rule: fills (areas, bands, ribbons, outlined bodies) use ``rv.shade(colour)``, one level lighter than the
default colour, and the line or outline keeps the default colour. All data is synthetic.
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from plotnine import *  # noqa: F401,F403  (a test bench: use everything)

import roygbviz as rv

warnings.filterwarnings("ignore")
out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
out.mkdir(parents=True, exist_ok=True)

STT = ["Whisper", "Parakeet", "Conformer"]
TTS = ["Kokoro", "Piper", "XTTS"]
LLM = ["Llama", "Qwen", "Gemma"]
NINE = STT + TTS + LLM  # rainbow order
STAGES = ["STT", "TTS", "LLM"]
S = {"P": None, "N": {}}  # current palette and neutrals


def c(name):
    p = S["P"]
    return p.roles.get(name) or p.groups.get(name) or name


def sh(name, k=1):
    return rv.shade(name, k)


def models():
    return rv.colour_map(NINE)


def stage_cols():
    return rv.group_map()


def ink():
    return S["N"]["text"]


def ink2():
    return S["N"]["text_2"]


def muted():
    return S["N"]["muted"]


def noleg():
    return theme(legend_position="none")


def foot():
    return dict(caption="Synthetic data")


# =============================================================================================== core charts
def line():
    rng = np.random.default_rng(1)
    x = np.arange(13)
    names = NINE[:5]
    floors = [3.1, 2.6, 2.1, 1.6, 1.1]
    d = pd.concat([pd.DataFrame({"epoch": x, "loss": 2.2 * np.exp(-x / (3 + .5 * i)) + floors[i] - .5 + rng.normal(0, .015, 13),
                                 "model": m}) for i, m in enumerate(names)])
    d["model"] = pd.Categorical(d["model"], names)
    return (ggplot(d, aes("epoch", "loss", colour="model")) + geom_line(size=1.2)
            + rv.end_labels(d, "epoch", "loss", "model") + rv.room(.34, breaks=[0, 4, 8, 12])
            + scale_colour_manual(values=models()) + noleg()
            + labs(title="Line", subtitle="Validation loss by epoch", x="Epoch", y="", **foot()))


def bar():
    score = [91, 88, 84, 79, 82, 74, 91, 83, 72]
    d = pd.DataFrame({"model": NINE, "score": score})
    d["model"] = pd.Categorical(d["model"], NINE[::-1])
    return (ggplot(d, aes("model", "score", fill="model")) + geom_col(width=.7, show_legend=False)
            + geom_text(aes(label="score"), ha="left", nudge_y=1.5, size=8.5, colour=ink2())
            + coord_flip() + scale_fill_manual(values=models()) + scale_y_continuous(limits=(0, 106), expand=(0, 0))
            + rv.theme_roygbviz(grid="x")
            + labs(title="Bar", subtitle="Score by model, rainbow order", x="", y="", **foot()))


def stacked():
    pipes = [f"Cascade {k}" for k in "ABCDE"]
    ms = {"STT": [180, 210, 150, 240, 190], "TTS": [210, 160, 260, 190, 140], "LLM": [520, 410, 640, 380, 450]}
    d = pd.DataFrame([(p, s, v) for s, vs in ms.items() for p, v in zip(pipes, vs)], columns=["pipe", "stage", "ms"])
    d["stage"] = pd.Categorical(d["stage"], ["LLM", "TTS", "STT"])
    d["pipe"] = pd.Categorical(d["pipe"], pipes[::-1])
    tot = d.groupby("pipe", observed=True)["ms"].sum().reset_index()
    return (ggplot(d, aes("pipe", "ms", fill="stage")) + geom_col(width=.68, colour=S["N"]["bg"], size=1.1)
            + geom_text(aes("pipe", "ms", label="ms"), data=tot, inherit_aes=False, ha="left", nudge_y=14, size=8, colour=ink2())
            + coord_flip() + scale_fill_manual(values=stage_cols(), breaks=STAGES)
            + scale_y_continuous(limits=(0, 1250), expand=(0, 0)) + rv.theme_roygbviz(grid="x")
            + theme(legend_position="top", legend_title=element_blank())
            + labs(title="Stacked bar", subtitle="Latency per stage (ms)", x="", y="", **foot()))


def candle():
    rng = np.random.default_rng(4)
    n = 16
    close = 100 + np.cumsum(rng.normal(0, 3, n))
    open_ = np.r_[100, close[:-1]] + rng.normal(0, 1, n)
    hi = np.maximum(open_, close) + rng.uniform(1, 4, n)
    lo = np.minimum(open_, close) - rng.uniform(1, 4, n)
    d = pd.DataFrame(dict(i=np.arange(n), o=open_, c=close, h=hi, l=lo))
    d["up"] = np.where(d.c >= d.o, "up", "down")
    d["ymin"], d["ymax"] = d[["o", "c"]].min(axis=1), d[["o", "c"]].max(axis=1)
    line_c = {"up": c("teal"), "down": c("red")}
    fill_c = {"up": sh("teal"), "down": sh("red")}
    return (ggplot(d) + geom_linerange(aes("i", ymin="l", ymax="h", colour="up"), size=.9)
            + geom_rect(aes(xmin="i-.32", xmax="i+.32", ymin="ymin", ymax="ymax", fill="up", colour="up"), size=.9)
            + scale_colour_manual(values=line_c) + scale_fill_manual(values=fill_c) + noleg()
            + labs(title="Candlestick", subtitle="Shaded body, default-colour outline", x="Day", y="", **foot()))


def area():
    rng = np.random.default_rng(5)
    x = np.arange(0, 25)
    base = {"STT": 30, "TTS": 22, "LLM": 48}
    d = pd.DataFrame([(xi, s, max(4, base[s] + 8 * np.sin(xi / 4 + k) + rng.normal(0, 1.2))) for k, s in enumerate(STAGES)
                      for xi in x], columns=["t", "stage", "v"])
    d["stage"] = pd.Categorical(d["stage"], ["LLM", "TTS", "STT"])
    return (ggplot(d, aes("t", "v", fill="stage", colour="stage")) + geom_area(size=.9, position="stack")
            + scale_fill_manual(values=rv.shade_map(stage_cols())) + scale_colour_manual(values=stage_cols())
            + scale_x_continuous(expand=(0, 0)) + scale_y_continuous(expand=(0, 0, .05, 0))
            + theme(legend_position="top", legend_title=element_blank())
            + labs(title="Area", subtitle="Stacked, shaded fill and default-colour edge", x="Hour", y="", **foot()))


def timeline():
    ev = pd.DataFrame(dict(t=[1, 3.2, 5, 7.5, 10, 12],
                           label=["Kick-off", "Data", "Baseline", "Cascade", "Eval", "Write-up"],
                           y=[1, -1, 1, -1, 1, -1], stage=["STT", "STT", "TTS", "TTS", "LLM", "LLM"]))
    ev["lab_y"] = ev.y * 1.6
    return (ggplot(ev) + geom_hline(yintercept=0, colour=S["N"]["rule"], size=1.2)
            + geom_segment(aes(x="t", xend="t", y=0, yend="y*1.15", colour="stage"), size=.9)
            + geom_point(aes("t", 0, fill="stage", colour="stage"), size=4.5)
            + geom_text(aes("t", "lab_y", label="label"), size=9, colour=ink())
            + scale_colour_manual(values=stage_cols()) + scale_fill_manual(values=rv.shade_map(stage_cols()))
            + scale_y_continuous(limits=(-2.4, 2.4)) + scale_x_continuous(limits=(0, 13))
            + noleg() + theme(axis_text_y=element_blank(), panel_grid_major=element_blank())
            + labs(title="Timeline", subtitle="Milestones coloured by stage", x="Week", y="", **foot()))


def horizon():
    rng = np.random.default_rng(6)
    x = np.arange(0, 60)
    rows = []
    for name, ph in (("Whisper", 0), ("Kokoro", 1.4), ("Llama", 2.7)):
        v = np.clip(np.cumsum(rng.normal(0, .25, 60)) + 3.2 * np.sin(x / 6 + ph) + 3.2, 0, None)
        for k in range(3):
            rows.append(pd.DataFrame(dict(x=x, model=name, band=k, ymax=np.clip(v - k * 2, 0, 2))))
    d = pd.concat(rows)
    d["model"] = pd.Categorical(d["model"], ["Whisper", "Kokoro", "Llama"])
    lv = {0: sh("blue", 1), 1: c("blue"), 2: rv.levels("blue", 5)[0]}
    d["band"] = d["band"].astype(int)
    layers = [geom_ribbon(aes(x="x", ymin=0, ymax="ymax"), data=d[d.band == k], fill=lv[k]) for k in range(3)]
    return (ggplot() + layers + facet_wrap("model", ncol=1) + scale_y_continuous(limits=(0, 2), breaks=[])
            + scale_x_continuous(expand=(0, 0))
            + theme(strip_text=element_text(ha="left"), panel_spacing_y=.08)
            + labs(title="Horizon", subtitle="Three bands of one colour, soft to deep", x="Minutes", y="", **foot()))


def waterfall():
    steps = [("Baseline", 62, "tot"), ("+ Data", 7, "inc"), ("+ Denoise", 4, "inc"), ("- Quant", -5, "dec"),
             ("+ Prompt", 6, "inc"), ("- Latency", -3, "dec"), ("Final", None, "tot")]
    run, rows = 0, []
    for i, (lab, v, kind) in enumerate(steps):
        if kind == "tot":
            val = run + v if v is not None and i == 0 else run
            start, end = 0, (v if v is not None else run)
            run = end
        else:
            start, end = run, run + v
            run = end
        rows.append((i, lab, start, end, kind))
    d = pd.DataFrame(rows, columns=["i", "lab", "start", "end", "kind"])
    d["lab"] = pd.Categorical(d["lab"], d["lab"])
    line_c = {"tot": c("indigo"), "inc": c("teal"), "dec": c("red")}
    fill_c = {k: sh(v) for k, v in line_c.items()}
    conn = pd.DataFrame(dict(x=d.i[:-1] + .34, xend=d.i[1:] - .34, y=d.end[:-1]))
    d["lab_y"] = d[["start", "end"]].max(axis=1) + 1.2
    d["txt"] = (d.end - d.start).astype(int).astype(str)
    return (ggplot(d) + geom_rect(aes(xmin="i-.34", xmax="i+.34", ymin="start", ymax="end", fill="kind", colour="kind"), size=.9)
            + geom_segment(aes(x="x", xend="xend", y="y", yend="y"), data=conn, colour=muted(), size=.6, linetype="dashed")
            + geom_text(aes("i", "lab_y", label="txt"), size=8.5, colour=ink2())
            + scale_x_continuous(breaks=list(d.i), labels=list(d.lab)) + scale_y_continuous(limits=(55, 82), expand=(0, 0))
            + scale_fill_manual(values=fill_c) + scale_colour_manual(values=line_c) + noleg()
            + theme(axis_text_x=element_text(rotation=30, ha="right"))
            + labs(title="Waterfall", subtitle="Accuracy change per step", x="", y="", **foot()))


def grouped():
    pipes = ["A", "B", "C", "D"]
    rng = np.random.default_rng(8)
    d = pd.DataFrame([(p, s, v) for s, base in (("STT", 190), ("TTS", 190), ("LLM", 480)) for p, v in
                      zip(pipes, base + rng.normal(0, 40, 4))], columns=["pipe", "stage", "ms"])
    d["stage"] = pd.Categorical(d["stage"], STAGES)
    return (ggplot(d, aes("pipe", "ms", fill="stage", colour="stage"))
            + geom_col(position=position_dodge(width=.82), width=.76, size=.9)
            + scale_fill_manual(values=rv.shade_map(stage_cols())) + scale_colour_manual(values=stage_cols())
            + scale_y_continuous(expand=(0, 0, .05, 0)) + theme(legend_position="top", legend_title=element_blank())
            + labs(title="Grouped bar", subtitle="Shaded fill with default-colour outline", x="Cascade", y="ms", **foot()))


CORE = [line, bar, stacked, candle, area, timeline, horizon, waterfall, grouped]


# ============================================================================================ chart elements
YEARS = np.arange(2020, 2026)
VALS = np.array([42, 47, 51, 58, 63, 71])


def _bars(highlight=None, fill_main=None, width=.62):
    d = pd.DataFrame(dict(x=YEARS, v=VALS))
    return d, ggplot(d, aes("x", "v")) + geom_col(width=width, fill=fill_main or sh("blue"), colour=c("blue"), size=.8)


def el_overlay_arrow():
    d, g = _bars()
    return (g + geom_segment(aes(x=2020, xend=2025, y=48, yend=79), data=pd.DataFrame(dict(a=[0])), inherit_aes=False,
                             colour=c("STT"), size=1.1, arrow=arrow(length=.12, type="closed"))
            + annotate("label", x=2022.3, y=80, label="+69%", size=9, colour=c("STT"), fill=S["N"]["bg"], label_size=0)
            + scale_y_continuous(limits=(0, 90), expand=(0, 0)) + scale_x_continuous(breaks=list(YEARS))
            + labs(title="Overlay arrow", subtitle="Growth drawn over the bars", x="", y="", **foot()))


def el_top_arrow():
    d, g = _bars()
    seg = pd.DataFrame(dict(x=[2020, 2020, 2025], xend=[2020, 2025, 2025], y=[VALS[0] + 3, 82, 82], yend=[82, 82, VALS[-1] + 3]))
    return (g + geom_segment(aes(x="x", xend="xend", y="y", yend="yend"), data=seg.iloc[:2], inherit_aes=False, colour=c("STT"), size=1)
            + geom_segment(aes(x="x", xend="xend", y="y", yend="yend"), data=seg.iloc[2:], inherit_aes=False, colour=c("STT"), size=1,
                           arrow=arrow(length=.12, type="closed"))
            + annotate("label", x=2022.5, y=82, label="+29 pts", size=9, colour=c("STT"), fill=S["N"]["bg"], label_size=0)
            + scale_y_continuous(limits=(0, 92), expand=(0, 0)) + scale_x_continuous(breaks=list(YEARS))
            + labs(title="Top arrow", subtitle="Change across the whole series", x="", y="", **foot()))


def el_level_diff():
    d, g = _bars()
    return (g + geom_hline(yintercept=VALS[0], linetype="dashed", colour=muted(), size=.7)
            + geom_segment(aes(x=2025.45, xend=2025.45, y=VALS[0], yend=VALS[-1]), data=pd.DataFrame(dict(a=[0])), inherit_aes=False,
                           colour=c("LLM"), size=1.1, arrow=arrow(length=.1, ends="both", type="closed"))
            + annotate("text", x=2025.6, y=(VALS[0] + VALS[-1]) / 2, label="+29", size=9, colour=c("LLM"), ha="left", fontweight="bold")
            + scale_y_continuous(limits=(0, 80), expand=(0, 0)) + scale_x_continuous(breaks=list(YEARS), limits=(2019.4, 2026.4))
            + labs(title="Level difference", subtitle="Gap between first and last", x="", y="", **foot()))


def el_reference():
    d, g = _bars()
    avg = VALS.mean()
    return (g + geom_hline(yintercept=avg, linetype="dashed", colour=c("STT"), size=.9)
            + annotate("text", x=2019.55, y=avg + 3, label=f"AVG {avg:.0f}", size=8.5, colour=c("STT"), ha="left", fontweight="bold")
            + scale_y_continuous(limits=(0, 85), expand=(0, 0)) + scale_x_continuous(breaks=list(YEARS))
            + labs(title="Reference line", subtitle="Mean of the series", x="", y="", **foot()))


def el_benchmark():
    d, g = _bars(fill_main=sh("teal"))
    g = ggplot(d, aes("x", "v")) + geom_col(width=.62, fill=sh("teal"), colour=c("teal"), size=.8)
    bm = pd.DataFrame(dict(x=YEARS, b=[45, 50, 55, 60, 65, 70]))
    return (g + geom_segment(aes(x="x-.38", xend="x+.38", y="b", yend="b"), data=bm, inherit_aes=False, colour=ink(), size=1.6)
            + annotate("text", x=2025.5, y=70, label="target", size=8, colour=ink2(), ha="left")
            + scale_y_continuous(limits=(0, 85), expand=(0, 0)) + scale_x_continuous(breaks=list(YEARS), limits=(2019.4, 2026.4))
            + labs(title="Benchmark", subtitle="Bars against a target per year", x="", y="", **foot()))


def el_trend():
    rng = np.random.default_rng(2)
    x = np.arange(0, 30)
    y = 20 + .9 * x + rng.normal(0, 4, 30)
    d = pd.DataFrame(dict(x=x, y=y))
    return (ggplot(d, aes("x", "y")) + geom_col(width=.7, fill=sh("violet"), colour=c("violet"), size=.4)
            + geom_smooth(method="lm", colour=c("STT"), fill=sh("STT"), size=1.1, linetype="dashed", alpha=.35)
            + scale_y_continuous(expand=(0, 0, .05, 0)) + scale_x_continuous(expand=(.01, 0))
            + labs(title="Trendline", subtitle="Linear fit with shaded interval", x="Run", y="", **foot()))


def el_shade():
    rng = np.random.default_rng(3)
    x = np.arange(0, 50)
    y = 60 + 8 * np.sin(x / 7) + np.cumsum(rng.normal(0, .8, 50))
    d = pd.DataFrame(dict(x=x, y=y))
    return (ggplot(d, aes("x", "y")) + annotate("rect", xmin=18, xmax=32, ymin=-np.inf, ymax=np.inf, fill=sh("LLM"), alpha=.55)
            + annotate("text", x=25, y=d.y.max() + 2, label="fine-tuning", size=8.5, colour=c("LLM"), fontweight="bold")
            + geom_line(colour=c("blue"), size=1.2)
            + scale_x_continuous(expand=(0, 0)) + scale_y_continuous(limits=(d.y.min() - 4, d.y.max() + 5), expand=(0, 0))
            + labs(title="Shade", subtitle="Highlighted region of the axis", x="Step", y="", **foot()))


def el_difference():
    x = np.arange(0, 40)
    a = 50 + 10 * np.sin(x / 5)
    b = 50 + 10 * np.sin(x / 5 - 1.1) + 3
    d = pd.DataFrame(dict(x=x, a=a, b=b, hi=np.maximum(a, b), lo=np.minimum(a, b)))
    d["ahead"] = d.a >= d.b
    return (ggplot(d, aes("x"))
            + geom_ribbon(aes(ymin="b", ymax="a"), data=d.assign(a=np.where(d.ahead, d.a, d.b)), fill=sh("STT"), alpha=.9)
            + geom_ribbon(aes(ymin="a", ymax="b"), data=d.assign(b=np.where(~d.ahead, d.b, d.a)), fill=sh("LLM"), alpha=.9)
            + geom_line(aes(y="a"), colour=c("STT"), size=1.1) + geom_line(aes(y="b"), colour=c("LLM"), size=1.1)
            + scale_x_continuous(expand=(0, 0)) + scale_y_continuous(limits=(30, 70))
            + labs(title="Difference", subtitle="Area between two series", x="Step", y="", **foot()))


def el_projection():
    d = pd.DataFrame(dict(x=np.arange(2020, 2029), v=[42, 47, 51, 58, 63, 71, 76, 81, 85]))
    d["kind"] = np.where(d.x <= 2025, "actual", "projected")
    return (ggplot(d, aes("x", "v", fill="kind")) + geom_col(aes(colour="kind", linetype="kind"), width=.64, size=.9)
            + geom_vline(xintercept=2025.5, colour=muted(), size=.6)
            + scale_fill_manual(values={"actual": c("blue"), "projected": sh("blue")})
            + scale_colour_manual(values={"actual": c("blue"), "projected": c("blue")})
            + scale_linetype_manual(values={"actual": "solid", "projected": "dashed"})
            + scale_y_continuous(limits=(0, 100), expand=(0, 0)) + scale_x_continuous(breaks=list(d.x)) + noleg()
            + theme(axis_text_x=element_text(size=7.5))
            + labs(title="Projection", subtitle="Solid actual, shaded dashed forecast", x="", y="", **foot()))


ELEMENTS = [el_overlay_arrow, el_top_arrow, el_level_diff, el_reference, el_benchmark, el_trend, el_shade, el_difference, el_projection]


# ================================================================================================ statistical
def st_hist():
    rng = np.random.default_rng(10)
    d = pd.DataFrame(dict(x=np.r_[rng.normal(6, 1.6, 700), rng.normal(11, 2.2, 300)]))
    return (ggplot(d, aes("x")) + geom_histogram(bins=26, fill=sh("blue"), colour=c("blue"), size=.5)
            + geom_vline(xintercept=d.x.mean(), colour=c("STT"), size=1, linetype="dashed")
            + scale_y_continuous(expand=(0, 0, .05, 0))
            + labs(title="Histogram", subtitle="Shaded bars, mean as dashed line", x="Word error rate (%)", y="", **foot()))


def st_density():
    rng = np.random.default_rng(11)
    d = pd.DataFrame([(s, v) for s, mu, sd in (("STT", 5, 1.3), ("TTS", 8, 1.6), ("LLM", 11, 1.9)) for v in rng.normal(mu, sd, 500)],
                     columns=["stage", "x"])
    d["stage"] = pd.Categorical(d["stage"], STAGES)
    return (ggplot(d, aes("x", fill="stage", colour="stage")) + geom_density(alpha=.72, size=1)
            + scale_fill_manual(values=rv.shade_map(stage_cols())) + scale_colour_manual(values=stage_cols())
            + scale_y_continuous(expand=(0, 0, .05, 0)) + theme(legend_position="top", legend_title=element_blank())
            + labs(title="Density", subtitle="Overlapping stages", x="Score", y="", **foot()))


def st_box():
    rng = np.random.default_rng(12)
    d = pd.DataFrame([(m, v) for k, m in enumerate(NINE) for v in rng.normal(70 + 2 * (k % 3) - k, 5 + k % 3, 40)], columns=["model", "v"])
    d["model"] = pd.Categorical(d["model"], NINE)
    return (ggplot(d, aes("model", "v", fill="model", colour="model")) + geom_boxplot(size=.8, outlier_size=1.5, show_legend=False)
            + scale_fill_manual(values=rv.shade_map(models())) + scale_colour_manual(values=models())
            + theme(axis_text_x=element_text(rotation=40, ha="right"), legend_position="none")
            + labs(title="Boxplot", subtitle="One colour per model, shaded boxes", x="", y="", **foot()))


def st_violin():
    rng = np.random.default_rng(13)
    d = pd.DataFrame([(s, v) for s, mu, sd in (("STT", 5, 1.3), ("TTS", 8, 1.6), ("LLM", 11, 1.9)) for v in rng.normal(mu, sd, 400)],
                     columns=["stage", "v"])
    d["stage"] = pd.Categorical(d["stage"], STAGES)
    return (ggplot(d, aes("stage", "v", fill="stage", colour="stage")) + geom_violin(size=.9, draw_quantiles=[.5], show_legend=False)
            + scale_fill_manual(values=rv.shade_map(stage_cols())) + scale_colour_manual(values=stage_cols()) + noleg()
            + labs(title="Violin", subtitle="Distribution per stage, median line", x="", y="", **foot()))


def st_scatter():
    rng = np.random.default_rng(14)
    x = rng.uniform(0, 10, 90)
    y = 3 + .7 * x + rng.normal(0, 1.4, 90)
    d = pd.DataFrame(dict(x=x, y=y))
    return (ggplot(d, aes("x", "y")) + geom_smooth(method="lm", colour=c("indigo"), fill=sh("indigo"), size=1.2, alpha=.45)
            + geom_point(colour=c("indigo"), fill=sh("indigo"), size=2.4, stroke=.7, shape="o")
            + labs(title="Scatter and fit", subtitle="Points, line and shaded interval", x="Audio length (s)", y="Latency (s)", **foot()))


def st_bubble():
    rng = np.random.default_rng(15)
    d = pd.DataFrame(dict(x=rng.uniform(1, 9, 9), y=rng.uniform(2, 8, 9), n=rng.uniform(10, 100, 9), model=NINE))
    d["model"] = pd.Categorical(d["model"], NINE)
    return (ggplot(d, aes("x", "y", size="n", fill="model", colour="model"))
            + geom_point(alpha=.9, stroke=1.1, show_legend=False)
            + scale_size(range=(5, 16)) + scale_fill_manual(values=rv.shade_map(models())) + scale_colour_manual(values=models()) + noleg()
            + scale_x_continuous(limits=(0, 10)) + scale_y_continuous(limits=(1, 9))
            + labs(title="Bubble", subtitle="Size is sample count", x="Latency", y="Quality", **foot()))


def st_errorbar():
    rng = np.random.default_rng(16)
    d = pd.DataFrame(dict(model=NINE, m=np.sort(rng.uniform(60, 90, 9))[::-1], e=rng.uniform(2, 6, 9)))
    d["model"] = pd.Categorical(d["model"], NINE[::-1])
    return (ggplot(d, aes("model", "m", colour="model")) + geom_pointrange(aes(ymin="m-e", ymax="m+e"), size=.9, fatten=3.5)
            + coord_flip() + scale_colour_manual(values=models()) + rv.theme_roygbviz(grid="x") + noleg()
            + labs(title="Point range", subtitle="Mean with 95% interval", x="", y="Score", **foot()))


def st_step():
    rng = np.random.default_rng(17)
    d = pd.DataFrame(dict(x=np.arange(0, 40), y=np.cumsum(rng.choice([0, 0, 1, 2], 40))))
    e = pd.DataFrame(dict(x=np.repeat(d.x.values, 2)[1:], y=np.repeat(d.y.values, 2)[:-1]))
    return (ggplot(d, aes("x", "y"))
            + geom_ribbon(aes(ymin=0, ymax="y"), data=e, fill=sh("teal"), alpha=.8)
            + geom_step(colour=c("teal"), size=1.2)
            + scale_x_continuous(expand=(0, 0)) + scale_y_continuous(expand=(0, 0, .05, 0))
            + labs(title="Step", subtitle="Cumulative count, shaded below", x="Minutes", y="", **foot()))


def st_bin2d():
    rng = np.random.default_rng(18)
    d = pd.DataFrame(dict(x=rng.normal(0, 1, 4000), y=rng.normal(0, 1, 4000)))
    d["y"] = d.y * .6 + d.x * .5
    return (ggplot(d, aes("x", "y")) + geom_bin_2d(bins=22) + rv.scale_fill_roygbviz_c("teal")
            + labs(title="2D bins", subtitle="Counts on a one-colour ramp", x="", y="", fill="n", **foot()))


def st_lollipop():
    rng = np.random.default_rng(19)
    d = pd.DataFrame(dict(model=NINE, v=np.sort(rng.uniform(40, 95, 9))))
    d["model"] = pd.Categorical(d["model"], d["model"].iloc[np.argsort(d.v.values)])
    return (ggplot(d, aes("model", "v", colour="model", fill="model"))
            + geom_segment(aes(xend="model", y=0, yend="v"), size=1.4) + geom_point(size=4.6, stroke=1)
            + coord_flip() + scale_colour_manual(values=models()) + scale_fill_manual(values=rv.shade_map(models()))
            + scale_y_continuous(expand=(0, 0, .08, 0)) + rv.theme_roygbviz(grid="x") + noleg()
            + labs(title="Lollipop", subtitle="Ranked scores", x="", y="", **foot()))


def st_dumbbell():
    rng = np.random.default_rng(20)
    before = rng.uniform(55, 75, 9)
    d = pd.DataFrame(dict(model=pd.Categorical(NINE, NINE[::-1]), a=before, b=before + rng.uniform(2, 14, 9)))
    return (ggplot(d) + geom_segment(aes(x="model", xend="model", y="a", yend="b"), colour=S["N"]["rule"], size=2)
            + geom_point(aes("model", "a"), colour=c("STT"), fill=sh("STT"), size=3.8, stroke=1)
            + geom_point(aes("model", "b"), colour=c("LLM"), fill=c("LLM"), size=3.8, stroke=1)
            + coord_flip() + rv.theme_roygbviz(grid="x")
            + labs(title="Dumbbell", subtitle="Before (shaded) and after", x="", y="Score", **foot()))


def st_slope():
    rng = np.random.default_rng(21)
    names = NINE[:6]
    a = np.array([52, 60, 66, 72, 78, 84.])
    b = a + np.array([14, -5, 13, -12, 4, -16])
    d = pd.DataFrame(dict(model=np.repeat(names, 2), t=np.tile([0, 1], 6), v=np.c_[a, b].ravel()))
    d["model"] = pd.Categorical(d["model"], names)
    l = d[d.t == 0]; r = d[d.t == 1]
    return (ggplot(d, aes("t", "v", colour="model", group="model")) + geom_line(size=1.3) + geom_point(size=3.4)
            + geom_text(aes(label="model"), data=r, ha="left", nudge_x=.05, size=8.5, colour=ink())
            + geom_text(aes(label="v.round().astype(int)"), data=l, ha="right", nudge_x=-.05, size=8.5, colour=ink2())
            + scale_x_continuous(limits=(-.25, 1.45), breaks=[0, 1], labels=["Before", "After"])
            + scale_colour_manual(values=models()) + noleg() + theme(panel_grid_major_y=element_blank())
            + labs(title="Slope", subtitle="Change per model", x="", y="", **foot()))


def st_facets():
    rng = np.random.default_rng(22)
    x = np.arange(0, 20)
    names = NINE[:6]
    d = pd.DataFrame([(m, xi, 80 - 40 * np.exp(-xi / (4 + k)) + rng.normal(0, 1.2)) for k, m in enumerate(names) for xi in x],
                     columns=["model", "x", "y"])
    d["model"] = pd.Categorical(d["model"], names)
    return (ggplot(d, aes("x", "y", colour="model", fill="model"))
            + geom_area(alpha=.0) + geom_ribbon(aes(ymin=40, ymax="y"), alpha=.85) + geom_line(size=1)
            + facet_wrap("model", nrow=2) + scale_colour_manual(values=models()) + scale_fill_manual(values=rv.shade_map(models())) + noleg()
            + scale_x_continuous(breaks=[0, 10, 20]) + scale_y_continuous(limits=(40, 85), breaks=[40, 60, 80])
            + theme(strip_text=element_text(size=8.5))
            + labs(title="Small multiples", subtitle="Shaded under each line", x="", y="", **foot()))


STATS = [st_hist, st_density, st_box, st_violin, st_scatter, st_bubble, st_errorbar, st_step, st_bin2d, st_lollipop, st_dumbbell, st_slope, st_facets]


# ================================================================================================== style variants
def _base(title, sub, level=0, shade_fill=True, grid="y", base_size=None, compact=False, legend=False):
    rng = np.random.default_rng(30)
    x = np.arange(0, 24)
    names = NINE[:3]
    d = pd.concat([pd.DataFrame(dict(x=x, y=38 + 16 * i + 5 * np.sin(x / 4 + i) + rng.normal(0, 1, 24), m=m)) for i, m in enumerate(names)])
    d["m"] = pd.Categorical(d["m"], names)
    cols = {k: rv.shade(v, level) if level else v for k, v in rv.colour_map(names).items()}
    g = ggplot(d, aes("x", "y", colour="m", fill="m"))
    if shade_fill:
        g = g + geom_ribbon(aes(ymin="y-4", ymax="y+4"), alpha=.8, colour="none")
    bs = 11 if base_size is None else base_size
    g = (g + geom_line(size=rv.stroke(1.2, bs)) + scale_colour_manual(values=cols) + scale_fill_manual(values=rv.shade_map(rv.colour_map(names)))
         + scale_x_continuous(expand=(0, 0)) + scale_y_continuous(limits=(25, 90), expand=(0, 0)))
    g = g + (rv.theme_roygbviz(grid=grid) if base_size is None else rv.theme_roygbviz(grid=grid, base_size=base_size))
    g = g + theme(legend_position="top" if legend else "none", legend_title=element_blank())
    return g + (labs(x="", y="") if compact else labs(title=title, subtitle=sub, x="Step", y="", **foot()))


def sty_grid_y(): return _base("Grid: y", "Horizontal hairlines (default)", grid="y")
def sty_grid_x(): return _base("Grid: x", "Vertical hairlines", grid="x")
def sty_grid_xy(): return _base("Grid: xy", "Both directions", grid="xy")
def sty_grid_none(): return _base("Grid: none", "Clean canvas", grid="none")
def sty_deeper(): return _base("Level -1", "Deeper lines for thin strokes", level=-1)
def sty_lighter(): return _base("Level +1", "Softer lines", level=1)
def sty_noshade(): return _base("No shading", "Lines only", shade_fill=False)
def sty_small(): return _base("Base size 9", "Text and strokes scale together", base_size=9)
def sty_large(): return _base("Base size 14", "Text and strokes scale together", base_size=14)
def sty_legend(): return _base("Legend on top", "When direct labels do not fit", legend=True)
def sty_compact(): return _base("", "", compact=True)


def sty_solid_vs_shaded():
    d = pd.DataFrame(dict(m=NINE, v=[91, 88, 84, 79, 82, 74, 91, 83, 72] * 1))
    d["m"] = pd.Categorical(d["m"], NINE)
    return (ggplot(d, aes("m", "v", fill="m", colour="m")) + geom_col(width=.8, show_legend=False)
            + scale_fill_manual(values=models()) + scale_colour_manual(values=models()) + noleg()
            + theme(axis_text_x=element_text(rotation=40, ha="right"))
            + labs(title="Solid bars", subtitle="Default colour, no shading", x="", y="", **foot()))


def sty_shaded_bars():
    d = pd.DataFrame(dict(m=NINE, v=[91, 88, 84, 79, 82, 74, 91, 83, 72]))
    d["m"] = pd.Categorical(d["m"], NINE)
    return (ggplot(d, aes("m", "v", fill="m", colour="m")) + geom_col(width=.8, size=1, show_legend=False)
            + scale_fill_manual(values=rv.shade_map(models())) + scale_colour_manual(values=models()) + noleg()
            + theme(axis_text_x=element_text(rotation=40, ha="right"))
            + labs(title="Shaded bars", subtitle="Fill one level lighter, outline default", x="", y="", **foot()))


def sty_shade2():
    d = pd.DataFrame(dict(m=NINE, v=[91, 88, 84, 79, 82, 74, 91, 83, 72]))
    d["m"] = pd.Categorical(d["m"], NINE)
    return (ggplot(d, aes("m", "v", fill="m", colour="m")) + geom_col(width=.8, size=1, show_legend=False)
            + scale_fill_manual(values={k: rv.shade(v, 2) for k, v in models().items()}) + scale_colour_manual(values=models()) + noleg()
            + theme(axis_text_x=element_text(rotation=40, ha="right"))
            + labs(title="Shaded, two steps", subtitle="For very soft backgrounds", x="", y="", **foot()))


STYLES = [sty_grid_y, sty_grid_x, sty_grid_xy, sty_grid_none, sty_deeper, sty_lighter, sty_noshade, sty_small, sty_large,
          sty_legend, sty_compact, sty_solid_vs_shaded, sty_shaded_bars, sty_shade2]

SHEETS = {"core": CORE, "elements": ELEMENTS, "stats": STATS, "styles": STYLES}


# ============================================================================================================= build
def build(mode):
    from PIL import Image
    S["P"] = rv.use(mode)
    S["N"] = S["P"].neutrals
    bg = S["N"]["bg"]
    for name, fns in SHEETS.items():
        tiles, fails = [], []
        for fn in fns:
            try:
                p = ggplot_build_safe(fn)
                f = out / f"_{name}_{fn.__name__}_{mode}.png"
                p.save(f, width=5.0, height=3.6, dpi=100, verbose=False)
                tiles.append(Image.open(f).convert("RGB"))
            except Exception as e:  # keep going: report every failure at the end
                fails.append((fn.__name__, repr(e)[:160]))
        cols = 3
        rows = -(-len(tiles) // cols)
        sheet = Image.new("RGB", (cols * 500, rows * 360), bg)
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % cols) * 500, (i // cols) * 360))
        sheet.save(out / f"mega_{name}_{mode}.png")
        for f in out.glob(f"_{name}_*_{mode}.png"):
            f.unlink()
        print(mode, name, len(tiles), "ok", "FAILS:" if fails else "", fails)


def ggplot_build_safe(fn):
    return fn()


if __name__ == "__main__":
    for m in ("light", "dark"):
        build(m)
