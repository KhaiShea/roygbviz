# Statistics: distributions, errors and boxes

These charts show the shape and spread of data, and how sure you can be about it. They are the figures a reviewer asks for.

**Matplotlib reference:** `ax.hist`, `ax.boxplot`, `ax.violinplot`, `ax.errorbar`, `ax.hexbin`, `ax.ecdf`. In plotnine: `geom_histogram`, `geom_boxplot`, `geom_violin`, `geom_density`, `geom_errorbar`, `stat_ecdf`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Histograms and densities**: Histogram, Bins, density and weights, Histogram types, Several histograms, Bihistogram, Cumulative histogram, ECDF, Density curve, Hexbin, 2D histogram of series
- **Boxes and violins**: Box plot, Styled box plot, Notched box plot, Box from saved statistics, Box against violin, Violin plot, Custom violin, Strip plot, Raincloud plot
- **Errors and uncertainty**: Error bars, Ways to give errors, Limits, Every nth error bar, Error band, Error boxes, Confidence ellipse, Regression with a band, Forest plot, Bland-Altman plot, Q-Q plot
- **Signals**: Power spectral density, Cross spectral density, Coherence, Cross and auto correlation

## Histograms and densities

### Histogram

<p align="center">
<img src="../img/stats/hist-basic_light.png#gh-light-mode-only" alt="A histogram: how many values fall in each bin." width="640">
<img src="../img/stats/hist-basic_dark.png#gh-dark-mode-only" alt="A histogram: how many values fall in each bin." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/hist-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(4)
data = rng.normal(70, 8, 1000)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.hist(data, bins=30, color=rv.shade("blue"), edgecolor=rv.colour("blue"))
ax.axvline(data.mean(), color=rv.colour("red"), lw=2, label=f"mean {data.mean():.1f}")
ax.legend()
ax.set(xlabel="listener score", ylabel="count", title="Histogram")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** The shape of one variable.
- **Key calls:** `ax.hist(x, bins=30)`
- **Watch out:** Try several bin counts; the shape depends on them.

### Bins, density and weights

<p align="center">
<img src="../img/stats/hist-bins_light.png#gh-light-mode-only" alt="Bins, density and weights: the same data with 5, 30 and 100 bins, as counts and as a density." width="640">
<img src="../img/stats/hist-bins_dark.png#gh-dark-mode-only" alt="Bins, density and weights: the same data with 5, 30 and 100 bins, as counts and as a density." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/hist-bins_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(6)
data = rng.normal(0, 1, 1200)
fig, axs = plt.subplots(1, 3, figsize=(7.2, 3), sharex=True, layout="constrained")
for ax, bins in zip(axs, (5, 30, 100)):
    ax.hist(data, bins=bins, density=True, color=rv.shade("teal"), edgecolor=rv.colour("teal"), lw=0.5)
    xs = np.linspace(-4, 4, 200)
    ax.plot(xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), color=rv.colour("red"), lw=2)
    ax.set_title(f"bins={bins}", fontsize=10)
axs[0].set_ylabel("density")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Comparing groups of different sizes.
- **Key calls:** `ax.hist(x, bins=, density=True, weights=)`
- **Watch out:** Use `density=True` when sample sizes differ.

### Histogram types

