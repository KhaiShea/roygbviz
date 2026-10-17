# Anatomy of a figure

Every part of a chart has a name, and knowing the names makes documentation, error messages and Stack Overflow answers make sense. This page follows the official matplotlib "Anatomy of a figure", then adds how the same parts appear in plotnine.

## The annotated figure

<p align="center">
<img src="../img/anatomy/figure-parts_light.png#gh-light-mode-only" alt="Anatomy of a matplotlib figure: every labelled part with the call that controls it." width="640">
<img src="../img/anatomy/figure-parts_dark.png#gh-dark-mode-only" alt="Anatomy of a matplotlib figure: every labelled part with the call that controls it." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/anatomy/figure-parts_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import Circle
from matplotlib.patheffects import withStroke
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

ink = rv.colour("blue")                      # colour of the callout rings and names
halo = plt.rcParams["figure.facecolor"]      # so the labels stay readable in light and dark

rng = np.random.default_rng(3)
X = np.linspace(0.5, 3.5, 100)
Y1 = 3 + np.cos(X)
Y2 = 1 + np.cos(1 + X / 0.75) / 2
Y3 = rng.uniform(Y2, Y1)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes((0.2, 0.17, 0.68, 0.7), aspect=1)

# a plain-looking Axes with everything switched on, so each part can be pointed at
for s in ax.spines.values():
    s.set_visible(True)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.xaxis.set_minor_formatter("{x:.2f}")
ax.set(xlim=(0, 4), ylim=(0, 4))
ax.tick_params(which="major", length=10, width=1, labelsize=14)
ax.tick_params(which="minor", length=5, width=1, labelsize=10)
ax.grid(True, axis="both", linestyle="--", linewidth=0.5)

ax.plot(X, Y1, c=rv.colour("blue"), lw=2.5, label="Blue signal", zorder=10)
ax.plot(X, Y2, c=rv.colour("orange"), lw=2.5, label="Orange signal")
ax.plot(X[::3], Y3[::3], lw=0, ms=9, marker="s", mfc="none", mec=rv.colour("violet"), mew=2.5)
ax.set_title("Anatomy of a figure", fontsize=20, va="bottom", pad=14, loc="center")
ax.set_xlabel("x Axis label", fontsize=14)
ax.set_ylabel("y Axis label", fontsize=14)
ax.legend(loc="upper right", fontsize=14)

def callout(x, y, name, code):
    ax.add_artist(Circle((x, y), 0.15, clip_on=False, zorder=10, lw=2.5, ec=ink, fc="none",
                         path_effects=[withStroke(linewidth=7, foreground=halo)]))
    for fx in ([withStroke(linewidth=7, foreground=halo)], []):
        ax.text(x, y - 0.2, name, zorder=100, ha="center", va="top", weight="bold", style="italic",
                family="monospace", color=halo if fx else ink, path_effects=fx)
        ax.text(x, y - 0.33, code, zorder=100, ha="center", va="top", family="monospace", fontsize="medium",
                color=halo if fx else plt.rcParams["text.color"], path_effects=fx)

callout(3.5, -0.13, "Minor tick label", "ax.xaxis.set_minor_formatter")
callout(-0.03, 1.0, "Major tick", "ax.yaxis.set_major_locator")
callout(0.0, 3.75, "Minor tick", "ax.yaxis.set_minor_locator")
callout(-0.15, 3.0, "Major tick label", "ax.yaxis.set_major_formatter")
callout(1.68, -0.39, "xlabel", "ax.set_xlabel")
callout(-0.38, 1.67, "ylabel", "ax.set_ylabel")
callout(1.52, 4.15, "Title", "ax.set_title")
callout(1.75, 2.8, "Line", "ax.plot")
callout(2.25, 1.54, "Markers", "ax.plot(marker=...)")
callout(3.0, 3.0, "Grid", "ax.grid")
callout(3.6, 3.58, "Legend", "ax.legend")
callout(2.5, 0.55, "Axes", "fig.add_axes")
callout(4, 4.5, "Figure", "plt.figure")
callout(0.65, 0.01, "x Axis", "ax.xaxis")
callout(0, 0.36, "y Axis", "ax.yaxis")
callout(4.0, 0.7, "Spine", "ax.spines")

