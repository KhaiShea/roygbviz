# Cascade comparisons

A **cascaded speech pipeline** turns speech into speech in three stages: **STT** (speech to text), **LLM** (a language model that writes the reply) and **TTS** (text to speech). Comparing cascades means comparing combinations of models, and that needs consistent colours and the right charts. All numbers in the pictures here are **made-up examples** to show the technique.

## Key terms

- **WER (word error rate)**: the share of words the recogniser gets wrong. Lower is better.
- **Latency**: the time before the user hears a reply. Lower is better.
- **MOS (mean opinion score)**: listeners rate speech from 1 to 5. Higher is better.
- **Pareto front**: pipelines for which no other pipeline is better on both measures.

## Colours: two jobs, kept apart

Roygbviz has **twelve colours in two groups**.

- **Three stage colours** (STT, LLM, TTS) tell you *which part of the pipeline* a mark belongs to.
- **Nine model colours** (red to pink) tell you *which model* a mark belongs to. Three per stage: STT red, orange, yellow; LLM green, teal, blue; TTS indigo, violet, pink.

Use stage colours when the chart is about stages, and model colours when it is about models. Never use a model colour to mean a stage.

```python
stage_colours = rv.group_map()                       # {"STT": ..., "LLM": ..., "TTS": ...}
model_colours = rv.colour_map(["Whisper", "Parakeet", "Conformer"])
```

**Pin colours once, at the top of your analysis**, and reuse the dictionary everywhere. That way a model is the same colour in every figure. `colour_map` accepts up to nine models; extra ones fold into `"Other"` (grey).

## 1. Where does the time go?

Stack the three stages in pipeline order, one bar per pipeline, in stage colours.

<p align="center">
<img src="../img/gg/cascade-stage-latency_light.png#gh-light-mode-only" alt="Where does the time go? Latency per stage for three pipelines, in stage colours, stacked left to right in pipeline order." width="640">
<img src="../img/gg/cascade-stage-latency_dark.png#gh-dark-mode-only" alt="Where does the time go? Latency per stage for three pipelines, in stage colours, stacked left to right in pipeline order." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/cascade-stage-latency_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"pipeline": np.repeat(["Whisper + Llama + Kokoro", "Parakeet + Llama + Kokoro", "Parakeet + Qwen + Piper"], 3),
                   "stage": ["STT", "LLM", "TTS"] * 3, "ms": [320, 540, 210, 150, 540, 210, 150, 380, 120]})
df["stage"] = pd.Categorical(df["stage"], ["TTS", "LLM", "STT"])

p = (ggplot(df, aes("pipeline", "ms", fill="stage")) + geom_col(width=0.6) + coord_flip()
     + scale_fill_manual(values=rv.group_map(), breaks=["STT", "LLM", "TTS"])
     + labs(title="The language model dominates latency", x="", y="Latency (ms)", fill="")
     + theme(legend_position="top", figure_size=(7.4, 3.2), panel_grid_major_x=element_line(), panel_grid_major_y=element_blank()))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Read it:** each bar is the total latency, split by stage. The language model is the widest piece. **Why bars and not a pie:** the lengths are comparable between pipelines.

## 2. Accuracy under different conditions

Dodged bars let you compare models inside each condition, and all bars start at zero.

<p align="center">
<img src="../img/gg/cascade-conditions_light.png#gh-light-mode-only" alt="Same pipelines, three listening conditions. Dodged bars with the model colours pinned so each model keeps its colour everywhere." width="640">
<img src="../img/gg/cascade-conditions_dark.png#gh-dark-mode-only" alt="Same pipelines, three listening conditions. Dodged bars with the model colours pinned so each model keeps its colour everywhere." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/cascade-conditions_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer"]
df = pd.DataFrame({"cond": np.repeat(["Clean", "Noisy", "Far-field"], 3), "model": models * 3, "wer": [3.1, 3.6, 4.4, 7.8, 9.2, 12.1, 10.5, 13.0, 15.8]})
df["cond"] = pd.Categorical(df["cond"], ["Clean", "Noisy", "Far-field"])
df["model"] = pd.Categorical(df["model"], models)