<p align="center">
<img src="../img/stats/hist-types_light.png#gh-light-mode-only" alt="The four histtype settings: bar, barstacked, step and stepfilled." width="640">
<img src="../img/stats/hist-types_dark.png#gh-dark-mode-only" alt="The four histtype settings: bar, barstacked, step and stepfilled." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/hist-types_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(5)
a, b = rng.normal(0, 1, 600), rng.normal(1.2, 1.1, 600)
fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.6), sharex=True, sharey=True, layout="constrained")
for ax, kind in zip(axs.ravel(), ("bar", "barstacked", "step", "stepfilled")):
    ax.hist([a, b], bins=20, histtype=kind, color=[rv.colour("red"), rv.colour("blue")], alpha=0.85)
    ax.set_title(f'histtype="{kind}"', fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Bars, stacked, outline or filled outline.
- **Key calls:** `histtype='bar'`, `'barstacked'`, `'step'`, `'stepfilled'`
- **Watch out:** Outlines compare overlapping groups better than filled bars.

### Several histograms

<p align="center">
<img src="../img/stats/hist-multiple_light.png#gh-light-mode-only" alt="Several datasets on one histogram, side by side, with a shared set of bins." width="640">
<img src="../img/stats/hist-multiple_dark.png#gh-dark-mode-only" alt="Several datasets on one histogram, side by side, with a shared set of bins." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/hist-multiple_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
data = {"Whisper": rng.normal(3.1, 0.8, 500), "Parakeet": rng.normal(3.6, 1.0, 500), "Conformer": rng.normal(4.4, 1.2, 500)}
cm = rv.colour_map(list(data))
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.hist(list(data.values()), bins=np.linspace(0, 8, 17), color=[cm[k] for k in data], label=list(data))
ax.legend()
ax.set(xlabel="word error rate (%)", ylabel="utterances", title="Three models, one set of bins")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Side-by-side groups.
- **Key calls:** `ax.hist([a, b, c], bins=edges)`
- **Watch out:** Share bin edges.

### Bihistogram

<p align="center">
<img src="../img/stats/bihistogram_light.png#gh-light-mode-only" alt="A bihistogram: two distributions mirrored on a shared axis, for a direct before-and-after." width="640">
<img src="../img/stats/bihistogram_dark.png#gh-dark-mode-only" alt="A bihistogram: two distributions mirrored on a shared axis, for a direct before-and-after." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/bihistogram_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(8)
a, b = rng.normal(5, 1.4, 800), rng.normal(6.2, 1.1, 800)
bins = np.linspace(0, 10, 31)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ca, _ = np.histogram(a, bins)
cb, _ = np.histogram(b, bins)
ax.stairs(ca, bins, fill=True, color=rv.shade("red"))
ax.stairs(ca, bins, color=rv.colour("red"), lw=2)
ax.stairs(-cb, bins, fill=True, baseline=0, color=rv.shade("blue"))
ax.stairs(-cb, bins, baseline=0, color=rv.colour("blue"), lw=2)
ax.axhline(0, color=plt.rcParams["text.color"], lw=1)
ax.text(0.2, ca.max() * 0.9, "before", color=rv.colour("red"), weight="bold")
ax.text(0.2, -cb.max() * 0.9, "after", color=rv.colour("blue"), weight="bold")
ax.set(xlabel="score", ylabel="count (after shown below zero)", title="Bihistogram")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Two groups mirrored.
- **Key calls:** `ax.hist(a)` and `ax.hist(b, weights=-1)`
- **Watch out:** Share the x axis.

### Cumulative histogram

<p align="center">
<img src="../img/stats/cumulative_light.png#gh-light-mode-only" alt="A cumulative histogram: what fraction of values are below each point." width="640">
<img src="../img/stats/cumulative_dark.png#gh-dark-mode-only" alt="A cumulative histogram: what fraction of values are below each point." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/cumulative_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(9)
data = rng.lognormal(5.5, 0.4, 1000)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.hist(data, bins=60, density=True, cumulative=True, histtype="stepfilled", color=rv.shade("blue"), edgecolor=rv.colour("blue"))
ax.axhline(0.95, color=rv.colour("red"), ls="--", lw=1.5)
ax.text(data.min(), 0.97, "95% of requests", ha="left", va="bottom", fontsize=8.5, color=rv.colour("red"))
ax.set(xlabel="response time (ms)", ylabel="fraction of requests", title="Cumulative distribution")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Share of values below a point.
- **Key calls:** `ax.hist(x, cumulative=True, density=True)`
- **Watch out:** ECDF avoids bins.

### ECDF

<p align="center">
<img src="../img/stats/ecdf_light.png#gh-light-mode-only" alt="An ECDF: every value drawn as a step, no bins and no smoothing. The fairest way to compare distributions." width="640">
<img src="../img/stats/ecdf_dark.png#gh-dark-mode-only" alt="An ECDF: every value drawn as a step, no bins and no smoothing. The fairest way to compare distributions." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/ecdf_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(23)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.lognormal(m, 0.35, 300) for m in (5.4, 5.6, 5.9)]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
for n, d in zip(names, data):
    ax.ecdf(d, color=cm[n], lw=2.2, label=n)
ax.axhline(0.5, color=rv.colour("grey"), lw=1, ls=":")
ax.legend(loc="lower right")
ax.set(xlabel="response time (ms)", ylabel="fraction of requests at or below", title="Empirical CDF")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Comparing distributions without bins.
- **Key calls:** `ax.ecdf(x)`
- **Watch out:** Read percentiles straight off the curve.

### Density curve

<p align="center">
<img src="../img/stats/kde_light.png#gh-light-mode-only" alt="A smooth density curve (kernel density estimate) with a rug of the real values underneath." width="640">
<img src="../img/stats/kde_dark.png#gh-dark-mode-only" alt="A smooth density curve (kernel density estimate) with a rug of the real values underneath." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/kde_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from scipy.stats import gaussian_kde

rng = np.random.default_rng(24)
d = np.concatenate([rng.normal(3, 0.6, 120), rng.normal(5.5, 0.9, 80)])
xs = np.linspace(0, 9, 300)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.fill_between(xs, gaussian_kde(d)(xs), color=rv.shade("teal"))
ax.plot(xs, gaussian_kde(d)(xs), color=rv.colour("teal"), lw=2.5)
ax.plot(d, np.full_like(d, -0.012), "|", color=rv.colour("teal"), ms=10, alpha=0.6)
ax.set(xlabel="score", ylabel="density", title="Density with a rug")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A smooth shape.
- **Key calls:** `scipy.stats.gaussian_kde(x)`
- **Watch out:** Smoothing can invent features; show raw data too.

### Hexbin

<p align="center">
<img src="../img/stats/hexbin_light.png#gh-light-mode-only" alt="A hexagonal bin plot: a scatter plot that stays readable when there are thousands of points." width="640">
<img src="../img/stats/hexbin_dark.png#gh-dark-mode-only" alt="A hexagonal bin plot: a scatter plot that stays readable when there are thousands of points." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/hexbin_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(10)
x = rng.normal(0, 1, 20000)
y = 0.6 * x + rng.normal(0, 0.8, 20000)
fig, ax = plt.subplots(figsize=(5.6, 4.4), layout="constrained")
hb = ax.hexbin(x, y, gridsize=28, cmap="roygbviz", mincnt=1)
fig.colorbar(hb, ax=ax, label="points per hexagon", shrink=0.85)
ax.set(xlabel="x", ylabel="y", title="Hexbin of 20 000 points")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Dense scatter plots.
- **Key calls:** `ax.hexbin(x, y, gridsize=30)`
- **Watch out:** Add a colourbar labelled count.