fig.patch.set(linewidth=4, edgecolor=plt.rcParams["axes.edgecolor"])   # the frame shows where the Figure ends

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


The parts, with the code that reaches each one:

| # | Part | What it is | How you reach it |
|---|---|---|---|
| 1 | **Figure** | The whole canvas holding everything | `fig = plt.figure()` or `plt.subplots()` |
| 2 | **Axes** | One plot area (the rectangle with data in it). A figure can hold many. | `fig.add_axes(...)`, `fig.add_subplot(...)`, `plt.subplots()` |
| 3 | **Axis** | One of the number lines (x axis or y axis), including ticks and labels | `ax.xaxis`, `ax.yaxis` |
| 4 | **Spine** | The line drawn along an edge of the Axes | `ax.spines["left"]` |
| 5 | **Title** | Text above the Axes | `ax.set_title()` |
| 6 | **X label / Y label** | Name and unit of each axis | `ax.set_xlabel()`, `ax.set_ylabel()` |
| 7 | **Major tick** | A longer mark with a label | `ax.set_xticks()`, `ax.xaxis.set_major_locator()` |
| 8 | **Major tick label** | The text at a major tick | `ax.set_xticklabels()`, `ax.xaxis.set_major_formatter()` |
| 9 | **Minor tick** | A shorter mark between major ticks, usually unlabelled | `ax.xaxis.set_minor_locator()` |
| 10 | **Minor tick label** | Text at a minor tick (rare) | `ax.xaxis.set_minor_formatter()` |
| 11 | **Line** | A curve drawn by `ax.plot()` | `ax.plot()` returns it |
| 12 | **Markers** | Symbols at data points | `ax.plot(..., marker="o")` or `ax.scatter()` |
| 13 | **Grid** | Reference lines across the Axes | `ax.grid()` |
| 14 | **Legend** | Key mapping colours or styles to names | `ax.legend()` |

**A note on the official page.** It labels the markers as `ax.scatter` and the axes as `fig.subplots`. A line with markers is really `ax.plot(marker=...)`, and an Axes is added with `fig.add_axes`. The labels above use the corrected calls.

## Two ways to talk to matplotlib

1. **Object-oriented (use this).** You hold the objects and call methods: `fig, ax = plt.subplots(); ax.plot(...)`. It is explicit, and it scales to many panels.
2. **pyplot state machine.** You call `plt.plot(...)` and matplotlib decides which Axes you meant. It is fine for a quick look and confusing for anything else.

## The family tree

<p align="center">
<img src="../img/anatomy/hierarchy_light.png#gh-light-mode-only" alt="The nesting of a matplotlib figure: a Figure holds Axes, an Axes holds Axis objects, spines and artists." width="640">
<img src="../img/anatomy/hierarchy_dark.png#gh-dark-mode-only" alt="The nesting of a matplotlib figure: a Figure holds Axes, an Axes holds Axis objects, spines and artists." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/anatomy/hierarchy_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import FancyBboxPatch

n = {k: plt.rcParams[k] for k in ("text.color", "axes.labelcolor", "axes.edgecolor")}
fig = plt.figure(figsize=(8, 5.4))
bg = fig.add_axes((0, 0, 1, 1))
bg.set(xlim=(0, 100), ylim=(0, 68))
bg.axis("off")

def box(x, y, w, h, colour, name, code, lw=2.2, fill=0.10):
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4",
                                fc=colour, ec=colour, alpha=fill, lw=0))
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4", fc="none", ec=colour, lw=lw))
    bg.text(x + 1.4, y + h - 1.6, name, weight="bold", va="top", fontsize=12, color=n["text.color"])
    bg.text(x + 1.4, y + h - 4.6, code, va="top", fontsize=8.5, family="monospace", color=n["axes.labelcolor"])