p = (ggplot(df, aes("cond", "wer", fill="model")) + geom_col(position="dodge", width=0.75)
     + scale_fill_manual(values=rv.colour_map(models))
     + labs(title="Noise hurts every model, far-field hurts most", x="", y="Word error rate (%)", fill="")
     + theme(legend_position="top", figure_size=(7, 3.8)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Read it:** noise hurts all models, and far-field audio hurts most. **Check:** same models, same colours as every other figure.

## 3. The accuracy and speed trade-off

A scatter plot with a step line marking the pipelines nothing beats.

<p align="center">
<img src="../img/gg/cascade-pareto_light.png#gh-light-mode-only" alt="A Pareto view: accuracy against speed. Pipelines toward the bottom left win, and a step line joins the ones nothing beats." width="640">
<img src="../img/gg/cascade-pareto_dark.png#gh-dark-mode-only" alt="A Pareto view: accuracy against speed. Pipelines toward the bottom left win, and a step line joins the ones nothing beats." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/cascade-pareto_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"pipeline": ["A", "B", "C", "D", "E", "F"], "latency": [1200, 900, 700, 1500, 650, 1000], "wer": [3.1, 3.6, 4.4, 3.0, 5.2, 4.8]})
front = df.sort_values("latency")
front = front[front["wer"] == front["wer"].cummin()]

p = (ggplot(df, aes("latency", "wer"))
     + geom_step(data=front, colour=rv.colour("grey"), direction="hv")
     + geom_point(colour=rv.colour("teal"), size=4)
     + geom_text(aes(label="pipeline"), nudge_x=35, nudge_y=0.12, ha="left", size=9)
     + labs(title="Trade-off between speed and accuracy", x="Latency (ms)", y="Word error rate (%)"))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


**Read it:** pipelines on the step line are the sensible choices; the others are beaten on both measures by something. Which point to pick depends on how much latency you can tolerate.

## 4. Show the uncertainty

Listener ratings come with spread. Intervals that overlap mean you cannot say which is better.

<p align="center">
<img src="../img/gg/cascade-ci_light.png#gh-light-mode-only" alt="Show uncertainty: mean opinion score with a 95% interval per pipeline. Overlapping intervals mean no clear winner." width="640">
<img src="../img/gg/cascade-ci_dark.png#gh-dark-mode-only" alt="Show uncertainty: mean opinion score with a 95% interval per pipeline. Overlapping intervals mean no clear winner." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/cascade-ci_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

df = pd.DataFrame({"pipeline": ["A", "B", "C", "D"], "mos": [4.1, 3.9, 3.5, 4.0], "lo": [3.9, 3.6, 3.2, 3.7], "hi": [4.3, 4.2, 3.8, 4.3]})
df["pipeline"] = pd.Categorical(df["pipeline"], df["pipeline"][::-1])

p = (ggplot(df, aes("mos", "pipeline"))
     + geom_errorbarh(aes(xmin="lo", xmax="hi"), height=0.18, colour=rv.colour("grey"))
     + geom_point(colour=rv.colour("blue"), size=4)
     + labs(title="Listener rating by pipeline", x="Mean opinion score (1 to 5)", y="")
     + theme(figure_size=(6.4, 3), panel_grid_major_y=element_blank(), panel_grid_major_x=element_line()))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


## 5. Compare against a baseline

A diverging scale centred on zero shows who is better or worse than a reference. Blue is lower error, red is higher.

<p align="center">
<img src="../img/gg/cascade-delta_light.png#gh-light-mode-only" alt="Change against a baseline: a diverging scale centred on zero, so blue is better and red is worse than the baseline." width="640">
<img src="../img/gg/cascade-delta_dark.png#gh-dark-mode-only" alt="Change against a baseline: a diverging scale centred on zero, so blue is better and red is worse than the baseline." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/cascade-delta_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

models = ["Whisper", "Parakeet", "Conformer"]
conds = ["Clean", "Noisy", "Far-field"]
delta = np.array([[0.0, 0.0, 0.0], [0.5, 1.4, 2.5], [1.3, 4.3, 5.3]]) - np.array([[0.4, 1.0, 1.8]] * 3)
df = pd.DataFrame([(m, c, delta[i, j]) for i, m in enumerate(models) for j, c in enumerate(conds)], columns=["model", "cond", "delta"])
df["cond"] = pd.Categorical(df["cond"], conds); df["model"] = pd.Categorical(df["model"], models[::-1])