### 2D histogram of series

<p align="center">
<img src="../img/stats/time-series-hist_light.png#gh-light-mode-only" alt="A two-dimensional histogram of many time series, so the typical path and its spread show as one image." width="640">
<img src="../img/stats/time-series-hist_dark.png#gh-dark-mode-only" alt="A two-dimensional histogram of many time series, so the typical path and its spread show as one image." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/time-series-hist_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(11)
t = np.linspace(0, 10, 100)
runs = np.cumsum(rng.normal(0.02, 0.15, (500, t.size)), axis=1)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
h = ax.hist2d(np.tile(t, 500), runs.ravel(), bins=(60, 50), cmap="roygbviz")
fig.colorbar(h[3], ax=ax, label="paths through each cell", shrink=0.85)
ax.set(xlabel="time", ylabel="value", title="500 random walks as one picture")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Many time series at once.
- **Key calls:** `ax.hist2d(t, y, bins=)`
- **Watch out:** Normalise each column to compare shapes.

## Boxes and violins

### Box plot

<p align="center">
<img src="../img/stats/boxplot-basic_light.png#gh-light-mode-only" alt="A box plot: the median, the middle half of the data, the whiskers and the outliers." width="640">
<img src="../img/stats/boxplot-basic_dark.png#gh-dark-mode-only" alt="A box plot: the median, the middle half of the data, the whiskers and the outliers." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/boxplot-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(12)
data = [rng.normal(m, s, 100) for m, s in ((3.1, 0.8), (3.6, 1.0), (4.4, 1.5))]
fig, ax = plt.subplots(figsize=(6, 3.8), layout="constrained")
ax.boxplot(data, tick_labels=["Whisper", "Parakeet", "Conformer"])
ax.set(ylabel="word error rate (%)", title="Box plot")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Median, spread and outliers per group.
- **Key calls:** `ax.boxplot(data, tick_labels=)`
- **Watch out:** Boxes hide shape; add points for small samples.

### Styled box plot

<p align="center">
<img src="../img/stats/boxplot-styled_light.png#gh-light-mode-only" alt="Customising every part of a box plot: boxes, medians, whiskers, caps and outlier points." width="640">
<img src="../img/stats/boxplot-styled_dark.png#gh-dark-mode-only" alt="Customising every part of a box plot: boxes, medians, whiskers, caps and outlier points." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/boxplot-styled_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(13)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.normal(m, s, 100) for m, s in ((3.1, 0.8), (3.6, 1.0), (4.4, 1.5))]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6, 3.8), layout="constrained")
bp = ax.boxplot(data, tick_labels=names, patch_artist=True, widths=0.55, showfliers=True,
                medianprops=dict(color=plt.rcParams["text.color"], lw=2.2),
                flierprops=dict(marker="o", ms=4, mfc="none", mec=rv.colour("grey")))
for patch, n in zip(bp["boxes"], names):
    patch.set(facecolor=rv.shade(cm[n]), edgecolor=cm[n], lw=2)
for key in ("whiskers", "caps"):
    for i, line in enumerate(bp[key]):
        line.set(color=cm[names[i // 2]], lw=1.8)
ax.set(ylabel="word error rate (%)", title="A styled box plot")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Matching a house style.
- **Key calls:** `boxprops`, `medianprops`, `whiskerprops`, `flierprops`
- **Watch out:** Roygbviz sets sensible defaults.

### Notched box plot

<p align="center">
<img src="../img/stats/boxplot-notched_light.png#gh-light-mode-only" alt="A notched box plot, horizontal: if the notches do not overlap, the medians probably differ." width="640">
<img src="../img/stats/boxplot-notched_dark.png#gh-dark-mode-only" alt="A notched box plot, horizontal: if the notches do not overlap, the medians probably differ." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/boxplot-notched_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(14)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.normal(m, s, 150) for m, s in ((3.1, 0.8), (3.2, 1.0), (4.4, 1.5))]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6.2, 3.4), layout="constrained")
bp = ax.boxplot(data, orientation="horizontal", notch=True, patch_artist=True, tick_labels=names, widths=0.55,
                medianprops=dict(color=plt.rcParams["text.color"], lw=2))
for patch, n in zip(bp["boxes"], names):
    patch.set(facecolor=rv.shade(cm[n]), edgecolor=cm[n], lw=2)
