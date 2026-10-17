# Specialty, units, widgets and animation

Less common charts, axes helpers, interactive controls and moving pictures.

**Matplotlib reference:** `mpl_toolkits.axes_grid1`, `matplotlib.widgets`, `matplotlib.animation`, `matplotlib.sankey`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Specialty plots**: Anscombe's quartet, Hinton diagram, Sankey, Bullseye, Venn, Chart plus table
- **Axes helpers (axes_grid1)**: Matching colourbar, Image grid, Zoom with mark_inset
- **Units**: Categorical axes, Time units
- **Widgets**: Slider, Check and radio buttons
- **Animation**: Moving line, Growing bars, Growing scatter

## Specialty plots

### Anscombe's quartet

<p align="center">
<img src="../img/specialty/anscombe_light.png#gh-light-mode-only" alt="Anscombe's quartet: four datasets with the same mean, variance and correlation, and four different shapes. Always plot your data." width="640">
<img src="../img/specialty/anscombe_dark.png#gh-dark-mode-only" alt="Anscombe's quartet: four datasets with the same mean, variance and correlation, and four different shapes. Always plot your data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/specialty/anscombe_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
ys = [np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
      np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
      np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
      np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])]
xs = [x, x, x, np.array([8] * 7 + [19] + [8] * 3)]
fig, axs = plt.subplots(2, 2, figsize=(6.4, 4.8), sharex=True, sharey=True, layout="constrained")
for ax, xx, yy, n, c in zip(axs.ravel(), xs, ys, "I II III IV".split(), ("red", "teal", "violet", "orange")):
    ax.scatter(xx, yy, color=rv.colour(c), s=30)
    m, b = np.polyfit(xx, yy, 1)
    ax.plot([3, 20], [m * 3 + b, m * 20 + b], color=rv.colour("grey"), lw=1.4)
    ax.set_title(n, fontsize=10)
    ax.set_xlim(2, 20); ax.set_ylim(2, 14)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Why you must plot your data.
- **Key calls:** Four scatters with a shared fit
- **Watch out:** Same statistics, four shapes.

### Hinton diagram

<p align="center">
<img src="../img/specialty/hinton_light.png#gh-light-mode-only" alt="A Hinton diagram: square area shows the size of a number and colour shows its sign. Handy for weight matrices." width="640">
<img src="../img/specialty/hinton_dark.png#gh-dark-mode-only" alt="A Hinton diagram: square area shows the size of a number and colour shows its sign. Handy for weight matrices." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/specialty/hinton_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
w = rng.normal(size=(6, 6))
fig, ax = plt.subplots(figsize=(4.6, 4.4), layout="constrained")
ax.set(xlim=(-0.5, 5.5), ylim=(-0.5, 5.5)); ax.set_aspect("equal"); ax.invert_yaxis()
ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
for (i, j), v in np.ndenumerate(w):
    s = np.sqrt(abs(v) / np.abs(w).max())
    ax.add_patch(plt.Rectangle((j - s / 2, i - s / 2), s, s, fc=rv.colour("red") if v > 0 else rv.colour("blue"), ec="none"))
ax.set_title("Red positive, blue negative")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Weight matrices.
- **Key calls:** Squares sized by value, coloured by sign
- **Watch out:** Scale squares by the square root of magnitude.

### Sankey

<p align="center">
<img src="../img/specialty/sankey_light.png#gh-light-mode-only" alt="Sankey: how a quantity flows and splits. Here a request is split between three stages' time." width="640">
<img src="../img/specialty/sankey_dark.png#gh-dark-mode-only" alt="Sankey: how a quantity flows and splits. Here a request is split between three stages' time." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/specialty/sankey_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.sankey import Sankey

fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
ax.axis("off")
s = Sankey(ax=ax, scale=1 / 1000, offset=0.3, head_angle=120, margin=0.4)
s.add(flows=[1000, -250, -540, -210], labels=["Request", "STT", "LLM", "TTS"], orientations=[0, 1, 0, -1],
      facecolor=rv.colour("blue"), edgecolor="none", pathlengths=[0.3, 0.3, 0.3, 0.3])
