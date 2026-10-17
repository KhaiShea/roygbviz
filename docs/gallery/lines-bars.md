# Lines, bars and markers

Lines show change, bars show amounts, and markers show individual observations. These are the workhorses of almost every report.

**Matplotlib reference:** `ax.plot`, `ax.bar`, `ax.barh`, `ax.step`, `ax.hlines`, `ax.axhline`. In plotnine: `geom_line`, `geom_col`, `geom_point`, `geom_step`, `geom_segment`, `geom_hline`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Lines**: Line plot, Line styles, Markers on some points, Cap and join styles, Marker reference, Reference lines, A line coloured by value, Line with a halo
- **Bars**: Grouped bars, Bar labels, Stacked bars, One colour per bar, Horizontal bars, Diverging bars for ratings, Broken bars (Gantt), Gradient bars, Bar plus markers
- **Dots, ranks and changes**: Lollipop chart, Dumbbell chart, Slope chart, Bump chart, Waterfall chart

## Lines

### Line plot

<p align="center">
<img src="../img/lines/line-basic_light.png#gh-light-mode-only" alt="A basic line plot with three series, a title, axis labels and a legend." width="640">
<img src="../img/lines/line-basic_dark.png#gh-dark-mode-only" alt="A basic line plot with three series, a title, axis labels and a legend." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/line-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 200)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.sin(x) * np.exp(-x / 6), label="damped")
ax.plot(x, 0.5 * np.cos(2 * x), label="cos(2x) / 2")
ax.set(title="A line plot", xlabel="x", ylabel="value", ylim=(-1.5, 1.1))
ax.legend(ncols=3, loc="lower left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Trends over an ordered variable, usually time.
- **Key calls:** `ax.plot(x, y, color=, lw=, label=)`; `ax.legend()`
- **Watch out:** Do not join points that are not ordered (categories); use bars or dots.

### Line styles

<p align="center">
<img src="../img/lines/linestyles_light.png#gh-light-mode-only" alt="Named and custom line styles." width="640">
<img src="../img/lines/linestyles_dark.png#gh-dark-mode-only" alt="Named and custom line styles." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/linestyles_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

styles = [("solid", "-"), ("dotted", ":"), ("dashed", "--"), ("dashdot", "-."),
          ("loosely dotted", (0, (1, 5))), ("densely dashed", (0, (5, 1))),
          ("dash, dot, dot", (0, (3, 5, 1, 5, 1, 5))), ("custom: 8 on, 3 off, 1 on, 3 off", (0, (8, 3, 1, 3)))]
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
for i, (name, ls) in enumerate(reversed(styles)):
    ax.plot([0, 1], [i, i], ls=ls, lw=2.5, color=rv.colour("blue"))
    ax.text(-0.03, i, name, ha="right", va="center")
    ax.text(1.03, i, repr(ls), ha="left", va="center", family="monospace", fontsize=8, color=rv.colour("grey"))
ax.set(xlim=(0, 1), ylim=(-0.6, len(styles) - 0.4), title="Line styles")
ax.axis("off")
ax.set_title("Line styles", loc="left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Telling lines apart without colour (print, colour blindness).
- **Key calls:** `ls='--'`, `ls=':'`, `ls=(0, (5, 1))`
- **Watch out:** Keep to two or three styles; more looks busy.

### Markers on some points

<p align="center">
<img src="../img/lines/markevery_light.png#gh-light-mode-only" alt="Putting markers on only some points of a line with markevery." width="640">
<img src="../img/lines/markevery_dark.png#gh-dark-mode-only" alt="Putting markers on only some points of a line with markevery." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/markevery_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 100)
y = np.sin(x)
options = [None, 12, (10, 20), 0.15, [0, 20, 55, 90]]
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
for i, opt in enumerate(options):
    ax.plot(x, y + (len(options) - 1 - i) * 2.6, marker="o", ms=5, markevery=opt, lw=1.8)
    ax.text(10.2, (len(options) - 1 - i) * 2.6, f"markevery={opt!r}", va="center", family="monospace", fontsize=8.5)
ax.set(xlim=(0, 14.5), title="Markers on some points only")
ax.set_yticks([])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Long lines where a marker on every point would clutter.
- **Key calls:** `ax.plot(..., marker='o', markevery=10)`
- **Watch out:** Pick a spacing that does not hide a real feature.

### Cap and join styles

<p align="center">
<img src="../img/lines/line-ends_light.png#gh-light-mode-only" alt="Cap styles (how a line ends) and join styles (how a corner looks) on very thick lines." width="640">
<img src="../img/lines/line-ends_dark.png#gh-dark-mode-only" alt="Cap styles (how a line ends) and join styles (how a corner looks) on very thick lines." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/line-ends_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.4), layout="constrained")
for i, cap in enumerate(["butt", "round", "projecting"]):
    a.plot([0.2, 0.8], [i, i], lw=16, solid_capstyle=cap, color=rv.colour("teal"), alpha=0.8)
    a.plot([0.2, 0.8], [i, i], lw=1, color=rv.colour("red"), marker="|", ms=14)      # the true ends
    a.text(0.5, i + 0.38, cap, ha="center")