ax.set(xlabel="word error rate (%)", title="Notched boxes")
ax.grid(axis="x", visible=True); ax.grid(axis="y", visible=False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A rough test of median differences.
- **Key calls:** `ax.boxplot(data, notch=True)`
- **Watch out:** Notches are a guide, not a test.

### Box from saved statistics

<p align="center">
<img src="../img/stats/boxplot-stats_light.png#gh-light-mode-only" alt="Calculate the box statistics yourself with boxplot_stats, then draw them with bxp (for example from saved summaries)." width="640">
<img src="../img/stats/boxplot-stats_dark.png#gh-dark-mode-only" alt="Calculate the box statistics yourself with boxplot_stats, then draw them with bxp (for example from saved summaries)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/boxplot-stats_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.cbook import boxplot_stats

rng = np.random.default_rng(15)
data = rng.lognormal(3, 0.5, 200)
stats = boxplot_stats(data, labels=["latency"])
fig, ax = plt.subplots(figsize=(4.8, 3.8), layout="constrained")
ax.bxp(stats, boxprops=dict(color=rv.colour("blue"), lw=2), medianprops=dict(color=rv.colour("red"), lw=2.2),
       whiskerprops=dict(color=rv.colour("blue")), capprops=dict(color=rv.colour("blue")))
for key in ("whislo", "q1", "med", "q3", "whishi"):
    ax.text(1.32, stats[0][key], f"{key} = {stats[0][key]:.0f}", va="center", fontsize=8.5)
ax.set(xlim=(0.6, 2.0), ylabel="latency (ms)", title="Box plot from statistics")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Plotting summaries you saved earlier.
- **Key calls:** `cbook.boxplot_stats`, `ax.bxp(stats)`
- **Watch out:** Useful for huge datasets.

### Box against violin

<p align="center">
<img src="../img/stats/box-vs-violin_light.png#gh-light-mode-only" alt="The same data as a box plot and as a violin plot: the violin also shows the shape." width="640">
<img src="../img/stats/box-vs-violin_dark.png#gh-dark-mode-only" alt="The same data as a box plot and as a violin plot: the violin also shows the shape." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/box-vs-violin_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(16)
data = [np.concatenate([rng.normal(3, 0.5, 150), rng.normal(6, 0.7, 100)]), rng.normal(4.5, 1.2, 250), rng.normal(4, 0.6, 250)]
fig, axs = plt.subplots(1, 2, figsize=(7, 3.6), sharey=True, layout="constrained")
axs[0].boxplot(data, tick_labels=["bimodal", "wide", "narrow"])
axs[0].set_title("Box plot", fontsize=10)
vp = axs[1].violinplot(data, showmedians=True)
axs[1].set_xticks([1, 2, 3], ["bimodal", "wide", "narrow"])
axs[1].set_title("Violin plot", fontsize=10)
for b in vp["bodies"]:
    b.set(facecolor=rv.shade("blue"), edgecolor=rv.colour("blue"), alpha=0.9)
for k in ("cmedians", "cmins", "cmaxes", "cbars"):
    vp[k].set(color=rv.colour("blue"))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Choosing between them.
- **Key calls:** `ax.boxplot`, `ax.violinplot`
- **Watch out:** Violins show multiple peaks; boxes do not.

### Violin plot

<p align="center">
<img src="../img/stats/violin-basic_light.png#gh-light-mode-only" alt="A violin plot of three groups, with the median marked." width="640">
<img src="../img/stats/violin-basic_dark.png#gh-dark-mode-only" alt="A violin plot of three groups, with the median marked." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/violin-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(17)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.normal(m, s, 300) for m, s in ((3.1, 0.8), (3.6, 1.0), (4.4, 1.5))]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6, 3.8), layout="constrained")
vp = ax.violinplot(data, showextrema=False, showmedians=True)
for b, n in zip(vp["bodies"], names):
    b.set(facecolor=rv.shade(cm[n]), edgecolor=cm[n], alpha=1, lw=2)
vp["cmedians"].set(color=plt.rcParams["text.color"], lw=2)
ax.set_xticks([1, 2, 3], names)
ax.set(ylabel="word error rate (%)", title="Violin plot")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Distribution shape per group.
- **Key calls:** `ax.violinplot(data, showmedians=True)`
- **Watch out:** Needs at least about 30 points per group.

### Custom violin

<p align="center">
<img src="../img/stats/violin-custom_light.png#gh-light-mode-only" alt="A customised violin: half violins, quartile marks and the individual points." width="640">
<img src="../img/stats/violin-custom_dark.png#gh-dark-mode-only" alt="A customised violin: half violins, quartile marks and the individual points." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/violin-custom_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(18)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.normal(m, s, 200) for m, s in ((3.1, 0.8), (3.6, 1.0), (4.4, 1.5))]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6, 3.8), layout="constrained")
vp = ax.violinplot(data, showextrema=False, side="low", widths=0.9)
for b, n in zip(vp["bodies"], names):
    b.set(facecolor=rv.shade(cm[n]), edgecolor=cm[n], alpha=1)
for i, (d, n) in enumerate(zip(data, names), 1):
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    ax.vlines(i, q1, q3, color=cm[n], lw=6)
    ax.scatter(i, med, s=40, color=plt.rcParams["figure.facecolor"], zorder=3)
    ax.scatter(i + rng.uniform(0.05, 0.3, 40), rng.choice(d, 40), s=6, color=cm[n], alpha=0.6)
ax.set_xticks([1, 2, 3], names)
ax.set(ylabel="word error rate (%)", title="Half violins with quartiles and points")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Half violins with quartiles and points.
- **Key calls:** `parts['bodies']`, `ax.scatter`
- **Watch out:** Show data points when you can.

### Strip plot

<p align="center">
<img src="../img/stats/strip-jitter_light.png#gh-light-mode-only" alt="A strip plot: every observation as a dot, spread sideways (jitter) so they do not hide each other, with the mean marked." width="640">
<img src="../img/stats/strip-jitter_dark.png#gh-dark-mode-only" alt="A strip plot: every observation as a dot, spread sideways (jitter) so they do not hide each other, with the mean marked." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/strip-jitter_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(27)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.normal(m, s, 60) for m, s in ((3.1, 0.8), (3.6, 1.0), (4.4, 1.5))]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6, 3.8), layout="constrained")
for i, (n, d) in enumerate(zip(names, data)):
    ax.scatter(i + rng.uniform(-0.18, 0.18, d.size), d, s=16, color=cm[n], alpha=0.65)
    ax.hlines(d.mean(), i - 0.3, i + 0.3, color=plt.rcParams["text.color"], lw=2.5)