s.finish()

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Flows that split.
- **Key calls:** `Sankey(ax=ax).add(flows=[...])`
- **Watch out:** Flows must sum to zero.

### Bullseye

<p align="center">
<img src="../img/specialty/bullseye_light.png#gh-light-mode-only" alt="A bullseye (concentric rings) made from nested wedges: a compact way to show nested categories." width="640">
<img src="../img/specialty/bullseye_dark.png#gh-dark-mode-only" alt="A bullseye (concentric rings) made from nested wedges: a compact way to show nested categories." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/specialty/bullseye_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import Wedge

fig, ax = plt.subplots(figsize=(4.4, 4.4), layout="constrained")
ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1)); ax.set_aspect("equal"); ax.axis("off")
for r, c in zip((1.0, 0.75, 0.5, 0.25), ("violet", "teal", "yellow", "red")):
    ax.add_patch(plt.Circle((0, 0), r, fc=rv.colour(c), ec=plt.rcParams["figure.facecolor"], lw=2))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Nested ranges.
- **Key calls:** `plt.Circle` from largest to smallest
- **Watch out:** Decorative; use sparingly.

### Venn

<p align="center">
<img src="../img/specialty/venn-sets_light.png#gh-light-mode-only" alt="A simple Venn diagram built from circles: overlap is shown by transparency, so keep it to two or three sets." width="640">
<img src="../img/specialty/venn-sets_dark.png#gh-dark-mode-only" alt="A simple Venn diagram built from circles: overlap is shown by transparency, so keep it to two or three sets." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/specialty/venn-sets_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import Circle

fig, ax = plt.subplots(figsize=(5, 3.6), layout="constrained")
ax.set(xlim=(0, 6), ylim=(0, 4)); ax.set_aspect("equal"); ax.axis("off")
for (x, y), c, n in (((2.2, 2.0), "red", "Fast"), ((3.8, 2.0), "teal", "Accurate")):
    ax.add_patch(Circle((x, y), 1.5, fc=rv.colour(c), alpha=0.5, ec="none"))
    ax.text(x + (-0.9 if c == "red" else 0.9), y, n, ha="center", va="center", weight="bold")
ax.text(3, 2, "Both", ha="center", va="center", weight="bold")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Two or three sets.
- **Key calls:** `Circle` with `alpha=0.5`
- **Watch out:** Do not show sizes unless you scale them.

### Chart plus table

<p align="center">
<img src="../img/specialty/table_light.png#gh-light-mode-only" alt="A table next to a chart: when readers need exact numbers, give them numbers." width="640">
<img src="../img/specialty/table_dark.png#gh-dark-mode-only" alt="A table next to a chart: when readers need exact numbers, give them numbers." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/specialty/table_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["Whisper", "Parakeet", "Conformer"]
vals = [3.1, 3.6, 4.4]
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.4, 2.8), gridspec_kw={"width_ratios": [1.2, 1]}, layout="constrained")
ax.barh(names, vals, color=rv.colour("teal")); ax.invert_yaxis(); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax2.axis("off")
tb = ax2.table(cellText=[[n, f"{v:.1f}"] for n, v in zip(names, vals)], colLabels=["Model", "WER (%)"], loc="center", cellLoc="left")
tb.auto_set_font_size(False); tb.set_fontsize(10); tb.scale(1, 1.5)
for (r, c), cell in tb.get_celld().items():
    cell.set_edgecolor(plt.rcParams["grid.color"]); cell.set_linewidth(0.8)
    if r == 0:
        cell.set_text_props(weight="bold")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Exact numbers beside a chart.
- **Key calls:** `ax.table(cellText=, colLabels=)`
- **Watch out:** Keep tables short.

## Axes helpers (axes_grid1)

### Matching colourbar

