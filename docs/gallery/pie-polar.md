# Pie and polar charts

Charts built on angles. Use them sparingly: people compare angles less accurately than lengths, so a bar chart is usually clearer.

**Matplotlib reference:** `ax.pie`, `plt.subplot(projection='polar')`. In plotnine: `coord_polar`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Pie and donut**: Pie chart, Donut, Nested pie, Bar of pie, Labelling
- **Polar axes**: Line on polar axes, Polar bars, Polar scatter, Polar error bars, Radar chart

## Pie and donut

### Pie chart

<p align="center">
<img src="../img/pie/basic_light.png#gh-light-mode-only" alt="A pie chart with percentage labels and one slice pulled out. Use it rarely: see the chart chooser." width="640">
<img src="../img/pie/basic_dark.png#gh-dark-mode-only" alt="A pie chart with percentage labels and one slice pulled out. Use it rarely: see the chart chooser." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/pie/basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

stages = ["STT", "LLM", "TTS"]
ms = [190, 480, 210]
fig, ax = plt.subplots(figsize=(4.8, 4.2), layout="constrained")
ax.pie(ms, labels=stages, colors=[rv.group_map()[s] for s in stages], autopct="%1.0f%%", startangle=90, counterclock=False,
       explode=(0, 0.06, 0), wedgeprops=dict(edgecolor=plt.rcParams["figure.facecolor"], linewidth=2),
       textprops=dict(color=plt.rcParams["text.color"]), pctdistance=0.68)
ax.set_title("Share of latency")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Two or three parts, one clearly large.
- **Key calls:** `ax.pie(values, labels=, autopct='%1.0f%%')`
- **Watch out:** More than four slices becomes unreadable; use bars.

### Donut

<p align="center">
<img src="../img/pie/donut_light.png#gh-light-mode-only" alt="A donut chart: a pie with the middle cut out, which leaves room for the total." width="640">
<img src="../img/pie/donut_dark.png#gh-dark-mode-only" alt="A donut chart: a pie with the middle cut out, which leaves room for the total." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/pie/donut_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

stages = ["STT", "LLM", "TTS"]
ms = [190, 480, 210]
fig, ax = plt.subplots(figsize=(4.8, 4.2), layout="constrained")
ax.pie(ms, colors=[rv.group_map()[s] for s in stages], startangle=90, counterclock=False,
       wedgeprops=dict(width=0.38, edgecolor=plt.rcParams["figure.facecolor"], linewidth=3))
ax.text(0, 0.05, f"{sum(ms)} ms", ha="center", va="center", fontsize=18, weight="bold")
ax.text(0, -0.2, "total latency", ha="center", va="center", fontsize=9, color=rv.colour("grey"))
ax.legend(stages, loc="lower center", ncols=3, bbox_to_anchor=(0.5, -0.08), frameon=False)
ax.set_title("Where the time goes", loc="center")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A pie with a central total.
- **Key calls:** `ax.pie(values, wedgeprops=dict(width=0.4))`
- **Watch out:** Same limits as a pie.

### Nested pie

<p align="center">
<img src="../img/pie/nested_light.png#gh-light-mode-only" alt="A nested pie: an inner ring for the stage and an outer ring for the models inside it." width="640">
<img src="../img/pie/nested_dark.png#gh-dark-mode-only" alt="A nested pie: an inner ring for the stage and an outer ring for the models inside it." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/pie/nested_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

stages = {"STT": {"Whisper": 90, "Parakeet": 60, "Conformer": 40}, "LLM": {"Llama": 260, "Qwen": 140, "Gemma": 80},
          "TTS": {"Kokoro": 110, "Piper": 60, "XTTS": 40}}
gm = rv.group_map()
inner = [sum(v.values()) for v in stages.values()]
outer = [x for v in stages.values() for x in v.values()]
out_cols = []
for s, v in stages.items():
    out_cols += rv.levels(s, 5)[1:4]
fig, ax = plt.subplots(figsize=(5.4, 4.6), layout="constrained")
kw = dict(startangle=90, counterclock=False)
ax.pie(outer, radius=1.0, colors=out_cols, wedgeprops=dict(width=0.32, edgecolor=plt.rcParams["figure.facecolor"], lw=2), **kw)
ax.pie(inner, radius=0.68, colors=[gm[s] for s in stages], labels=list(stages), labeldistance=0.45,
       wedgeprops=dict(width=0.32, edgecolor=plt.rcParams["figure.facecolor"], lw=2),
       textprops=dict(color=plt.rcParams["figure.facecolor"], weight="bold", ha="center"), **kw)
