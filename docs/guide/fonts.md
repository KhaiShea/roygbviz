# Fonts and text

Fonts are the most common thing people want to change. This page explains how Roygbviz chooses fonts, how to install and override them, and how to handle special text.

## How Roygbviz picks fonts

Roygbviz tries a list of fonts in order and uses the first one installed.

- **Body text** (labels, ticks, legends): Inter, Helvetica Neue, Helvetica, Arial, Liberation Sans, DejaVu Sans.
- **Titles in plotnine** (title and facet labels): Source Serif 4, Georgia, Iowan Old Style, Palatino, TeX Gyre Pagella, Caladea, Liberation Serif, DejaVu Serif.

So a computer with nothing special installed still gets a clean figure (DejaVu Sans is bundled with matplotlib). Installing Inter and Source Serif 4 gives the intended look.

## Install the intended fonts

1. Download **Inter** (rsms.me/inter) and **Source Serif 4** (fonts.google.com) as `.ttf` or `.otf` files.
2. Install them:
   - **Linux:** copy to `~/.local/share/fonts/`, then run `fc-cache -f`.
   - **macOS:** open the file and click Install Font.
   - **Windows:** right-click, Install for all users.
3. **Clear matplotlib's font cache** and restart Python:

```python
import matplotlib, shutil
shutil.rmtree(matplotlib.get_cachedir(), ignore_errors=True)
```

Matplotlib reads `.ttf`, `.otf` and `.ttc` only. It cannot use old Type 1 fonts. Variable fonts (one file holding many weights) can fall back to a single weight, so prefer static files when bold looks wrong.

## Changing fonts

**For the whole session**, in matplotlib:

```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Georgia"        # after rv.use()
```

**In plotnine**, pass fonts to the theme:

```python
from plotnine import *
import roygbviz as rv
p + rv.theme_roygbviz(base_family="Helvetica", title_family="Georgia")
```

**For one piece of text**:

```python
ax.set_title("Results", fontfamily="serif", fontsize=15)
ax.text(0.5, 0.5, "note", fontfamily="monospace")
```

<p align="center">
<img src="../img/text/ticklabel-fonts_light.png#gh-light-mode-only" alt="Serif titles, sans labels: set the font per element rather than globally." width="640">
<img src="../img/text/ticklabel-fonts_dark.png#gh-dark-mode-only" alt="Serif titles, sans labels: set the font per element rather than globally." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/ticklabel-fonts_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.2, 3.4), layout="constrained")
ax.bar(["A", "B", "C"], [3, 5, 4], color=rv.colour("violet"))
ax.set_title("A serif title over sans labels", fontfamily="serif", fontsize=15)
ax.set_xlabel("category", fontfamily="sans-serif")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


**Add a font file without installing it**:

```python
from matplotlib import font_manager
font_manager.fontManager.addfont("/path/to/MyFont.ttf")
plt.rcParams["font.family"] = "My Font Name"   # the family name inside the file
```

To list what matplotlib can see: `sorted({f.name for f in font_manager.fontManager.ttflist})`.

## Sizes

Everything scales from one number, `base_size` (default 11 points):

```python
rv.use("light", base_size=14)
```

<p align="center">
<img src="../img/text/font-sizes_light.png#gh-light-mode-only" alt="Font sizes in one figure: title, labels, ticks and legend scale from base_size in rv.use()." width="640">
<img src="../img/text/font-sizes_dark.png#gh-dark-mode-only" alt="Font sizes in one figure: title, labels, ticks and legend scale from base_size in rv.use()." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/font-sizes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axs = plt.subplots(1, 3, figsize=(8, 2.8), layout="constrained")
t = np.linspace(0, 6, 50)
for ax, bs in zip(axs, (9, 11, 14)):
    with plt.rc_context({"font.size": bs, "axes.titlesize": bs * 1.3, "axes.labelsize": bs * 0.9, "xtick.labelsize": bs * 0.8, "ytick.labelsize": bs * 0.8}):
        ax.plot(t, np.sin(t), color=rv.colour("teal"), label="sin")
        ax.set(title=f"base_size={bs}", xlabel="x", ylabel="y")
        ax.legend()

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


