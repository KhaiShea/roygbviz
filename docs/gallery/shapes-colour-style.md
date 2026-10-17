# Shapes, colour and style

Drawing shapes by hand, choosing colour maps, and styling a whole session.

**Matplotlib reference:** `matplotlib.patches`, `matplotlib.collections`, `matplotlib.colors`, `plt.style`, `plt.rc_context`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Shapes and collections**: Patches, Fancy boxes, Pipeline diagram, Custom paths, Patch collections, Line collections, Hatches
- **Colour**: The nine colours, Colormaps, Lightness, Colour vision deficiency
- **Style**: Style sheets, Roygbviz against default, Temporary settings

## Shapes and collections

### Patches

<p align="center">
<img src="../img/shapes/patches_light.png#gh-light-mode-only" alt="Patches: circles, rectangles, ellipses, polygons and wedges drawn in data coordinates." width="640">
<img src="../img/shapes/patches_dark.png#gh-dark-mode-only" alt="Patches: circles, rectangles, ellipses, polygons and wedges drawn in data coordinates." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/patches_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, Wedge

fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.set(xlim=(0, 6), ylim=(0, 3.4), xticks=[], yticks=[]); ax.set_aspect("equal"); ax.grid(False)
cs = [rv.colour(c) for c in ("red", "orange", "yellow", "green", "teal", "blue")]
ax.add_patch(Circle((0.8, 2.3), 0.6, fc=cs[0], ec="none"))
ax.add_patch(Rectangle((1.8, 1.7), 1.2, 1.2, fc=cs[1], ec="none"))
ax.add_patch(Ellipse((4.2, 2.3), 1.6, 0.9, fc=cs[2], ec="none"))
ax.add_patch(Polygon([[0.3, 0.3], [1.5, 0.3], [0.9, 1.4]], fc=cs[3], ec="none"))
ax.add_patch(Wedge((2.8, 0.8), 0.8, 30, 300, fc=cs[4], ec="none"))
ax.add_patch(Rectangle((4, 0.2), 1.6, 1.2, fc=cs[5], ec="none", hatch="///"))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Circles, rectangles, polygons, wedges.
- **Key calls:** `ax.add_patch(Circle((x, y), r))`
- **Watch out:** Set `ax.set_aspect('equal')`.

### Fancy boxes

