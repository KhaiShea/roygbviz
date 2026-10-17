# Scatter, fills and areas

Scatter plots show how two numbers relate. Fills and areas show ranges, totals and gaps.

**Matplotlib reference:** `ax.scatter`, `ax.fill_between`, `ax.stackplot`, `ax.step`, `ax.stem`, `ax.eventplot`. In plotnine: `geom_point`, `geom_ribbon`, `geom_area`, `geom_step`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Scatter plots**: Basic scatter, Size and colour, Legends for colour and size, Masked points, Marginal histograms
- **Ranges and areas**: Band between curves, Conditional fill, Shaded spans, Polygon, Stacked area, Streamgraph
- **Steps, stems and events**: Step plot, Stairs, Stem plot, Event plot, Timeline, Many short lines, Plot by category names, Gaps for missing data, Signal spectra

## Scatter plots

### Basic scatter

<p align="center">
<img src="../img/scatter/basic_light.png#gh-light-mode-only" alt="A scatter plot of quality against latency with every point labelled." width="640">
<img src="../img/scatter/basic_dark.png#gh-dark-mode-only" alt="A scatter plot of quality against latency with every point labelled." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scatter/basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Canary", "Kokoro", "Piper"]
latency = np.array([310, 420, 520, 380, 650, 480])
quality = np.array([4.5, 4.3, 4.0, 4.4, 4.2, 3.9])
cm = rv.colour_map(models)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
ax.scatter(latency, quality, s=90, c=[cm[m] for m in models], zorder=3)
for m, x, y in zip(models, latency, quality):
    ax.annotate(m, (x, y), xytext=(8, 4), textcoords="offset points", fontsize=9)
ax.set(xlabel="Latency (ms), lower is better", ylabel="Quality (MOS), higher is better",
       xlim=(250, 720), ylim=(3.7, 4.7), title="Quality against latency")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Relationship between two numbers.
- **Key calls:** `ax.scatter(x, y, s=, color=)`
- **Watch out:** Label only the few points that matter.

### Size and colour

<p align="center">
<img src="../img/scatter/size-and-colour_light.png#gh-light-mode-only" alt="Mapping three more variables to a point: size is parameters, colour is cost." width="640">
<img src="../img/scatter/size-and-colour_dark.png#gh-dark-mode-only" alt="Mapping three more variables to a point: size is parameters, colour is cost." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scatter/size-and-colour_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(5)
n = 40
x = rng.uniform(100, 900, n)                      # latency
y = 5.2 - 0.0018 * x + rng.normal(0, 0.25, n)     # quality
params = rng.uniform(0.1, 70, n)                  # billions of parameters
cost = rng.uniform(0.2, 6, n)                     # dollars per hour
fig, ax = plt.subplots(figsize=(6.4, 4.2), layout="constrained")
sc = ax.scatter(x, y, s=params * 6 + 20, c=cost, cmap="roygbviz", alpha=0.85, edgecolor=plt.rcParams["figure.facecolor"], lw=0.8)
fig.colorbar(sc, ax=ax, label="Cost ($ per hour)", shrink=0.85)
ax.set(xlabel="Latency (ms)", ylabel="Quality (MOS)", title="Four variables in one plot")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Up to four variables on one plot.
- **Key calls:** `ax.scatter(x, y, s=size, c=value, cmap='roygbviz')`
- **Watch out:** Size reads poorly; use only when needed, and add a colourbar.

### Legends for colour and size

<p align="center">
<img src="../img/scatter/legend_light.png#gh-light-mode-only" alt="A scatter plot with two legends: one for the colour groups and one for the sizes." width="640">
<img src="../img/scatter/legend_dark.png#gh-dark-mode-only" alt="A scatter plot with two legends: one for the colour groups and one for the sizes." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scatter/legend_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.lines import Line2D

rng = np.random.default_rng(6)
stages = ["STT", "LLM", "TTS"]
stage = rv.group_map()
fig, ax = plt.subplots(figsize=(6.4, 4.2), layout="constrained")
for s_name in stages:
    pts = rng.normal({"STT": (2, 3), "LLM": (5, 6), "TTS": (4, 2)}[s_name], 0.9, (14, 2))
    ax.scatter(*pts.T, s=rng.uniform(20, 220, 14), color=stage[s_name], alpha=0.8, label=s_name,
               edgecolor=plt.rcParams["figure.facecolor"])