<p align="center">
<img src="../img/grid1/inset-colorbar_light.png#gh-light-mode-only" alt="axes_grid1: make_axes_locatable adds a colourbar that always matches the image height, however the figure is resized." width="640">
<img src="../img/grid1/inset-colorbar_dark.png#gh-dark-mode-only" alt="axes_grid1: make_axes_locatable adds a colourbar that always matches the image height, however the figure is resized." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/grid1/inset-colorbar_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from mpl_toolkits.axes_grid1 import make_axes_locatable

rng = np.random.default_rng(1)
fig, ax = plt.subplots(figsize=(4.8, 3.6))
im = ax.imshow(rng.random((8, 12)), cmap="roygbviz"); ax.grid(False)
cax = make_axes_locatable(ax).append_axes("right", size="4%", pad=0.1)
fig.colorbar(im, cax=cax)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A colourbar the same height as the image.
- **Key calls:** `make_axes_locatable(ax).append_axes('right', size='4%')`
- **Watch out:** Resizes correctly.

### Image grid

<p align="center">
<img src="../img/grid1/image-grid_light.png#gh-light-mode-only" alt="ImageGrid: a tight grid of images with one shared colourbar and no wasted space." width="640">
<img src="../img/grid1/image-grid_dark.png#gh-dark-mode-only" alt="ImageGrid: a tight grid of images with one shared colourbar and no wasted space." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/grid1/image-grid_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from mpl_toolkits.axes_grid1 import ImageGrid

rng = np.random.default_rng(2)
fig = plt.figure(figsize=(6.4, 3.2))
grid = ImageGrid(fig, 111, nrows_ncols=(2, 3), axes_pad=0.08, cbar_mode="single", cbar_location="right", cbar_pad=0.1)
for ax in grid:
    im = ax.imshow(rng.random((8, 8)), vmin=0, vmax=1, cmap="roygbviz"); ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([])
grid.cbar_axes[0].colorbar(im)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A tight grid of images.
- **Key calls:** `ImageGrid(fig, 111, nrows_ncols=(2, 3), cbar_mode='single')`
- **Watch out:** Shared scale.

### Zoom with mark_inset

<p align="center">
<img src="../img/grid1/parasite_light.png#gh-light-mode-only" alt="A second view of the same plot: zoom inset with mark_inset, placed by inset_axes from axes_grid1." width="640">
<img src="../img/grid1/parasite_dark.png#gh-dark-mode-only" alt="A second view of the same plot: zoom inset with mark_inset, placed by inset_axes from axes_grid1." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/grid1/parasite_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

rng = np.random.default_rng(3)
x = np.linspace(0, 10, 300); y = np.sin(x) + 0.4 * np.sin(8 * x) * (x > 6) + rng.normal(0, 0.03, 300)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.plot(x, y, color=rv.colour("blue"))
ins = inset_axes(ax, width="40%", height="40%", loc="lower left", borderpad=1.5)
ins.plot(x, y, color=rv.colour("blue")); ins.set_xlim(6, 8); ins.set_ylim(-1.5, 1.5); ins.set_xticks([]); ins.set_yticks([]); ins.grid(False)
mark_inset(ax, ins, loc1=2, loc2=4, fc="none", ec=rv.colour("grey"))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Detail of a region.
- **Key calls:** `inset_axes(...)`, `mark_inset(...)`
- **Watch out:** Pick a corner that avoids data.

## Units

### Categorical axes

<p align="center">
<img src="../img/units/categorical_light.png#gh-light-mode-only" alt="Categorical axes: pass strings and matplotlib places them on integer positions in the order first seen." width="640">
<img src="../img/units/categorical_dark.png#gh-dark-mode-only" alt="Categorical axes: pass strings and matplotlib places them on integer positions in the order first seen." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/units/categorical_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axs = plt.subplots(1, 2, figsize=(7, 3), layout="constrained")
names = ["low", "medium", "high"]
axs[0].plot(["medium", "high", "low", "high"], [2, 3, 1, 3], "o-", color=rv.colour("red")); axs[0].set_title("Order first seen", fontsize=10)
axs[1].plot(names + ["high"], [1, 2, 3, 3], "o-", color=rv.colour("teal")); axs[1].set_title("Order you set", fontsize=10)
axs[1].set_xticks(names)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Strings as positions.
- **Key calls:** `ax.plot(['a', 'b'], [1, 2])`
- **Watch out:** Set order explicitly.

