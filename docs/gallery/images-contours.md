# Images, contours and fields

Anything laid out on a grid: pictures, matrices, heat maps, surfaces and vector fields.

**Matplotlib reference:** `ax.imshow`, `ax.pcolormesh`, `ax.contour`, `ax.contourf`, `ax.quiver`, `ax.streamplot`. In plotnine: `geom_tile`, `geom_raster`, `geom_contour`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Grids of numbers**: imshow, Masked cells, Shared colourbar, Interpolation, Blend two layers, Colour normalisations, matshow, Sparsity pattern, Barcode, Affine transform, Clip to a shape
- **Heat maps**: Annotated heat map, Confusion matrix, Correlation matrix, Spectrogram
- **Grids with real coordinates**: pcolormesh, Shading options, Triangulated data, Hillshade
- **Contours**: Contour lines, Filled contours, Hatched contours, Log contours
- **Vector fields**: Quiver, Wind barbs, Streamplot

## Grids of numbers

### imshow

<p align="center">
<img src="../img/images/imshow_light.png#gh-light-mode-only" alt="imshow() draws a grid of numbers as coloured cells." width="640">
<img src="../img/images/imshow_dark.png#gh-dark-mode-only" alt="imshow() draws a grid of numbers as coloured cells." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/imshow_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-3, 3, 240), np.linspace(-2, 2, 160))
z = np.exp(-(x - 1) ** 2 - y ** 2) - 0.7 * np.exp(-(x + 1) ** 2 - (y + 0.5) ** 2) + 0.2 * np.sin(3 * x) * np.exp(-y ** 2)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
im = ax.imshow(z, cmap="roygbviz", origin="lower", extent=(-3, 3, -2, 2), aspect="auto")
fig.colorbar(im, ax=ax, label="value", shrink=0.9)
ax.set(xlabel="x", ylabel="y", title="imshow")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A regular grid of values.
- **Key calls:** `ax.imshow(a, cmap='roygbviz', vmin=, vmax=)`
- **Watch out:** Set `vmin` and `vmax` when comparing images.

### Masked cells

<p align="center">
<img src="../img/images/masked_light.png#gh-light-mode-only" alt="Masked values: cells you mark as missing are drawn in a 'bad' colour (here a hatched grey), not the colormap's lowest colour." width="640">
<img src="../img/images/masked_dark.png#gh-dark-mode-only" alt="Masked values: cells you mark as missing are drawn in a 'bad' colour (here a hatched grey), not the colormap's lowest colour." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/masked_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
z = np.exp(-x ** 2 - y ** 2)
z = np.ma.masked_where(np.hypot(x - 1, y) < 0.9, z)
cmap = plt.get_cmap("roygbviz").copy()
cmap.set_bad(rv.colour("grey"))
fig, ax = plt.subplots(figsize=(5, 4.2), layout="constrained")
im = ax.imshow(z, cmap=cmap, origin="lower", extent=(-3, 3, -3, 3))
fig.colorbar(im, ax=ax, shrink=0.85)
ax.set(title="Masked cells in grey")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Missing values.
- **Key calls:** `np.ma.masked_invalid(a)`; `cmap.set_bad(...)`
- **Watch out:** Choose a 'bad' colour that is not in the scale.

### Shared colourbar

<p align="center">
<img src="../img/images/shared-colorbar_light.png#gh-light-mode-only" alt="Several images on one colour scale, with one colorbar: only honest if they share vmin and vmax." width="640">
<img src="../img/images/shared-colorbar_dark.png#gh-dark-mode-only" alt="Several images on one colour scale, with one colorbar: only honest if they share vmin and vmax." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/shared-colorbar_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(1)
base = np.add.outer(np.linspace(0, 1, 30), np.linspace(0, 1, 30))
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9), layout="constrained")
for ax, k, name in zip(axs, (1.0, 0.7, 0.4), ("Whisper", "Parakeet", "Conformer")):
    im = ax.imshow(base * k + rng.normal(0, 0.04, base.shape), cmap="roygbviz", vmin=0, vmax=2)
    ax.set_title(name, fontsize=10)
    ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(im, ax=axs, shrink=0.8, label="error")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Several images that must be compared.
