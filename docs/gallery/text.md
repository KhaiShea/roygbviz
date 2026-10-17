# Text, labels and annotations

Words make a chart readable. This page covers text, arrows, legends, titles and maths.

**Matplotlib reference:** `ax.text`, `ax.annotate`, `ax.legend`, `ax.set_title`, `ax.bar_label`. In plotnine: `geom_text`, `geom_label`, `annotate`, `labs`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Text itself**: Text properties, Alignment, Wrapping and line spacing, Rotation, Maths, Font sizes, Fonts per element, Axis labels
- **Annotating**: Annotate, Arrow styles, Text boxes, Data labels, Halos, Watermark
- **Titles and legends**: Title position, Legend placement, Custom legends

## Text itself

### Text properties

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


- **Use when:** Styling words.
- **Key calls:** `fontsize=`, `weight=`, `style=`, `family=`, `color=`, `bbox=`
- **Watch out:** Few styles in one figure.

### Alignment

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


- **Use when:** Placing text exactly.
- **Key calls:** `ha='left'|'center'|'right'`, `va='bottom'|'center'|'top'`
- **Watch out:** Alignment is relative to the point.

### Wrapping and line spacing

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


- **Use when:** Long notes.
- **Key calls:** `wrap=True`, `linespacing=1.4`
- **Watch out:** Wrap fits the figure width.

### Rotation

<p align="center">
<img src="../img/text/rotation_light.png#gh-light-mode-only" alt="Rotation: rotation_mode='anchor' rotates about the anchor point, so the label stays attached to its dot." width="640">
<img src="../img/text/rotation_dark.png#gh-dark-mode-only" alt="Rotation: rotation_mode='anchor' rotates about the anchor point, so the label stays attached to its dot." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/rotation_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axs = plt.subplots(1, 2, figsize=(7, 3), layout="constrained")
for ax, mode in zip(axs, ("default", "anchor")):
    ax.set(xlim=(0, 4.4), ylim=(0, 2), xticks=[], yticks=[]); ax.grid(False)
    for k, ang in enumerate((0, 30, 60, 90)):
        x = 0.4 + k * 1.1
        ax.plot(x, 0.6, "o", color=rv.colour("red"), ms=4)
        ax.text(x, 0.6, f"{ang} deg", rotation=ang, rotation_mode=mode, ha="left", va="bottom", fontsize=10)
    ax.set_title(f"rotation_mode='{mode}'", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Angled text.
- **Key calls:** `rotation=45, rotation_mode='anchor'`
- **Watch out:** Anchor mode keeps labels attached.

### Maths

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


- **Use when:** Formulae and symbols.
- **Key calls:** `r'$\sigma^2$'`
- **Watch out:** Use raw strings.

### Font sizes

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


- **Use when:** Scaling a figure.
- **Key calls:** `rv.use('light', base_size=14)`
- **Watch out:** Size for the final page.

### Fonts per element

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


- **Use when:** Serif titles over sans labels.
- **Key calls:** `fontfamily='serif'`
- **Watch out:** Two families at most.

### Axis labels

<p align="center">
<img src="../img/text/units-label_light.png#gh-light-mode-only" alt="Axis labels with units: say what, then the unit in brackets, and keep the same wording across figures." width="640">
<img src="../img/text/units-label_dark.png#gh-dark-mode-only" alt="Axis labels with units: say what, then the unit in brackets, and keep the same wording across figures." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/units-label_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(5.8, 3.4), layout="constrained")
t = np.linspace(0, 10, 50)
ax.plot(t, 100 + 30 * np.sin(t), color=rv.colour("red"))
ax.set(xlabel="Audio length (s)", ylabel="Response time (ms)", title="Label what and in which unit")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Saying what and in which unit.
- **Key calls:** `ax.set(xlabel='Time (s)')`
- **Watch out:** Same wording across figures.

## Annotating

### Annotate

