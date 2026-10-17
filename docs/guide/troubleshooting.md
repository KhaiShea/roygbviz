# Troubleshooting

Find the symptom, then try the fix.

## Installing

**`error: externally-managed-environment`**
Your system Python is protected. Use a virtual environment (`python3 -m venv .venv`, then activate it) and install inside it. See [Setup](setup.md).

**`ModuleNotFoundError: No module named 'roygbviz'`**
You are running a different Python from the one you installed into. Check with `which python` and `pip show roygbviz`. In Jupyter, pick the kernel that matches your venv.

## Fonts

**Fonts look wrong or plain.** Inter is not installed, so a fallback is used. Install it, then clear the matplotlib cache (see [Fonts and text](fonts.md)).

**`findfont: Font family 'X' not found`.** The name is wrong or the font is not installed. List what matplotlib can see with `sorted({f.name for f in matplotlib.font_manager.fontManager.ttflist})`.

**Bold does not work.** Variable fonts may expose only one weight. Install static font files.

**Boxes instead of characters.** The font lacks that glyph (often macrons or maths symbols). Pick a font that has it.

## Layout

**Labels are cut off when saving.** Use `layout="constrained"` when you make the figure, or `bbox_inches="tight"` on save.

<p align="center">
<img src="../img/layout/layout-engines_light.png#gh-light-mode-only" alt="No layout engine, tight_layout and constrained layout on the same content: labels collide, then get room." width="640">
<img src="../img/layout/layout-engines_dark.png#gh-dark-mode-only" alt="No layout engine, tight_layout and constrained layout on the same content: labels collide, then get room." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/layout-engines_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

def render(engine):
    fig, axs = plt.subplots(2, 2, figsize=(2.6, 2.6), dpi=130, layout=engine)
    for a in axs.ravel():
        a.plot([0, 1], [0, 1], color=rv.colour("blue"))
        a.set_xlabel("x label"); a.set_ylabel("y label"); a.set_title("title", fontsize=9)
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    return img

fig, axs = plt.subplots(1, 3, figsize=(7.4, 3), layout="constrained")
for ax, (name, engine) in zip(axs, (("no layout", None), ("layout='tight'", "tight"), ("layout='constrained'", "constrained"))):
    ax.imshow(render(engine))
    ax.set_title(name, fontsize=10)
    ax.grid(False); ax.axis("off")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


**Panels overlap.** Same fix. Do not mix `tight_layout()` and `constrained` in one figure.

**Legend covers data.** Move it outside (`bbox_to_anchor`) or use direct labels.

<p align="center">
<img src="../img/text/legend-placement_light.png#gh-light-mode-only" alt="Legend placement: loc names, an outside legend with bbox_to_anchor, and columns." width="640">
<img src="../img/text/legend-placement_dark.png#gh-dark-mode-only" alt="Legend placement: loc names, an outside legend with bbox_to_anchor, and columns." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/legend-placement_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 50)
fig, axs = plt.subplots(1, 3, figsize=(8, 3), layout="constrained")
for ax in axs:
    for k, c in enumerate(("red", "teal", "violet")):
        ax.plot(x, np.sin(x + k), color=rv.colour(c), label=f"series {k + 1}")