- **Key calls:** `fig.colorbar(im, ax=axs)`
- **Watch out:** Same `vmin` and `vmax` for all.

### Interpolation

<p align="center">
<img src="../img/images/interpolation_light.png#gh-light-mode-only" alt="The same 4 x 4 array shown with six interpolation methods: nearest keeps the squares, the rest smooth them." width="640">
<img src="../img/images/interpolation_dark.png#gh-dark-mode-only" alt="The same 4 x 4 array shown with six interpolation methods: nearest keeps the squares, the rest smooth them." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/interpolation_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

a = np.array([[0.1, 0.8, 0.3, 0.9], [0.6, 0.2, 0.7, 0.4], [0.9, 0.5, 0.1, 0.8], [0.3, 0.7, 0.6, 0.2]])
fig, axs = plt.subplots(2, 3, figsize=(6.8, 4.6), layout="constrained")
for ax, m in zip(axs.ravel(), ("nearest", "bilinear", "bicubic", "hanning", "lanczos", "antialiased")):
    ax.imshow(a, interpolation=m, cmap="roygbviz")
    ax.set_title(m, fontsize=10)
    ax.grid(False); ax.set_xticks([]); ax.set_yticks([])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** How pixels are smoothed.
- **Key calls:** `interpolation='nearest'`, `'bilinear'`, `'bicubic'`
- **Watch out:** Use `nearest` for data; smoothing can invent detail.

### Blend two layers

<p align="center">
<img src="../img/images/alpha-blend_light.png#gh-light-mode-only" alt="Layering: a hot spot drawn over a base image with alpha, so the picture underneath still shows through." width="640">
<img src="../img/images/alpha-blend_dark.png#gh-dark-mode-only" alt="Layering: a hot spot drawn over a base image with alpha, so the picture underneath still shows through." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/alpha-blend_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

xx, yy = np.meshgrid(np.linspace(-1, 1, 200), np.linspace(-1, 1, 140))
base = np.sin(8 * xx) * np.cos(6 * yy) + 0.5 * np.sin(3 * (xx + yy))          # a stand-in for a photo
spot = np.exp(-4 * ((xx - 0.3) ** 2 + (yy + 0.2) ** 2)) + 0.6 * np.exp(-8 * ((xx + 0.5) ** 2 + (yy - 0.4) ** 2))
fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
ax.imshow(base, cmap="gray", alpha=0.55)
im = ax.imshow(np.ma.masked_less(spot, 0.25), cmap="roygbviz_spectrum", alpha=0.8, vmin=0, vmax=1.1)
fig.colorbar(im, ax=ax, shrink=0.85, label="attention")
ax.set(title="Two layers with alpha")
ax.grid(False); ax.set_xticks([]); ax.set_yticks([])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A map over a base image.
- **Key calls:** `ax.imshow(top, alpha=0.6)`
- **Watch out:** Keep the base image muted.

### Colour normalisations

<p align="center">
<img src="../img/images/normalisations_light.png#gh-light-mode-only" alt="The same data under six colour normalisations. The data did not change, only how values map to colour." width="640">
<img src="../img/images/normalisations_dark.png#gh-dark-mode-only" alt="The same data under six colour normalisations. The data did not change, only how values map to colour." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/normalisations_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import colors as mc

x, y = np.meshgrid(np.linspace(0, 3, 120), np.linspace(0, 3, 120))
z = np.exp(x * 1.6) * np.sin(2 * y) * 0.3
norms = {"Normalize (linear)": mc.Normalize(), "PowerNorm(0.4)": mc.PowerNorm(0.4),
         "SymLogNorm": mc.SymLogNorm(linthresh=1, vmin=z.min(), vmax=z.max()),
         "TwoSlopeNorm(0)": mc.TwoSlopeNorm(0, z.min(), z.max()),
         "BoundaryNorm (6 bins)": mc.BoundaryNorm(np.linspace(z.min(), z.max(), 7), 256),
         "CenteredNorm": mc.CenteredNorm()}