first = ax.legend(title="Stage", loc="upper left")
ax.add_artist(first)
sizes = [Line2D([], [], marker="o", ls="", color=rv.colour("grey"), ms=np.sqrt(s), label=f"{lab}")
         for s, lab in ((30, "small"), (100, "medium"), (220, "large"))]
ax.legend(handles=sizes, title="Model size", loc="lower right")
ax.set(xlabel="x", ylabel="y", title="Two legends on one plot")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Explaining two encodings.
- **Key calls:** `ax.legend(*sc.legend_elements(), title=...)`
- **Watch out:** Keep one legend per encoding, clearly titled.

### Masked points

<p align="center">
<img src="../img/scatter/masked_light.png#gh-light-mode-only" alt="Masked values: points beyond a threshold are drawn in another colour, or hidden." width="640">
<img src="../img/scatter/masked_dark.png#gh-dark-mode-only" alt="Masked values: points beyond a threshold are drawn in another colour, or hidden." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scatter/masked_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
x = rng.uniform(0, 1, 120)
y = rng.uniform(0, 1, 120)
r = np.hypot(x - 0.5, y - 0.5)
inside = np.ma.masked_where(r > 0.35, r)                          # hidden where r > 0.35
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
ax.scatter(x, y, color=rv.colour("grey"), alpha=0.5, label="outside the circle")
sc = ax.scatter(x, y, c=inside, cmap="roygbviz", s=45)
fig.colorbar(sc, ax=ax, label="distance from the centre", shrink=0.8)
ax.set(aspect="equal", xlim=(0, 1), ylim=(0, 1), title="Masked scatter")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), fontsize=8)
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Highlight values over a threshold.
- **Key calls:** `np.ma.masked_where(cond, y)`
- **Watch out:** Say what the threshold is.

### Marginal histograms

<p align="center">
<img src="../img/scatter/marginal_light.png#gh-light-mode-only" alt="A scatter plot with a histogram of each variable along its edge." width="640">
<img src="../img/scatter/marginal_dark.png#gh-dark-mode-only" alt="A scatter plot with a histogram of each variable along its edge." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scatter/marginal_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(8)
x = rng.normal(0, 1, 500)
y = 0.6 * x + rng.normal(0, 0.8, 500)
fig = plt.figure(figsize=(5.6, 5.2), layout="constrained")
gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4), hspace=0.03, wspace=0.03)
ax = fig.add_subplot(gs[1, 0])
top = fig.add_subplot(gs[0, 0], sharex=ax)
right = fig.add_subplot(gs[1, 1], sharey=ax)
ax.scatter(x, y, s=16, alpha=0.6, color=rv.colour("teal"))
top.hist(x, bins=30, color=rv.shade("teal"), edgecolor=rv.colour("teal"))
right.hist(y, bins=30, orientation="horizontal", color=rv.shade("teal"), edgecolor=rv.colour("teal"))
for a in (top, right):
    a.grid(False)
    a.tick_params(labelbottom=False, labelleft=False)
ax.grid(axis="x", visible=True)
ax.set(xlabel="x", ylabel="y")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A scatter plus the distribution of each variable.
- **Key calls:** `fig.add_gridspec` with ratios; `ax.hist`
- **Watch out:** Share axes with `sharex` and `sharey`.

## Ranges and areas

### Band between curves

<p align="center">
<img src="../img/fill/between_light.png#gh-light-mode-only" alt="fill_between() shades the space between two curves: the usual way to draw an uncertainty band." width="640">
<img src="../img/fill/between_dark.png#gh-dark-mode-only" alt="fill_between() shades the space between two curves: the usual way to draw an uncertainty band." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/between_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(10)
x = np.linspace(0, 10, 60)
mean = 2 * np.log1p(x)
sd = 0.25 + 0.06 * x
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.fill_between(x, mean - 2 * sd, mean + 2 * sd, color=rv.shade("blue", 2), label="95% band")
ax.fill_between(x, mean - sd, mean + sd, color=rv.shade("blue", 1), label="68% band")
ax.plot(x, mean, color=rv.colour("blue"), lw=2.5, label="mean")
ax.legend(loc="upper left")
ax.set(xlabel="epoch", ylabel="score", title="A curve with an uncertainty band")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Uncertainty around a line.
- **Key calls:** `ax.fill_between(x, lo, hi, alpha=0.3)`
- **Watch out:** Say what the band is (standard deviation, 95% interval).

