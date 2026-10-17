# Layout: subplots, axes and figures

How to arrange panels, size a figure, and put axes where you want them.

**Matplotlib reference:** `plt.subplots`, `plt.subplot_mosaic`, `fig.add_gridspec`, `fig.subfigures`, `ax.inset_axes`. In plotnine: `facet_wrap`, `facet_grid`, and `|` and `/` to combine plots.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Grids of panels**: Subplots, Mosaic, GridSpec ratios, Nested grids, Subfigures, Shared axes, Panel labels, Figure title and labels
- **Spacing and size**: Layout engines, Manual spacing, Margins, Aspect, Figure size, Align labels
- **Axes tricks**: Inverted axis, Twin axes, Secondary axis, Many y axes, Zoom inset, Broken axis, Map projections

## Grids of panels

### Subplots

<p align="center">
<img src="../img/layout/subplots_light.png#gh-light-mode-only" alt="A grid of subplots that share their axes, so the panels can be compared by eye." width="640">
<img src="../img/layout/subplots_dark.png#gh-dark-mode-only" alt="A grid of subplots that share their axes, so the panels can be compared by eye." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/subplots_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
fig, axs = plt.subplots(2, 3, figsize=(7, 4.4), sharex=True, sharey=True, layout="constrained")
x = np.linspace(0, 10, 50)
for ax, (i, j) in zip(axs.ravel(), np.ndindex(2, 3)):
    ax.plot(x, np.sin(x + i + j) + rng.normal(0, 0.1, x.size), color=rv.colour("blue"))
    ax.set_title(f"row {i}, col {j}", fontsize=9)
fig.supxlabel("time (s)")
fig.supylabel("amplitude")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Panels to compare.
- **Key calls:** `fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, layout='constrained')`
- **Watch out:** Share axes when panels are compared.

### Mosaic