Rules of thumb: **8 to 10 pt** for a two-column paper figure, **11 to 12 pt** for a one-column figure, **14 to 18 pt** for slides, **20 pt and up** for posters. If your figure is shrunk when placed in a document, size the text for the final size, not the original.

## Text properties

<p align="center">
<img src="../img/text/properties_light.png#gh-light-mode-only" alt="Text properties: size, weight, style, family, colour and background on the same string." width="640">
<img src="../img/text/properties_dark.png#gh-dark-mode-only" alt="Text properties: size, weight, style, family, colour and background on the same string." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/properties_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.axis("off")
props = [dict(fontsize=10), dict(fontsize=16, weight="bold"), dict(fontsize=14, style="italic"),
         dict(fontsize=14, family="serif"), dict(fontsize=14, family="monospace"),
         dict(fontsize=14, color=rv.colour("red")), dict(fontsize=14, bbox=dict(boxstyle="round", fc=rv.shade("yellow"), ec="none"))]
for k, kw in enumerate(props):
    ax.text(0.02, 0.92 - k * 0.14, "Kia ora, whole text " + ", ".join(f"{a}={b}" if a != "bbox" else "bbox" for a, b in kw.items() if a != "color") , transform=ax.transAxes, **kw)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


The properties you will use most: `fontsize`, `fontweight` (or `weight`), `fontstyle`, `fontfamily`, `color`, `alpha`, `rotation`, `ha` and `va` (alignment), `bbox` (background box), `linespacing`.

## Alignment

<p align="center">
<img src="../img/text/alignment_light.png#gh-light-mode-only" alt="Alignment: ha and va say which part of the text sits at the point you give." width="640">
<img src="../img/text/alignment_dark.png#gh-dark-mode-only" alt="Alignment: ha and va say which part of the text sits at the point you give." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/alignment_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
ax.set(xlim=(0, 3), ylim=(0, 3), xticks=[], yticks=[])
ax.grid(False)
for i, ha in enumerate(("left", "center", "right")):
    for j, va in enumerate(("bottom", "center", "top")):
        x, y = 0.5 + i, 0.5 + j
        ax.plot(x, y, "o", color=rv.colour("red"), ms=5)
        ax.text(x, y, f"{ha}\n{va}", ha=ha, va=va, fontsize=9)
ax.set_title("Dot = the point; text hangs off it by ha and va")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


**Remember:** `ha` and `va` say which part of the text sits on the point you gave. `ha="left"` means the left edge of the text sits at x.

## Wrapping and multi-line text

<p align="center">
<img src="../img/text/multiline-wrap_light.png#gh-light-mode-only" alt="Multi-line text: wrap=True fits text to the figure width, and linespacing opens up explicit newlines." width="640">
<img src="../img/text/multiline-wrap_dark.png#gh-dark-mode-only" alt="Multi-line text: wrap=True fits text to the figure width, and linespacing opens up explicit newlines." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/multiline-wrap_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.4, 3.2), layout="constrained")
ax.axis("off")
msg = "Cascaded pipelines chain speech to text, a language model and text to speech, so errors compound at each stage."
ax.text(0.0, 0.98, "wrap=True", weight="bold", transform=ax.transAxes, va="top")
ax.text(0.0, 0.88, msg, wrap=True, transform=ax.transAxes, va="top", fontsize=10)
ax.text(0.0, 0.55, "linespacing=1.8", weight="bold", transform=ax.transAxes, va="top")
ax.text(0.0, 0.45, "line one\nline two\nline three", linespacing=1.8, transform=ax.transAxes, va="top", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## Maths, Greek letters and units

Wrap maths in dollar signs and use LaTeX commands. No LaTeX install is needed.

```python
ax.set_xlabel(r"$\sigma$ (dB)")          # use a raw string (r"...")
ax.set_title(r"$\mathrm{WER} = (S + D + I) / N$")
```

<p align="center">
<img src="../img/text/mathtext_light.png#gh-light-mode-only" alt="mathtext: LaTeX-style maths in any label, with no LaTeX install. Wrap the maths in dollar signs." width="640">
<img src="../img/text/mathtext_dark.png#gh-dark-mode-only" alt="mathtext: LaTeX-style maths in any label, with no LaTeX install. Wrap the maths in dollar signs." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/mathtext_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6.6, 3.6), layout="constrained")
ax.axis("off")
eqs = [r"$\mathrm{WER} = \frac{S + D + I}{N}$", r"$\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \mu)^2}$",
       r"$\alpha_i > \beta_i,\ \ \Delta E = 3.2\times 10^{-4}$", r"$\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}$"]