ax.set_xticks(range(3), names)
ax.set(ylabel="word error rate (%)", title="Every observation, with the mean")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Small samples per group.
- **Key calls:** `ax.scatter(x + jitter, y)`
- **Watch out:** Jitter in x only.

### Raincloud plot

<p align="center">
<img src="../img/stats/raincloud_light.png#gh-light-mode-only" alt="A raincloud plot: half a violin (the cloud), the raw points (the rain) and a box, all in one." width="640">
<img src="../img/stats/raincloud_dark.png#gh-dark-mode-only" alt="A raincloud plot: half a violin (the cloud), the raw points (the rain) and a box, all in one." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/raincloud_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(28)
names = ["Whisper", "Parakeet", "Conformer"]
data = [rng.normal(m, s, 80) for m, s in ((3.1, 0.8), (3.6, 1.0), (4.4, 1.5))]
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6.2, 3.8), layout="constrained")
vp = ax.violinplot(data, showextrema=False, side="high", widths=0.8)
for b, n in zip(vp["bodies"], names):
    b.set(facecolor=rv.shade(cm[n]), edgecolor=cm[n], alpha=1)
bp = ax.boxplot(data, widths=0.1, positions=[0.82, 1.82, 2.82], showfliers=False, patch_artist=True,
                medianprops=dict(color=plt.rcParams["text.color"], lw=2))
for p, n in zip(bp["boxes"], names):
    p.set(facecolor=rv.shade(cm[n]), edgecolor=cm[n])
for i, (n, d) in enumerate(zip(names, data)):
    ax.scatter(i + 0.62 + rng.uniform(-0.06, 0.06, d.size), d, s=6, color=cm[n], alpha=0.7)
ax.set_xticks([1, 2, 3], names)
ax.set(ylabel="word error rate (%)", title="Raincloud plot")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Shape, points and summary together.
- **Key calls:** Half violin, jittered points, thin box
- **Watch out:** Best default for a few groups.

## Errors and uncertainty

### Error bars

<p align="center">
<img src="../img/stats/errorbar-basic_light.png#gh-light-mode-only" alt="Error bars in y, in x, and in both." width="640">
<img src="../img/stats/errorbar-basic_dark.png#gh-dark-mode-only" alt="Error bars in y, in x, and in both." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/errorbar-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)
fig, axs = plt.subplots(1, 3, figsize=(7, 3), sharey=True, layout="constrained")
kw = dict(fmt="o", capsize=3, color=rv.colour("blue"), ecolor=rv.colour("grey"), elinewidth=1.4)
axs[0].errorbar(x, y, yerr=0.1 + 0.1 * np.sqrt(x), **kw)
axs[1].errorbar(x, y, xerr=0.25, **kw)
axs[2].errorbar(x, y, xerr=0.25, yerr=0.1 + 0.1 * np.sqrt(x), **kw)
for a, t in zip(axs, ("yerr", "xerr", "both")):
    a.set_title(t, fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Uncertainty on means.
- **Key calls:** `ax.errorbar(x, y, yerr=, xerr=)`
- **Watch out:** Say what the bar is: SD, SEM or 95% CI.

### Ways to give errors

<p align="center">
<img src="../img/stats/errorbar-styles_light.png#gh-light-mode-only" alt="Ways to specify errors: one number, one per point, or different above and below." width="640">
<img src="../img/stats/errorbar-styles_dark.png#gh-dark-mode-only" alt="Ways to specify errors: one number, one per point, or different above and below." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/errorbar-styles_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(6)
y = np.array([3.0, 4.1, 3.6, 5.2, 4.8, 6.0])
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.errorbar(x - 0.15, y, yerr=0.5, fmt="o", capsize=3, color=rv.colour("red"), label="one value for all")
ax.errorbar(x, y + 1.5, yerr=np.linspace(0.2, 1.0, 6), fmt="s", capsize=3, color=rv.colour("teal"), label="one per point")
ax.errorbar(x + 0.15, y + 3, yerr=[np.full(6, 0.3), np.full(6, 0.9)], fmt="D", capsize=3, color=rv.colour("violet"),
            label="asymmetric [below, above]")
ax.legend(loc="upper left")
ax.set(ylim=(1.5, 11.5), title="Specifying error bars")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Constant, per-point and asymmetric errors.
- **Key calls:** `yerr=[lower, upper]`
- **Watch out:** Asymmetric errors need a 2 by N array.

### Limits

<p align="center">
<img src="../img/stats/errorbar-limits_light.png#gh-light-mode-only" alt="Upper and lower limits: arrows say 'at least this much' or 'at most this much'." width="640">
<img src="../img/stats/errorbar-limits_dark.png#gh-dark-mode-only" alt="Upper and lower limits: arrows say 'at least this much' or 'at most this much'." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/errorbar-limits_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(5)
y = np.array([2.0, 3.2, 2.8, 4.1, 3.5])
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.errorbar(x, y, yerr=0.6, fmt="o", color=rv.colour("blue"), capsize=3, label="measured")
ax.errorbar(x, y + 2, yerr=0.8, uplims=True, fmt="o", color=rv.colour("red"), label="upper limit")
ax.errorbar(x, y + 4, yerr=0.8, lolims=True, fmt="o", color=rv.colour("teal"), label="lower limit")
ax.legend(loc="upper left", ncols=3)
ax.set(ylim=(0, 9.8), title="Limits on error bars")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** At least, or at most, values.
- **Key calls:** `lolims=True`, `uplims=True`
- **Watch out:** Explain the arrows in the caption.

### Every nth error bar

<p align="center">
<img src="../img/stats/errorbar-subsample_light.png#gh-light-mode-only" alt="errorevery draws an error bar on every nth point only, so dense data stay readable." width="640">
<img src="../img/stats/errorbar-subsample_dark.png#gh-dark-mode-only" alt="errorevery draws an error bar on every nth point only, so dense data stay readable." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/errorbar-subsample_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 6, 120)
y = np.sin(x) + 2
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.errorbar(x, y, yerr=0.25, errorevery=10, color=rv.colour("blue"), ecolor=rv.colour("grey"), capsize=3, lw=2)
ax.errorbar(x, y - 1.2, yerr=0.25, errorevery=(5, 15), color=rv.colour("violet"), ecolor=rv.colour("grey"), capsize=3, lw=2)
ax.set(title="errorevery=10 (top) and errorevery=(5, 15) (bottom)")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Dense data.
- **Key calls:** `errorevery=5`
- **Watch out:** Do not hide large errors.