fig, axs = plt.subplots(2, 3, figsize=(7.2, 4.6), layout="constrained")
for ax, (name, norm) in zip(axs.ravel(), norms.items()):
    cmap = "roygbviz_div" if "Two" in name or "Centered" in name or "SymLog" in name else "roygbviz"
    im = ax.imshow(z, norm=norm, cmap=cmap, origin="lower")
    ax.set_title(name, fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.grid(False); ax.set_xticks([]); ax.set_yticks([])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Skewed data.
- **Key calls:** `norm=LogNorm()`, `PowerNorm`, `TwoSlopeNorm`
- **Watch out:** State the scale in the colourbar label.

### matshow

<p align="center">
<img src="../img/images/matshow_light.png#gh-light-mode-only" alt="matshow() is imshow() tuned for matrices: the x ticks go on top and the first row is at the top." width="640">
<img src="../img/images/matshow_dark.png#gh-dark-mode-only" alt="matshow() is imshow() tuned for matrices: the x ticks go on top and the first row is at the top." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/matshow_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(5)
a = rng.random((8, 8))
fig, ax = plt.subplots(figsize=(4.6, 4.4), layout="constrained")
ax.matshow(a, cmap="roygbviz")
ax.set(title="matshow")
ax.title.set_position((0.5, 1.12))
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Matrices.
- **Key calls:** `ax.matshow(m)`
- **Watch out:** Row zero is at the top.

### Sparsity pattern

<p align="center">
<img src="../img/images/spy_light.png#gh-light-mode-only" alt="spy() shows where a matrix is non-zero: a quick look at sparsity." width="640">
<img src="../img/images/spy_dark.png#gh-dark-mode-only" alt="spy() shows where a matrix is non-zero: a quick look at sparsity." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/spy_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from scipy import sparse

a = sparse.random(60, 60, density=0.05, random_state=1) + sparse.diags([1, 1, 1], [-1, 0, 1], shape=(60, 60))
fig, ax = plt.subplots(figsize=(4.6, 4.6), layout="constrained")
ax.spy(a, markersize=3, color=rv.colour("blue"))
ax.set(title="Sparsity pattern")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Where a matrix is non-zero.
- **Key calls:** `ax.spy(m)`
- **Watch out:** Quick check, not a final figure.

### Barcode

<p align="center">
<img src="../img/images/barcode_light.png#gh-light-mode-only" alt="A barcode: a one-dimensional signal as stripes, handy for showing many on/off tracks compactly." width="640">
<img src="../img/images/barcode_dark.png#gh-dark-mode-only" alt="A barcode: a one-dimensional signal as stripes, handy for showing many on/off tracks compactly." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/barcode_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.colors import ListedColormap

rng = np.random.default_rng(7)
code = (rng.random(120) > 0.55).astype(float)
fig, ax = plt.subplots(figsize=(6, 1.8), layout="constrained")
ax.imshow(code.reshape(1, -1), aspect="auto", cmap=ListedColormap([plt.rcParams["figure.facecolor"], rv.colour("blue")]), interpolation="nearest")
ax.set_axis_off()
ax.set_title("Speech (dark) and silence (light) per frame", loc="left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Many on/off tracks.
- **Key calls:** `ax.imshow(bits, aspect='auto', cmap='binary')`
- **Watch out:** Label rows.

### Affine transform

<p align="center">
<img src="../img/images/affine_light.png#gh-light-mode-only" alt="An affine transform of an image: rotate and shear it without resampling the data yourself." width="640">
<img src="../img/images/affine_dark.png#gh-dark-mode-only" alt="An affine transform of an image: rotate and shear it without resampling the data yourself." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/affine_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import matplotlib.transforms as mtransforms

x, y = np.meshgrid(np.linspace(-2, 2, 100), np.linspace(-2, 2, 100))
z = np.sin(x * 3) * np.cos(y * 3)
fig, axs = plt.subplots(1, 2, figsize=(7, 3.4), layout="constrained")
axs[0].imshow(z, cmap="roygbviz", extent=(-2, 2, -2, 2), origin="lower")
axs[0].set_title("original", fontsize=10)
ax = axs[1]
tr = mtransforms.Affine2D().rotate_deg(25).skew_deg(15, 0) + ax.transData
ax.imshow(z, cmap="roygbviz", extent=(-2, 2, -2, 2), origin="lower", transform=tr, clip_on=True)
ax.set(xlim=(-4, 4), ylim=(-3, 3))
ax.set_title("rotated and sheared", fontsize=10)
for a in axs:
    a.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Rotate or shear an image.
- **Key calls:** `im.set_transform(Affine2D()...)`
- **Watch out:** Reset the axis limits afterwards.

### Clip to a shape

<p align="center">
<img src="../img/images/clip-patch_light.png#gh-light-mode-only" alt="Clipping an image with a patch: show the picture only inside a circle." width="640">
<img src="../img/images/clip-patch_dark.png#gh-dark-mode-only" alt="Clipping an image with a patch: show the picture only inside a circle." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/clip-patch_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.patches import Circle

x, y = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
z = np.sin(3 * x) * np.cos(3 * y)
fig, ax = plt.subplots(figsize=(4.6, 4.4), layout="constrained")
im = ax.imshow(z, cmap="roygbviz_spectrum", extent=(-2, 2, -2, 2), origin="lower")
patch = Circle((0, 0), 1.7, transform=ax.transData)
im.set_clip_path(patch)
ax.add_patch(Circle((0, 0), 1.7, fill=False, ec=rv.colour("grey"), lw=2))
ax.set(title="Clipped to a circle")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Show part of an image.
- **Key calls:** `im.set_clip_path(patch)`
- **Watch out:** Add the patch to the axes first.

## Heat maps

### Annotated heat map

<p align="center">
<img src="../img/images/heatmap-annotated_light.png#gh-light-mode-only" alt="An annotated heat map: the number in each cell, in a text colour that stays readable on every background." width="640">
<img src="../img/images/heatmap-annotated_dark.png#gh-dark-mode-only" alt="An annotated heat map: the number in each cell, in a text colour that stays readable on every background." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/heatmap-annotated_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["STT", "LLM", "TTS", "Total"]
conds = ["Clean", "Noisy", "Accented", "Far-field"]
v = np.array([[3.1, 7.4, 9.2, 12.8], [2.8, 8.9, 8.1, 13.5], [3.9, 9.8, 10.7, 16.2], [4.5, 9.0, 11.0, 14.0]])
fig, ax = plt.subplots(figsize=(5.6, 4.2), layout="constrained")
im = ax.imshow(v, cmap="roygbviz")
ax.set_xticks(range(4), conds)
ax.set_yticks(range(4), ["Whisper", "Parakeet", "Conformer", "Canary"])
for i in range(4):
    for j in range(4):
        dark = im.norm(v[i, j]) > 0.55                   # pale cells get dark text, deep cells get light text
        ax.text(j, i, f"{v[i, j]:.1f}", ha="center", va="center", fontsize=10,
                color=plt.rcParams["figure.facecolor"] if dark else plt.rcParams["text.color"])
ax.set_xticks(np.arange(-0.5, 4), minor=True)
ax.set_yticks(np.arange(-0.5, 4), minor=True)
ax.grid(which="minor", color=plt.rcParams["figure.facecolor"], lw=3)
ax.tick_params(which="minor", length=0)
ax.grid(False, which="major")
fig.colorbar(im, ax=ax, label="word error rate (%)", shrink=0.85)
ax.set(title="Annotated heat map")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A table you want readers to scan.
- **Key calls:** `ax.imshow` plus `ax.text(j, i, value)`
- **Watch out:** Switch the text colour by cell darkness.

### Confusion matrix

<p align="center">
<img src="../img/images/confusion-matrix_light.png#gh-light-mode-only" alt="A confusion matrix, normalised by row so each row sums to 1: the diagonal is what the model got right." width="640">
<img src="../img/images/confusion-matrix_dark.png#gh-dark-mode-only" alt="A confusion matrix, normalised by row so each row sums to 1: the diagonal is what the model got right." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/confusion-matrix_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

labels = ["happy", "sad", "angry", "neutral"]
counts = np.array([[82, 5, 3, 10], [6, 74, 8, 12], [4, 9, 79, 8], [11, 10, 7, 72]], float)
rate = counts / counts.sum(1, keepdims=True)
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
im = ax.imshow(rate, cmap="roygbviz", vmin=0, vmax=1)
ax.set_xticks(range(4), labels)
ax.set_yticks(range(4), labels)
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{rate[i, j]:.0%}", ha="center", va="center", fontsize=10,
                color=plt.rcParams["figure.facecolor"] if rate[i, j] > 0.5 else plt.rcParams["text.color"])
ax.set(xlabel="Predicted", ylabel="Actual", title="Emotion recognition")
ax.grid(False)
fig.colorbar(im, ax=ax, shrink=0.85)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Where a classifier is wrong.
- **Key calls:** `ConfusionMatrixDisplay` or `imshow` of counts
- **Watch out:** Normalise by row so classes of different sizes compare.

### Correlation matrix

<p align="center">
<img src="../img/images/correlation-matrix_light.png#gh-light-mode-only" alt="A correlation matrix: a diverging scale centred on zero, so positive and negative are different colours." width="640">
<img src="../img/images/correlation-matrix_dark.png#gh-dark-mode-only" alt="A correlation matrix: a diverging scale centred on zero, so positive and negative are different colours." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/correlation-matrix_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(4)
names = ["WER", "CER", "Latency", "MOS", "Cost"]
base = rng.normal(size=(200, 2))
data = np.column_stack([base[:, 0], base[:, 0] * 0.9 + rng.normal(0, 0.3, 200), base[:, 1], -base[:, 0] * 0.6 + rng.normal(0, 0.7, 200),
                        base[:, 1] * 0.7 + rng.normal(0, 0.7, 200)])
c = np.corrcoef(data.T)
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
im = ax.imshow(c, cmap="roygbviz_div", vmin=-1, vmax=1)
ax.set_xticks(range(5), names, rotation=30)
ax.set_yticks(range(5), names)
for i in range(5):
    for j in range(5):
        ax.text(j, i, f"{c[i, j]:.2f}", ha="center", va="center", fontsize=9)
fig.colorbar(im, ax=ax, label="correlation", shrink=0.85)
ax.set(title="Correlation matrix")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Which variables move together.
- **Key calls:** `imshow(corr, cmap='roygbviz_div', vmin=-1, vmax=1)`
- **Watch out:** Centre on zero with a diverging map.

### Spectrogram

<p align="center">
<img src="../img/images/spectrogram_light.png#gh-light-mode-only" alt="A spectrogram: frequency against time, coloured by loudness. This is the standard picture of speech." width="640">
<img src="../img/images/spectrogram_dark.png#gh-dark-mode-only" alt="A spectrogram: frequency against time, coloured by loudness. This is the standard picture of speech." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/spectrogram_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fs = 8000
t = np.arange(0, 2.5, 1 / fs)
f0 = 140 + 40 * np.sin(2 * np.pi * 0.8 * t)                       # a wobbling pitch, like a voice
phase = 2 * np.pi * np.cumsum(f0) / fs
sig = sum(np.sin(h * phase) / h for h in range(1, 12)) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t) ** 2)
sig += 0.05 * np.random.default_rng(6).standard_normal(t.size)
fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
pxx, freqs, bins, im = ax.specgram(sig, NFFT=512, Fs=fs, noverlap=384, cmap="roygbviz", vmin=-100)
fig.colorbar(im, ax=ax, label="power (dB)", shrink=0.9)
ax.set(xlabel="time (s)", ylabel="frequency (Hz)", ylim=(0, 3000), title="Spectrogram of a synthetic voice")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Sound over time and frequency.
- **Key calls:** `ax.specgram(x, Fs=fs)`
- **Watch out:** Label time in seconds and frequency in Hz.

