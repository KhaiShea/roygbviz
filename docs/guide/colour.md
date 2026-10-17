# Colour guide

Colour is the easiest thing to get wrong and the hardest to notice. This page explains what colour is for, which kind of colour scale to use, and how Roygbviz's colours are built.

## Colour has three jobs

| Job | Question it answers | Scale type | Example |
|---|---|---|---|
| **Identity** | Which group is this? | **Categorical**: distinct hues | Model A is red, model B is teal |
| **Magnitude** | How much? | **Sequential**: one hue, light to dark | Density, count |
| **Polarity** | Above or below a midpoint? | **Diverging**: two hues with a neutral middle | Change from baseline |

**Match the job to the scale.** A rainbow ramp for magnitude misleads because the eye sees bands that are not in the data.

## The palette

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


Nine series colours in rainbow order, plus three stage colours (STT, LLM, TTS) and a neutral grey. Get any by name:

```python
rv.colour("teal")      # one hex colour
rv.group_map()         # the three stage colours
rv.colour_map(labels)  # pin colours to labels, up to nine
rv.levels("red", 5)    # five lightness steps of one colour
rv.shade("red")        # one step lighter, for fills
```

## Colormaps

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


- `roygbviz` is a **sequential** map (light to deep blue-teal).
- `roygbviz_spectrum` is a multi-hue sequential map.
- `roygbviz_div` is **diverging**: cold (deep blue) through a pale middle to hot (red).

Use them by name: `ax.imshow(a, cmap="roygbviz")`, or `scale_fill_roygbviz_c()`, `scale_fill_roygbviz_div(midpoint=0)` in plotnine.

## Why lightness matters

A good sequential map gets steadily lighter or darker, so greyscale printing still works. A bad one (like `jet`) rises and falls, creating false edges.

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


## Colour vision deficiency

About 1 in 12 men and 1 in 200 women have some colour vision difference. Never rely on colour alone:

- **Add a second cue**: direct labels, line styles, marker shapes or hatching.
- **Check with a simulator**; the picture below applies standard simulations to the nine colours.

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


Where hues become hard to separate (for example red and green in the red-green deficiencies), the pairs usually still differ in lightness. A dedicated colour-blind-safe set is a known gap in Roygbviz, so for now add labels or hatching for important figures.

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


## Fills and lines

Use the **default colour for lines and outlines**, and a **lighter shade for fills**. They read as the same colour, with the line staying crisp.

```python
ax.fill_between(x, lo, hi, color=rv.shade("blue"))
ax.plot(x, y, color=rv.colour("blue"))
```

## Text colour

Text uses the **ink** colour, never a pale series colour. Pale yellow text on a white or cream background is unreadable. Use a coloured mark beside the text instead.

## Light, dark and cream

There are three modes. `rv.use("light")` is **white paper** and is the default. `rv.use("cream")` is the original warm paper. `rv.use("dark")` is navy paper with its own colour versions tuned for dark backgrounds.

Light and cream share exactly the same colours, and only the paper and the neutral greys change. Dark is a separate set, so do not just invert a light figure: contrast and lightness change.

## Choosing quickly

1. **Groups?** Use `rv.colour_map(...)` and keep it for the whole project.
2. **A number?** Use a sequential map in one hue.
3. **Above or below zero?** Use the diverging map with the midpoint at zero.
4. **More than nine groups?** Facet instead.
5. **Highlight one?** Grey for the rest, one colour for the star.

## Sources

- Crameri, F., Shephard, G. E., and Heron, P. J. (2020). The misuse of colour in science communication. *Nature Communications*, 11, 5444.
- Wong, B. (2011). Points of view: Color blindness. *Nature Methods*, 8, 441.
- Machado, G. M., Oliveira, M. M., and Fernandes, L. A. F. (2009). A physiologically-based model for simulation of color vision deficiency. *IEEE TVCG*, 15(6), 1291 to 1298.

**Next:** [Saving and exporting](saving.md).