<p align="center">
<img src="../img/shapes/fancy-boxes_light.png#gh-light-mode-only" alt="Fancy boxes: rounded and bevelled boxes, useful for diagrams and call-outs." width="640">
<img src="../img/shapes/fancy-boxes_dark.png#gh-dark-mode-only" alt="Fancy boxes: rounded and bevelled boxes, useful for diagrams and call-outs." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/fancy-boxes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(6.4, 3), layout="constrained")
ax.set(xlim=(0, 6), ylim=(0, 2.6), xticks=[], yticks=[]); ax.grid(False)
for k, (style, c) in enumerate((("round", "red"), ("round4", "teal"), ("sawtooth", "violet"), ("roundtooth", "orange"))):
    x = 0.2 + k * 1.45
    ax.add_patch(FancyBboxPatch((x, 0.9), 1.0, 0.9, boxstyle=f"{style},pad=0.1", fc=rv.shade(c), ec=rv.colour(c), lw=1.6))
    ax.text(x + 0.5, 0.55, style, ha="center", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Diagram boxes.
- **Key calls:** `FancyBboxPatch(..., boxstyle='round,pad=0.1')`
- **Watch out:** Keep styles consistent.

### Pipeline diagram

<p align="center">
<img src="../img/shapes/pipeline-diagram_light.png#gh-light-mode-only" alt="A real diagram with patches and arrows: the cascade, STT to LLM to TTS, as boxes you can reuse." width="640">
<img src="../img/shapes/pipeline-diagram_dark.png#gh-dark-mode-only" alt="A real diagram with patches and arrows: the cascade, STT to LLM to TTS, as boxes you can reuse." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/pipeline-diagram_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

g = rv.group_map()
fig, ax = plt.subplots(figsize=(7.4, 2.6), layout="constrained")
ax.set(xlim=(0, 10), ylim=(0, 3)); ax.axis("off")
names = [("Audio in", "grey"), ("STT", g["STT"]), ("LLM", g["LLM"]), ("TTS", g["TTS"]), ("Audio out", "grey")]
for k, (n, c) in enumerate(names):
    col = rv.colour("grey") if c == "grey" else c
    x = 0.2 + k * 2.0
    ax.add_patch(FancyBboxPatch((x, 1.0), 1.5, 1.0, boxstyle="round,pad=0.05", fc=col if c != "grey" else rv.shade(rv.colour("grey")), ec="none"))
    ax.text(x + 0.75, 1.5, n, ha="center", va="center", fontsize=11, weight="bold", color="white" if c != "grey" else plt.rcParams["text.color"])
    if k < 4:
        ax.add_patch(FancyArrowPatch((x + 1.6, 1.5), (x + 1.95, 1.5), arrowstyle="-|>", mutation_scale=12, color=plt.rcParams["text.color"]))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Showing the STT, LLM, TTS cascade.
- **Key calls:** `FancyBboxPatch` and `FancyArrowPatch`
- **Watch out:** Use stage colours.

### Custom paths

<p align="center">
<img src="../img/shapes/paths_light.png#gh-light-mode-only" alt="Paths: a custom shape from Bezier curves, with codes saying how to draw each point." width="640">
<img src="../img/shapes/paths_dark.png#gh-dark-mode-only" alt="Paths: a custom shape from Bezier curves, with codes saying how to draw each point." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/paths_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import PathPatch
from matplotlib.path import Path as P

verts = [(0.2, 0.2), (0.2, 1.0), (1.0, 1.0), (1.0, 0.2), (0.6, 0.0), (0.2, 0.2)]
codes = [P.MOVETO, P.CURVE4, P.CURVE4, P.CURVE4, P.LINETO, P.CLOSEPOLY]
fig, ax = plt.subplots(figsize=(4.4, 3.4), layout="constrained")
ax.add_patch(PathPatch(P(verts, codes), fc=rv.shade("violet"), ec=rv.colour("violet"), lw=2))
ax.set(xlim=(0, 1.2), ylim=(-0.1, 1.2)); ax.set_aspect("equal"); ax.grid(False)
ax.set_title("Custom Path")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Bezier shapes.
- **Key calls:** `Path(verts, codes)`; `PathPatch`
- **Watch out:** Close the path with `CLOSEPOLY`.

### Patch collections

<p align="center">
<img src="../img/shapes/collections_light.png#gh-light-mode-only" alt="Collections: draw thousands of shapes as one object (fast), here circles coloured by value." width="640">
<img src="../img/shapes/collections_dark.png#gh-dark-mode-only" alt="Collections: draw thousands of shapes as one object (fast), here circles coloured by value." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/collections_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

rng = np.random.default_rng(1)
xy = rng.uniform(0, 10, (200, 2)); r = rng.uniform(0.1, 0.5, 200)
pc = PatchCollection([Circle(p, rr) for p, rr in zip(xy, r)], cmap="roygbviz", alpha=0.8)
pc.set_array(r)
fig, ax = plt.subplots(figsize=(5.4, 4), layout="constrained")
ax.add_collection(pc); ax.set(xlim=(0, 10), ylim=(0, 10)); ax.set_aspect("equal"); ax.grid(False)
fig.colorbar(pc, ax=ax, label="radius", shrink=0.8)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Thousands of shapes, fast.
- **Key calls:** `PatchCollection(patches, cmap=)`
- **Watch out:** Set the array for colour.

### Line collections

<p align="center">
<img src="../img/shapes/line-collection_light.png#gh-light-mode-only" alt="LineCollection: many line segments in one call, coloured by a value." width="640">
<img src="../img/shapes/line-collection_dark.png#gh-dark-mode-only" alt="LineCollection: many line segments in one call, coloured by a value." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/line-collection_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.collections import LineCollection

rng = np.random.default_rng(2)
segs = [np.c_[np.arange(30), rng.normal(size=30).cumsum() + k * 3] for k in range(12)]
lc = LineCollection(segs, array=np.arange(12), cmap="roygbviz", linewidths=1.8)
fig, ax = plt.subplots(figsize=(6, 3.6), layout="constrained")
ax.add_collection(lc); ax.autoscale()
ax.set_title("LineCollection")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Many lines at once.
- **Key calls:** `LineCollection(segments, array=)`
- **Watch out:** Call `ax.autoscale()`.

### Hatches

<p align="center">
<img src="../img/shapes/hatches_light.png#gh-light-mode-only" alt="Hatches: patterns that keep bars apart in black and white print or for colour-blind readers." width="640">
<img src="../img/shapes/hatches_dark.png#gh-dark-mode-only" alt="Hatches: patterns that keep bars apart in black and white print or for colour-blind readers." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/shapes/hatches_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
patterns = ["", "///", "\\\\\\", "xxx", "...", "ooo"]
for k, h in enumerate(patterns):
    ax.bar(k, 3 + (k % 3), color=rv.shade(("red", "orange", "teal", "blue", "violet", "pink")[k]), edgecolor=rv.colour(("red", "orange", "teal", "blue", "violet", "pink")[k]), hatch=h, lw=1.2)
ax.set_xticks(range(6)); ax.set_xticklabels([repr(h) for h in patterns])
ax.set_title("Hatching as a second encoding")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Black and white printing.
- **Key calls:** `hatch='///'`
- **Watch out:** Pair with a pale fill and a coloured edge.

## Colour

### The nine colours

<p align="center">
<img src="../img/colour/named-ramps_light.png#gh-light-mode-only" alt="The nine role colours as swatches, in rainbow order, each fetched by name with rv.colour()." width="640">
<img src="../img/colour/named-ramps_dark.png#gh-dark-mode-only" alt="The nine role colours as swatches, in rainbow order, each fetched by name with rv.colour()." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/colour/named-ramps_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["red", "orange", "yellow", "green", "teal", "blue", "indigo", "violet", "pink"]
cols = {n: rv.colour(n) for n in names}
fig, ax = plt.subplots(figsize=(7, 1.8), layout="constrained")
for k, (n, c) in enumerate(cols.items()):
    ax.add_patch(plt.Rectangle((k, 0), 0.92, 1, fc=c, ec="none"))
    ax.text(k + 0.46, -0.12, n, ha="center", va="top", fontsize=8)
ax.set(xlim=(0, 9), ylim=(-0.4, 1)); ax.axis("off")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Looking up the palette.
- **Key calls:** `rv.colour('teal')`
- **Watch out:** Fetch by name.

### Colormaps

<p align="center">
<img src="../img/colour/colormaps_light.png#gh-light-mode-only" alt="Roygbviz colormaps beside matplotlib's: sequential, multi-hue spectrum and diverging." width="640">
<img src="../img/colour/colormaps_dark.png#gh-dark-mode-only" alt="Roygbviz colormaps beside matplotlib's: sequential, multi-hue spectrum and diverging." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/colour/colormaps_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

g = np.linspace(0, 1, 256)[None, :]
names = ["roygbviz", "roygbviz_spectrum", "roygbviz_div", "viridis"]
fig, axs = plt.subplots(len(names), 1, figsize=(6.4, 2.6), layout="constrained")
for ax, n in zip(axs, names):
    ax.imshow(np.repeat(g, 8, 0), cmap=n, aspect="auto"); ax.axis("off")
    ax.set_title(n, loc="left", fontsize=8, pad=2)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Choosing a map.
- **Key calls:** `cmap='roygbviz'`, `'roygbviz_spectrum'`, `'roygbviz_div'`
- **Watch out:** Match scale type to the job.

### Lightness

<p align="center">
<img src="../img/colour/colormap-lightness_light.png#gh-light-mode-only" alt="Perceptual lightness (L*) along each colormap. A good sequential map rises smoothly in one direction." width="640">
<img src="../img/colour/colormap-lightness_dark.png#gh-dark-mode-only" alt="Perceptual lightness (L*) along each colormap. A good sequential map rises smoothly in one direction." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/colour/colormap-lightness_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

def lstar(rgb):
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    y = lin @ np.array([0.2126, 0.7152, 0.0722])
    return np.where(y > 216 / 24389, 116 * np.cbrt(y) - 16, 24389 / 27 * y)

g = np.linspace(0, 1, 256)
fig, ax = plt.subplots(figsize=(6, 3.6), layout="constrained")
for n, c in (("roygbviz", "blue"), ("roygbviz_spectrum", "red"), ("roygbviz_div", "violet"), ("viridis", "grey"), ("jet", "orange")):
    ax.plot(g, lstar(plt.get_cmap(n)(g)[:, :3]), color=rv.colour(c), label=n)
ax.set(xlabel="position along colormap", ylabel="lightness L*", title="Lightness along each colormap")
ax.legend()

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Checking a map is smooth.
- **Key calls:** Plot L* against position
- **Watch out:** Avoid maps whose lightness rises and falls.

### Colour vision deficiency

<p align="center">
<img src="../img/colour/cvd_light.png#gh-light-mode-only" alt="What the series colours look like with and without colour vision deficiency (simulated)." width="640">
<img src="../img/colour/cvd_dark.png#gh-dark-mode-only" alt="What the series colours look like with and without colour vision deficiency (simulated)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/colour/cvd_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

cols = [rv.colour(n) for n in ["red", "orange", "yellow", "green", "teal", "blue", "indigo", "violet", "pink"]]
rgb = np.array([[int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)] for c in cols])
# Machado et al. (2009) severity 1.0 matrices, applied in linear RGB
M = {"Normal": np.eye(3),
     "Protanopia": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]),
     "Deuteranopia": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]),
     "Tritanopia": np.array([[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]])}
lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
fig, ax = plt.subplots(figsize=(7, 2.8), layout="constrained")
for r, (name, m) in enumerate(M.items()):
    sim = np.clip(lin @ m.T, 0, 1)
    out = np.where(sim <= 0.0031308, sim * 12.92, 1.055 * sim ** (1 / 2.4) - 0.055)
    for k, c in enumerate(np.clip(out, 0, 1)):
        ax.add_patch(plt.Rectangle((k, -r), 0.92, 0.85, fc=c, ec="none"))
    ax.text(-0.15, -r + 0.42, name, ha="right", va="center", fontsize=9)
ax.set(xlim=(-2.4, 9), ylim=(-3.1, 1)); ax.axis("off")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Accessible figures.
- **Key calls:** Apply a CVD simulation
- **Watch out:** Add labels or hatching.

## Style

### Style sheets

<p align="center">
<img src="../img/style/sheets_light.png#gh-light-mode-only" alt="The same chart in five built-in style sheets, so you can see what Roygbviz changes." width="640">
<img src="../img/style/sheets_dark.png#gh-dark-mode-only" alt="The same chart in five built-in style sheets, so you can see what Roygbviz changes." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/style/sheets_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(5); y = [3, 5, 4, 6, 4.5]
sheets = ["default", "ggplot", "seaborn-v0_8", "bmh", "fivethirtyeight"]
fig = plt.figure(figsize=(8.4, 2.6))
for k, st in enumerate(sheets):
    with plt.style.context(st):
        ax = fig.add_subplot(1, 5, k + 1)
        ax.bar(x, y); ax.plot(x, y, "o-", color="k", lw=1)
        ax.set_title(st, fontsize=8)
        ax.tick_params(labelsize=6)