### Time units

<p align="center">
<img src="../img/units/timedelta_light.png#gh-light-mode-only" alt="Time units: plot timedeltas directly, then label the axis in whatever unit the reader expects." width="640">
<img src="../img/units/timedelta_dark.png#gh-dark-mode-only" alt="Time units: plot timedeltas directly, then label the axis in whatever unit the reader expects." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/units/timedelta_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import pandas as pd

t = pd.to_timedelta(np.arange(0, 600, 30), unit="s")
fig, ax = plt.subplots(figsize=(5.8, 3.2), layout="constrained")
ax.plot(t.total_seconds() / 60, np.arange(len(t)) ** 1.3, color=rv.colour("blue"))
ax.set(xlabel="elapsed (minutes)", ylabel="requests served", title="Convert once, label clearly")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Seconds or minutes.
- **Key calls:** Convert once, label clearly
- **Watch out:** Say the unit.

## Widgets

### Slider

<p align="center">
<img src="../img/widgets/slider_light.png#gh-light-mode-only" alt="A Slider widget, drawn as it would appear in an interactive window. Use it in Jupyter or a desktop window, not in a saved PNG." width="640">
<img src="../img/widgets/slider_dark.png#gh-dark-mode-only" alt="A Slider widget, drawn as it would appear in an interactive window. Use it in Jupyter or a desktop window, not in a saved PNG." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/widgets/slider_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.widgets import Slider

t = np.linspace(0, 1, 500)
fig, ax = plt.subplots(figsize=(6, 3.8))
fig.subplots_adjust(bottom=0.25)
line, = ax.plot(t, np.sin(2 * np.pi * 3 * t), color=rv.colour("blue"))
ax.set_ylim(-1.2, 1.2)
sax = fig.add_axes([0.15, 0.08, 0.7, 0.04])
s = Slider(sax, "freq", 1, 10, valinit=3, color=rv.colour("blue"))
s.on_changed(lambda v: (line.set_ydata(np.sin(2 * np.pi * v * t)), fig.canvas.draw_idle()))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Exploring a parameter.
- **Key calls:** `Slider(ax, 'freq', 1, 10, valinit=3)`
- **Watch out:** Needs an interactive backend.

### Check and radio buttons

<p align="center">
<img src="../img/widgets/buttons_light.png#gh-light-mode-only" alt="Check buttons and radio buttons, to turn series on and off or pick one option." width="640">
<img src="../img/widgets/buttons_dark.png#gh-dark-mode-only" alt="Check buttons and radio buttons, to turn series on and off or pick one option." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/widgets/buttons_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.widgets import CheckButtons, RadioButtons

fig, ax = plt.subplots(figsize=(6.4, 3.6))
fig.subplots_adjust(left=0.28)
t = np.linspace(0, 6, 100)
ls = [ax.plot(t, np.sin(t + k), color=rv.colour(c), label=n)[0] for k, (c, n) in enumerate((("red", "STT"), ("teal", "LLM"), ("violet", "TTS")))]
cax = fig.add_axes([0.02, 0.55, 0.2, 0.3]); cax.set_facecolor("none")
chk = CheckButtons(cax, ["STT", "LLM", "TTS"], [True, True, True])
rax = fig.add_axes([0.02, 0.15, 0.2, 0.3]); rax.set_facecolor("none")
rad = RadioButtons(rax, ["linear", "log"])
chk.on_clicked(lambda lab: (ls[["STT", "LLM", "TTS"].index(lab)].set_visible(not ls[["STT", "LLM", "TTS"].index(lab)].get_visible()), fig.canvas.draw_idle()))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Toggle series or options.
- **Key calls:** `CheckButtons`, `RadioButtons`
- **Watch out:** Static images show the layout only.

## Animation

### Moving line

