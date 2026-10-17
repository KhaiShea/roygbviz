"""Matplotlib side: rcParams, colormaps, and the one-call ``use()``."""
from __future__ import annotations

import warnings

import matplotlib as mpl
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap

from .config import _STATE, pick_font, resolve
from .palettes import ROLES, get_palette


def cmap(kind: str = "blue", mode=None, colourblind=None, n: int = 256) -> LinearSegmentedColormap:
    """Matplotlib colormap. ``kind``: a role name, ``"spectrum"``, or ``"diverging"``."""
    mode, colourblind, _ = resolve(mode, colourblind)
    p = get_palette(mode, colourblind)
    cols = p.diverging(11) if kind == "diverging" else p.sequential(kind, 11)
    return LinearSegmentedColormap.from_list(f"roygbviz_{kind}_{mode}", cols, N=n)


def use(mode: str = "light", colourblind: bool = False, order: str = "series",
        plotnine: bool = True, base_size: float = 11, grid: str = "y"):
    """Make Roygbviz the default for the whole session: matplotlib rcParams, colormaps, and plotnine's theme.

    ``mode`` is ``"light"`` (white paper, the default), ``"dark"``, or ``"cream"`` (the original warm paper).
    ``grid`` is ``"y"`` (horizontal hairlines, the default), ``"x"``, ``"xy"`` or ``"none"``.
    Returns the active :class:`~roygbviz.palettes.Palette`.
    """
    if grid not in ("y", "x", "xy", "none"):
        raise ValueError("grid must be 'y', 'x', 'xy' or 'none'")
    p = get_palette(mode, colourblind)
    _STATE.update(mode=mode, colourblind=colourblind, order=order, grid=grid, base_size=float(base_size))
    n = p.neutrals
    mpl.rcParams.update({
        "font.family": pick_font(),
        "figure.facecolor": n["bg"], "savefig.facecolor": n["bg"],
        "axes.facecolor": n["panel"], "axes.edgecolor": n["rule"], "axes.linewidth": 0.9,
        "axes.labelcolor": n["text_2"], "axes.titlecolor": n["text"], "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlesize": base_size * 1.3, "axes.labelsize": base_size * 0.9,
        "axes.grid": grid != "none", "axes.grid.axis": {"y": "y", "x": "x", "xy": "both", "none": "both"}[grid],
        "axes.axisbelow": True,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "axes.spines.bottom": True,
        "grid.color": n["grid"], "grid.linewidth": 0.8,
        "xtick.color": n["muted"], "ytick.color": n["muted"],
        "xtick.labelcolor": n["muted"], "ytick.labelcolor": n["muted"],
        "xtick.major.size": 0, "ytick.major.size": 0, "xtick.minor.size": 0, "ytick.minor.size": 0,
        "xtick.labelsize": base_size * 0.8, "ytick.labelsize": base_size * 0.8,
        "text.color": n["text"],
        "legend.frameon": False, "legend.labelcolor": n["text_2"],
        "lines.linewidth": 2.0 * base_size / 11, "lines.markersize": 7 * base_size / 11,
        "axes.prop_cycle": cycler(color=p.series(order=order)),
        "image.cmap": "roygbviz",
        "boxplot.boxprops.color": n["text_2"], "boxplot.whiskerprops.color": n["text_2"], "boxplot.capprops.color": n["text_2"],
        "boxplot.medianprops.color": p.roles["red"], "boxplot.medianprops.linewidth": 1.8 * base_size / 11,
        "boxplot.boxprops.linewidth": 1.3 * base_size / 11, "boxplot.whiskerprops.linewidth": 1.3 * base_size / 11,
        "boxplot.capprops.linewidth": 1.3 * base_size / 11, "boxplot.flierprops.markeredgecolor": n["muted"],
        "errorbar.capsize": 3,
    })
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # re-registering on every use() is intentional
        for name, kind in (("roygbviz", "blue"), ("roygbviz_spectrum", "spectrum"), ("roygbviz_div", "diverging")):
            mpl.colormaps.register(cmap(kind, mode, colourblind), name=name, force=True)
    if plotnine:
        from plotnine import theme_set
        from .theme import theme_roygbviz
        theme_set(theme_roygbviz(mode, colourblind, base_size, grid=grid))
    return p