### Conditional fill

<p align="center">
<img src="../img/fill/between-where_light.png#gh-light-mode-only" alt="fill_between(where=...) colours the gaps differently depending on which curve is ahead." width="640">
<img src="../img/fill/between-where_dark.png#gh-dark-mode-only" alt="fill_between(where=...) colours the gaps differently depending on which curve is ahead." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/between-where_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 300)
a = 3 + np.sin(x) * 1.5
b = 3 + np.cos(0.8 * x) * 1.2
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.fill_between(x, a, b, where=a >= b, interpolate=True, color=rv.shade("red"), label="model A ahead")
ax.fill_between(x, a, b, where=a < b, interpolate=True, color=rv.shade("blue"), label="model B ahead")
ax.plot(x, a, color=rv.colour("red"), lw=2)
ax.plot(x, b, color=rv.colour("blue"), lw=2)
ax.legend(ncols=2, loc="upper center", bbox_to_anchor=(0.5, 1.0))
ax.set(ylim=(0.5, 6), xlabel="time", title="Who is ahead, and when")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Which curve is ahead.
- **Key calls:** `fill_between(..., where=a > b)`
- **Watch out:** Use two colours with different meanings.

### Shaded spans

<p align="center">
<img src="../img/fill/spans_light.png#gh-light-mode-only" alt="axvspan() and axhspan() shade a whole band of the plot; fill_betweenx() fills between curves sideways." width="640">
<img src="../img/fill/spans_dark.png#gh-dark-mode-only" alt="axvspan() and axhspan() shade a whole band of the plot; fill_betweenx() fills between curves sideways." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/spans_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 200)
y = np.sin(x) + 0.1 * x
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.axvspan(2.5, 4.5, color=rv.shade("orange"), label="fine-tuning")
ax.axhspan(-0.2, 0.2, color=rv.shade("teal"), alpha=0.8, label="acceptable range")
ax.plot(x, y, color=rv.colour("blue"), lw=2.2)
ax.legend(loc="upper left", ncols=2)
ax.set(ylim=(-1.4, 2.0), title="Shaded regions")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Highlight a period or range.
- **Key calls:** `ax.axvspan(x0, x1)`, `ax.axhspan(y0, y1)`
- **Watch out:** Keep the shade pale so the data stays visible.

### Polygon

<p align="center">
<img src="../img/fill/polygon_light.png#gh-light-mode-only" alt="fill() paints a polygon from a list of points." width="640">
<img src="../img/fill/polygon_dark.png#gh-dark-mode-only" alt="fill() paints a polygon from a list of points." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/polygon_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.linspace(0, 2 * np.pi, 11)[:-1]
r = np.where(np.arange(10) % 2 == 0, 1.0, 0.45)
fig, ax = plt.subplots(figsize=(4.6, 4.2), layout="constrained")
ax.fill(r * np.cos(t), r * np.sin(t), color=rv.shade("orange"), ec=rv.colour("orange"), lw=2.5)
ax.fill([1.3, 1.9, 1.6], [0.2, 0.2, 0.9], color=rv.shade("violet"), ec=rv.colour("violet"), lw=2.5)
ax.set(aspect="equal", xlim=(-1.3, 2.1), ylim=(-1.3, 1.3), title="Filled polygons")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Custom shaded regions.
- **Key calls:** `ax.fill(xs, ys)`
- **Watch out:** Check the points are in order, or it twists.

### Stacked area

<p align="center">
<img src="../img/fill/stackplot_light.png#gh-light-mode-only" alt="A stacked area chart: how a total is made of parts over time." width="640">
<img src="../img/fill/stackplot_dark.png#gh-dark-mode-only" alt="A stacked area chart: how a total is made of parts over time." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/stackplot_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.arange(2018, 2027)
parts = {"Whisper": [5, 9, 16, 26, 35, 41, 44, 45, 46], "Parakeet": [0, 0, 2, 7, 14, 21, 26, 30, 33],
         "Other": [20, 19, 17, 15, 13, 11, 9, 8, 7]}