<p align="center">
<img src="../img/text/annotate-basic_light.png#gh-light-mode-only" alt="annotate: text in one place, an arrow pointing at another. xy is the target, xytext is where the words go." width="640">
<img src="../img/text/annotate-basic_dark.png#gh-dark-mode-only" alt="annotate: text in one place, an arrow pointing at another. xy is the target, xytext is where the words go." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/annotate-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 200)
y = np.sin(x)
fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
ax.plot(x, y, color=rv.colour("blue"))
ax.annotate("peak", xy=(np.pi / 2, 1), xytext=(3.4, 1.15), arrowprops=dict(arrowstyle="->", color=rv.colour("red")), color=rv.colour("red"), weight="bold")
ax.annotate("trough", xy=(3 * np.pi / 2, -1), xytext=(6.2, -1.2), arrowprops=dict(arrowstyle="->", color=rv.colour("red")), color=rv.colour("red"), weight="bold")
ax.set_ylim(-1.5, 1.5)
ax.set_title("annotate()")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Point at something.
- **Key calls:** `ax.annotate('peak', xy=, xytext=, arrowprops=)`
- **Watch out:** Put the text where it does not cover data.

### Arrow styles

<p align="center">
<img src="../img/text/arrow-styles_light.png#gh-light-mode-only" alt="Arrow styles and connection styles: straight, curved, wedge and fancy arrows." width="640">
<img src="../img/text/arrow-styles_dark.png#gh-dark-mode-only" alt="Arrow styles and connection styles: straight, curved, wedge and fancy arrows." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/arrow-styles_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
ax.set(xlim=(0, 4), ylim=(0, 3), xticks=[], yticks=[]); ax.grid(False)
specs = [("->", "arc3,rad=0"), ("-|>", "arc3,rad=0.3"), ("<->", "arc3,rad=-0.3"), ("fancy", "arc3,rad=0.2"),
         ("simple", "angle3,angleA=90,angleB=0"), ("wedge", "arc3,rad=0")]
for k, (st, cs) in enumerate(specs):
    x0, y0 = 0.4 + (k % 3) * 1.3, 2.4 - (k // 3) * 1.4
    ax.annotate("", xy=(x0 + 1, y0 - 0.5), xytext=(x0, y0), arrowprops=dict(arrowstyle=st, connectionstyle=cs, color=rv.colour("blue"), lw=1.6, mutation_scale=18))
    ax.text(x0 + 0.5, y0 - 0.8, f"{st}\n{cs}", ha="center", va="top", fontsize=7)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Choosing arrows.
- **Key calls:** `arrowstyle='->'`, `connectionstyle='arc3,rad=0.3'`
- **Watch out:** Simple arrows are usually enough.

### Text boxes

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


- **Use when:** Readable labels on lines.
- **Key calls:** `bbox=dict(boxstyle='round', fc=...)`
- **Watch out:** Match the background.

### Data labels

<p align="center">
<img src="../img/text/data-labels_light.png#gh-light-mode-only" alt="Labelling bars and points directly: bar_label for values, text for the one point that matters." width="640">
<img src="../img/text/data-labels_dark.png#gh-dark-mode-only" alt="Labelling bars and points directly: bar_label for values, text for the one point that matters." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/data-labels_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["Whisper", "Parakeet", "Conformer", "wav2vec"]
vals = [3.1, 3.6, 4.4, 5.9]
fig, ax = plt.subplots(figsize=(6, 3.4), layout="constrained")
bars = ax.bar(names, vals, color=[rv.colour("teal")] * 3 + [rv.colour("grey")])
ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=10)
ax.set_ylim(0, 7); ax.set_title("Word error rate (lower is better)")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Exact values.
- **Key calls:** `ax.bar_label(bars, fmt='%.1f')`
- **Watch out:** Label what matters.

### Halos

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


- **Use when:** Text on busy data.
- **Key calls:** `path_effects=[withStroke(linewidth=3, foreground=bg)]`
- **Watch out:** Use the background colour.

### Watermark