<p align="center">
<img src="../img/anim/sine-wave_light.gif" alt="A sine wave that travels. FuncAnimation calls update() once per frame; blit=False is the safe choice." width="640">
</p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(5.6, 3), layout="constrained")
x = np.linspace(0, 2 * np.pi, 200)
line, = ax.plot(x, np.sin(x), color=rv.colour("blue"))
ax.set(ylim=(-1.3, 1.3), title="FuncAnimation")

def update(i):
    line.set_ydata(np.sin(x + i * 0.1))
    return (line,)

anim = FuncAnimation(fig, update, frames=62, interval=50)

anim.save("figure.gif", writer="pillow", fps=20)
```

</details>


- **Use when:** Showing change.
- **Key calls:** `FuncAnimation(fig, update, frames=, interval=)`
- **Watch out:** Keep it short.

### Growing bars

<p align="center">
<img src="../img/anim/bar-race_light.gif" alt="Bars that grow as a number is revealed. Keep animations short, and make sure the last frame says the whole story." width="640">
</p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(5.6, 3), layout="constrained")
names = ["Whisper", "Parakeet", "Conformer"]; final = np.array([3.1, 3.6, 4.4])
bars = ax.bar(names, np.zeros(3), color=[rv.colour(c) for c in ("red", "yellow", "teal")])
ax.set(ylim=(0, 5), ylabel="WER (%)", title="Word error rate")

def update(i):
    k = min(i, 30) / 30
    for b, v in zip(bars, final * k):
        b.set_height(v)
    return bars

anim = FuncAnimation(fig, update, frames=45, interval=50)

anim.save("figure.gif", writer="pillow", fps=20)
```

</details>


- **Use when:** Revealing values.
- **Key calls:** Set bar heights each frame
- **Watch out:** End on the full picture.

### Growing scatter

<p align="center">
<img src="../img/anim/scatter-grow_light.gif" alt="A scatter plot that fills in point by point, to show how a sample builds up." width="640">
</p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
pts = rng.normal(size=(120, 2))
fig, ax = plt.subplots(figsize=(4.6, 4), layout="constrained")
sc = ax.scatter([], [], color=rv.colour("violet"), s=24)
ax.set(xlim=(-3.5, 3.5), ylim=(-3.5, 3.5), title="Sampling")
ax.set_aspect("equal")

def update(i):
    sc.set_offsets(pts[: i + 1])
    return (sc,)

anim = FuncAnimation(fig, update, frames=120, interval=40)

anim.save("figure.gif", writer="pillow", fps=20)
```

</details>


- **Use when:** How a sample builds.
- **Key calls:** `sc.set_offsets(pts[:i])`
- **Watch out:** Fix the axis limits first.

## Event handling and embedding

These have no still picture, because they are about reacting to a mouse, key or window. The patterns are short.

**Respond to clicks**

```python
def on_click(event):
    if event.inaxes:
        print(f"clicked at x={event.xdata:.2f}, y={event.ydata:.2f}")

fig.canvas.mpl_connect("button_press_event", on_click)
```

**Respond to keys**

```python
def on_key(event):
    if event.key == "q":
        plt.close(event.canvas.figure)

fig.canvas.mpl_connect("key_press_event", on_key)
```

**Pick a point** (set `picker=True` on the artist, then connect `pick_event`).

**Interactive notebooks:** `%matplotlib widget` (needs `ipympl`) gives pan, zoom and sliders in Jupyter.

**Embedding in apps:** use `FigureCanvasQTAgg` (Qt), `FigureCanvasTkAgg` (Tk) or `FigureCanvasWebAgg`. In web apps, saving a PNG or SVG with `fig.savefig(buffer, format="png")` is usually simpler.

**Headless servers:** set the backend to `Agg` (`MPLBACKEND=Agg`) so no window is needed.

## Rules of thumb

- **Animations** should loop quickly and end on a clear frame.
- **Widgets** need an interactive backend (`%matplotlib widget`).
- **Specialty charts** are rarely the best choice. Check the [choosing guide](../guide/choosing.md) first.

**Back to the [home page](../index.md).**