## Grids with real coordinates

### pcolormesh

<p align="center">
<img src="../img/images/pcolormesh_light.png#gh-light-mode-only" alt="pcolormesh() colours a grid whose cell edges you choose: the right tool for non-uniform spacing." width="640">
<img src="../img/images/pcolormesh_dark.png#gh-dark-mode-only" alt="pcolormesh() colours a grid whose cell edges you choose: the right tool for non-uniform spacing." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/pcolormesh_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.array([0, 1, 2, 4, 7, 11, 16.0])           # edges, spaced unevenly
y = np.array([0, 1, 3, 6, 10.0])
z = np.arange(6 * 4, dtype=float).reshape(4, 6) % 7
fig, axs = plt.subplots(1, 2, figsize=(7, 3.6), layout="constrained")
axs[0].pcolormesh(x, y, z, cmap="roygbviz", edgecolors=plt.rcParams["figure.facecolor"], linewidth=2)
axs[0].set_title("pcolormesh: true cell sizes", fontsize=10)
axs[1].imshow(z, cmap="roygbviz", origin="lower", aspect="auto")
axs[1].set_title("imshow: every cell the same size", fontsize=10)
for a in axs:
    a.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Cells with uneven sizes.
- **Key calls:** `ax.pcolormesh(X, Y, Z)`
- **Watch out:** Prefer to `imshow` when spacing is not even.

