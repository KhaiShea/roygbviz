# Grammar of graphics

The **grammar of graphics** is a way of describing any chart as a small set of parts that snap together, like a sentence is built from words. If you learn the parts, you can build charts nobody has named, instead of hunting for a template.

It was set out by Leland Wilkinson (*The Grammar of Graphics*, 2005) and turned into a practical tool for R by Hadley Wickham (*A Layered Grammar of Graphics*, 2010). **plotnine** is the Python version of that tool, and matplotlib follows the same ideas in a more hands-on way.

## Key terms

- **Data**: a table. One row per observation, one column per variable.
- **Aesthetic (aes)**: a link from a column to a visual property, such as x, y, colour, size or shape.
- **Geom**: the shape drawn (point, line, bar, area, text).
- **Stat**: a calculation done before drawing (counting, averaging, smoothing).
- **Scale**: the rule turning data values into positions and colours (linear, log, a fixed colour per level).
- **Coord**: how positions are placed on the page (Cartesian, flipped, polar).
- **Facet**: splitting one chart into small panels by a column.
- **Theme**: everything that is not data (fonts, background, grid).
- **Position**: what to do when marks overlap (stack, dodge, jitter).

## The sentence

> Take **data**, map **columns** to **aesthetics**, draw them as **geoms** (after any **stat**), place them with **scales** and a **coord**, split with **facets**, and style with a **theme**.

In plotnine it reads almost the same:

```python
from plotnine import *
(ggplot(df, aes("snr", "wer", colour="model"))   # data + aesthetics
 + geom_point()                                  # geom
 + scale_y_log10()                               # scale
 + facet_wrap("model")                           # facet
 + theme_roygbviz())                             # theme
```

## Building a chart, one part at a time

All eight figures below use the same data: word error rate (WER) for three speech recognisers at five noise levels. Each step adds one idea. Click **Show the code** to see the whole script.

### Step 1. Data, aesthetics and a geom

Two columns map to position. Each row becomes a point.

<p align="center">
<img src="../img/gg/g1-points_light.png#gh-light-mode-only" alt="Step 1: data plus aesthetics plus one geom. snr goes to x, wer goes to y, and each row becomes a point." width="640">
<img src="../img/gg/g1-points_dark.png#gh-dark-mode-only" alt="Step 1: data plus aesthetics plus one geom. snr goes to x, wer goes to y, and each row becomes a point." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g1-points_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = ggplot(df, aes("snr", "wer")) + geom_point()

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 2. A third variable as colour

Mapping `colour="model"` splits the points by model and adds a legend automatically.

<p align="center">
<img src="../img/gg/g2-colour_light.png#gh-light-mode-only" alt="Step 2: map a third column, model, to colour. A legend appears because colour is now mapped to data." width="640">
<img src="../img/gg/g2-colour_dark.png#gh-dark-mode-only" alt="Step 2: map a third column, model, to colour. A legend appears because colour is now mapped to data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g2-colour_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = ggplot(df, aes("snr", "wer", colour="model")) + geom_point() + rv.scale_colour_roygbviz_d()

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 3. Layers

Layers stack. Points show the raw data and a line shows the trend.

<p align="center">
<img src="../img/gg/g3-layers_light.png#gh-light-mode-only" alt="Step 3: layers stack. Points show every measurement; a line through the mean of each group shows the trend." width="640">
<img src="../img/gg/g3-layers_dark.png#gh-dark-mode-only" alt="Step 3: layers stack. Points show every measurement; a line through the mean of each group shows the trend." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g3-layers_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = (ggplot(df, aes("snr", "wer", colour="model"))
     + geom_point(alpha=0.5)
     + stat_summary(fun_y=np.mean, geom="line", size=1.2)
     + rv.scale_colour_roygbviz_d())

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 4. Stats

A **stat** computes something before drawing. Here `stat_summary` finds the mean and a band for the spread. You did not make a table of means; the grammar did.