ax.set_title("Stage (inside) and model (outside)", loc="center")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Two levels, such as stage and model.
- **Key calls:** Two `ax.pie` calls with different `radius`
- **Watch out:** Hard to read exactly; add a table.

### Bar of pie

<p align="center">
<img src="../img/pie/bar-of-pie_light.png#gh-light-mode-only" alt="A bar of pie: one slice is broken down into a stacked bar, with lines linking the two." width="640">
<img src="../img/pie/bar-of-pie_dark.png#gh-dark-mode-only" alt="A bar of pie: one slice is broken down into a stacked bar, with lines linking the two." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/pie/bar-of-pie_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import ConnectionPatch

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.8), gridspec_kw=dict(width_ratios=[1.4, 0.8]), layout="constrained")
ratios = [0.55, 0.30, 0.15]
labels = ["Whisper", "Parakeet", "Other"]
cols = [rv.colour("red"), rv.colour("yellow"), rv.colour("violet")]
ax1.pie(ratios, labels=labels, colors=cols, autopct="%.0f%%", startangle=-0.15 * 360 * 0 + 90, counterclock=False,
        wedgeprops=dict(edgecolor=plt.rcParams["figure.facecolor"], lw=2))
sub = [0.45, 0.30, 0.15, 0.10]
sub_labels = ["Canary", "Moonshine", "Vosk", "Others"]
bottom = 1.0
for h, lab, c in zip(sub, sub_labels, rv.levels("violet", 5)[:4]):
    bottom -= h
    bar = ax2.bar(0, h, 0.5, bottom=bottom, color=c, edgecolor=plt.rcParams["figure.facecolor"], lw=2)
    ax2.bar_label(bar, labels=[f"{h:.0%}"], label_type="center", fontsize=9)
    ax2.text(0.32, bottom + h / 2, lab, va="center", fontsize=9)
ax2.set(xlim=(-0.4, 1.0), ylim=(0, 1.0)); ax2.axis("off")
ax2.set_title("Inside 'Other'", loc="left", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Break one slice down.
- **Key calls:** A pie plus `ax.bar` with `ConnectionPatch` lines
- **Watch out:** Keep the linked slice obvious.

### Labelling

<p align="center">
<img src="../img/pie/labels_light.png#gh-light-mode-only" alt="Labelling a pie: a legend with the numbers is often clearer than labels printed round the edge." width="640">
<img src="../img/pie/labels_dark.png#gh-dark-mode-only" alt="Labelling a pie: a legend with the numbers is often clearer than labels printed round the edge." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/pie/labels_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["Clean speech", "Noisy speech", "Accents", "Far-field", "Music"]
n = np.array([5200, 2600, 1800, 900, 500])
cm = rv.colour_map(names)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
wedges, _ = ax.pie(n, colors=[cm[k] for k in names], startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.45, edgecolor=plt.rcParams["figure.facecolor"], lw=2))
ax.legend(wedges, [f"{k}: {v:,} ({v / n.sum():.0%})" for k, v in zip(names, n)], loc="center left", bbox_to_anchor=(1.0, 0.5),
          frameon=False, title="Test clips")
ax.set_title("Test set makeup", loc="center")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Readable pies.
- **Key calls:** `ax.legend(wedges, labels)`
- **Watch out:** Put numbers in a legend, not on slices.

## Polar axes

### Line on polar axes

<p align="center">
<img src="../img/polar/line_light.png#gh-light-mode-only" alt="A line on polar axes: the angle is theta, the distance from the centre is r." width="640">
<img src="../img/polar/line_dark.png#gh-dark-mode-only" alt="A line on polar axes: the angle is theta, the distance from the centre is r." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/polar/line_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

theta = np.linspace(0, 4 * np.pi, 300)
fig, ax = plt.subplots(figsize=(4.6, 4.6), subplot_kw={"projection": "polar"}, layout="constrained")
ax.plot(theta, 1 + theta / (4 * np.pi) * 3, color=rv.colour("red"), lw=2.4)
ax.plot(theta, 4 - theta / (4 * np.pi) * 3, color=rv.colour("blue"), lw=2.4)
ax.set_rticks([1, 2, 3, 4])
ax.set_rlabel_position(112)
ax.set_title("Two spirals", y=1.08)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Cyclic data (angle, direction).
- **Key calls:** `ax = fig.add_subplot(projection='polar'); ax.plot(theta, r)`
- **Watch out:** Tick labels can overlap data; move them with `set_rlabel_position`.

### Polar bars

<p align="center">
<img src="../img/polar/bar_light.png#gh-light-mode-only" alt="A bar chart on polar axes: each bar is a direction, its length a value." width="640">
<img src="../img/polar/bar_dark.png#gh-dark-mode-only" alt="A bar chart on polar axes: each bar is a direction, its length a value." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/polar/bar_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