### Shading options

<p align="center">
<img src="../img/images/pcolormesh-shading_light.png#gh-light-mode-only" alt="The shading option: flat (one colour per cell), nearest (colour centred on the point) and gouraud (smoothly blended)." width="640">
<img src="../img/images/pcolormesh-shading_dark.png#gh-dark-mode-only" alt="The shading option: flat (one colour per cell), nearest (colour centred on the point) and gouraud (smoothly blended)." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/pcolormesh-shading_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(0, 4, 6), np.linspace(0, 3, 5))
z = np.sin(x) * np.cos(y)
fig, axs = plt.subplots(1, 3, figsize=(7.4, 3), layout="constrained")
axs[0].pcolormesh(x, y, z[:-1, :-1], shading="flat", cmap="roygbviz")
axs[1].pcolormesh(x, y, z, shading="nearest", cmap="roygbviz")
axs[2].pcolormesh(x, y, z, shading="gouraud", cmap="roygbviz")
for a, t in zip(axs, ("flat", "nearest", "gouraud")):
    a.set_title(f'shading="{t}"', fontsize=10)
    a.plot(x, y, "o", ms=2.5, color=plt.rcParams["text.color"], alpha=0.5)
    a.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Flat or smooth.
- **Key calls:** `shading='flat'`, `'nearest'`, `'gouraud'`
- **Watch out:** Use `flat` for exact cell values.