<p align="center">
<img src="../img/gg/g4-stat_light.png#gh-light-mode-only" alt="Step 4: a stat transforms data before drawing. stat_summary computes mean and spread; you never built that table." width="640">
<img src="../img/gg/g4-stat_dark.png#gh-dark-mode-only" alt="Step 4: a stat transforms data before drawing. stat_summary computes mean and spread; you never built that table." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g4-stat_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = (ggplot(df, aes("snr", "wer", colour="model", fill="model"))
     + stat_summary(fun_data="mean_sdl", fun_args={"mult": 1}, geom="ribbon", alpha=0.2, colour="none")
     + stat_summary(fun_y=np.mean, geom="line", size=1.2)
     + rv.scale_colour_roygbviz_d() + rv.scale_fill_roygbviz_d())

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 5. Scales

Scales decide how data become positions and colours. A log y scale spreads out the low values, and a pinned colour map keeps each model the same colour in every figure.

<p align="center">
<img src="../img/gg/g5-scales_light.png#gh-light-mode-only" alt="Step 5: scales control how data becomes position and colour. Pin each model's colour and put the y axis on a log scale." width="640">
<img src="../img/gg/g5-scales_dark.png#gh-dark-mode-only" alt="Step 5: scales control how data becomes position and colour. Pin each model's colour and put the y axis on a log scale." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g5-scales_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = (ggplot(df, aes("snr", "wer", colour="model"))
     + stat_summary(fun_y=np.mean, geom="line", size=1.2)
     + scale_colour_manual(values=rv.colour_map(models))
     + scale_y_log10(name="Word error rate (%)")
     + scale_x_continuous(name="Signal to noise (dB)", breaks=[0, 5, 10, 15, 20]))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 6. Facets

Facets make small multiples: the same chart repeated for each level of a column, sharing axes so panels can be compared.