p = (ggplot(df, aes("cond", "model", fill="delta")) + geom_tile(colour="white", size=1)
     + geom_text(aes(label="delta"), format_string="{:+.1f}", size=10)
     + rv.scale_fill_roygbviz_div(midpoint=0, name="Change in WER")
     + labs(title="Difference from the average model", x="", y="") + theme(figure_size=(6, 3.2)))

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


## 6. Many models: small multiples

Instead of nine lines on one panel, give each its own panel with a shared axis.

<p align="center">
<img src="../img/gg/choose-colours_light.png#gh-light-mode-only" alt="Too many colours: eleven lines in one panel are unreadable. Faceting gives each its own space." width="640">
<img src="../img/gg/choose-colours_dark.png#gh-dark-mode-only" alt="Too many colours: eleven lines in one panel are unreadable. Faceting gives each its own space." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/gg/choose-colours_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(2)
names = [f"m{i}" for i in range(1, 10)]
df = pd.DataFrame([(n, t, np.sin(t / 3 + k) + rng.normal(0, 0.05)) for k, n in enumerate(names) for t in range(30)], columns=["model", "t", "y"])

bad = ggplot(df, aes("t", "y", colour="model")) + geom_line() + scale_colour_manual(values=rv.colour_map(names)) + labs(title="Nine lines in one panel") + theme(legend_position="none")
good = ggplot(df, aes("t", "y")) + geom_line(colour=rv.colour("blue")) + facet_wrap("model", ncol=3) + labs(title="Small multiples") + theme(axis_text=element_blank())
p = bad | good

p.show()  # or: p.save("figure.png", dpi=300)
```

</details>


## 7. Error bars on model means

<p align="center">
<img src="../img/stats/errorbar-basic_light.png#gh-light-mode-only" alt="Error bars in y, in x, and in both." width="640">
<img src="../img/stats/errorbar-basic_dark.png#gh-dark-mode-only" alt="Error bars in y, in x, and in both." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/stats/errorbar-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)
fig, axs = plt.subplots(1, 3, figsize=(7, 3), sharey=True, layout="constrained")
kw = dict(fmt="o", capsize=3, color=rv.colour("blue"), ecolor=rv.colour("grey"), elinewidth=1.4)
axs[0].errorbar(x, y, yerr=0.1 + 0.1 * np.sqrt(x), **kw)
axs[1].errorbar(x, y, xerr=0.25, **kw)
axs[2].errorbar(x, y, xerr=0.25, yerr=0.1 + 0.1 * np.sqrt(x), **kw)
for a, t in zip(axs, ("yerr", "xerr", "both")):
    a.set_title(t, fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## 8. A diagram of the pipeline itself

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


## Which chart for which question

| Question | Chart |
|---|---|
| Which stage is the bottleneck? | Stacked bars in stage colours |
| Which model is most accurate? | Sorted horizontal bars, from zero |
| Does accuracy change with noise? | Lines by condition, or dodged bars |
| Is the faster pipeline worse? | Scatter (speed against accuracy) with a Pareto line |
| Is the difference real? | Intervals or error bars; a test if you need one |
| How is performance distributed? | Box, violin or raincloud over utterances |
| Do two measures agree? | Scatter with identity line, or Bland-Altman |
| Where do errors cluster? | Heatmap or confusion matrix |

## Good practice for papers

1. **Report the data and the uncertainty**, not only the mean.
2. **Same axis limits** across panels that will be compared.
3. **Say how WER was computed** (normalisation, lowercase, punctuation) in the caption or methods.
4. **State the number of utterances** behind each point.
5. **Do not smooth** unless you say so.
6. **Describe colour in the caption** if figures may be printed in black and white; add hatching if needed (see [Shapes](../gallery/shapes-colour-style.md)).

## A reusable pattern

```python
import pandas as pd
from plotnine import *
import roygbviz as rv

rv.use("light")
models = ["Whisper", "Parakeet", "Conformer"]
colours = rv.colour_map(models)           # pin once

p = (ggplot(df, aes("condition", "wer", fill="model"))
     + geom_col(position="dodge")
     + scale_fill_manual(values=colours)
     + labs(x="", y="Word error rate (%)", fill=""))
p.save("wer.png", dpi=300)
```

**Next:** [Colour guide](colour.md).