### Triangulated data

<p align="center">
<img src="../img/images/triangulation_light.png#gh-light-mode-only" alt="Scattered points (no grid): the triangles between them, a colour per triangle, smooth colour and contour lines." width="640">
<img src="../img/images/triangulation_dark.png#gh-dark-mode-only" alt="Scattered points (no grid): the triangles between them, a colour per triangle, smooth colour and contour lines." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/triangulation_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import matplotlib.tri as mtri

rng = np.random.default_rng(3)
x, y = rng.uniform(-1, 1, 70), rng.uniform(-1, 1, 70)
z = np.exp(-3 * ((x - 0.3) ** 2 + (y + 0.2) ** 2)) + 0.5 * np.exp(-4 * ((x + 0.5) ** 2 + (y - 0.4) ** 2))
tri = mtri.Triangulation(x, y)
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.9), layout="constrained")
axs[0].triplot(tri, color=rv.colour("grey"), lw=0.8)
axs[0].plot(x, y, "o", ms=3, color=rv.colour("red"))
axs[0].set_title("triplot", fontsize=10)
axs[1].tripcolor(tri, z, shading="gouraud", cmap="roygbviz")
axs[1].set_title("tripcolor", fontsize=10)
axs[2].tricontourf(tri, z, levels=10, cmap="roygbviz")
axs[2].tricontour(tri, z, levels=10, colors=plt.rcParams["figure.facecolor"], linewidths=0.6)
axs[2].set_title("tricontourf", fontsize=10)
for a in axs:
    a.set(aspect="equal"); a.grid(False); a.set_xticks([]); a.set_yticks([])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Scattered measurements.
- **Key calls:** `ax.tripcolor(x, y, z)`, `ax.tricontourf`
- **Watch out:** Mask long thin triangles at the edge.

### Hillshade

<p align="center">
<img src="../img/images/hillshade_light.png#gh-light-mode-only" alt="Hillshading: light a surface from one direction so its shape shows, here for pretend hills." width="640">
<img src="../img/images/hillshade_dark.png#gh-dark-mode-only" alt="Hillshading: light a surface from one direction so its shape shows, here for pretend hills." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/hillshade_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.colors import LightSource