axs[0].legend(loc="lower left"); axs[0].set_title("loc='lower left'", fontsize=9)
axs[1].legend(loc="upper center", ncols=3, bbox_to_anchor=(0.5, -0.12)); axs[1].set_title("below, ncols=3", fontsize=9)
axs[2].legend(loc="center left", bbox_to_anchor=(1.0, 0.5)); axs[2].set_title("outside right", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


**Too many ticks.** Thin them with `MaxNLocator`.

<p align="center">
<img src="../img/ticks/too-many_light.png#gh-light-mode-only" alt="Fixing crowded ticks: thin them out with a MaxNLocator rather than shrinking the font." width="640">
<img src="../img/ticks/too-many_dark.png#gh-dark-mode-only" alt="Fixing crowded ticks: thin them out with a MaxNLocator rather than shrinking the font." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/too-many_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import ticker

x = np.arange(60)
y = np.random.default_rng(2).normal(size=60).cumsum()
fig, axs = plt.subplots(2, 1, figsize=(6.4, 4), layout="constrained")
axs[0].bar(x.astype(str), y, color=rv.colour("red")); axs[0].set_title("Every category labelled", fontsize=10)
axs[1].bar(x.astype(str), y, color=rv.colour("teal"))
axs[1].xaxis.set_major_locator(ticker.MaxNLocator(8)); axs[1].set_title("MaxNLocator(8)", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## Colours

**Everything is plain blue or has the default colours.** `rv.use()` was not called, or was called before a `plt.style.use(...)` that overrode it. Call `rv.use()` last.

**A colour changes between figures.** You let the library assign colours by order. Pin them with `rv.colour_map(labels)` and pass the same dictionary each time.

**`ValueError: Roygbviz has nine series colours`.** You asked for more than nine. Fold extras into `"Other"` or facet.

**`ValueError: role must be one of ...`.** `rv.levels()` only accepts colour or stage names, not `"grey"`. Use `rv.shade(rv.colour("grey"), k)` for greys.

## plotnine

**A legend shows nothing or the wrong colours.** Check that the column is the one mapped to `colour` or `fill`, and that you used the matching scale (`scale_colour_*` for colour, `scale_fill_*` for fill).

**`PlotnineWarning: ... scale for fill`.** A scale was added for an aesthetic that is not mapped. Remove it.

**Figure size ignored.** Set it in `theme(figure_size=(w, h))`.

**Categories in the wrong order.** Convert to an ordered category: `df["g"] = pd.Categorical(df["g"], ["low", "mid", "high"])`.

## Plots

**Bars start somewhere other than zero.** You set a limit or used a scale that crops. Remove it for bars.

**The plot is a flat line.** One series has much bigger values than the others. Try a log scale, or separate panels.

<p align="center">
<img src="../img/scales/linear-log_light.png#gh-light-mode-only" alt="Linear against log: the same data, where each gridline on the log plot is a factor of ten." width="640">
<img src="../img/scales/linear-log_dark.png#gh-dark-mode-only" alt="Linear against log: the same data, where each gridline on the log plot is a factor of ten." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/linear-log_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0.1, 5, 100)
y = 10 ** x
fig, axs = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
axs[0].plot(x, y, color=rv.colour("red")); axs[0].set_title("Linear", fontsize=10)
axs[1].plot(x, y, color=rv.colour("red")); axs[1].set_yscale("log"); axs[1].set_title("set_yscale('log')", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


**Points hide each other.** Use transparency or binning.

<p align="center">
<img src="../img/gg/choose-overplot_light.png#gh-light-mode-only" alt="Overplotting: ten thousand points hide the shape. Transparency or binning shows where the data is dense." width="640">
<img src="../img/gg/choose-overplot_dark.png#gh-dark-mode-only" alt="Overplotting: ten thousand points hide the shape. Transparency or binning shows where the data is dense." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/choose-overplot_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
df = pd.DataFrame({"x": rng.normal(size=10000)}); df["y"] = 0.6 * df["x"] + rng.normal(size=10000)

bad = ggplot(df, aes("x", "y")) + geom_point(colour=rv.colour("red")) + labs(title="Solid points: a blob")
good = ggplot(df, aes("x", "y")) + geom_bin_2d(bins=40) + scale_fill_gradientn(colors=[rv.cmap("blue")(i) for i in np.linspace(0, 1, 7)]) + labs(title="2D bins: the density shows") + theme(legend_position="none")
p = bad | good

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Dates look cramped.** Use `ConciseDateFormatter`.

<p align="center">
<img src="../img/ticks/dates_light.png#gh-light-mode-only" alt="Dates: ConciseDateFormatter picks sensible labels at any zoom level, with the year shown once." width="640">
<img src="../img/ticks/dates_dark.png#gh-dark-mode-only" alt="Dates: ConciseDateFormatter picks sensible labels at any zoom level, with the year shown once." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/dates_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import matplotlib.dates as mdates
import pandas as pd

t = pd.date_range("2026-01-01", periods=240, freq="D")
y = np.random.default_rng(1).normal(size=240).cumsum()
fig, axs = plt.subplots(2, 1, figsize=(6.4, 4.4), layout="constrained")
axs[0].plot(t, y, color=rv.colour("blue")); axs[0].set_title("Default date labels", fontsize=10)
plt.setp(axs[0].get_xticklabels(), rotation=0)
axs[1].plot(t, y, color=rv.colour("blue"))
loc = mdates.AutoDateLocator()
axs[1].xaxis.set_major_locator(loc)
axs[1].xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
axs[1].set_title("ConciseDateFormatter", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


**Circles look like ovals.** Set `ax.set_aspect("equal")`.

## Notebooks

**Figures do not appear.** Add `%matplotlib inline`, or call `plt.show()`.

**Figures look blurry.** Add `%config InlineBackend.figure_format = "retina"`.

**Old settings stick around.** Restart the kernel; rcParams persist until then. To avoid it, use `with plt.rc_context({...}):`.

<p align="center">
<img src="../img/style/rc-context_light.png#gh-light-mode-only" alt="rc_context: change settings for one figure only, then go back automatically." width="640">
<img src="../img/style/rc-context_dark.png#gh-dark-mode-only" alt="rc_context: change settings for one figure only, then go back automatically." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/style/rc-context_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.linspace(0, 6, 80)
fig = plt.figure(figsize=(7, 2.8))
for k, lw in enumerate((1, 2.5, 5)):
    with plt.rc_context({"lines.linewidth": lw, "axes.grid": k == 1}):
        ax = fig.add_subplot(1, 3, k + 1)
        ax.plot(t, np.sin(t), color=rv.colour("blue"))
        ax.set_title(f"lines.linewidth={lw}", fontsize=9)
fig.tight_layout()

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## Still stuck?

1. Make the smallest example that shows the problem.
2. Print the versions: `import matplotlib, plotnine; print(matplotlib.__version__, plotnine.__version__)`.
3. Search the error text, then ask with the example and versions.

**Next:** [Glossary](glossary.md).