box(1, 1, 98, 66, rv.colour("grey"), "Figure", "fig = plt.figure()", lw=2.6, fill=0.06)
box(5, 5, 56, 56, rv.colour("blue"), "Axes (one plot)", "ax = fig.add_subplot()")
box(8, 7, 50, 8, rv.colour("teal"), "x Axis", "ax.xaxis: ticks, tick labels, axis label")
box(8, 16, 14, 36, rv.colour("teal"), "y Axis", "ax.yaxis")
box(26, 42, 31, 10, rv.colour("orange"), "Spines", "ax.spines: the four edges")
box(26, 16, 31, 24, rv.colour("violet"), "Artists", "what is drawn inside")
for i, (t, c) in enumerate([("Line2D", "ax.plot"), ("PathCollection", "ax.scatter"), ("Rectangle", "ax.bar"), ("Text", "ax.text")]):
    bg.text(28, 31 - i * 4.0, t, weight="bold", fontsize=9, color=n["text.color"], va="center")
    bg.text(42, 31 - i * 4.0, c, family="monospace", fontsize=8.5, color=n["axes.labelcolor"], va="center")

box(65, 36, 31, 25, rv.colour("pink"), "A second Axes", "ax2 = fig.add_subplot()")
box(65, 5, 15.5, 27, rv.colour("green"), "Legend", "fig.legend()")
box(81.5, 5, 15.5, 27, rv.colour("indigo"), "Colorbar", "fig.colorbar()")
bg.text(97, 63.6, "fig.suptitle()  fig.text()", ha="right", va="center", family="monospace", fontsize=8.5, color=n["axes.labelcolor"])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


A **Figure** contains **Axes**. An **Axes** contains two **Axis** objects, four **Spines**, and the **artists** (lines, text, patches) that make up the picture. Everything you see is an artist. This is why the same method names (`set_color`, `set_alpha`, `set_visible`) work on almost everything.

## Coordinates: where does a thing go?

Matplotlib has several coordinate systems, and picking the right one stops labels from moving when data changes.

<p align="center">
<img src="../img/anatomy/coordinates_light.png#gh-light-mode-only" alt="One point, four ways to say where it is: data, axes fraction, figure fraction and display pixels." width="640">
<img src="../img/anatomy/coordinates_dark.png#gh-dark-mode-only" alt="One point, four ways to say where it is: data, axes fraction, figure fraction and display pixels." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/anatomy/coordinates_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.4, 4.4), layout="constrained")
ax.set(xlim=(0, 10), ylim=(0, 100), xlabel="x in data units", ylabel="y in data units")
ax.plot([6], [70], "o", ms=11, color=rv.colour("red"), zorder=5)
fig.canvas.draw()                                            # layout must exist before we read positions

px = ax.transData.transform((6, 70))                         # data -> display pixels
axf = ax.transAxes.inverted().transform(px)                  # display -> axes fraction
fgf = fig.transFigure.inverted().transform(px)               # display -> figure fraction
kinds = [("data", (6, 70), "data", "(6, 70)", (-105, 35)),
         ("axes fraction", tuple(axf), "axes fraction", f"({axf[0]:.2f}, {axf[1]:.2f})", (105, 35)),
         ("figure fraction", tuple(fgf), "figure fraction", f"({fgf[0]:.2f}, {fgf[1]:.2f})", (0, -75))]
for name, xy, coords, text, off in kinds:
    ax.annotate(f"{name}\n{text}", xy=xy, xycoords=coords, xytext=off, textcoords="offset points",
                ha="center", fontsize=9.5, color=rv.colour("blue"),
                arrowprops=dict(arrowstyle="-|>", color=rv.colour("blue"), lw=1.2, shrinkA=2, shrinkB=7))
ax.text(0.98, 0.04, f"display pixels at {fig.dpi:.0f} dpi: ({px[0]:.0f}, {px[1]:.0f})\n(this one changes if you change the dpi)",
        transform=ax.transAxes, ha="right", fontsize=9, color=rv.colour("grey"))
ax.set_title("Four coordinate systems, one point")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