rng = np.random.default_rng(8)
x, y = np.meshgrid(np.linspace(0, 10, 300), np.linspace(0, 10, 300))
z = sum(a * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s ** 2))
        for a, cx, cy, s in zip(rng.uniform(0.5, 1.5, 9), rng.uniform(1, 9, 9), rng.uniform(1, 9, 9), rng.uniform(0.6, 1.6, 9)))
ls = LightSource(azdeg=315, altdeg=40)
rgb = ls.shade(z, cmap=plt.get_cmap("roygbviz"), blend_mode="soft", vert_exag=4, dx=10 / 300, dy=10 / 300)
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
ax.imshow(rgb, origin="lower", extent=(0, 10, 0, 10))
ax.set(title="Hillshading")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Terrain and surfaces.
- **Key calls:** `LightSource().shade(z, cmap=)`
- **Watch out:** Exaggerate heights a little.

## Contours

### Contour lines

<p align="center">
<img src="../img/images/contour-lines_light.png#gh-light-mode-only" alt="Contour lines with labels: every line joins points of equal height." width="640">
<img src="../img/images/contour-lines_dark.png#gh-dark-mode-only" alt="Contour lines with labels: every line joins points of equal height." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/contour-lines_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-2, 2, 150))
z = np.exp(-(x - 1) ** 2 - y ** 2) - 0.7 * np.exp(-(x + 1) ** 2 - (y + 0.5) ** 2)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
cs = ax.contour(x, y, z, levels=12, cmap="roygbviz_spectrum", linewidths=1.6)
ax.clabel(cs, inline=True, fontsize=8, fmt="%.2f")
ax.set(xlabel="x", ylabel="y", title="Contour lines")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Surfaces of equal value.
- **Key calls:** `ax.contour(X, Y, Z, levels=)`; `ax.clabel`
- **Watch out:** Label some lines.

### Filled contours

<p align="center">
<img src="../img/images/contourf_light.png#gh-light-mode-only" alt="Filled contours: bands of colour between levels, with a colorbar that shows the bands." width="640">
<img src="../img/images/contourf_dark.png#gh-dark-mode-only" alt="Filled contours: bands of colour between levels, with a colorbar that shows the bands." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/contourf_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-2, 2, 150))
z = np.exp(-(x - 1) ** 2 - y ** 2) - 0.7 * np.exp(-(x + 1) ** 2 - (y + 0.5) ** 2)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
cs = ax.contourf(x, y, z, levels=np.linspace(-0.7, 1, 11), cmap="roygbviz")
ax.contour(x, y, z, levels=np.linspace(-0.7, 1, 11), colors=plt.rcParams["figure.facecolor"], linewidths=0.5)
fig.colorbar(cs, ax=ax, label="value", shrink=0.9)
ax.set(xlabel="x", ylabel="y", title="Filled contours")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Bands of value.
- **Key calls:** `ax.contourf(X, Y, Z, levels=)`
- **Watch out:** Choose levels at round numbers.

### Hatched contours

<p align="center">
<img src="../img/images/contourf-hatch_light.png#gh-light-mode-only" alt="Hatching instead of colour: regions stay distinguishable in black and white print." width="640">
<img src="../img/images/contourf-hatch_dark.png#gh-dark-mode-only" alt="Hatching instead of colour: regions stay distinguishable in black and white print." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/contourf-hatch_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
z = np.exp(-x ** 2 - y ** 2) - np.exp(-(x - 1) ** 2 - (y - 1) ** 2)
fig, ax = plt.subplots(figsize=(5.2, 4.2), layout="constrained")
cs = ax.contourf(x, y, z, levels=[-1, -0.2, 0.2, 1], hatches=["//", "", "xx"],
                 colors=[rv.shade("blue"), rv.shade(rv.colour("grey"), 2), rv.shade("red")], alpha=0.8)
ax.contour(x, y, z, levels=[-0.2, 0.2], colors=plt.rcParams["text.color"], linewidths=0.8)
ax.set(aspect="equal", title="Hatched contour regions")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Print without colour.
- **Key calls:** `ax.contourf(..., hatches=[...], colors='none')`
- **Watch out:** Combine with a legend.

### Log contours

<p align="center">
<img src="../img/images/contour-log_light.png#gh-light-mode-only" alt="Contours on a log colour scale: for values that span several orders of magnitude." width="640">
<img src="../img/images/contour-log_dark.png#gh-dark-mode-only" alt="Contours on a log colour scale: for values that span several orders of magnitude." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/contour-log_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.colors import LogNorm

