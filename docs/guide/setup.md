# Setup

Get from nothing to a first figure. Pick your operating system, then follow the steps.

## 1. What you need

- **Python 3.10 or newer.** Check with `python3 --version`.
- **A virtual environment** (a private folder of packages for one project, so projects do not break each other).
- **Roygbviz**, which brings matplotlib and plotnine with it.

## 2. Make an environment and install

**Linux and macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate        # fish shell: source .venv/bin/activate.fish
pip install roygbviz
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install roygbviz
```

**Why a virtual environment?** Many Linux systems refuse `pip install` into the system Python (a rule called PEP 668, with the message "externally-managed-environment"). A venv avoids that and keeps your project tidy.

## 3. Your first figure

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")                       # white paper (the default); one call sets matplotlib AND plotnine
fig, ax = plt.subplots()
ax.plot(np.arange(10), np.arange(10) ** 1.5)
ax.set(title="Hello", xlabel="x", ylabel="y")
plt.show()
```

<p align="center">
<img src="../img/lines/line-basic_light.png#gh-light-mode-only" alt="A basic line plot with three series, a title, axis labels and a legend." width="640">
<img src="../img/lines/line-basic_dark.png#gh-dark-mode-only" alt="A basic line plot with three series, a title, axis labels and a legend." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/lines/line-basic_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

x = np.linspace(0, 10, 200)
fig, ax = plt.subplots(figsize=(6.4, 4), layout="constrained")
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.sin(x) * np.exp(-x / 6), label="damped")
ax.plot(x, 0.5 * np.cos(2 * x), label="cos(2x) / 2")
ax.set(title="A line plot", xlabel="x", ylabel="value", ylim=(-1.5, 1.1))
ax.legend(ncols=3, loc="lower left")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


## 4. Modes and sizes

```python
rv.use("dark")                # dark slides
rv.use("cream")               # the original warm paper
rv.use("light", base_size=14) # bigger text for posters and slides
rv.use("light", grid="xy")    # grid on both axes (good for scatter plots)
```

`rv.use()` returns the active palette and changes the defaults for the rest of the session. Call it once at the top of a script or notebook.

## 5. Working in an editor

**VS Code.** Install the Python and Jupyter extensions, choose your `.venv` as the interpreter (Ctrl+Shift+P, "Python: Select Interpreter"), then run cells in a `.ipynb` file.

**Jupyter.** Install with `pip install jupyterlab` inside the venv, then `jupyter lab`. Add `%matplotlib inline` at the top of a notebook if figures do not appear. For crisp figures on high-resolution screens, use `%config InlineBackend.figure_format = "retina"`.

**Plain scripts.** Use `plt.show()` to open a window or `fig.savefig("name.png", dpi=300)` to write a file. On a server with no screen, set `MPLBACKEND=Agg` first.

## 6. Checking it worked

```python
import roygbviz as rv
rv.use("light")
print(rv.colour("red"))           # a hex colour
print(rv.colour_map(["A", "B"]))  # pinned colours for two labels
```

If the colour prints, the install is fine. If figures look plain, you forgot `rv.use(...)`.

## 7. Keeping a project reproducible

- Record versions: `pip freeze > requirements.txt`.
- Put `rv.use("light")` in one shared file (for example `style.py`) and import it from every notebook.
- Seed random numbers (`np.random.default_rng(1)`) so figures do not change each run.

**Next:** [Fonts and text](fonts.md) or jump to the [gallery](../index.md).