n = 12
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
r = np.array([8, 5, 9, 4, 7, 10, 6, 3, 8, 7, 5, 9], float)
fig, ax = plt.subplots(figsize=(4.6, 4.6), subplot_kw={"projection": "polar"}, layout="constrained")
ax.bar(theta, r, width=2 * np.pi / n * 0.85, color=rv.cmap("spectrum")(r / r.max()), edgecolor=plt.rcParams["figure.facecolor"])
ax.set_title("Polar bars", y=1.08)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Counts by direction.
- **Key calls:** `ax.bar(theta, r, width=)`
- **Watch out:** Use for cycles (hours of the day, compass).

### Polar scatter

<p align="center">
<img src="../img/polar/scatter_light.png#gh-light-mode-only" alt="A scatter plot on polar axes, with size and colour carrying extra information." width="640">
<img src="../img/polar/scatter_dark.png#gh-dark-mode-only" alt="A scatter plot on polar axes, with size and colour carrying extra information." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/polar/scatter_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
theta = 2 * np.pi * rng.random(60)
r = 2 * np.sqrt(rng.random(60))
fig, ax = plt.subplots(figsize=(4.8, 4.6), subplot_kw={"projection": "polar"}, layout="constrained")
sc = ax.scatter(theta, r, c=r, s=60 * r + 10, cmap="roygbviz", alpha=0.85)
ax.set_rticks([0.5, 1, 1.5, 2])
ax.set_title("Polar scatter", y=1.08)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Points by angle and distance.
- **Key calls:** `ax.scatter(theta, r, c=, s=)`
- **Watch out:** Check for clutter near the centre.

### Polar error bars

<p align="center">
<img src="../img/polar/errorbar_light.png#gh-light-mode-only" alt="Error bars on polar axes." width="640">
<img src="../img/polar/errorbar_dark.png#gh-dark-mode-only" alt="Error bars on polar axes." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/polar/errorbar_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

theta = np.linspace(0, 2 * np.pi, 12, endpoint=False)
r = 3 + np.sin(theta * 2)
fig, ax = plt.subplots(figsize=(4.6, 4.6), subplot_kw={"projection": "polar"}, layout="constrained")
ax.errorbar(theta, r, yerr=0.4, xerr=0.08, fmt="o", color=rv.colour("teal"), capsize=3, ecolor=rv.colour("grey"))
ax.set_rticks([1, 2, 3, 4])
ax.set_title("Polar error bars", y=1.08)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Uncertainty on polar data.
- **Key calls:** `ax.errorbar(theta, r, yerr=)`
- **Watch out:** Keep errors small enough to read.

### Radar chart

<p align="center">
<img src="../img/polar/radar_light.png#gh-light-mode-only" alt="A radar chart: several measures on spokes, one polygon per model. Compare shapes, not exact values." width="640">
<img src="../img/polar/radar_dark.png#gh-dark-mode-only" alt="A radar chart: several measures on spokes, one polygon per model. Compare shapes, not exact values." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/polar/radar_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

cats = ["Accuracy", "Speed", "Streaming", "Robustness", "Cost", "Languages"]
data = {"Whisper": [0.9, 0.55, 0.3, 0.8, 0.6, 0.95], "Parakeet": [0.85, 0.9, 0.85, 0.65, 0.8, 0.4]}
# these are normalised so that outward is always better
ang = np.linspace(0, 2 * np.pi, len(cats), endpoint=False)
ang = np.append(ang, ang[0])
cm = rv.colour_map(list(data))
fig, ax = plt.subplots(figsize=(5, 4.6), subplot_kw={"projection": "polar"}, layout="constrained")
for name, vals in data.items():
    v = np.append(vals, vals[0])
    ax.plot(ang, v, color=cm[name], lw=2.4, label=name)
    ax.fill(ang, v, color=cm[name], alpha=0.18)
ax.set_xticks(ang[:-1], cats)
ax.set_yticks([0.25, 0.5, 0.75, 1.0], ["", "", "", ""])
ax.set_ylim(0, 1)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.12), frameon=False)
ax.set_title("Radar chart", y=1.12)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Profiles across 5 to 8 measures.
- **Key calls:** Polar axes with a closed line and `ax.fill`
- **Watch out:** Scale every spoke 0 to 1 first; compare shapes, not exact values.

## Rules of thumb

- **Prefer bars** for exact comparison.
- **Pie only for parts of one whole.**
- **Order slices** from largest, clockwise from 12 o'clock.
- **Radar charts** distort area; use a table if values matter.

**Back to the [home page](../index.md).**
