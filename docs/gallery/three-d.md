# 3D plots

3D plots look impressive, but they are hard to read: depth distorts size and hides data. Use them to **explore** a surface, and prefer 2D (heat maps, contours, small multiples) to **report** numbers.

**Matplotlib reference:** `fig.add_subplot(projection='3d')`, `ax.plot_surface`, `ax.plot_wireframe`, `ax.scatter`, `ax.bar3d`, `ax.contour`.

**How to read each entry:** the picture and code are real output; **Use when** says why you would draw it; **Key calls** are the functions to remember; **Watch out** is the usual mistake.

## On this page

- **3D**: Surface, Wireframe and scatter, 3D bars and floor contours, Lines and triangulated surfaces

## 3D

### Surface

<p align="center">
<img src="../img/3d/surface_light.png#gh-light-mode-only" alt="3D surface: a function of two variables. Use it to explore, not to report numbers." width="640">
<img src="../img/3d/surface_dark.png#gh-dark-mode-only" alt="3D surface: a function of two variables. Use it to explore, not to report numbers." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/3d/surface_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

X, Y = np.meshgrid(np.linspace(-3, 3, 60), np.linspace(-3, 3, 60))
Z = np.sin(np.hypot(X, Y)) * np.exp(-0.1 * np.hypot(X, Y))
fig = plt.figure(figsize=(6, 4.4))
ax = fig.add_subplot(projection="3d")
ax.plot_surface(X, Y, Z, cmap="roygbviz", linewidth=0, antialiased=True)
ax.set(xlabel="x", ylabel="y", zlabel="z")

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** A function of two variables.
- **Key calls:** `ax.plot_surface(X, Y, Z, cmap='roygbviz')`
- **Watch out:** Colour by height adds redundancy that helps reading.

### Wireframe and scatter

<p align="center">
<img src="../img/3d/wireframe-scatter_light.png#gh-light-mode-only" alt="3D wireframe and scatter: points in space, coloured by a fourth variable." width="640">
<img src="../img/3d/wireframe-scatter_dark.png#gh-dark-mode-only" alt="3D wireframe and scatter: points in space, coloured by a fourth variable." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/3d/wireframe-scatter_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

rng = np.random.default_rng(3)
n = 120
x, y = rng.normal(size=(2, n)); z = x * y + rng.normal(0, 0.2, n)
fig = plt.figure(figsize=(7, 3.4))
ax = fig.add_subplot(1, 2, 1, projection="3d")
X, Y = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
ax.plot_wireframe(X, Y, X * Y, color=rv.colour("teal"), lw=0.7); ax.set_title("wireframe", fontsize=10)
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.scatter(x, y, z, c=z, cmap="roygbviz", s=18); ax2.set_title("scatter", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Structure and points in space.
- **Key calls:** `ax.plot_wireframe`, `ax.scatter(x, y, z, c=)`
- **Watch out:** Rotate and check from several angles.

### 3D bars and floor contours

<p align="center">
<img src="../img/3d/bars-contours_light.png#gh-light-mode-only" alt="3D bars and projected contours: bars on a grid, and contour lines drawn on the floor of the box." width="640">
<img src="../img/3d/bars-contours_dark.png#gh-dark-mode-only" alt="3D bars and projected contours: bars on a grid, and contour lines drawn on the floor of the box." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/3d/bars-contours_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig = plt.figure(figsize=(7, 3.4))
ax = fig.add_subplot(1, 2, 1, projection="3d")
xs, ys = np.meshgrid(np.arange(4), np.arange(4))
ax.bar3d(xs.ravel(), ys.ravel(), 0, 0.7, 0.7, np.random.default_rng(1).uniform(1, 5, 16), color=rv.colour("blue"), shade=True)
ax.set_title("bar3d", fontsize=10)
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
X, Y = np.meshgrid(np.linspace(-3, 3, 50), np.linspace(-3, 3, 50)); Z = np.exp(-(X ** 2 + Y ** 2) / 3)
ax2.plot_surface(X, Y, Z, cmap="roygbviz", alpha=0.7, linewidth=0)
ax2.contour(X, Y, Z, zdir="z", offset=-0.4, cmap="roygbviz")
ax2.set_zlim(-0.4, 1); ax2.set_title("contour on the floor", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Counts on a grid.
- **Key calls:** `ax.bar3d(...)`; `ax.contour(..., zdir='z', offset=)`
- **Watch out:** Bars hide each other; a heat map is clearer.

### Lines and triangulated surfaces

<p align="center">
<img src="../img/3d/trisurf-lines_light.png#gh-light-mode-only" alt="3D line and triangulated surface: a helix, and a surface built from scattered points." width="640">
<img src="../img/3d/trisurf-lines_dark.png#gh-dark-mode-only" alt="3D line and triangulated surface: a helix, and a surface built from scattered points." width="640">
</p>

<p align="center"><sub>Also in <a href="../img/3d/trisurf-lines_cream.png">cream</a></sub></p>

<details markdown="1">
<summary>Show the code</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
import roygbviz as rv

rv.use("light")  # white by default; or "dark", or "cream"

fig = plt.figure(figsize=(7, 3.4))
ax = fig.add_subplot(1, 2, 1, projection="3d")
t = np.linspace(0, 6 * np.pi, 300)
ax.plot(np.cos(t), np.sin(t), t, color=rv.colour("red")); ax.set_title("helix", fontsize=10)
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
rng = np.random.default_rng(4)
x, y = rng.uniform(-2, 2, (2, 200)); ax2.plot_trisurf(x, y, np.sin(x) * np.cos(y), cmap="roygbviz", linewidth=0.1)
ax2.set_title("plot_trisurf", fontsize=10)

plt.show()  # or: fig.savefig("figure.png", dpi=300)
```

</details>


- **Use when:** Paths and scattered points.
- **Key calls:** `ax.plot(x, y, z)`; `ax.plot_trisurf`
- **Watch out:** Triangulation needs enough points.

## Rules of thumb

- **Set the view**: `ax.view_init(elev=25, azim=-60)`.
- **Label all three axes.**
- **Prefer a heat map** to show values; use 3D to explore.
- **Interactive** rotation helps: use a Jupyter widget backend.

**Back to the [home page](../index.md).**
