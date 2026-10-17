# Ticks, scales and spines

The numbers and lines around your data. Getting these right turns a plot from default to professional.

**Matplotlib reference:** `matplotlib.ticker`, `ax.set_xscale`, `ax.spines`, `ax.tick_params`. In plotnine: `scale_x_*`, `scale_y_*`, `breaks=`, `labels=`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **Ticks**: Locators, Formatters, Major and minor ticks, Tick parameters, Long labels, Dates, Too many ticks
- **Scales**: Linear against log, Log-log, Symmetric log, Logit, asinh, Custom scale, Readable log labels
- **Spines**: Spines at zero, Range frames, Dropped spines, Arrow axes

## Ticks

### Locators

<p align="center">
<img src="../img/ticks/locators_light.png#gh-light-mode-only" alt="Tick locators decide where ticks go: MultipleLocator, MaxNLocator, LinearLocator and FixedLocator." width="640">
<img src="../img/ticks/locators_dark.png#gh-dark-mode-only" alt="Tick locators decide where ticks go: MultipleLocator, MaxNLocator, LinearLocator and FixedLocator." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/locators_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import ticker

x = np.linspace(0, 10, 100)
locs = [("MultipleLocator(2.5)", ticker.MultipleLocator(2.5)), ("MaxNLocator(4)", ticker.MaxNLocator(4)),
        ("LinearLocator(6)", ticker.LinearLocator(6)), ("FixedLocator([0, 1, 5, 10])", ticker.FixedLocator([0, 1, 5, 10]))]
fig, axs = plt.subplots(len(locs), 1, figsize=(6.4, 5), layout="constrained")
for ax, (name, loc) in zip(axs, locs):
    ax.plot(x, np.sin(x), color=rv.colour("blue"))
    ax.xaxis.set_major_locator(loc)
    ax.set_title(name, fontsize=9)
    ax.set_yticks([])

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Choosing where ticks go.
- **Key calls:** `MultipleLocator`, `MaxNLocator`, `LinearLocator`, `FixedLocator`
- **Watch out:** Fewer ticks read better.

### Formatters

<p align="center">
<img src="../img/ticks/formatters_light.png#gh-light-mode-only" alt="Tick formatters decide what the labels say: percent, thousands separators, dollars and units." width="640">
<img src="../img/ticks/formatters_dark.png#gh-dark-mode-only" alt="Tick formatters decide what the labels say: percent, thousands separators, dollars and units." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/formatters_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import ticker

fig, axs = plt.subplots(1, 3, figsize=(7.4, 3), layout="constrained")
x = np.linspace(0, 1, 6)
axs[0].plot(x, x, color=rv.colour("red")); axs[0].xaxis.set_major_formatter(ticker.PercentFormatter(1.0)); axs[0].set_title("PercentFormatter", fontsize=9)
y = np.linspace(0, 2_000_000, 6)
axs[1].plot(x, y, color=rv.colour("teal")); axs[1].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}")); axs[1].set_title("StrMethodFormatter", fontsize=9)
axs[2].plot(x, y / 1000, color=rv.colour("violet")); axs[2].yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"${v:,.0f}k")); axs[2].set_title("FuncFormatter", fontsize=9)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Choosing what labels say.
- **Key calls:** `PercentFormatter`, `StrMethodFormatter`, `FuncFormatter`
- **Watch out:** Put units in the axis label, not on every tick.

### Major and minor ticks

<p align="center">
<img src="../img/ticks/major-minor_light.png#gh-light-mode-only" alt="Major and minor ticks: labelled majors, unlabelled minors, and a faint minor grid." width="640">
<img src="../img/ticks/major-minor_dark.png#gh-dark-mode-only" alt="Major and minor ticks: labelled majors, unlabelled minors, and a faint minor grid." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/major-minor_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import ticker