| System | Origin and range | Use for |
|---|---|---|
| **Data** (default) | Your numbers on the axes | Anything tied to the data, such as an arrow at a peak |
| **Axes fraction** (`transform=ax.transAxes`) | (0, 0) is bottom left of the Axes, (1, 1) is top right | Panel labels, notes, legends in fixed places |
| **Figure fraction** (`transform=fig.transFigure`) | (0, 0) is the bottom left of the whole Figure | Figure-level titles and footers |
| **Pixels / points** (`offset points`) | Measured in screen units | Small nudges that must keep their size |

Pixel size depends on dpi: a figure `6.4 x 4.8` inches at 100 dpi is 640 by 480 pixels, and at 300 dpi it is 1920 by 1440. **Figure size is in inches. One inch is 2.54 cm.**

<p align="center">
<img src="../img/layout/figure-size_light.png#gh-light-mode-only" alt="Figure size is in inches. 1 inch = 2.54 cm, so a 12 cm wide figure is 12 / 2.54 inches." width="640">
<img src="../img/layout/figure-size_dark.png#gh-dark-mode-only" alt="Figure size is in inches. 1 inch = 2.54 cm, so a 12 cm wide figure is 12 / 2.54 inches." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/figure-size_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

cm = 1 / 2.54
fig, ax = plt.subplots(figsize=(12 * cm, 7 * cm), layout="constrained")
ax.plot([0, 1, 2, 3], [0, 1, 0.5, 2], color=rv.colour("blue"))
ax.set(title="12 cm x 7 cm")
ax.text(0.5, 0.15, f"figsize = ({12 * cm:.2f}, {7 * cm:.2f}) inches\n{int(12 * cm * fig.dpi)} x {int(7 * cm * fig.dpi)} pixels at {fig.dpi:.0f} dpi",
        transform=ax.transAxes, ha="center", fontsize=8, color=rv.colour("grey"))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## Anatomy in plotnine

plotnine draws with matplotlib underneath, but names the parts differently. Every one of these is set with `theme()`.

<p align="center">
<img src="../img/anatomy/plotnine-parts_light.png#gh-light-mode-only" alt="The parts of a plotnine figure, numbered. The table beside it names each part and the call that sets it." width="640">
<img src="../img/anatomy/plotnine-parts_dark.png#gh-dark-mode-only" alt="The parts of a plotnine figure, numbered. The table beside it names each part and the call that sets it." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/anatomy/plotnine-parts_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import matplotlib.pyplot as plt

rng = np.random.default_rng(4)
epoch = np.arange(0, 13)
rows = [(p, m, e, base * np.exp(-e / (4 + k)) + 0.4 + 0.02 * rng.standard_normal())
        for p, base in (("Small models", 2.0), ("Large models", 1.6))
        for k, m in enumerate(("Whisper", "Parakeet", "Conformer")) for e in epoch]
df = pd.DataFrame(rows, columns=["panel", "model", "epoch", "loss"])
df["loss"] += df["model"].map({"Whisper": 0.0, "Parakeet": 0.35, "Conformer": 0.7})
df["panel"] = pd.Categorical(df["panel"], ["Small models", "Large models"])

p = (ggplot(df, aes("epoch", "loss", colour="model"))
     + geom_line(size=1.2)
     + facet_wrap("panel")
     + scale_colour_manual(values=rv.colour_map(["Whisper", "Parakeet", "Conformer"]))
     + labs(title="Validation loss falls with training", subtitle="Three models, two sizes",
            x="Epoch", y="Loss", colour="Model", caption="Synthetic data")
     + theme(figure_size=(8, 5.2)))
fig = p.draw()

# number tags, placed by pixel position in the 1280 x 832 picture
spots = [(690, 62), (350, 110), (190, 776), (632, 741), (58, 350), (300, 727), (572, 203), (420, 290),
         (130, 686), (285, 142), (1175, 364), (1255, 398), (275, 330), (15, 15)]