a.set(xlim=(0, 1), ylim=(-0.5, 2.8), title="Cap style")
a.axis("off"); a.set_title("Cap style", loc="left")
for i, join in enumerate(["miter", "round", "bevel"]):
    b.plot([0.1 + i * 0.33, 0.2 + i * 0.33, 0.3 + i * 0.33], [0.2, 0.7, 0.2], lw=14, solid_joinstyle=join,
           color=rv.colour("violet"), alpha=0.8)
    b.text(0.2 + i * 0.33, 0.95, join, ha="center")
b.set(xlim=(0, 1.1), ylim=(0, 1.1))
b.axis("off"); b.set_title("Join style", loc="left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Thick lines and dashes whose ends and corners look rough.
- **Key calls:** `solid_capstyle='round'`, `solid_joinstyle='round'`
- **Watch out:** Round caps look softer; butt caps keep exact lengths.

### Marker reference

<p align="center">
<img src="../img/lines/marker-reference_light.png#gh-light-mode-only" alt="Every built-in marker with the string that selects it." width="640">
<img src="../img/lines/marker-reference_dark.png#gh-dark-mode-only" alt="Every built-in marker with the string that selects it." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/marker-reference_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.lines import Line2D

marks = [k for k in Line2D.markers if isinstance(k, str) and k.strip() and k.lower() != "none"]
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
cols = 8
for i, m in enumerate(marks):
    x, y = i % cols, -(i // cols)
    filled = m in Line2D.filled_markers
    ax.plot(x, y, marker=m, ms=13, color=rv.colour("blue"), mfc=rv.colour("blue") if filled else "none", mew=1.8)
    ax.text(x, y - 0.42, repr(m), ha="center", va="top", family="monospace", fontsize=9)
ax.set(xlim=(-0.6, cols - 0.4), ylim=(-(len(marks) // cols) - 0.9, 0.5), title="Markers: filled and open")
ax.axis("off"); ax.set_title("Markers: filled and open", loc="left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Choosing a marker shape for points.
- **Key calls:** `marker='o'`, `'s'`, `'^'`, `'D'`, `'x'`, `'+'`
- **Watch out:** Shape is a second cue for groups; avoid more than five.

### Reference lines

<p align="center">
<img src="../img/lines/infinite-lines_light.png#gh-light-mode-only" alt="Reference lines that span the whole plot: axhline, axvline and axline." width="640">
<img src="../img/lines/infinite-lines_dark.png#gh-dark-mode-only" alt="Reference lines that span the whole plot: axhline, axvline and axline." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/infinite-lines_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
truth = rng.uniform(1, 9, 40)
pred = truth + rng.normal(0, 0.8, 40)
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
ax.scatter(truth, pred, color=rv.colour("teal"), alpha=0.8)
ax.axline((0, 0), slope=1, color=rv.colour("grey"), ls="--", label="perfect prediction (y = x)")
ax.axhline(pred.mean(), color=rv.colour("orange"), lw=1.5, label="mean prediction")
ax.axvline(truth.mean(), color=rv.colour("violet"), lw=1.5, label="mean truth")
ax.set(xlim=(0, 10), ylim=(0, 10), aspect="equal", xlabel="True value", ylabel="Predicted value",
       title="Reference lines")
ax.legend(loc="upper left", fontsize=8)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Thresholds, targets and baselines.
- **Key calls:** `ax.axhline(y)`, `ax.axvline(x)`, `ax.axline((x0, y0), slope=m)`
- **Watch out:** Label the line directly, so readers do not guess its meaning.

### A line coloured by value

<p align="center">
<img src="../img/lines/multicolour-line_light.png#gh-light-mode-only" alt="One line whose colour follows a value, drawn as a LineCollection." width="640">
<img src="../img/lines/multicolour-line_dark.png#gh-dark-mode-only" alt="One line whose colour follows a value, drawn as a LineCollection." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/multicolour-line_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.collections import LineCollection

x = np.linspace(0, 3 * np.pi, 400)
y = np.sin(x)
pts = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
lc = LineCollection(segments, cmap="roygbviz_spectrum", norm=plt.Normalize(-1, 1), linewidth=3.5)
lc.set_array(y)
ax.add_collection(lc)
ax.set(xlim=(0, x.max()), ylim=(-1.2, 1.2), title="A line coloured by its own value")
fig.colorbar(lc, ax=ax, label="value", shrink=0.8)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Showing a third variable along a path.
- **Key calls:** `LineCollection(segments, array=values, cmap='roygbviz')`
- **Watch out:** Add a colourbar and say what the colour means.

### Line with a halo

<p align="center">
<img src="../img/lines/line-outline_light.png#gh-light-mode-only" alt="A halo around a line (a path effect) keeps it readable over a busy background." width="640">
<img src="../img/lines/line-outline_dark.png#gh-dark-mode-only" alt="A halo around a line (a path effect) keeps it readable over a busy background." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/line-outline_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patheffects import withStroke

rng = np.random.default_rng(2)
x = np.linspace(0, 10, 120)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
for k in range(10):                                    # a busy background
    ax.axvspan(k, k + 0.5, color=rv.colour("grey"), alpha=0.25, lw=0)
ax.plot(x, 3 + np.sin(x) + rng.normal(0, 0.05, x.size), color=rv.colour("red"), lw=2.5, label="no halo")
halo = plt.rcParams["figure.facecolor"]
ax.plot(x, 1 + np.sin(x) + rng.normal(0, 0.05, x.size), color=rv.colour("red"), lw=2.5, label="with halo",
        path_effects=[withStroke(linewidth=6, foreground=halo)])
ax.set(xlim=(0, 10), ylim=(-0.5, 4.6), title="Path effects: a halo behind the line")
ax.legend(loc="upper right", ncols=2)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Lines drawn over busy backgrounds.
- **Key calls:** `path_effects=[pe.withStroke(linewidth=4, foreground=bg)]`
- **Watch out:** Use the background colour so the line looks separated, not outlined.

## Bars

### Grouped bars

<p align="center">
<img src="../img/lines/bar-grouped_light.png#gh-light-mode-only" alt="Grouped bars with value labels: three models across four test conditions." width="640">
<img src="../img/lines/bar-grouped_dark.png#gh-dark-mode-only" alt="Grouped bars with value labels: three models across four test conditions." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-grouped_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

cond = ["Clean", "Noisy", "Accented", "Far-field"]
wer = {"Whisper": [3.1, 7.4, 9.2, 12.8], "Parakeet": [2.8, 8.9, 8.1, 13.5], "Conformer": [3.9, 9.8, 10.7, 16.2]}
cols = rv.colour_map(list(wer))
x = np.arange(len(cond))
width = 0.26
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
for i, (model, vals) in enumerate(wer.items()):
    rects = ax.bar(x + (i - 1) * width, vals, width * 0.92, label=model, color=cols[model])
    ax.bar_label(rects, fmt="%.1f", padding=2, fontsize=8)
ax.set_xticks(x, cond)
ax.set(ylabel="Word error rate (%)", ylim=(0, 19), title="Word error rate by condition")
ax.legend(ncols=3, loc="upper left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Comparing a few groups across a few conditions.
- **Key calls:** `ax.bar(x + offset, y, width)`
- **Watch out:** More than about four groups per cluster gets crowded; facet instead.

### Bar labels

<p align="center">
<img src="../img/lines/bar-labels_light.png#gh-light-mode-only" alt="Bars with the value written on them (bar_label), inside or outside the bar." width="640">
<img src="../img/lines/bar-labels_dark.png#gh-dark-mode-only" alt="Bars with the value written on them (bar_label), inside or outside the bar." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-labels_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Kokoro"]
score = [91, 88, 84, 79]
fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.6), layout="constrained", sharey=True)
for ax, where in ((a, "edge"), (b, "center")):
    bars = ax.bar(models, score, color=rv.colour("blue"), width=0.65)
    ax.bar_label(bars, label_type=where, padding=3 if where == "edge" else 0, fontsize=9,
                 color=plt.rcParams["text.color"] if where == "edge" else plt.rcParams["figure.facecolor"])
    ax.set_title(f'label_type="{where}"', fontsize=10)
    ax.tick_params(axis="x", labelrotation=30)
a.set(ylim=(0, 105), ylabel="Score")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** When readers need the exact value.
- **Key calls:** `ax.bar_label(bars, fmt='%.1f', padding=3)`
- **Watch out:** Add labels or a grid, not both.

### Stacked bars

<p align="center">
<img src="../img/lines/bar-stacked_light.png#gh-light-mode-only" alt="A stacked bar of latency per stage, in the stage colours, with the total on top." width="640">
<img src="../img/lines/bar-stacked_dark.png#gh-dark-mode-only" alt="A stacked bar of latency per stage, in the stage colours, with the total on top." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-stacked_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

pipes = ["Cascade A", "Cascade B", "Cascade C", "Cascade D"]
ms = {"STT": np.array([180, 210, 150, 240]), "LLM": np.array([520, 410, 640, 380]), "TTS": np.array([210, 160, 260, 190])}
stage = rv.group_map()
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
bottom = np.zeros(len(pipes))
for name, vals in ms.items():
    ax.bar(pipes, vals, bottom=bottom, label=name, color=stage[name], width=0.62,
           edgecolor=plt.rcParams["figure.facecolor"], linewidth=1.5)
    bottom += vals
for i, total in enumerate(bottom):
    ax.text(i, total + 18, f"{total:.0f} ms", ha="center", fontsize=9)
ax.set(ylabel="Latency (ms)", ylim=(0, 1200), title="Where the time goes")
ax.legend(ncols=3, loc="upper left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A total split into parts.
- **Key calls:** `ax.bar(x, y, bottom=running_total)`
- **Watch out:** Only the bottom segment compares well. Put the key part there.

### One colour per bar

<p align="center">
<img src="../img/lines/bar-colours_light.png#gh-light-mode-only" alt="One colour per bar, kept the same for each model in every figure with colour_map." width="640">
<img src="../img/lines/bar-colours_dark.png#gh-dark-mode-only" alt="One colour per bar, kept the same for each model in every figure with colour_map." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-colours_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Llama", "Qwen", "Gemma", "Kokoro", "Piper", "XTTS"]
score = [91, 88, 84, 79, 82, 74, 91, 83, 72]
cm = rv.colour_map(models)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
ax.bar(models, score, color=[cm[m] for m in models], width=0.7)
ax.set(ylim=(0, 100), ylabel="Overall score", title="Nine models, nine colours")
ax.tick_params(axis="x", labelrotation=35)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Keeping a model the same colour everywhere.
- **Key calls:** `color=[cmap[m] for m in names]` with `rv.colour_map(names)`
- **Watch out:** Do not colour by rank; colour follows the entity.

### Horizontal bars

<p align="center">
<img src="../img/lines/bar-horizontal_light.png#gh-light-mode-only" alt="A horizontal ranking with one bar highlighted and the rest in grey." width="640">
<img src="../img/lines/bar-horizontal_dark.png#gh-dark-mode-only" alt="A horizontal ranking with one bar highlighted and the rest in grey." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-horizontal_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Llama", "Qwen", "Gemma", "Kokoro", "Piper", "XTTS"]
score = np.array([91, 88, 84, 79, 82, 74, 91, 83, 72])
order = np.argsort(score)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
colours = [rv.colour("red") if models[i] == "Whisper" else rv.colour("grey") for i in order]
bars = ax.barh([models[i] for i in order], score[order], color=colours, height=0.7)
ax.bar_label(bars, padding=4, fontsize=9)
ax.set(xlim=(0, 105), title="Overall score, best at the top")
ax.grid(axis="x"); ax.grid(axis="y", visible=False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Rankings and long category names.
- **Key calls:** `ax.barh(names, values)`; `ax.invert_yaxis()`
- **Watch out:** Sort by value unless the order is natural.

### Diverging bars for ratings

<p align="center">
<img src="../img/lines/bar-likert_light.png#gh-light-mode-only" alt="A diverging stacked bar for ratings: the middle category sits on zero, bad to the left, good to the right." width="640">
<img src="../img/lines/bar-likert_dark.png#gh-dark-mode-only" alt="A diverging stacked bar for ratings: the middle category sits on zero, bad to the left, good to the right." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-likert_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

q = ["Naturalness", "Clarity", "Pacing", "Pronunciation"]
pct = np.array([[4, 12, 22, 38, 24], [2, 6, 14, 44, 34], [8, 20, 30, 28, 14], [3, 9, 18, 40, 30]], float)
labels = ["Very poor", "Poor", "OK", "Good", "Excellent"]
bad, good = rv.levels("red", 5), rv.levels("teal", 5)               # two colour families, deep to soft
cols = [bad[1], bad[3], rv.colour("grey"), good[3], good[1]]       # the middle category is neutral
left = -(pct[:, 0] + pct[:, 1] + pct[:, 2] / 2)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
for k in range(5):
    ax.barh(q[::-1], pct[::-1, k], left=left[::-1], color=cols[k], label=labels[k], height=0.62,
            edgecolor=plt.rcParams["figure.facecolor"], linewidth=1)
    left = left + pct[:, k]
ax.axvline(0, color=plt.rcParams["text.color"], lw=1)
ax.set(xlim=(-60, 60), xlabel="% of listeners", title="Listener ratings")
ax.legend(ncols=5, loc="upper center", bbox_to_anchor=(0.5, -0.18), fontsize=8, handlelength=1, columnspacing=1)
ax.grid(axis="x"); ax.grid(axis="y", visible=False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Survey and Likert scales.
- **Key calls:** Negative values to the left via `left=`
- **Watch out:** Put neutral in the middle in grey.

### Broken bars (Gantt)

<p align="center">
<img src="../img/lines/bar-broken_light.png#gh-light-mode-only" alt="Broken horizontal bars: a timeline of which stage is running when (a Gantt chart)." width="640">
<img src="../img/lines/bar-broken_dark.png#gh-dark-mode-only" alt="Broken horizontal bars: a timeline of which stage is running when (a Gantt chart)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-broken_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

stage = rv.group_map()
fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
runs = {"Request 1": [(0, 180, "STT"), (180, 520, "LLM"), (700, 210, "TTS")],
        "Request 2": [(0, 210, "STT"), (210, 410, "LLM"), (620, 160, "TTS")],
        "Request 3": [(0, 150, "STT"), (150, 640, "LLM"), (790, 260, "TTS")]}
for row, (name, spans) in enumerate(reversed(list(runs.items()))):
    for start, length, s in spans:
        ax.broken_barh([(start, length)], (row - 0.32, 0.64), facecolors=stage[s],
                       edgecolor=plt.rcParams["figure.facecolor"], linewidth=1.5)
        ax.text(start + length / 2, row, s, ha="center", va="center", fontsize=8.5,
                color=plt.rcParams["figure.facecolor"] if s != "LLM" else "white", weight="bold")
ax.set_yticks(range(3), list(runs)[::-1])
ax.set(xlabel="Time since the user stopped speaking (ms)", xlim=(0, 1100), title="One request, three stages")
ax.grid(axis="x"); ax.grid(axis="y", visible=False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Which thing runs when.
- **Key calls:** `ax.broken_barh([(start, length)], (y, height))`
- **Watch out:** Order rows by start time.

### Gradient bars

<p align="center">
<img src="../img/lines/bar-gradient_light.png#gh-light-mode-only" alt="Bars filled with a gradient: draw an image, then clip it to each bar's shape." width="640">
<img src="../img/lines/bar-gradient_dark.png#gh-dark-mode-only" alt="Bars filled with a gradient: draw an image, then clip it to each bar's shape." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-gradient_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
vals = [0.9, 0.7, 0.55, 0.8]
ax.set(xlim=(0, len(vals)), ylim=(0, 1))
grad = np.linspace(0, 1, 256).reshape(-1, 1)
for i, v in enumerate(vals):
    im = ax.imshow(grad, extent=(i + 0.15, i + 0.85, 0, v), aspect="auto", origin="lower",
                   cmap=rv.cmap("blue"), vmin=0, vmax=1, zorder=2)
ax.set_xticks(np.arange(len(vals)) + 0.5, ["A", "B", "C", "D"])
ax.set(xlim=(0, len(vals)), ylim=(0, 1), title="Gradient bars")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Decoration; use rarely.
- **Key calls:** `ax.imshow(gradient, extent=..., clip_path=bar)`
- **Watch out:** Gradients add no information. Use for hero images only.

### Bar plus markers

<p align="center">
<img src="../img/lines/bar-baseline-markers_light.png#gh-light-mode-only" alt="A bar for the baseline with a marker for each new result: easy to read as 'better or worse than the bar'." width="640">
<img src="../img/lines/bar-baseline-markers_dark.png#gh-dark-mode-only" alt="A bar for the baseline with a marker for each new result: easy to read as 'better or worse than the bar'." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bar-baseline-markers_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

cond = ["Clean", "Noisy", "Accented", "Far-field"]
base = np.array([3.9, 9.8, 10.7, 16.2])
new = np.array([3.1, 7.4, 9.2, 12.8])
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.bar(cond, base, color=rv.shade(rv.colour("grey"), 2), width=0.6, label="Baseline (Conformer)")
ax.plot(cond, new, "_", ms=46, mew=3.5, color=rv.colour("red"), label="Whisper")
for i, (b, n) in enumerate(zip(base, new)):
    ax.annotate(f"{(n - b) / b:+.0%}", (i, n), xytext=(0, -14), textcoords="offset points", ha="center", fontsize=8.5,
                color=rv.colour("red"))
ax.set(ylabel="Word error rate (%)", title="New model against the baseline")
ax.legend(loc="upper left", markerscale=0.35)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Baseline against many new results.
- **Key calls:** `ax.bar(...)` then `ax.plot(..., 'o')`
- **Watch out:** Make the marker meaning explicit in the legend.

## Dots, ranks and changes

### Lollipop chart

<p align="center">
<img src="../img/lines/lollipop_light.png#gh-light-mode-only" alt="A lollipop chart: a thin stem and a dot instead of a heavy bar, good for many categories." width="640">
<img src="../img/lines/lollipop_dark.png#gh-dark-mode-only" alt="A lollipop chart: a thin stem and a dot instead of a heavy bar, good for many categories." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/lollipop_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Llama", "Qwen", "Gemma", "Kokoro", "Piper", "XTTS"]
score = np.array([91, 88, 84, 79, 82, 74, 91, 83, 72])
o = np.argsort(score)
y = np.arange(len(models))
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
ax.hlines(y, 60, score[o], color=rv.colour("grey"), lw=1.8)
ax.scatter(score[o], y, s=70, color=rv.colour("teal"), zorder=3)
ax.set_yticks(y, [models[i] for i in o])
ax.set(xlim=(60, 96), xlabel="Score", title="Lollipop chart")
ax.grid(axis="x"); ax.grid(axis="y", visible=False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Many categories where bars feel heavy.
- **Key calls:** `ax.stem(...)` or `ax.hlines` plus `ax.plot('o')`
- **Watch out:** Start at zero, as with bars.

### Dumbbell chart

<p align="center">
<img src="../img/lines/dumbbell_light.png#gh-light-mode-only" alt="A dumbbell chart: the size of each change, before and after, on a shared scale." width="640">
<img src="../img/lines/dumbbell_dark.png#gh-dark-mode-only" alt="A dumbbell chart: the size of each change, before and after, on a shared scale." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/dumbbell_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Kokoro", "Piper"]
before = np.array([12.8, 13.5, 16.2, 9.0, 11.2])
after = np.array([9.1, 11.0, 12.9, 8.2, 8.0])
y = np.arange(len(models))[::-1]
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.hlines(y, after, before, color=rv.colour("grey"), lw=3, alpha=0.6)
ax.scatter(before, y, s=90, color=rv.colour("grey"), label="Before", zorder=3)
ax.scatter(after, y, s=90, color=rv.colour("red"), label="After fine-tuning", zorder=3)
ax.set_yticks(y, models)
ax.set(xlabel="Word error rate (%), lower is better", title="What fine-tuning bought")
ax.legend(loc="lower right")
ax.grid(axis="x"); ax.grid(axis="y", visible=False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Before and after for each item.
- **Key calls:** `ax.hlines(y, x1, x2)` plus two scatters
- **Watch out:** Sort by the size of the change.

### Slope chart

<p align="center">
<img src="../img/lines/slope-chart_light.png#gh-light-mode-only" alt="A slope chart: two moments, one line per item. The steepest lines are the story." width="640">
<img src="../img/lines/slope-chart_dark.png#gh-dark-mode-only" alt="A slope chart: two moments, one line per item. The steepest lines are the story." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/slope-chart_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer", "Kokoro", "Piper"]
a = np.array([12.8, 13.5, 16.2, 9.0, 11.2])
b = np.array([9.1, 11.0, 12.9, 8.2, 8.0])
cm = rv.colour_map(models)

def spread(values, gap):
    """Push labels apart so none sit closer than `gap`, keeping their order."""
    order = np.argsort(values)
    out = np.array(values, float)
    for prev, cur in zip(order, order[1:]):
        out[cur] = max(out[cur], out[prev] + gap)
    return out

left, right = spread(a, 0.75), spread(b, 0.75)
fig, ax = plt.subplots(figsize=(5.4, 4.2), layout="constrained")
for m, y0, y1, l0, l1 in zip(models, a, b, left, right):
    ax.plot([0, 1], [y0, y1], "o-", color=cm[m], lw=2.2)
    ax.text(-0.04, l0, f"{m}  {y0:.1f}", ha="right", va="center", fontsize=9)
    ax.text(1.04, l1, f"{y1:.1f}  {m}", ha="left", va="center", fontsize=9)
ax.set(xlim=(-0.6, 1.6), title="Word error rate, before and after")
ax.set_xticks([0, 1], ["Before", "After"])
ax.set_yticks([]); ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Two moments, many items.
- **Key calls:** `ax.plot([0, 1], [a, b])` per item
- **Watch out:** Label both ends; space labels apart so they do not collide.

### Bump chart

<p align="center">
<img src="../img/lines/bump-chart_light.png#gh-light-mode-only" alt="A bump chart: how each item's rank changes across conditions." width="640">
<img src="../img/lines/bump-chart_dark.png#gh-dark-mode-only" alt="A bump chart: how each item's rank changes across conditions." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/bump-chart_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

cond = ["Clean", "Noisy", "Accented", "Far-field"]
wer = {"Whisper": [3.1, 7.4, 9.2, 12.8], "Parakeet": [2.8, 8.9, 8.1, 13.5], "Conformer": [3.9, 9.8, 10.7, 16.2],
       "Canary": [3.3, 7.9, 8.8, 11.9]}
arr = np.array(list(wer.values()))
ranks = arr.argsort(axis=0).argsort(axis=0) + 1
cm = rv.colour_map(list(wer))
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
for i, m in enumerate(wer):
    ax.plot(cond, ranks[i], "o-", color=cm[m], lw=3, ms=14, solid_capstyle="round")
    ax.text(len(cond) - 1 + 0.12, ranks[i, -1], m, va="center", fontsize=9)
ax.set(ylim=(4.6, 0.4), xlim=(-0.2, 3.9), title="Rank by word error rate (1 is best)")
ax.set_yticks([1, 2, 3, 4]); ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Rank changes across conditions.
- **Key calls:** `ax.plot(x, rank, 'o-')`; `ax.invert_yaxis()`
- **Watch out:** Rank 1 at the top; keep to about eight items.

### Waterfall chart

<p align="center">
<img src="../img/lines/waterfall_light.png#gh-light-mode-only" alt="A waterfall chart: how each step adds to (or takes from) a total, for example a latency budget." width="640">
<img src="../img/lines/waterfall_dark.png#gh-dark-mode-only" alt="A waterfall chart: how each step adds to (or takes from) a total, for example a latency budget." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/waterfall_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

steps = [("Audio capture", 40), ("Network", 55), ("STT", 180), ("LLM", 520), ("TTS", 210), ("Playback", 30)]
names = [s for s, _ in steps] + ["Total"]
vals = [v for _, v in steps]
cum = np.cumsum([0] + vals)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.bar(names[:-1], vals, bottom=cum[:-1], color=rv.colour("blue"), width=0.62)
ax.bar(names[-1], cum[-1], color=rv.colour("grey"), width=0.62)
for i, v in enumerate(vals):
    ax.text(i, cum[i] + v + 14, f"+{v}", ha="center", fontsize=8.5)
    ax.plot([i + 0.31, i + 0.69], [cum[i + 1]] * 2, color=rv.colour("grey"), lw=1)
ax.text(len(vals), cum[-1] + 14, f"{cum[-1]} ms", ha="center", fontsize=8.5)
ax.set(ylabel="Cumulative latency (ms)", ylim=(0, 1150), title="A latency budget")
ax.tick_params(axis="x", labelrotation=25)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** How steps add up to a total.
- **Key calls:** `ax.bar(x, step, bottom=start)`
- **Watch out:** Colour increases and decreases differently.

## Rules of thumb

- **Bars start at zero.** Always.
- **Sort** categories by value unless they have a natural order.
- **Direct labels beat legends** when you have fewer than six series.
- **Lines for ordered, bars for categories.**

**Back to the [home page](../index.md).**