### Error band

<p align="center">
<img src="../img/stats/error-band_light.png#gh-light-mode-only" alt="A curve with an error band: the neater alternative to many error bars." width="640">
<img src="../img/stats/error-band_dark.png#gh-dark-mode-only" alt="A curve with an error band: the neater alternative to many error bars." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/error-band_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
x = np.linspace(0, 10, 40)
runs = np.sin(x) + rng.normal(0, 0.25, (8, x.size))
mean, sd = runs.mean(0), runs.std(0)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
for r in runs:
    ax.plot(x, r, color=rv.colour("grey"), lw=0.7, alpha=0.5)
ax.fill_between(x, mean - sd, mean + sd, color=rv.shade("blue"), label="mean ± 1 sd")
ax.plot(x, mean, color=rv.colour("blue"), lw=2.5, label="mean of 8 runs")
ax.legend(loc="upper right")
ax.set(xlabel="epoch", title="Eight runs and their average")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Smooth uncertainty on a curve.
- **Key calls:** `ax.fill_between(x, y - e, y + e)`
- **Watch out:** Neater than many bars.

### Error boxes

<p align="center">
<img src="../img/stats/error-boxes_light.png#gh-light-mode-only" alt="Error boxes: a rectangle that spans the uncertainty in both directions." width="640">
<img src="../img/stats/error-boxes_dark.png#gh-dark-mode-only" alt="Error boxes: a rectangle that spans the uncertainty in both directions." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/error-boxes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

rng = np.random.default_rng(3)
x = np.array([1.0, 2.2, 3.1, 4.4])
y = np.array([2.0, 3.6, 2.7, 4.8])
xe, ye = rng.uniform(0.2, 0.5, 4), rng.uniform(0.3, 0.8, 4)
boxes = [Rectangle((a - e, b - f), 2 * e, 2 * f) for a, b, e, f in zip(x, y, xe, ye)]
fig, ax = plt.subplots(figsize=(5.6, 3.8), layout="constrained")
ax.add_collection(PatchCollection(boxes, facecolor=rv.shade("orange"), edgecolor=rv.colour("orange"), alpha=0.9))
ax.errorbar(x, y, fmt="o", color=rv.colour("orange"))
ax.set(xlim=(0, 5.5), ylim=(1, 6), title="Error boxes")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Uncertainty in both directions.
- **Key calls:** `PatchCollection` of rectangles
- **Watch out:** Use a light shade.

### Confidence ellipse

<p align="center">
<img src="../img/stats/confidence-ellipse_light.png#gh-light-mode-only" alt="A confidence ellipse around a two-variable dataset, at 1, 2 and 3 standard deviations." width="640">
<img src="../img/stats/confidence-ellipse_dark.png#gh-dark-mode-only" alt="A confidence ellipse around a two-variable dataset, at 1, 2 and 3 standard deviations." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/confidence-ellipse_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D

def ellipse(x, y, ax, n_std, **kw):
    cov = np.cov(x, y)
    r = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    e = Ellipse((0, 0), 2 * np.sqrt(1 + r), 2 * np.sqrt(1 - r), **kw)
    e.set_transform(Affine2D().rotate_deg(45).scale(np.sqrt(cov[0, 0]) * n_std, np.sqrt(cov[1, 1]) * n_std)
                    .translate(x.mean(), y.mean()) + ax.transData)
    return ax.add_patch(e)

rng = np.random.default_rng(2)
x = rng.normal(0, 1.2, 400)
y = 0.7 * x + rng.normal(0, 0.9, 400)
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
ax.scatter(x, y, s=10, color=rv.colour("grey"), alpha=0.6)
for n_std, col in ((1, "teal"), (2, "blue"), (3, "violet")):
    ellipse(x, y, ax, n_std, fc="none", ec=rv.colour(col), lw=2, label=f"{n_std} sd")