x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
z = np.exp(-(x ** 2 + y ** 2) * 2) * 1e4 + 1
fig, ax = plt.subplots(figsize=(5.4, 4.2), layout="constrained")
cs = ax.contourf(x, y, z, levels=np.logspace(0, 4, 17), norm=LogNorm(), cmap="roygbviz")
fig.colorbar(cs, ax=ax, label="value (log scale)", shrink=0.85)
ax.set(aspect="equal", title="Contours with LogNorm")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Huge range of values.
- **Key calls:** `norm=LogNorm()`, `locator=LogLocator()`
- **Watch out:** Label in plain numbers.

## Vector fields

### Quiver

<p align="center">
<img src="../img/images/quiver_light.png#gh-light-mode-only" alt="A quiver plot: an arrow at each point, pointing in the direction of the vector and coloured by its length." width="640">
<img src="../img/images/quiver_dark.png#gh-dark-mode-only" alt="A quiver plot: an arrow at each point, pointing in the direction of the vector and coloured by its length." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/quiver_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-2, 2, 16), np.linspace(-2, 2, 16))
u, v = -y, x
speed = np.hypot(u, v)
fig, ax = plt.subplots(figsize=(5.4, 4.6), layout="constrained")
q = ax.quiver(x, y, u, v, speed, cmap="roygbviz", pivot="mid")
ax.quiverkey(q, 0.88, 1.03, 1, label="1 unit", labelpos="W", coordinates="axes", fontproperties=dict(size=8))
fig.colorbar(q, ax=ax, label="speed", shrink=0.8)
ax.set(aspect="equal", title="Quiver: a rotating field")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Direction and size at points.
- **Key calls:** `ax.quiver(X, Y, U, V, C)`
- **Watch out:** Thin out the grid.

### Wind barbs

<p align="center">
<img src="../img/images/barbs_light.png#gh-light-mode-only" alt="Wind barbs: the weather-map way to show speed and direction with flags and feathers." width="640">
<img src="../img/images/barbs_dark.png#gh-dark-mode-only" alt="Wind barbs: the weather-map way to show speed and direction with flags and feathers." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/barbs_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x, y = np.meshgrid(np.linspace(-3, 3, 7), np.linspace(-3, 3, 7))
u, v = 12 * x + 6 * y, -9 * x + 10 * y
fig, ax = plt.subplots(figsize=(5.2, 4.4), layout="constrained")
ax.barbs(x, y, u, v, np.hypot(u, v), cmap="roygbviz", length=6)
ax.set(aspect="equal", title="Barbs")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Weather charts.
- **Key calls:** `ax.barbs(X, Y, U, V)`
- **Watch out:** Needs a legend for the flags.

### Streamplot

<p align="center">
<img src="../img/images/streamplot_light.png#gh-light-mode-only" alt="streamplot() follows a vector field with flowing lines, here thicker where the flow is faster." width="640">
<img src="../img/images/streamplot_dark.png#gh-dark-mode-only" alt="streamplot() follows a vector field with flowing lines, here thicker where the flow is faster." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/images/streamplot_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

y, x = np.mgrid[-3:3:200j, -3:3:200j]
u, v = -1 - x ** 2 + y, 1 + x - y ** 2
speed = np.hypot(u, v)
fig, ax = plt.subplots(figsize=(5.6, 4.4), layout="constrained")
st = ax.streamplot(x, y, u, v, color=speed, linewidth=0.5 + 2.4 * speed / speed.max(), cmap="roygbviz", density=1.4)
fig.colorbar(st.lines, ax=ax, label="speed", shrink=0.85)
ax.set(aspect="equal", title="Streamplot")
ax.grid(False)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Flow.
- **Key calls:** `ax.streamplot(X, Y, U, V, linewidth=speed)`
- **Watch out:** Make line width show speed.

## Rules of thumb

- **Same colour scale** (`vmin`, `vmax`) whenever images are compared.
- **Diverging map** only when zero or another midpoint means something.
- **Label the colourbar** with the unit.
- **Avoid smoothing** unless you mean it.

**Back to the [home page](../index.md).**