def stroke(size: float = 1.0, base_size: float | None = None) -> float:
    """Scale a line width or marker size with the text size, so a figure grows or shrinks as one.

    ``size`` is the width you would use at the default base size (11). ``base_size`` defaults to the one set by ``use()``.
    """
    return size * (_STATE["base_size"] if base_size is None else base_size) / 11.0


def colour(role: str, mode=None, colourblind=None) -> str:
    """One hex colour by name: ``"red"``, ``"orange"``, ``"yellow"``, ``"green"``, ``"teal"``, ``"blue"``,
    ``"indigo"``, ``"violet"``, ``"pink"``, a stage (``"STT"``, ``"LLM"``, ``"TTS"``), or ``"grey"`` for the neutral."""
    from .palettes import GROUPS
    if role not in ROLES + GROUPS + ("grey",):
        raise ValueError(f"unknown colour {role!r}; try one of {ROLES + GROUPS + ('grey',)}")
    mode, colourblind, _ = resolve(mode, colourblind)
    p = get_palette(mode, colourblind)
    return p.neutrals["grey"] if role == "grey" else (p.roles.get(role) or p.groups[role])


def colour_map(levels, mode=None, colourblind=None, order=None) -> dict:
    """Pin each level to one colour so it looks the same in every figure: ``scale_colour_manual(values=colour_map(MODELS))``.

    Up to nine levels. A level called ``"Other"`` gets the neutral grey and does not use up a colour.
    """
    from .config import resolve

    mode, colourblind, order = resolve(mode, colourblind, order)
    p = get_palette(mode, colourblind)
    named = [lv for lv in levels if lv != "Other"]
    if len(named) > len(ROLES):
        raise ValueError("Roygbviz has nine series colours. Fold the rest into 'Other', or facet.")
    out = dict(zip(named, p.series(order=order)))
    if "Other" in levels:
        out["Other"] = p.neutrals["grey"]
    return out


def levels(role: str, n: int = 5, mode=None, colourblind=None) -> list[str]:
    """``n`` (3, 5 or 7) lightness levels of one colour, deepest first. Handy for stacked bars or one family of series."""
    mode, colourblind, _ = resolve(mode, colourblind)
    return get_palette(mode, colourblind).levels(role, n)


def group_map(mode=None, colourblind=None) -> dict:
    """The stage colours, ``{"STT": ..., "LLM": ..., "TTS": ...}``, for top-level comparisons.
    Use with ``scale_fill_manual(values=rv.group_map())``, or the ``scale_*_roygbviz_groups`` scales."""
    mode, colourblind, _ = resolve(mode, colourblind)
    return get_palette(mode, colourblind).groups


def shade(colour: str, steps: int = 1, mode=None, colourblind=None) -> str:
    """The shading colour for a fill: ``steps`` levels lighter than ``colour`` (default one).

    ``colour`` is a role or stage name (``"blue"``, ``"STT"``) or any hex. Use it for areas, bands, ribbons and the
    bodies of outlined marks, and keep the line or outline in the default colour, so the shade reads as the same
    colour, one step softer::

        geom_area(fill=rv.shade("blue")) + geom_line(colour=rv.colour("blue"))
    """
    from .palettes import GROUPS, _shift

    mode, colourblind, _ = resolve(mode, colourblind)
    p = get_palette(mode, colourblind)
    if colour in p.roles:
        base = p.roles[colour]
    elif colour in GROUPS:
        base = p.groups[colour]
    else:
        base = colour
    return _shift(base, steps)


def shade_map(mapping: dict, steps: int = 1, mode=None, colourblind=None) -> dict:
    """:func:`shade` applied to every value of a ``{level: colour}`` map, for ``scale_fill_manual``."""
    return {k: shade(v, steps, mode, colourblind) for k, v in mapping.items()}