cm = rv.colour_map(list(parts))
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.stackplot(t, list(parts.values()), colors=[rv.shade(cm[k]) for k in parts], edgecolors=[cm[k] for k in parts],
             linewidths=1.2, labels=list(parts))
ax.legend(loc="upper left")
ax.set(xlim=(t[0], t[-1]), ylabel="Share of downloads (%)", title="Stacked area")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** How a total is made of parts over time.
- **Key calls:** `ax.stackplot(x, ys, labels=)`
- **Watch out:** The middle layers are hard to read; prefer small multiples for many parts.

### Streamgraph

<p align="center">
<img src="../img/fill/streamgraph_light.png#gh-light-mode-only" alt="A streamgraph: a stack that is centred and wiggles, so shapes are easy to follow." width="640">
<img src="../img/fill/streamgraph_dark.png#gh-dark-mode-only" alt="A streamgraph: a stack that is centred and wiggles, so shapes are easy to follow." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/streamgraph_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(11)
x = np.linspace(0, 10, 100)
layers = [np.abs(np.sin(x * f + p)) * a + 0.2 for f, p, a in ((0.8, 0, 2), (1.1, 1, 1.4), (0.6, 2, 2.4), (1.5, 3, 1))]
cols = [rv.colour(c) for c in ("red", "teal", "violet", "orange")]
fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
ax.stackplot(x, layers, baseline="wiggle", colors=cols, edgecolor=plt.rcParams["figure.facecolor"], linewidth=0.8)
ax.set(xlim=(0, 10), title="Streamgraph")
ax.set_yticks([]); ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Shapes of many categories over time (decorative).
- **Key calls:** `stackplot(..., baseline='wiggle')`
- **Watch out:** Trades accuracy for looks. Use for overview only.

## Steps, stems and events

### Step plot

<p align="center">
<img src="../img/fill/step_light.png#gh-light-mode-only" alt="step() with where='pre', 'mid' and 'post' decides which side of each point the step sits." width="640">
<img src="../img/fill/step_dark.png#gh-dark-mode-only" alt="step() with where='pre', 'mid' and 'post' decides which side of each point the step sits." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/step_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(8)
y = np.array([1, 3, 2, 5, 4, 6, 3, 4])
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
for where, col in (("pre", "red"), ("mid", "teal"), ("post", "violet")):
    ax.step(x, y, where=where, color=rv.colour(col), lw=2.2, label=f'where="{where}"')
ax.plot(x, y, "o--", color=rv.colour("grey"), lw=1, label="the data")
ax.legend(ncols=2, loc="upper left")
ax.set(ylim=(0, 8), title="Step plots")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Values that hold until the next change.
- **Key calls:** `ax.step(x, y, where='post')`
- **Watch out:** Choose `where` to match how the data is measured.

### Stairs

<p align="center">
<img src="../img/fill/stairs_light.png#gh-light-mode-only" alt="stairs() draws a step outline from bin heights and edges: the honest way to show a histogram's counts." width="640">
<img src="../img/fill/stairs_dark.png#gh-dark-mode-only" alt="stairs() draws a step outline from bin heights and edges: the honest way to show a histogram's counts." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/stairs_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(9)
counts, edges = np.histogram(rng.normal(0, 1, 800), bins=24)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.stairs(counts, edges, fill=True, color=rv.shade("blue"), alpha=0.9)
ax.stairs(counts, edges, color=rv.colour("blue"), lw=2)
ax.set(xlabel="value", ylabel="count", title="Stairs")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Histogram outlines from bin counts.
- **Key calls:** `ax.stairs(values, edges)`
- **Watch out:** Use for pre-binned data.

### Stem plot

<p align="center">
<img src="../img/fill/stem_light.png#gh-light-mode-only" alt="A stem plot: a vertical line to each value. Good for discrete signals and sparse counts." width="640">
<img src="../img/fill/stem_dark.png#gh-dark-mode-only" alt="A stem plot: a vertical line to each value. Good for discrete signals and sparse counts." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/stem_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(0, 16)
y = np.exp(-x / 6) * np.cos(x)
fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
m, s, base = ax.stem(x, y)
plt.setp(m, color=rv.colour("red"), markersize=8)
plt.setp(s, color=rv.colour("grey"), linewidth=1.8)
plt.setp(base, color=plt.rcParams["axes.edgecolor"])
ax.set(xlabel="sample", title="Stem plot")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Discrete signals and sparse counts.
- **Key calls:** `ax.stem(x, y)`
- **Watch out:** Use bars for categories, stems for samples.