ax.legend(loc="upper left")
ax.set(aspect="equal", title="Confidence ellipses")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Spread of two variables.
- **Key calls:** `matplotlib.patches.Ellipse` from the covariance
- **Watch out:** State the level (for example 95%).

### Regression with a band

<p align="center">
<img src="../img/stats/regression-band_light.png#gh-light-mode-only" alt="A fitted line with a bootstrap confidence band: how sure are we about the trend?" width="640">
<img src="../img/stats/regression-band_dark.png#gh-dark-mode-only" alt="A fitted line with a bootstrap confidence band: how sure are we about the trend?" width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/regression-band_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(26)
x = rng.uniform(0, 10, 60)
y = 1.5 + 0.6 * x + rng.normal(0, 1.2, 60)
grid = np.linspace(0, 10, 100)
boots = []
for _ in range(500):
    i = rng.integers(0, len(x), len(x))
    boots.append(np.polyval(np.polyfit(x[i], y[i], 1), grid))
lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.scatter(x, y, s=22, color=rv.colour("grey"), alpha=0.8)
ax.fill_between(grid, lo, hi, color=rv.shade("blue"), label="95% bootstrap band")
ax.plot(grid, np.polyval(np.polyfit(x, y, 1), grid), color=rv.colour("blue"), lw=2.5, label="fitted line")
ax.legend(loc="upper left")
ax.set(xlabel="audio length (s)", ylabel="latency (s)", title="Trend with uncertainty")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Trend with its uncertainty.
- **Key calls:** Bootstrap with `np.polyfit` in a loop
- **Watch out:** A line without a band overstates certainty.

### Forest plot

<p align="center">
<img src="../img/stats/forest-plot_light.png#gh-light-mode-only" alt="A forest plot: an estimate and its confidence interval for each model, against a reference line." width="640">
<img src="../img/stats/forest-plot_dark.png#gh-dark-mode-only" alt="A forest plot: an estimate and its confidence interval for each model, against a reference line." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/forest-plot_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["Whisper", "Parakeet", "Conformer", "Canary", "Kokoro"]
diff = np.array([-1.2, -0.4, 0.6, -0.9, 0.1])
lo, hi = diff - np.array([0.5, 0.6, 0.7, 0.4, 0.5]), diff + np.array([0.6, 0.5, 0.8, 0.5, 0.6])
y = np.arange(len(names))[::-1]
sig = (hi < 0) | (lo > 0)
fig, ax = plt.subplots(figsize=(6.2, 3.6), layout="constrained")
ax.axvline(0, color=rv.colour("grey"), lw=1.5, ls="--")
for yi, d, l, h, s in zip(y, diff, lo, hi, sig):
    c = rv.colour("red") if s else rv.colour("grey")
    ax.hlines(yi, l, h, color=c, lw=2.5)
    ax.scatter(d, yi, s=60, color=c, zorder=3)
ax.set_yticks(y, names)
ax.set(xlabel="change in word error rate against the baseline (points)", title="Differences with 95% intervals")
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Estimates and intervals for many items.
- **Key calls:** `ax.errorbar(est, y, xerr=ci, fmt='o')`
- **Watch out:** Add a reference line (often zero or one).

### Bland-Altman plot

<p align="center">
<img src="../img/stats/bland-altman_light.png#gh-light-mode-only" alt="A Bland-Altman plot: agreement between two ways of measuring the same thing (for example human and automatic scores)." width="640">
<img src="../img/stats/bland-altman_dark.png#gh-dark-mode-only" alt="A Bland-Altman plot: agreement between two ways of measuring the same thing (for example human and automatic scores)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/bland-altman_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(29)
truth = rng.uniform(2, 5, 80)
a = truth + rng.normal(0, 0.15, 80)
b = truth + 0.1 + rng.normal(0, 0.2, 80)
mean, diff = (a + b) / 2, a - b
md, sd = diff.mean(), diff.std()
fig, ax = plt.subplots(figsize=(6.2, 3.8), layout="constrained")
ax.scatter(mean, diff, s=20, color=rv.colour("blue"), alpha=0.8)
ax.axhline(md, color=rv.colour("red"), lw=2)
for k in (-1.96, 1.96):
    ax.axhline(md + k * sd, color=rv.colour("red"), lw=1.2, ls="--")
ax.text(5.0, md + 1.96 * sd + 0.02, "+1.96 sd", ha="right", fontsize=8.5, color=rv.colour("red"))
ax.text(5.0, md - 1.96 * sd - 0.02, "-1.96 sd", ha="right", va="top", fontsize=8.5, color=rv.colour("red"))
ax.set(xlabel="mean of the two scores", ylabel="difference (human minus automatic)", title="Bland-Altman agreement plot")
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Agreement between two measures.
- **Key calls:** Plot difference against mean with limits
- **Watch out:** Report the mean difference and limits.

### Q-Q plot

<p align="center">
<img src="../img/stats/qq-plot_light.png#gh-light-mode-only" alt="A Q-Q plot: if the points hug the line, the data look normally distributed." width="640">
<img src="../img/stats/qq-plot_dark.png#gh-dark-mode-only" alt="A Q-Q plot: if the points hug the line, the data look normally distributed." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/qq-plot_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from scipy import stats