<p align="center">
<img src="../img/gg/g6-facets_light.png#gh-light-mode-only" alt="Step 6: facets split the data into small multiples that share axes, one panel per model." width="640">
<img src="../img/gg/g6-facets_dark.png#gh-dark-mode-only" alt="Step 6: facets split the data into small multiples that share axes, one panel per model." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g6-facets_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = (ggplot(df, aes("snr", "wer", colour="model"))
     + geom_point(alpha=0.6)
     + facet_wrap("model")
     + scale_colour_manual(values=rv.colour_map(models), guide=None)
     + theme(figure_size=(8, 3.2)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 7. Coordinates

`coord_flip()` swaps x and y. It does not change the data, only where marks land. Long labels read far better on the vertical axis.

<p align="center">
<img src="../img/gg/g7-coords_light.png#gh-light-mode-only" alt="Step 7: coordinates decide how positions are laid on the page. coord_flip swaps x and y without touching the data." width="640">
<img src="../img/gg/g7-coords_dark.png#gh-dark-mode-only" alt="Step 7: coordinates decide how positions are laid on the page. coord_flip swaps x and y without touching the data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g7-coords_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"model": ["Whisper large-v3", "Parakeet TDT", "Conformer CTC", "wav2vec 2.0"], "wer": [3.1, 3.6, 4.4, 5.9]})
df["model"] = pd.Categorical(df["model"], df["model"][::-1])

p = (ggplot(df, aes("model", "wer")) + geom_col(fill=rv.colour("teal"), width=0.6) + coord_flip()
     + labs(x="", y="Word error rate (%)") + theme(figure_size=(6, 3), panel_grid_major_x=element_line(), panel_grid_major_y=element_blank()))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


### Step 8. Theme and labels

Titles, labels, legend position and size. `theme_roygbviz` is already on after `rv.use()`, so you only adjust what you need.

<p align="center">
<img src="../img/gg/g8-theme_light.png#gh-light-mode-only" alt="Step 8: the theme styles everything that is not data. theme_roygbviz is already on after rv.use(); tweak it with theme()." width="640">
<img src="../img/gg/g8-theme_dark.png#gh-dark-mode-only" alt="Step 8: the theme styles everything that is not data. theme_roygbviz is already on after rv.use(); tweak it with theme()." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/g8-theme_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(7)
models = ["Whisper", "Parakeet", "Conformer"]
base = {"Whisper": 4.0, "Parakeet": 5.0, "Conformer": 6.5}
df = pd.DataFrame([(m, s, base[m] * np.exp(-s / 12) + 1 + rng.normal(0, 0.15)) for m in models for s in [0, 5, 10, 15, 20] for _ in range(4)],
                  columns=["model", "snr", "wer"])

p = (ggplot(df, aes("snr", "wer", colour="model"))
     + stat_summary(fun_y=np.mean, geom="line", size=1.3)
     + scale_colour_manual(values=rv.colour_map(models))
     + labs(title="Word error falls as the audio gets cleaner", subtitle="Mean of four runs per setting",
            x="Signal to noise (dB)", y="Word error rate (%)", colour="", caption="Synthetic data")
     + theme(legend_position="top", figure_size=(7, 4)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


## Position adjustments

When marks land on the same spot, **position** decides what happens.

**Dodge** puts them side by side, so every bar can be read from zero:

<p align="center">
<img src="../img/gg/pos-dodge_light.png#gh-light-mode-only" alt="position='dodge' (the default for geom_col(position='dodge')) puts bars side by side so each can be read from zero." width="640">
<img src="../img/gg/pos-dodge_dark.png#gh-dark-mode-only" alt="position='dodge' (the default for geom_col(position='dodge')) puts bars side by side so each can be read from zero." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/pos-dodge_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"cond": ["Clean", "Noisy"] * 3, "model": np.repeat(["Whisper", "Parakeet", "Conformer"], 2), "wer": [3.1, 7.8, 3.6, 9.2, 4.4, 12.1]})
df["cond"] = pd.Categorical(df["cond"], ["Clean", "Noisy"])

p = (ggplot(df, aes("cond", "wer", fill="model")) + geom_col(position="dodge", width=0.7)
     + scale_fill_manual(values=rv.colour_map(["Whisper", "Parakeet", "Conformer"])) + labs(x="", y="WER (%)", fill="")
     + theme(figure_size=(5.6, 3.4)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Stack** adds them up. Only the bottom segment can be compared exactly:

<p align="center">
<img src="../img/gg/pos-stack_light.png#gh-light-mode-only" alt="position='stack': parts add up to a total. Only the bottom segment can be compared exactly." width="640">
<img src="../img/gg/pos-stack_dark.png#gh-dark-mode-only" alt="position='stack': parts add up to a total. Only the bottom segment can be compared exactly." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/pos-stack_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"pipe": np.repeat(["A", "B", "C"], 3), "stage": ["STT", "LLM", "TTS"] * 3,
                   "ms": [180, 520, 210, 150, 380, 260, 240, 700, 180]})
df["stage"] = pd.Categorical(df["stage"], ["TTS", "LLM", "STT"])

p = (ggplot(df, aes("pipe", "ms", fill="stage")) + geom_col(width=0.6) + scale_fill_manual(values=rv.group_map())
     + labs(x="Pipeline", y="Latency (ms)", fill="") + theme(figure_size=(5.6, 3.4)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Fill** rescales every bar to 100%, so you compare shares and lose totals:

<p align="center">
<img src="../img/gg/pos-fill_light.png#gh-light-mode-only" alt="position='fill': every bar is scaled to 100%, so you compare shares and lose the totals." width="640">
<img src="../img/gg/pos-fill_dark.png#gh-dark-mode-only" alt="position='fill': every bar is scaled to 100%, so you compare shares and lose the totals." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/pos-fill_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"pipe": np.repeat(["A", "B", "C"], 3), "stage": ["STT", "LLM", "TTS"] * 3,
                   "ms": [180, 520, 210, 150, 380, 260, 240, 700, 180]})
df["stage"] = pd.Categorical(df["stage"], ["TTS", "LLM", "STT"])

p = (ggplot(df, aes("pipe", "ms", fill="stage")) + geom_col(position="fill", width=0.6) + scale_fill_manual(values=rv.group_map())
     + scale_y_continuous(labels=lambda l: [f"{v:.0%}" for v in l]) + labs(x="Pipeline", y="Share of latency", fill="")
     + theme(figure_size=(5.6, 3.4)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Jitter** nudges points apart so none hide. The nudge is noise, not data:

<p align="center">
<img src="../img/gg/pos-jitter_light.png#gh-light-mode-only" alt="position='jitter': nudge overlapping points apart so each stays visible. The nudge is noise, not data." width="640">
<img src="../img/gg/pos-jitter_dark.png#gh-dark-mode-only" alt="position='jitter': nudge overlapping points apart so each stays visible. The nudge is noise, not data." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/pos-jitter_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(3)
df = pd.DataFrame({"model": np.repeat(["Whisper", "Parakeet", "Conformer"], 30), "wer": np.concatenate([rng.normal(m, 0.6, 30) for m in (3.1, 3.6, 4.4)])})
df["model"] = pd.Categorical(df["model"], ["Whisper", "Parakeet", "Conformer"])

p = (ggplot(df, aes("model", "wer", colour="model")) + geom_jitter(width=0.15, height=0, size=2.4, alpha=0.8)
     + scale_colour_manual(values=rv.colour_map(["Whisper", "Parakeet", "Conformer"]), guide=None) + labs(x="", y="WER (%)")
     + theme(figure_size=(5.6, 3.4)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


## The same idea in matplotlib

Matplotlib does not have a grammar object, but the parts are all there. You do by hand what plotnine does for you:

| Grammar part | plotnine | matplotlib |
|---|---|---|
| Data to position | `aes("x", "y")` | pass `x`, `y` arrays |
| Data to colour | `aes(colour="g")` | loop over groups, one `color=` each |
| Geom | `geom_line()` | `ax.plot()` |
| Stat | `stat_summary()` | compute with numpy or pandas first |
| Scale | `scale_y_log10()` | `ax.set_yscale("log")` |
| Facet | `facet_wrap("g")` | `plt.subplots(...)` |
| Coord | `coord_flip()` | `ax.barh()` or swap arguments |
| Theme | `theme(...)` | `rcParams`, `ax.set(...)` |

**Which should you use?** Use **plotnine** when your data is a table and you want to split, colour and summarise by columns: you write less and make fewer mistakes. Use **matplotlib** when you need exact control of every pixel, unusual plots (3D, polar, images, animation) or fine annotations. They mix well: `p.draw()` returns a matplotlib figure.

## Trade-offs

- **Faster to write vs. easier to bend.** plotnine is short for standard charts, but unusual layouts need matplotlib.
- **Declarative vs. imperative.** plotnine describes what you want; matplotlib describes what to do step by step.
- **Tidy data.** plotnine wants one row per observation (long format). Use `df.melt()` to reshape wide tables.

## Habits that follow from the grammar

1. **Say what each column does** before choosing a chart type.
2. **One aesthetic, one variable.** If colour means model, do not also use shape for model.
3. **Keep scales consistent** across figures: same colour for the same model, same axis limits when charts are compared.
4. **Let stats do the arithmetic** where you can, so the chart and the numbers cannot disagree.

## Sources

- Wilkinson, L. (2005). *The Grammar of Graphics* (2nd ed.). Springer.
- Wickham, H. (2010). A Layered Grammar of Graphics. *Journal of Computational and Graphical Statistics*, 19(1), 3 to 28.
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90 to 95.

**Next:** [Anatomy of a figure](anatomy.md).