<p align="center">
<img src="../img/text/watermark_light.png#gh-light-mode-only" alt="A DRAFT watermark: large, rotated, transparent text behind the data." width="640">
<img src="../img/text/watermark_dark.png#gh-dark-mode-only" alt="A DRAFT watermark: large, rotated, transparent text behind the data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/watermark_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, ax = plt.subplots(figsize=(6, 3.4), layout="constrained")
ax.plot(np.linspace(0, 10, 50), np.random.default_rng(1).normal(size=50).cumsum(), color=rv.colour("blue"))
ax.text(0.5, 0.5, "DRAFT", transform=ax.transAxes, fontsize=64, weight="bold", color=rv.colour("grey"), alpha=0.18, ha="center", va="center", rotation=25, zorder=0)
ax.set_title("Watermark")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** DRAFT stamps.
- **Key calls:** Large text with `alpha=0.18`
- **Watch out:** Put it behind data (`zorder=0`).

## Titles and legends

### Title position

<p align="center">
<img src="../img/text/title-position_light.png#gh-light-mode-only" alt="Title positions: loc='left', 'center' or 'right'. Left is the Roygbviz default because it is where reading starts." width="640">
<img src="../img/text/title-position_dark.png#gh-dark-mode-only" alt="Title positions: loc='left', 'center' or 'right'. Left is the Roygbviz default because it is where reading starts." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/title-position_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig, axs = plt.subplots(1, 3, figsize=(8, 2.8), layout="constrained")
for ax, loc in zip(axs, ("left", "center", "right")):
    ax.plot([0, 1], [0, 1], color=rv.colour("blue"))
    ax.set_title(f"loc='{loc}'", loc=loc, fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Left, centre, right.
- **Key calls:** `ax.set_title(..., loc='left')`
- **Watch out:** Left-aligned titles match reading.

### Legend placement

<p align="center">
<img src="../img/text/legend-placement_light.png#gh-light-mode-only" alt="Legend placement: loc names, an outside legend with bbox_to_anchor, and columns." width="640">
<img src="../img/text/legend-placement_dark.png#gh-dark-mode-only" alt="Legend placement: loc names, an outside legend with bbox_to_anchor, and columns." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/legend-placement_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 50)
fig, axs = plt.subplots(1, 3, figsize=(8, 3), layout="constrained")
for ax in axs:
    for k, c in enumerate(("red", "teal", "violet")):
        ax.plot(x, np.sin(x + k), color=rv.colour(c), label=f"series {k + 1}")
axs[0].legend(loc="lower left"); axs[0].set_title("loc='lower left'", fontsize=9)
axs[1].legend(loc="upper center", ncols=3, bbox_to_anchor=(0.5, -0.12)); axs[1].set_title("below, ncols=3", fontsize=9)
axs[2].legend(loc="center left", bbox_to_anchor=(1.0, 0.5)); axs[2].set_title("outside right", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Keeping the legend off the data.
- **Key calls:** `ax.legend(loc=, bbox_to_anchor=, ncols=)`
- **Watch out:** Prefer direct labels for a few series.

### Custom legends

<p align="center">
<img src="../img/text/legend-handles_light.png#gh-light-mode-only" alt="Custom legends: build the handles yourself when the plot has no single artist to point at." width="640">
<img src="../img/text/legend-handles_dark.png#gh-dark-mode-only" alt="Custom legends: build the handles yourself when the plot has no single artist to point at." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/text/legend-handles_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib.lines import Line2D
from matplotlib.patches import Patch

fig, ax = plt.subplots(figsize=(6, 3.2), layout="constrained")
ax.axis("off")
handles = [Patch(color=rv.colour("red"), label="STT"), Line2D([0], [0], color=rv.colour("teal"), lw=2, label="a line"),
           Line2D([0], [0], marker="o", ls="", color=rv.colour("violet"), label="a marker")]
ax.legend(handles=handles, loc="center", fontsize=12, title="Custom handles")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Several kinds of mark.
- **Key calls:** `Patch`, `Line2D` handles
- **Watch out:** Match colour and shape exactly.

## Rules of thumb

- **Title the finding**, not the topic.
- **Direct labels** beat legends.
- **Ink-coloured text**, not pale colours.
- **Same terms** in text and labels.

**Back to the [home page](../index.md).**