rng = np.random.default_rng(25)
fig, axs = plt.subplots(1, 2, figsize=(7, 3.4), layout="constrained")
for ax, d, name in ((axs[0], rng.normal(0, 1, 200), "normal data"), (axs[1], rng.lognormal(0, 0.8, 200), "skewed data")):
    (osm, osr), (slope, icpt, _) = stats.probplot(d)
    ax.scatter(osm, osr, s=14, color=rv.colour("blue"))
    ax.plot(osm, slope * osm + icpt, color=rv.colour("red"), lw=2)
    ax.set(title=name, xlabel="theoretical quantiles")
axs[0].set_ylabel("sample quantiles")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Is the data normal?
- **Key calls:** `scipy.stats.probplot(x, plot=ax)`
- **Watch out:** Look at the tails.

## Signals

### Power spectral density

<p align="center">
<img src="../img/stats/psd_light.png#gh-light-mode-only" alt="Power spectral density: how much power the signal has at each frequency." width="640">
<img src="../img/stats/psd_dark.png#gh-dark-mode-only" alt="Power spectral density: how much power the signal has at each frequency." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/psd_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(20)
fs = 1000
t = np.arange(0, 5, 1 / fs)
sig = np.sin(2 * np.pi * 60 * t) + 0.4 * np.sin(2 * np.pi * 150 * t) + rng.normal(0, 1, t.size)
fig, (a, b) = plt.subplots(2, 1, figsize=(6.4, 4.4), layout="constrained")
a.plot(t[:300], sig[:300], color=rv.colour("blue"), lw=1)
a.set(xlabel="time (s)", title="Signal (first 0.3 s)")
b.psd(sig, NFFT=512, Fs=fs, color=rv.colour("red"))
b.set(title="Power spectral density")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Frequency content.
- **Key calls:** `ax.psd(x, Fs=fs)`
- **Watch out:** Check units (dB per Hz).

### Cross spectral density

<p align="center">
<img src="../img/stats/csd_light.png#gh-light-mode-only" alt="Cross spectral density: the shared frequency content of two signals." width="640">
<img src="../img/stats/csd_dark.png#gh-dark-mode-only" alt="Cross spectral density: the shared frequency content of two signals." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/csd_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(21)
fs = 1000
t = np.arange(0, 10, 1 / fs)
common = np.sin(2 * np.pi * 80 * t)
a_sig = common + rng.normal(0, 1, t.size)
b_sig = 0.8 * common + rng.normal(0, 1, t.size)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.csd(a_sig, b_sig, NFFT=512, Fs=fs, color=rv.colour("violet"))
ax.set(title="Cross spectral density (peak at the shared 80 Hz tone)")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Shared frequency content.
- **Key calls:** `ax.csd(x, y, Fs=fs)`
- **Watch out:** Needs the same sampling rate.

### Coherence

<p align="center">
<img src="../img/stats/coherence_light.png#gh-light-mode-only" alt="Coherence of two signals: near 1 at frequencies where one follows the other, near 0 elsewhere." width="640">
<img src="../img/stats/coherence_dark.png#gh-dark-mode-only" alt="Coherence of two signals: near 1 at frequencies where one follows the other, near 0 elsewhere." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/coherence_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(22)
fs = 1000
t = np.arange(0, 20, 1 / fs)
common = np.sin(2 * np.pi * 80 * t)
a_sig = common + rng.normal(0, 1, t.size) + np.sin(2 * np.pi * 200 * t)
b_sig = 0.8 * common + rng.normal(0, 1, t.size) + np.sin(2 * np.pi * 220 * t)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.cohere(a_sig, b_sig, NFFT=512, Fs=fs, color=rv.colour("teal"))
ax.set(title="Coherence")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** How linked two signals are by frequency.
- **Key calls:** `ax.cohere(x, y, Fs=fs)`
- **Watch out:** Values range from 0 to 1.

### Cross and auto correlation

<p align="center">
<img src="../img/stats/xcorr-acorr_light.png#gh-light-mode-only" alt="Cross-correlation and auto-correlation of two noisy signals." width="640">
<img src="../img/stats/xcorr-acorr_dark.png#gh-dark-mode-only" alt="Cross-correlation and auto-correlation of two noisy signals." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/xcorr-acorr_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(19)
x, y = rng.standard_normal(200).cumsum(), rng.standard_normal(200).cumsum()
fig, (a, b) = plt.subplots(2, 1, figsize=(6.4, 4.4), sharex=True, layout="constrained")
a.xcorr(x, y, usevlines=True, maxlags=50, normed=True, lw=2, color=rv.colour("blue"))
a.axhline(0, color=plt.rcParams["axes.edgecolor"], lw=1)
a.set_title("Cross-correlation", fontsize=10)
b.acorr(x, usevlines=True, normed=True, maxlags=50, lw=2, color=rv.colour("red"))
b.axhline(0, color=plt.rcParams["axes.edgecolor"], lw=1)
b.set_title("Auto-correlation", fontsize=10)
b.set_xlabel("lag")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Lag between signals.
- **Key calls:** `ax.xcorr(x, y)`, `ax.acorr(x)`
- **Watch out:** A peak at lag 0 means in step.

## Rules of thumb

- **Show the data** when you can (points, rain) and the summary beside it.
- **Say what your error bar is** every time.
- **Same bins** when histograms are compared.
- **A bigger n** makes boxes and violins more trustworthy.

**Back to the [home page](../index.md).**