for k, e in enumerate(eqs):
    ax.text(0.04, 0.85 - k * 0.24, e, fontsize=16, transform=ax.transAxes)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


For real LaTeX rendering (slower, needs LaTeX installed), set `plt.rcParams["text.usetex"] = True`. For maths in a font close to the body font, try `plt.rcParams["mathtext.fontset"] = "stix"`.

## Special characters and macrons

Aotearoa and te reo Māori need macrons (ā, ē, ī, ō, ū). Matplotlib handles them if the font has them (Inter and DejaVu Sans do). If you see boxes, the font is missing the glyph: choose another font.

```python
ax.set_title("Pūrorohiko: Te Kura Mātai")
```

## Fonts in PDFs and papers

Journals often reject documents with Type 3 fonts. Matplotlib can embed real TrueType fonts instead:

```python
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
```

## Making text readable

- Put text in the **ink** colour, not a pale series colour.
- Use a **halo** when text sits on busy data:

<p align="center">
<img src="../img/text/path-effects_light.png#gh-light-mode-only" alt="Path effects: a halo (stroke) around text keeps it readable over busy data." width="640">
<img src="../img/text/path-effects_dark.png#gh-dark-mode-only" alt="Path effects: a halo (stroke) around text keeps it readable over busy data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/path-effects_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import matplotlib.patheffects as pe

rng = np.random.default_rng(2)
fig, ax = plt.subplots(figsize=(6, 3.4), layout="constrained")
ax.imshow(rng.random((20, 30)), cmap="roygbviz", aspect="auto"); ax.grid(False)
ax.text(0.3, 0.5, "plain", transform=ax.transAxes, fontsize=18, weight="bold", color=plt.rcParams["text.color"])
ax.text(0.62, 0.5, "halo", transform=ax.transAxes, fontsize=18, weight="bold", color=plt.rcParams["text.color"],
        path_effects=[pe.withStroke(linewidth=3.5, foreground=plt.rcParams["axes.facecolor"])])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- Use a **background box** for labels on top of lines:

<p align="center">
<img src="../img/text/text-boxes_light.png#gh-light-mode-only" alt="Text boxes: bbox gives a label a background, which keeps it legible over lines and grids." width="640">
<img src="../img/text/text-boxes_dark.png#gh-dark-mode-only" alt="Text boxes: bbox gives a label a background, which keeps it legible over lines and grids." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/text-boxes_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.plot(x, np.sin(x), color=rv.colour("blue")); ax.plot(x, np.cos(x), color=rv.colour("red"))
ax.text(5, 0, "no box", ha="center")
ax.text(2, 0.55, "round box", ha="center", bbox=dict(boxstyle="round,pad=0.4", fc=rv.shade("yellow"), ec=rv.colour("yellow")))
ax.text(8, -0.6, "square box", ha="center", bbox=dict(boxstyle="square,pad=0.4", fc=plt.rcParams["axes.facecolor"], ec=rv.colour("grey")))

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## Checklist

- [ ] Font installed and cache cleared
- [ ] Size chosen for the final printed size
- [ ] Macrons and symbols render
- [ ] PDF fonts embedded (`pdf.fonttype = 42`)

**Next:** [Grammar of graphics](grammar.md).