### Event plot

<p align="center">
<img src="../img/fill/eventplot_light.png#gh-light-mode-only" alt="An event plot (raster): one row per source, one tick for each event. Handy for turn-taking and word timings." width="640">
<img src="../img/fill/eventplot_dark.png#gh-dark-mode-only" alt="An event plot (raster): one row per source, one tick for each event. Handy for turn-taking and word timings." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/eventplot_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(12)
rows = ["Speaker A", "Speaker B", "Silence markers"]
events = [np.sort(rng.uniform(0, 30, 24)), np.sort(rng.uniform(0, 30, 18)), np.sort(rng.uniform(0, 30, 8))]
fig, ax = plt.subplots(figsize=(6.4, 3), layout="constrained")
ax.eventplot(events, colors=[rv.colour("red"), rv.colour("blue"), rv.colour("grey")], lineoffsets=[2, 1, 0], linelengths=0.7,
             linewidths=2)
ax.set_yticks([2, 1, 0], rows)
ax.set(xlabel="time (s)", title="Event plot")
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** When events occurred (turn-taking, word timings).
- **Key calls:** `ax.eventplot(list_of_times)`
- **Watch out:** One row per source, same time axis.

### Timeline

<p align="center">
<img src="../img/fill/timeline_light.png#gh-light-mode-only" alt="A timeline: stems of different heights stop the labels from colliding." width="640">
<img src="../img/fill/timeline_dark.png#gh-dark-mode-only" alt="A timeline: stems of different heights stop the labels from colliding." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/timeline_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import datetime as dt

ev = [("2017", "Transformer"), ("2019", "BERT"), ("2020", "wav2vec 2.0"), ("2022", "Whisper"), ("2023", "Llama 2"), ("2024", "Voice agents")]
dates = [dt.date(int(y), 6, 1) for y, _ in ev]
levels = np.tile([-4, 4, -2.5, 2.5, -1.2, 1.2], 2)[:len(ev)]
fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
ax.axhline(0, color=rv.colour("grey"), lw=2)
ax.vlines(dates, 0, levels, color=rv.colour("teal"), lw=1.5)
ax.scatter(dates, np.zeros(len(dates)), s=70, color=rv.colour("teal"), zorder=3)
for d, lv, (y, name) in zip(dates, levels, ev):
    ax.annotate(f"{name}\n{y}", (d, lv), xytext=(0, 4 if lv > 0 else -4), textcoords="offset points", ha="center",
                va="bottom" if lv > 0 else "top", fontsize=9)
ax.set(ylim=(-6.5, 6.5), title="Speech and language milestones")
ax.set_yticks([]); ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Dated milestones.
- **Key calls:** `ax.stem(dates, levels)` with text
- **Watch out:** Vary stem heights so labels do not collide.

### Many short lines

<p align="center">
<img src="../img/fill/hlines-vlines_light.png#gh-light-mode-only" alt="hlines() and vlines() draw many short lines at once: ranges, error spans and thresholds." width="640">
<img src="../img/fill/hlines-vlines_dark.png#gh-dark-mode-only" alt="hlines() and vlines() draw many short lines at once: ranges, error spans and thresholds." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/hlines-vlines_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(13)
y = np.arange(6)
lo = rng.uniform(1, 4, 6)
hi = lo + rng.uniform(1, 4, 6)
fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
ax.hlines(y, lo, hi, color=rv.colour("blue"), lw=5, capstyle="round")
ax.vlines([5.0], -0.5, 5.5, color=rv.colour("red"), ls="--", lw=1.5, label="threshold")
ax.legend(loc="lower right")
ax.set(ylim=(-0.5, 5.5), xlabel="value", title="Ranges with hlines and vlines")
ax.set_yticks(y, [f"run {i + 1}" for i in y])
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Ranges and thresholds.
- **Key calls:** `ax.hlines(y, xmin, xmax)`, `ax.vlines(x, ymin, ymax)`
- **Watch out:** Prefer a single call to a loop.