x = np.linspace(0, 10, 200)
fig, ax = plt.subplots(figsize=(6.4, 3.4), layout="constrained")
ax.plot(x, np.exp(-x / 4) * np.cos(3 * x), color=rv.colour("blue"))
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
ax.tick_params(which="minor", length=3, color=rv.colour("grey"))
ax.tick_params(which="major", length=6, color=rv.colour("grey"))
ax.grid(which="minor", axis="x", linewidth=0.4)
ax.grid(which="major", axis="x")
ax.set_title("Major (every 2) and minor (every 0.5) ticks")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Fine reading.
- **Key calls:** `ax.xaxis.set_minor_locator(...)`
- **Watch out:** Add a minor grid only when readers need precision.

### Tick parameters

<p align="center">
<img src="../img/ticks/tick-params_light.png#gh-light-mode-only" alt="tick_params: length, width, direction, colour, label size and padding in one call." width="640">
<img src="../img/ticks/tick-params_dark.png#gh-dark-mode-only" alt="tick_params: length, width, direction, colour, label size and padding in one call." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/tick-params_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 50)
fig, axs = plt.subplots(1, 2, figsize=(7, 3), layout="constrained")
for ax in axs:
    ax.plot(x, np.sin(x), color=rv.colour("blue"))
axs[0].set_title("Theme default (no tick marks)", fontsize=10)
axs[1].tick_params(axis="both", length=6, width=1.2, direction="out", color=rv.colour("red"), labelsize=11, pad=6)
axs[1].set_title("length=6, direction='out', pad=6", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Length, direction and colour.
- **Key calls:** `ax.tick_params(axis='both', length=, direction=, pad=)`
- **Watch out:** Roygbviz hides tick marks by default.

### Long labels

<p align="center">
<img src="../img/ticks/rotated-labels_light.png#gh-light-mode-only" alt="Long category names: rotate and right-align them, or better, turn the chart on its side." width="640">
<img src="../img/ticks/rotated-labels_dark.png#gh-dark-mode-only" alt="Long category names: rotate and right-align them, or better, turn the chart on its side." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/rotated-labels_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

names = ["Whisper large-v3", "Parakeet TDT 1.1B", "Conformer CTC", "wav2vec 2.0 base", "Distil-Whisper medium"]
vals = [3.1, 3.6, 4.4, 5.9, 4.0]
fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.6), layout="constrained")
axs[0].bar(names, vals, color=rv.colour("teal"))
plt.setp(axs[0].get_xticklabels(), rotation=35, ha="right", rotation_mode="anchor")
axs[0].set_title("Rotated labels", fontsize=10)
axs[1].barh(names, vals, color=rv.colour("teal"))
axs[1].invert_yaxis(); axs[1].grid(axis="y", visible=False); axs[1].grid(axis="x", visible=True)
axs[1].set_title("Horizontal bars (usually better)", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Names too long to fit.
- **Key calls:** `plt.setp(labels, rotation=35, ha='right', rotation_mode='anchor')`
- **Watch out:** Horizontal bars avoid rotation.

### Dates

<p align="center">
<img src="../img/ticks/dates_light.png#gh-light-mode-only" alt="Dates: ConciseDateFormatter picks sensible labels at any zoom level, with the year shown once." width="640">
<img src="../img/ticks/dates_dark.png#gh-dark-mode-only" alt="Dates: ConciseDateFormatter picks sensible labels at any zoom level, with the year shown once." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/dates_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

import matplotlib.dates as mdates
import pandas as pd

t = pd.date_range("2026-01-01", periods=240, freq="D")
y = np.random.default_rng(1).normal(size=240).cumsum()
fig, axs = plt.subplots(2, 1, figsize=(6.4, 4.4), layout="constrained")
axs[0].plot(t, y, color=rv.colour("blue")); axs[0].set_title("Default date labels", fontsize=10)
plt.setp(axs[0].get_xticklabels(), rotation=0)
axs[1].plot(t, y, color=rv.colour("blue"))
loc = mdates.AutoDateLocator()
axs[1].xaxis.set_major_locator(loc)
axs[1].xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
axs[1].set_title("ConciseDateFormatter", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Time axes.
- **Key calls:** `mdates.ConciseDateFormatter(mdates.AutoDateLocator())`
- **Watch out:** Let it choose; override only if needed.

### Too many ticks

<p align="center">
<img src="../img/ticks/too-many_light.png#gh-light-mode-only" alt="Fixing crowded ticks: thin them out with a MaxNLocator rather than shrinking the font." width="640">
<img src="../img/ticks/too-many_dark.png#gh-dark-mode-only" alt="Fixing crowded ticks: thin them out with a MaxNLocator rather than shrinking the font." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/ticks/too-many_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import ticker

x = np.arange(60)
y = np.random.default_rng(2).normal(size=60).cumsum()
fig, axs = plt.subplots(2, 1, figsize=(6.4, 4), layout="constrained")
axs[0].bar(x.astype(str), y, color=rv.colour("red")); axs[0].set_title("Every category labelled", fontsize=10)
axs[1].bar(x.astype(str), y, color=rv.colour("teal"))
axs[1].xaxis.set_major_locator(ticker.MaxNLocator(8)); axs[1].set_title("MaxNLocator(8)", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Crowded categories.
- **Key calls:** `ax.xaxis.set_major_locator(MaxNLocator(8))`
- **Watch out:** Thin out rather than shrink the text.

## Scales

### Linear against log

<p align="center">
<img src="../img/scales/linear-log_light.png#gh-light-mode-only" alt="Linear against log: the same data, where each gridline on the log plot is a factor of ten." width="640">
<img src="../img/scales/linear-log_dark.png#gh-dark-mode-only" alt="Linear against log: the same data, where each gridline on the log plot is a factor of ten." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/linear-log_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0.1, 5, 100)
y = 10 ** x
fig, axs = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
axs[0].plot(x, y, color=rv.colour("red")); axs[0].set_title("Linear", fontsize=10)
axs[1].plot(x, y, color=rv.colour("red")); axs[1].set_yscale("log"); axs[1].set_title("set_yscale('log')", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Data across many powers of ten.
- **Key calls:** `ax.set_yscale('log')`
- **Watch out:** Log scales cannot show zero or negatives.

### Log-log

<p align="center">
<img src="../img/scales/loglog_light.png#gh-light-mode-only" alt="Log-log: a power law y = x^2 becomes a straight line whose slope is the exponent." width="640">
<img src="../img/scales/loglog_dark.png#gh-dark-mode-only" alt="Log-log: a power law y = x^2 becomes a straight line whose slope is the exponent." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/loglog_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.logspace(0, 3, 50)
fig, ax = plt.subplots(figsize=(5.4, 3.8), layout="constrained")
ax.loglog(x, x ** 2, "o-", color=rv.colour("blue"), label="y = x^2")
ax.loglog(x, 5 * x ** 0.5, "s-", color=rv.colour("red"), label="y = 5 x^0.5")
ax.legend(); ax.grid(which="both", linewidth=0.4)
ax.set_title("Power laws are straight lines")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Power laws.
- **Key calls:** `ax.loglog(x, y)`
- **Watch out:** A straight line means a power law.

### Symmetric log

<p align="center">
<img src="../img/scales/symlog_light.png#gh-light-mode-only" alt="symlog: logarithmic far from zero, linear near it, so negative values and zero still fit." width="640">
<img src="../img/scales/symlog_dark.png#gh-dark-mode-only" alt="symlog: logarithmic far from zero, linear near it, so negative values and zero still fit." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/symlog_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(-100, 100, 400)
y = np.sinh(x / 20)
fig, axs = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
axs[0].plot(x, y, color=rv.colour("teal")); axs[0].set_title("Linear", fontsize=10)
axs[1].plot(x, y, color=rv.colour("teal")); axs[1].set_yscale("symlog", linthresh=1); axs[1].set_title("symlog(linthresh=1)", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Both signs and large range.
- **Key calls:** `ax.set_yscale('symlog', linthresh=1)`
- **Watch out:** Say the linear threshold.

### Logit

<p align="center">
<img src="../img/scales/logit_light.png#gh-light-mode-only" alt="logit: spreads out probabilities near 0 and 1, where differences matter most." width="640">
<img src="../img/scales/logit_dark.png#gh-dark-mode-only" alt="logit: spreads out probabilities near 0 and 1, where differences matter most." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/logit_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

p = np.linspace(0.001, 0.999, 300)
fig, axs = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
axs[0].plot(p, p ** 3, color=rv.colour("violet")); axs[0].set_title("Linear", fontsize=10)
axs[1].plot(p, p ** 3, color=rv.colour("violet")); axs[1].set_yscale("logit"); axs[1].set_title("logit", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Probabilities near 0 and 1.
- **Key calls:** `ax.set_yscale('logit')`
- **Watch out:** Values must lie strictly between 0 and 1.

### asinh

<p align="center">
<img src="../img/scales/asinh_light.png#gh-light-mode-only" alt="asinh: like symlog but smooth through zero. Good for data that spans many orders of magnitude and both signs." width="640">
<img src="../img/scales/asinh_dark.png#gh-dark-mode-only" alt="asinh: like symlog but smooth through zero. Good for data that spans many orders of magnitude and both signs." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/asinh_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(-1000, 1000, 400)
fig, ax = plt.subplots(figsize=(5.4, 3.6), layout="constrained")
ax.plot(x, x ** 3 / 1e6, color=rv.colour("orange"))
ax.set_yscale("asinh")
ax.set_yticks([-1000, -100, -10, 0, 10, 100, 1000])
ax.set_yticklabels(["-1000", "-100", "-10", "0", "10", "100", "1000"])
ax.yaxis.set_minor_locator(plt.NullLocator())
ax.set_title("asinh scale")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Smooth alternative to symlog.
- **Key calls:** `ax.set_yscale('asinh')`
- **Watch out:** Set ticks yourself.

### Custom scale

<p align="center">
<img src="../img/scales/custom_light.png#gh-light-mode-only" alt="A custom scale from two functions: here a square-root axis, handy for counts." width="640">
<img src="../img/scales/custom_dark.png#gh-dark-mode-only" alt="A custom scale from two functions: here a square-root axis, handy for counts." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/custom_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 100, 200)
fig, axs = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
axs[0].plot(x, x ** 2, color=rv.colour("blue")); axs[0].set_title("Linear", fontsize=10)
axs[1].plot(x, x ** 2, color=rv.colour("blue"))
axs[1].set_yscale("function", functions=(np.sqrt, np.square))
axs[1].set_title("function scale (sqrt)", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Any transformation.
- **Key calls:** `ax.set_yscale('function', functions=(f, inverse))`
- **Watch out:** Provide both directions.

### Readable log labels

<p align="center">
<img src="../img/scales/dual-log_light.png#gh-light-mode-only" alt="Log axes with minor ticks and real units: round numbers read better than 10^3." width="640">
<img src="../img/scales/dual-log_dark.png#gh-dark-mode-only" alt="Log axes with minor ticks and real units: round numbers read better than 10^3." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/scales/dual-log_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

from matplotlib import ticker

n = np.logspace(1, 6, 40)
fig, ax = plt.subplots(figsize=(6, 3.6), layout="constrained")
ax.semilogx(n, 100 * (1 - np.exp(-n / 5e4)), color=rv.colour("teal"))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.set(xlabel="training hours", ylabel="accuracy (%)", title="Log x axis, plain labels")
ax.grid(which="minor", axis="x", linewidth=0.4)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Plain numbers on a log axis.
- **Key calls:** `FuncFormatter(lambda v, _: f'{v:,.0f}')`
- **Watch out:** Show minor gridlines faintly.

## Spines

### Spines at zero

<p align="center">
<img src="../img/spines/placement_light.png#gh-light-mode-only" alt="Spines placed at zero: the axes cross in the middle, as in a school maths graph." width="640">
<img src="../img/spines/placement_dark.png#gh-dark-mode-only" alt="Spines placed at zero: the axes cross in the middle, as in a school maths graph." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/spines/placement_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(-6, 6, 300)
fig, ax = plt.subplots(figsize=(5.4, 3.6), layout="constrained")
ax.plot(x, np.sin(x) * x / 3, color=rv.colour("red"))
for side in ("left", "bottom"):
    ax.spines[side].set_position("zero"); ax.spines[side].set_visible(True)
ax.grid(False)
ax.set_title("Spines at zero", loc="center", y=1.08)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Maths-style axes.
- **Key calls:** `ax.spines['left'].set_position('zero')`
- **Watch out:** Tick labels may collide with data.

### Range frames

<p align="center">
<img src="../img/spines/bounds_light.png#gh-light-mode-only" alt="Range frames: spines drawn only from the first to the last data value." width="640">
<img src="../img/spines/bounds_dark.png#gh-dark-mode-only" alt="Range frames: spines drawn only from the first to the last data value." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/spines/bounds_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(3)
x = rng.uniform(1, 9, 30); y = 2 * x + rng.normal(0, 1.5, 30)
fig, ax = plt.subplots(figsize=(5.4, 3.6), layout="constrained")
ax.scatter(x, y, color=rv.colour("blue"))
for side in ("left", "bottom"):
    ax.spines[side].set_visible(True)
ax.spines["left"].set_bounds(y.min(), y.max()); ax.spines["bottom"].set_bounds(x.min(), x.max())
ax.grid(False)
ax.set_title("set_bounds() range frame")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Spines that match the data.
- **Key calls:** `ax.spines['left'].set_bounds(lo, hi)`
- **Watch out:** A Tufte-style look.

### Dropped spines

<p align="center">
<img src="../img/spines/dropped_light.png#gh-light-mode-only" alt="Dropped spines: the axes float away from the data (Tufte style) with set_position(('outward', n))." width="640">
<img src="../img/spines/dropped_dark.png#gh-dark-mode-only" alt="Dropped spines: the axes float away from the data (Tufte style) with set_position(('outward', n))." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/spines/dropped_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(6); y = np.array([3, 5, 4, 7, 6, 8])
fig, ax = plt.subplots(figsize=(5.4, 3.4), layout="constrained")
ax.bar(x, y, color=rv.colour("teal"))
ax.spines["bottom"].set_position(("outward", 8))
ax.set_title("Outward spine")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Floating axes.
- **Key calls:** `ax.spines['bottom'].set_position(('outward', 8))`
- **Watch out:** Keeps bars off the axis.

### Arrow axes

<p align="center">
<img src="../img/spines/arrows_light.png#gh-light-mode-only" alt="Axes drawn as arrows: remove the spines, then plot an arrow marker at the end of each axis." width="640">
<img src="../img/spines/arrows_dark.png#gh-dark-mode-only" alt="Axes drawn as arrows: remove the spines, then plot an arrow marker at the end of each axis." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/spines/arrows_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 4, 200)
fig, ax = plt.subplots(figsize=(5.4, 3.6), layout="constrained")
ax.plot(x, x ** 2 / 4, color=rv.colour("red"))
ax.set_xlim(0, 4.3); ax.set_ylim(0, 4.6)
ax.grid(False)
for side in ("left", "bottom"):
    ax.spines[side].set_visible(False)
ax.plot(1, 0, ">", color=plt.rcParams["text.color"], transform=ax.transAxes, clip_on=False)
ax.plot(0, 1, "^", color=plt.rcParams["text.color"], transform=ax.transAxes, clip_on=False)
ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=dict(arrowstyle="-", color=plt.rcParams["text.color"]))
ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=dict(arrowstyle="-", color=plt.rcParams["text.color"]))
ax.set_title("Arrow axes")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Teaching diagrams.
- **Key calls:** Plot a marker at the axis end with `transform=ax.transAxes`
- **Watch out:** Decoration only.

## Rules of thumb

- **Fewer ticks**, rounder numbers.
- **Units in the label**, not on every tick.
- **Log scales** for ratios; always say so.
- **Dates:** `ConciseDateFormatter` first.

**Back to the [home page](../index.md).**
