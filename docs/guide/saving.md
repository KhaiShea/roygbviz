# Saving and exporting

Choose the format by where the figure is going, and size it for the final page.

## Format cheat sheet

| Destination | Format | Why |
|---|---|---|
| **Journal or thesis** | **PDF** (vector) | Crisp at any zoom, small for line art |
| **Word or Google Docs** | **PNG** at 300 dpi, or SVG | Widely supported |
| **Slides** | **PNG** at 200 dpi or SVG | Fine for screens |
| **Web page** | **SVG** or **PNG** | SVG stays sharp; PNG is simplest |
| **Photos, images, heatmaps with millions of cells** | **PNG** | Vector files can become huge |
| **Animation** | **GIF** or MP4 | GIF works everywhere |

**Vector vs. raster.** Vector files (PDF, SVG, EPS) store shapes and stay sharp when zoomed. Raster files (PNG, JPEG) store pixels and blur when enlarged. Never use JPEG for charts: it smudges lines and text.

## Saving in matplotlib

```python
fig.savefig("figure.pdf")                      # vector
fig.savefig("figure.png", dpi=300)             # raster
fig.savefig("figure.svg")
fig.savefig("figure.png", dpi=300, bbox_inches="tight", transparent=False)
```

- `dpi` only matters for raster files.
- `bbox_inches="tight"` trims empty margins. With `layout="constrained"` you rarely need it.
- Set text to be real text in PDFs: `plt.rcParams["pdf.fonttype"] = 42`.

## Saving in plotnine

```python
p.save("figure.pdf", width=6, height=4)               # inches
p.save("figure.png", width=6, height=4, dpi=300)
```

If you leave `width` and `height` out, plotnine uses the size set in `theme(figure_size=(w, h))`.

## Sizing for a paper

1. Find the **column width** in the journal guide (for example 8.5 cm one-column, 17 cm two-column).
2. Convert to inches: divide centimetres by 2.54.
3. Make the figure **that exact width**, so text is the size you chose.

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


Text should be about **8 to 10 pt** after placement. If a journal wants 300 or 600 dpi, set it on save.

## Light, dark and cream versions

To produce all three, render once per mode:

```python
for mode in ("light", "dark", "cream"):
    rv.use(mode)
    fig = make_figure()                       # your function that builds the figure
    fig.savefig(f"figure_{mode}.png", dpi=300)
```

For web pages, a `<picture>` element picks the right one automatically. This documentation does exactly that.

## Transparent backgrounds

```python
fig.savefig("figure.png", dpi=300, transparent=True)
```

Roygbviz figures have a white, navy or cream background by design. Transparent PNGs work well on slides with a matching background but look poor on a different colour.

## Animations

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


```python
anim.save("figure.gif", writer="pillow", fps=20)
anim.save("figure.mp4", writer="ffmpeg", fps=30)   # needs ffmpeg installed
```

Keep GIFs short (a few seconds), small (under about 5 MB), and finish on a frame that tells the whole story.

## Checklist before you submit

- [ ] Right format for the destination
- [ ] Size matches the column width
- [ ] Text readable at final size
- [ ] Fonts embedded
- [ ] Colours distinguishable in greyscale
- [ ] Axis labels have units
- [ ] Caption explains everything needed to read the figure alone

**Next:** [Troubleshooting](troubleshooting.md).