fig.tight_layout()

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Seeing the built-in options.
- **Key calls:** `plt.style.use('ggplot')`
- **Watch out:** Call `rv.use()` after.

### Roygbviz against default

<p align="center">
<img src="../img/style/roygbviz-vs-default_light.png#gh-light-mode-only" alt="Matplotlib defaults on the left, Roygbviz on the right: same code, same data." width="640">
<img src="../img/style/roygbviz-vs-default_dark.png#gh-dark-mode-only" alt="Matplotlib defaults on the left, Roygbviz on the right: same code, same data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/style/roygbviz-vs-default_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
t = np.linspace(0, 10, 100)
data = [np.sin(t + k) + rng.normal(0, 0.08, 100) for k in range(4)]
fig = plt.figure(figsize=(8, 3))
for k, ctx in enumerate((plt.style.context("default"), plt.rc_context(plt.rcParams.copy()))):
    with ctx:
        ax = fig.add_subplot(1, 2, k + 1)
        for i, d in enumerate(data):
            ax.plot(t, d, label=f"s{i + 1}")
        ax.legend(fontsize=7, ncols=4, loc="upper center")
        ax.set_title(("matplotlib default", "Roygbviz")[k])
fig.tight_layout()

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** What the theme changes.
- **Key calls:** `rv.use('light')`
- **Watch out:** One call is enough.

### Temporary settings

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


- **Use when:** One figure only.
- **Key calls:** `with plt.rc_context({'lines.linewidth': 3}):`
- **Watch out:** Does not leak to later figures.

## Rules of thumb

- **Pin colours** with `rv.colour_map`.
- **Use `rc_context`** for one-off changes.
- **Hatch** if the figure might be printed in greyscale.

**Back to the [home page](../index.md).**