### Plot by category names

<p align="center">
<img src="../img/fill/categorical_light.png#gh-light-mode-only" alt="Plotting straight from category names: matplotlib turns strings into positions for you." width="640">
<img src="../img/fill/categorical_dark.png#gh-dark-mode-only" alt="Plotting straight from category names: matplotlib turns strings into positions for you." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/categorical_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["STT", "LLM", "TTS"]
values = [180, 520, 210]
fig, axs = plt.subplots(1, 3, figsize=(6.8, 3), sharey=True, layout="constrained")
axs[0].bar(names, values, color=[rv.group_map()[n] for n in names])
axs[1].scatter(names, values, s=80, color=[rv.group_map()[n] for n in names])
axs[2].plot(names, values, "o-", color=rv.colour("grey"))
for a, t in zip(axs, ("bar", "scatter", "plot")):
    a.set_title(t, fontsize=10)
axs[0].set_ylabel("Latency (ms)")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Quick charts with strings on the axis.
- **Key calls:** `ax.bar(['a', 'b'], [1, 2])`
- **Watch out:** Set the order yourself with `set_xticks`.

### Gaps for missing data

<p align="center">
<img src="../img/fill/nan-gaps_light.png#gh-light-mode-only" alt="NaN and masked values make gaps instead of being joined, so missing data looks missing." width="640">
<img src="../img/fill/nan-gaps_dark.png#gh-dark-mode-only" alt="NaN and masked values make gaps instead of being joined, so missing data looks missing." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/nan-gaps_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 60)
y = np.sin(x)
y_nan = y.copy(); y_nan[20:28] = np.nan
y_mask = np.ma.masked_where((x > 6.5) & (x < 8), y)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.plot(x, y_nan + 2.5, "o-", ms=4, label="NaN values", color=rv.colour("teal"))
ax.plot(x, y_mask, "o-", ms=4, label="masked array", color=rv.colour("violet"))
ax.legend(loc="lower left", ncols=2)
ax.set(ylim=(-1.6, 4.2), title="Gaps for missing data")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Missing values should look missing.
- **Key calls:** `y[mask] = np.nan`
- **Watch out:** Never fill gaps with zero.

### Signal spectra

<p align="center">
<img src="../img/fill/spectrum_light.png#gh-light-mode-only" alt="A signal and three views of its spectrum: magnitude, angle and phase." width="640">
<img src="../img/fill/spectrum_dark.png#gh-dark-mode-only" alt="A signal and three views of its spectrum: magnitude, angle and phase." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/fill/spectrum_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(14)
fs = 1000
t = np.arange(0, 1, 1 / fs)
sig = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + 0.2 * rng.standard_normal(t.size)
fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.6), layout="constrained")
axs[0, 0].plot(t[:200], sig[:200], color=rv.colour("blue"), lw=1.2); axs[0, 0].set_title("Signal (first 0.2 s)", fontsize=10)
axs[0, 1].magnitude_spectrum(sig, Fs=fs, color=rv.colour("red")); axs[0, 1].set_title("Magnitude spectrum", fontsize=10)
axs[1, 0].angle_spectrum(sig, Fs=fs, color=rv.colour("teal")); axs[1, 0].set_title("Angle spectrum", fontsize=10)
axs[1, 1].phase_spectrum(sig, Fs=fs, color=rv.colour("violet")); axs[1, 1].set_title("Phase spectrum", fontsize=10)
for a in axs.ravel()[1:]:
    a.set_xlim(0, 250)
    a.set_xlabel("frequency (Hz)")
axs[0, 0].set_xlabel("time (s)")
for a in axs.ravel():
    a.set_ylabel("")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Frequency content of a signal.
- **Key calls:** `ax.magnitude_spectrum`, `ax.angle_spectrum`, `ax.phase_spectrum`
- **Watch out:** Use a log or dB scale for a wide range.

## Rules of thumb

- **Use transparency** (`alpha=0.4`) when points overlap.
- **Equal aspect** for scatter plots of two variables in the same units.
- **Never fill under a line** unless the area means something.
- **Add a line or band for the trend**, not only the cloud.

**Back to the [home page](../index.md).**