for n, (x, y) in enumerate(spots, 1):
    fig.text(x / 1280, 1 - y / 832, str(n), ha="center", va="center", fontsize=9, weight="bold",
             color=plt.rcParams["figure.facecolor"], zorder=100,
             bbox=dict(boxstyle="circle,pad=0.3", fc=rv.colour("blue"), ec="none"))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


| # | Part | Set with |
|---|---|---|
| 1 | Plot title | `labs(title=...)`, `theme(plot_title=element_text(...))` |
| 2 | Subtitle | `labs(subtitle=...)` |
| 3 | Caption | `labs(caption=...)` |
| 4 | X axis title | `labs(x=...)`, `theme(axis_title_x=...)` |
| 5 | Y axis title | `labs(y=...)`, `theme(axis_title_y=...)` |
| 6 | Axis text (tick labels) | `theme(axis_text=element_text(...))` |
| 7 | Panel grid | `theme(panel_grid_major=element_line(...))` |
| 8 | Panel background | `theme(panel_background=element_rect(...))` |
| 9 | Axis line | `theme(axis_line_x=element_line(...))` |
| 10 | Strip (facet label) | `theme(strip_text=element_text(...))` |
| 11 | Legend title | `theme(legend_title=element_text(...))`, `labs(colour=...)` |
| 12 | Legend key and text | `theme(legend_text=..., legend_key=...)` |
| 13 | Geom (the data marks) | `geom_line(size=...)` |
| 14 | Plot margin | `theme(plot_margin=...)` |

The four `element_*` helpers cover almost everything: `element_text` (words), `element_line` (lines), `element_rect` (boxes), `element_blank()` (remove it).

## Matplotlib to plotnine: a translation table

| Matplotlib | plotnine |
|---|---|
| `fig` | the `ggplot` object (`p.draw()` returns the matplotlib `fig`) |
| `ax` | a panel (several with `facet_*`) |
| `ax.set_title("t")` | `labs(title="t")` |
| `ax.set_xlabel("x")` | `labs(x="x")` |
| `ax.spines[...]` | `axis_line_*` and `panel_border` in `theme()` |
| `ax.tick_params(...)` | `axis_text`, `axis_ticks` in `theme()` |
| `ax.grid()` | `panel_grid_*` in `theme()` |
| `ax.legend()` | automatic; tune with `legend_position`, `guides()` |
| `fig.suptitle()` | `labs(title=...)` |
| `figsize=(w, h)` | `theme(figure_size=(w, h))` |
| `dpi` | `p.save("f.png", dpi=300)` |

## Size, shape and proportion

<p align="center">
<img src="../img/layout/aspect_light.png#gh-light-mode-only" alt="Aspect: equal makes a circle round, box_aspect makes the plot area a fixed shape." width="640">
<img src="../img/layout/aspect_dark.png#gh-dark-mode-only" alt="Aspect: equal makes a circle round, box_aspect makes the plot area a fixed shape." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/aspect_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.linspace(0, 2 * np.pi, 200)
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.8), layout="constrained")
for ax, name in zip(axs, ("aspect='auto'", "aspect='equal'", "set_box_aspect(1)")):
    ax.plot(2 * np.cos(t), np.sin(t), color=rv.colour("red"), lw=2.2)
    ax.set_title(name, fontsize=9)
axs[1].set_aspect("equal")
axs[2].set_box_aspect(1)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- `ax.set_aspect("equal")` makes one unit on x the same length as one on y (use for maps, circles, images).
- `ax.set_box_aspect(1)` makes the Axes box square regardless of the data.
- Keep wide data wide: time series read best near 3:1 or 2:1, scatter plots near square.

## Putting it together: a checklist for reading any figure

1. Read the **title**: what claim is being made?
2. Read both **axis labels**: what is measured, in what unit?
3. Check the **scale**: does it start at zero (bars)? Is it linear or log?
4. Find the **legend or direct labels**: what do colours mean?
5. Look at **marks**: raw data, summary or fit?
6. Read the **caption or source**: where do the data come from?

**Next:** [Choosing a plot](choosing.md).