<p align="center">
<img src="../img/layout/mosaic_light.png#gh-light-mode-only" alt="subplot_mosaic: draw the layout as text, then use the letters to find each Axes." width="640">
<img src="../img/layout/mosaic_dark.png#gh-dark-mode-only" alt="subplot_mosaic: draw the layout as text, then use the letters to find each Axes." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/mosaic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axd = plt.subplot_mosaic([["wide", "wide", "tall"], ["a", "b", "tall"]], figsize=(6.4, 4), layout="constrained")
x = np.linspace(0, 6, 100)
axd["wide"].plot(x, np.sin(x), color=rv.colour("red"))
axd["tall"].barh(range(5), [3, 5, 2, 6, 4], color=rv.colour("teal"))
axd["a"].scatter(*np.random.default_rng(2).normal(size=(2, 30)), color=rv.colour("violet"), s=14)
axd["b"].imshow(np.random.default_rng(3).random((6, 6)), cmap="roygbviz")
axd["b"].grid(False)
for name, ax in axd.items():
    ax.set_title(f"'{name}'", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Irregular layouts.
- **Key calls:** `plt.subplot_mosaic([['a', 'a', 'b'], ['c', 'd', 'b']])`
- **Watch out:** Easiest way to read a complicated layout.

### GridSpec ratios

<p align="center">
<img src="../img/layout/gridspec-ratios_light.png#gh-light-mode-only" alt="GridSpec with width and height ratios: panels of different sizes on one grid." width="640">
<img src="../img/layout/gridspec-ratios_dark.png#gh-dark-mode-only" alt="GridSpec with width and height ratios: panels of different sizes on one grid." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/gridspec-ratios_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig = plt.figure(figsize=(6.4, 4.2), layout="constrained")
gs = fig.add_gridspec(2, 3, width_ratios=[3, 1, 1], height_ratios=[1, 2])
rng = np.random.default_rng(4)
big = fig.add_subplot(gs[1, 0])
big.plot(rng.normal(size=60).cumsum(), color=rv.colour("blue"))
big.set_title("big panel", fontsize=9)
top = fig.add_subplot(gs[0, :])
top.plot(rng.normal(size=120).cumsum(), color=rv.colour("red"))
top.set_title("wide strip across the top", fontsize=9)
for k in (1, 2):
    a = fig.add_subplot(gs[1, k])
    a.hist(rng.normal(size=200), bins=14, color=rv.shade("teal"), edgecolor=rv.colour("teal"))
    a.set_title("small", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Panels of different sizes.
- **Key calls:** `fig.add_gridspec(2, 3, width_ratios=, height_ratios=)`
- **Watch out:** Index with slices: `gs[0, :]`.

### Nested grids

<p align="center">
<img src="../img/layout/gridspec-nested_light.png#gh-light-mode-only" alt="Nested grids: a grid inside one cell of another grid." width="640">
<img src="../img/layout/gridspec-nested_dark.png#gh-dark-mode-only" alt="Nested grids: a grid inside one cell of another grid." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/gridspec-nested_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig = plt.figure(figsize=(6.4, 4), layout="constrained")
outer = fig.add_gridspec(1, 2, width_ratios=[1, 1.4])
left = fig.add_subplot(outer[0])
left.imshow(np.random.default_rng(5).random((12, 12)), cmap="roygbviz")
left.set_title("one big Axes", fontsize=9); left.grid(False)
inner = outer[1].subgridspec(2, 2, wspace=0.1, hspace=0.15)
cols = [rv.colour(c) for c in ("red", "teal", "violet", "orange")]
for k, c in enumerate(cols):
    ax = fig.add_subplot(inner[k // 2, k % 2])
    ax.plot(np.random.default_rng(k).normal(size=30).cumsum(), color=c)
    ax.set_title(f"inner {k + 1}", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A grid inside a cell.
- **Key calls:** `gs[1].subgridspec(2, 2)`
- **Watch out:** Use `constrained` layout.

### Subfigures

<p align="center">
<img src="../img/layout/subfigures_light.png#gh-light-mode-only" alt="Subfigures: independent mini-figures inside one figure, each with its own title and layout." width="640">
<img src="../img/layout/subfigures_dark.png#gh-dark-mode-only" alt="Subfigures: independent mini-figures inside one figure, each with its own title and layout." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/subfigures_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig = plt.figure(figsize=(7.2, 3.8), layout="constrained")
left, right = fig.subfigures(1, 2, width_ratios=[1, 1.5])
left.suptitle("(a) Latency", fontsize=10, weight="bold")
ax = left.subplots()
ax.bar(["STT", "LLM", "TTS"], [190, 480, 210], color=list(rv.group_map().values()))
right.suptitle("(b) Quality, three conditions", fontsize=10, weight="bold")
axs = right.subplots(1, 3, sharey=True)
rng = np.random.default_rng(6)
for a, c in zip(axs, ("Clean", "Noisy", "Far-field")):
    a.hist(rng.normal(4 + 0.5 * len(c) / 3, 0.6, 200), bins=14, color=rv.shade("teal"), edgecolor=rv.colour("teal"))
    a.set_title(c, fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Independent mini-figures.
- **Key calls:** `fig.subfigures(1, 2)`
- **Watch out:** Each has its own title and legend.

### Shared axes

<p align="center">
<img src="../img/layout/shared-axes_light.png#gh-light-mode-only" alt="Shared axes: pan or zoom one panel and the others follow, and tick labels are not repeated." width="640">
<img src="../img/layout/shared-axes_dark.png#gh-dark-mode-only" alt="Shared axes: pan or zoom one panel and the others follow, and tick labels are not repeated." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/shared-axes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
fig, axs = plt.subplots(3, 1, figsize=(6.4, 4.6), sharex=True, layout="constrained")
t = np.linspace(0, 10, 200)
for ax, name, c in zip(axs, ("STT", "LLM", "TTS"), ("STT", "LLM", "TTS")):
    ax.plot(t, np.sin(t + len(name)) + rng.normal(0, 0.1, t.size), color=rv.group_map()[c])
    ax.set_ylabel(name)
axs[-1].set_xlabel("time (s)")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Stacked panels on one time axis.
- **Key calls:** `sharex=True`
- **Watch out:** Label only the bottom axis.

### Panel labels

<p align="center">
<img src="../img/layout/panel-labels_light.png#gh-light-mode-only" alt="Panel labels (a), (b), (c): the standard way to refer to parts of a figure in a caption." width="640">
<img src="../img/layout/panel-labels_dark.png#gh-dark-mode-only" alt="Panel labels (a), (b), (c): the standard way to refer to parts of a figure in a caption." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/panel-labels_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import string

fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.8), layout="constrained")
t = np.linspace(0, 6, 80)
for ax, k in zip(axs, range(3)):
    ax.plot(t, np.sin(t * (k + 1)), color=rv.colour("teal"))
    ax.text(-0.02, 1.08, f"({string.ascii_lowercase[k]})", transform=ax.transAxes, weight="bold", fontsize=11, va="bottom")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Referring to (a), (b), (c) in text.
- **Key calls:** `ax.text(-0.02, 1.08, '(a)', transform=ax.transAxes)`
- **Watch out:** Same position in every panel.

### Figure title and labels

<p align="center">
<img src="../img/layout/suptitle_light.png#gh-light-mode-only" alt="A figure-level title, x label and y label over a grid of panels." width="640">
<img src="../img/layout/suptitle_dark.png#gh-dark-mode-only" alt="A figure-level title, x label and y label over a grid of panels." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/suptitle_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axs = plt.subplots(2, 2, figsize=(6.4, 4.2), sharex=True, sharey=True, layout="constrained")
t = np.linspace(0, 6, 80)
for ax, k in zip(axs.ravel(), range(4)):
    ax.plot(t, np.sin(t * (k + 1)), color=rv.colour("teal"))
fig.suptitle("fig.suptitle()", x=0.01, ha="left", weight="bold")
fig.supxlabel("fig.supxlabel()")
fig.supylabel("fig.supylabel()")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** One title for many panels.
- **Key calls:** `fig.suptitle()`, `fig.supxlabel()`, `fig.supylabel()`
- **Watch out:** Left-align to match the theme.

## Spacing and size

### Layout engines

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


- **Use when:** Labels that collide.
- **Key calls:** `layout='constrained'` (best) or `'tight'`
- **Watch out:** Do not mix engines.

### Manual spacing

<p align="center">
<img src="../img/layout/spacing_light.png#gh-light-mode-only" alt="Setting the gaps yourself with subplots_adjust (wspace and hspace are fractions of an Axes)." width="640">
<img src="../img/layout/spacing_dark.png#gh-dark-mode-only" alt="Setting the gaps yourself with subplots_adjust (wspace and hspace are fractions of an Axes)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/spacing_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axs = plt.subplots(2, 2, figsize=(6, 4))
for ax in axs.ravel():
    ax.plot(np.arange(5), color=rv.colour("teal"))
    ax.set_title("title", fontsize=9)
fig.subplots_adjust(left=0.1, right=0.97, bottom=0.1, top=0.9, wspace=0.5, hspace=0.6)
fig.suptitle("subplots_adjust(wspace=0.5, hspace=0.6)", x=0.1, ha="left", fontsize=10, weight="bold")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Exact control.
- **Key calls:** `fig.subplots_adjust(wspace=, hspace=)`
- **Watch out:** Constrained layout overrides this.

### Margins

<p align="center">
<img src="../img/layout/margins_light.png#gh-light-mode-only" alt="Margins and sticky edges: lines get padding round them, bars stay glued to zero." width="640">
<img src="../img/layout/margins_dark.png#gh-dark-mode-only" alt="Margins and sticky edges: lines get padding round them, bars stay glued to zero." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/margins_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(1, 6)
fig, axs = plt.subplots(1, 3, figsize=(7.2, 3), layout="constrained")
axs[0].plot(x, x ** 1.5, "o-", color=rv.colour("blue")); axs[0].set_title("default margins", fontsize=9)
axs[1].plot(x, x ** 1.5, "o-", color=rv.colour("blue")); axs[1].margins(0); axs[1].set_title("margins(0)", fontsize=9)
axs[2].bar(x, x ** 1.5, color=rv.colour("blue")); axs[2].set_title("bars: sticky at zero", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Padding round data.
- **Key calls:** `ax.margins(0)`; sticky edges for bars
- **Watch out:** Bars stay at zero by design.

### Aspect

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


- **Use when:** Round circles and square plots.
- **Key calls:** `ax.set_aspect('equal')`, `ax.set_box_aspect(1)`
- **Watch out:** Use equal aspect for maps and images.

### Figure size

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


- **Use when:** Matching a page.
- **Key calls:** `figsize=(12 / 2.54, 7 / 2.54)`
- **Watch out:** Size in inches for the final width.

### Align labels

<p align="center">
<img src="../img/layout/align-labels_light.png#gh-light-mode-only" alt="fig.align_ylabels() lines the y labels of stacked panels up, however wide their tick labels are." width="640">
<img src="../img/layout/align-labels_dark.png#gh-dark-mode-only" alt="fig.align_ylabels() lines the y labels of stacked panels up, however wide their tick labels are." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/align-labels_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.linspace(0, 10, 100)
fig, axs = plt.subplots(2, 2, figsize=(6.4, 4), layout="constrained")
for ax, scale in zip(axs[:, 0], (1, 10000)):
    ax.plot(t, scale * np.sin(t), color=rv.colour("blue"))
    ax.set_ylabel("amplitude")
for ax, scale in zip(axs[:, 1], (1, 10000)):
    ax.plot(t, scale * np.cos(t), color=rv.colour("red"))
    ax.set_ylabel("amplitude")
fig.align_ylabels(axs[:, 0])
fig.align_ylabels(axs[:, 1])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Neat stacked panels.
- **Key calls:** `fig.align_ylabels(axs[:, 0])`
- **Watch out:** Call after plotting.

## Axes tricks

### Inverted axis

<p align="center">
<img src="../img/layout/inverted-axis_light.png#gh-light-mode-only" alt="An inverted axis: here rank 1 is at the top, as people expect." width="640">
<img src="../img/layout/inverted-axis_dark.png#gh-dark-mode-only" alt="An inverted axis: here rank 1 is at the top, as people expect." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/inverted-axis_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rank = np.array([1, 2, 3, 4, 5])
wer = np.array([3.1, 3.4, 4.2, 5.0, 6.1])
fig, ax = plt.subplots(figsize=(5.6, 3.6), layout="constrained")
ax.plot(wer, rank, "o-", color=rv.colour("red"))
ax.invert_yaxis()
ax.set(xlabel="word error rate (%)", ylabel="rank (1 is best)", title="invert_yaxis()")
ax.set_yticks(rank)
ax.grid(axis="x", visible=True)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Rank 1 at top.
- **Key calls:** `ax.invert_yaxis()`
- **Watch out:** Check labels still make sense.

### Twin axes

<p align="center">
<img src="../img/layout/twin-axes_light.png#gh-light-mode-only" alt="twinx(): two y axes on one plot. Use it with care: the eye reads the crossing points, which mean nothing." width="640">
<img src="../img/layout/twin-axes_dark.png#gh-dark-mode-only" alt="twinx(): two y axes on one plot. Use it with care: the eye reads the crossing points, which mean nothing." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/twin-axes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.arange(1, 11)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.plot(t, 40 / t + 2, "o-", color=rv.colour("red"))
ax.set_ylabel("word error rate (%)", color=rv.colour("red"))
ax2 = ax.twinx()
ax2.plot(t, 0.5 * t ** 1.4, "s-", color=rv.colour("blue"))
ax2.set_ylabel("latency (s)", color=rv.colour("blue"))
ax2.grid(False)
ax2.spines["right"].set_visible(False)
ax.set(xlabel="model size (B parameters)", title="Two y axes with twinx()")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Two measures (use rarely).
- **Key calls:** `ax2 = ax.twinx()`
- **Watch out:** Colour each axis like its line; consider two panels instead.

### Secondary axis

<p align="center">
<img src="../img/layout/secondary-axis_light.png#gh-light-mode-only" alt="A secondary axis that is the same scale in other units: a clean use of two axes." width="640">
<img src="../img/layout/secondary-axis_dark.png#gh-dark-mode-only" alt="A secondary axis that is the same scale in other units: a clean use of two axes." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/secondary-axis_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

ms = np.linspace(50, 1000, 100)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.plot(ms, 100 * np.exp(-ms / 400), color=rv.colour("teal"), lw=2.4)
ax.set(xlabel="latency (ms)", ylabel="users still waiting (%)", title="secondary_xaxis")
sec = ax.secondary_xaxis("top", functions=(lambda x: x / 1000, lambda x: x * 1000))
sec.set_xlabel("latency (s)")
sec.spines["top"].set_visible(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Same data in other units.
- **Key calls:** `ax.secondary_xaxis('top', functions=(f, inv))`
- **Watch out:** A good use of two axes.

### Many y axes

<p align="center">
<img src="../img/layout/many-y-axes_light.png#gh-light-mode-only" alt="Three y axes with spines moved outward (shown here to explain the technique, not to recommend it)." width="640">
<img src="../img/layout/many-y-axes_dark.png#gh-dark-mode-only" alt="Three y axes with spines moved outward (shown here to explain the technique, not to recommend it)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/many-y-axes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

t = np.linspace(0, 10, 100)
fig, host = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
a2, a3 = host.twinx(), host.twinx()
a3.spines["right"].set_position(("outward", 52))
for ax, y, c, name in ((host, np.sin(t), "red", "STT"), (a2, 10 * np.cos(t / 2), "teal", "LLM"), (a3, 100 * t / 10, "violet", "TTS")):
    ax.plot(t, y, color=rv.colour(c), lw=2.2)
    ax.set_ylabel(name, color=rv.colour(c))
    ax.tick_params(axis="y", colors=rv.colour(c))
    ax.grid(False)
    ax.spines["right"].set_visible(ax is not host)
    ax.spines["right"].set_color(rv.colour(c))
host.set_xlabel("time")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Shown for completeness.
- **Key calls:** `ax3.spines['right'].set_position(('outward', 50))`
- **Watch out:** Hard to read; avoid in papers.

### Zoom inset

<p align="center">
<img src="../img/layout/inset-zoom_light.png#gh-light-mode-only" alt="A zoom inset: a magnified view of one region, with lines showing where it comes from." width="640">
<img src="../img/layout/inset-zoom_dark.png#gh-dark-mode-only" alt="A zoom inset: a magnified view of one region, with lines showing where it comes from." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/inset-zoom_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(8)
x = np.linspace(0, 10, 400)
y = np.sin(x) + 0.3 * np.sin(6 * x) + rng.normal(0, 0.05, x.size)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.plot(x, y, color=rv.colour("blue"), lw=1.4)
axins = ax.inset_axes([0.55, 0.58, 0.4, 0.36], xlim=(6.2, 7.2), ylim=(-1.5, -0.2))
axins.plot(x, y, color=rv.colour("blue"), lw=1.4)
axins.set_xticks([]); axins.set_yticks([]); axins.grid(False)
ax.indicate_inset_zoom(axins, edgecolor=rv.colour("grey"))
ax.set(title="Zoom inset")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A detail of a busy plot.
- **Key calls:** `ax.inset_axes([...])`; `ax.indicate_inset_zoom(axins)`
- **Watch out:** Show where the zoom comes from.

### Broken axis

<p align="center">
<img src="../img/layout/broken-axis_light.png#gh-light-mode-only" alt="A broken axis: two panels with the gap between them removed, so a far-off value does not squash everything else." width="640">
<img src="../img/layout/broken-axis_dark.png#gh-dark-mode-only" alt="A broken axis: two panels with the gap between them removed, so a far-off value does not squash everything else." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/broken-axis_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["Whisper", "Parakeet", "Conformer", "Baseline"]
vals = [3.1, 3.6, 4.4, 41.0]
fig, (top, bot) = plt.subplots(2, 1, figsize=(5.6, 4), sharex=True, gridspec_kw=dict(height_ratios=[1, 3], hspace=0.06))
for ax in (top, bot):
    ax.bar(names, vals, color=[rv.colour("teal")] * 3 + [rv.colour("grey")])
top.set_ylim(38, 44); bot.set_ylim(0, 6)
top.set_yticks([40, 44]); bot.set_yticks([0, 2, 4])
top.spines["bottom"].set_visible(False)
top.tick_params(bottom=False)
d = 0.012
kw = dict(transform=top.transAxes, color=plt.rcParams["text.color"], clip_on=False, lw=1.2)
top.plot((-d, +d), (-d * 3, +d * 3), **kw)
kw.update(transform=bot.transAxes)
bot.plot((-d, +d), (1 - d, 1 + d), **kw)
bot.set_ylabel("word error rate (%)")
bot.yaxis.set_label_coords(-0.09, 0.8)
top.set_title("Broken y axis", loc="left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** One far-off value.
- **Key calls:** Two panels sharing x with `height_ratios`
- **Watch out:** Mark the break and say so; avoid for bars where possible.

### Map projections

<p align="center">
<img src="../img/layout/projections_light.png#gh-light-mode-only" alt="Geographic projections: the same grid on Mollweide and Hammer axes." width="640">
<img src="../img/layout/projections_dark.png#gh-dark-mode-only" alt="Geographic projections: the same grid on Mollweide and Hammer axes." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/layout/projections_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig = plt.figure(figsize=(7, 3.2), layout="constrained")
for k, name in enumerate(("mollweide", "hammer")):
    ax = fig.add_subplot(1, 2, k + 1, projection=name)
    ax.grid(True, color=rv.colour("grey"), alpha=0.4)
    ax.scatter(np.deg2rad([174.8, 144.9, -0.1, -74.0, 139.7]), np.deg2rad([-41.3, -37.8, 51.5, 40.7, 35.7]), s=40, color=rv.colour("red"))
    ax.set_title(name, fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Geographic data.
- **Key calls:** `fig.add_subplot(projection='mollweide')`
- **Watch out:** Angles are in radians.

## Rules of thumb

- **Use `layout='constrained'`** from the start.
- **Size for the final page**, not for the screen.
- **Share axes** when panels will be compared.
- **Label panels** (a), (b), (c) so captions can refer to them.

**Back to the [home page](../index.md).**
