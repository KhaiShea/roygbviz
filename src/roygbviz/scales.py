"""Colour and fill scales for plotnine, plus a one-call bundle."""
from __future__ import annotations

from functools import partial

from mizani.bounds import rescale_mid
from plotnine import (scale_colour_gradientn, scale_colour_manual, scale_fill_gradientn,
                      scale_fill_manual)

from .config import resolve
from .palettes import get_palette
from .theme import theme_roygbviz


def _p(mode, colourblind):
    mode, colourblind, _ = resolve(mode, colourblind)
    return get_palette(mode, colourblind)


# ---- categorical -----------------------------------------------------------------------------------
def scale_colour_roygbviz_d(mode=None, colourblind=None, order=None, level=0, **kwargs):
    """Discrete colour scale. Up to nine levels; fold the tail into "Other" or facet for more.

    ``level`` shifts all colours lighter (+) or deeper (-), e.g. ``level=-1`` for thin lines."""
    _, _, order = resolve(None, None, order)
    p = _p(mode, colourblind)
    kwargs.setdefault("na_value", p.neutrals["grey"])
    return scale_colour_manual(values=p.series(order=order, level=level), **kwargs)


def scale_fill_roygbviz_d(mode=None, colourblind=None, order=None, level=0, **kwargs):
    """Discrete fill scale. See :func:`scale_colour_roygbviz_d`."""
    _, _, order = resolve(None, None, order)
    p = _p(mode, colourblind)
    kwargs.setdefault("na_value", p.neutrals["grey"])
    return scale_fill_manual(values=p.series(order=order, level=level), **kwargs)


def scale_colour_roygbviz_groups(mode=None, colourblind=None, **kwargs):
    """Colour scale for the three stages: STT, LLM, TTS. Different in kind from the nine model colours."""
    return scale_colour_manual(values=_p(mode, colourblind).groups, **kwargs)


def scale_fill_roygbviz_groups(mode=None, colourblind=None, **kwargs):
    """Fill scale for the three stages: STT, LLM, TTS."""
    return scale_fill_manual(values=_p(mode, colourblind).groups, **kwargs)


# ---- sequential (magnitude) ------------------------------------------------------------------------
def scale_colour_roygbviz_c(hue="blue", mode=None, colourblind=None, n=9, **kwargs):
    """Sequential colour scale. ``hue`` is any of the nine colour names, ``"spectrum"`` for a multi-hue ramp."""
    p = _p(mode, colourblind)
    kwargs.setdefault("na_value", p.neutrals["grey"])
    return scale_colour_gradientn(colors=p.sequential(hue, n), **kwargs)


def scale_fill_roygbviz_c(hue="blue", mode=None, colourblind=None, n=9, **kwargs):
    """Sequential fill scale. See :func:`scale_colour_roygbviz_c`."""
    p = _p(mode, colourblind)
    kwargs.setdefault("na_value", p.neutrals["grey"])
    return scale_fill_gradientn(colors=p.sequential(hue, n), **kwargs)


# ---- diverging (polarity) --------------------------------------------------------------------------
def scale_colour_roygbviz_div(midpoint=0, mode=None, colourblind=None, n=9, **kwargs):
    """Diverging colour scale: cold to hot (indigo and blue, neutral, orange and red), centred on ``midpoint``."""
    p = _p(mode, colourblind)
    kwargs.setdefault("na_value", p.neutrals["grey"])
    return scale_colour_gradientn(colors=p.diverging(n), rescaler=partial(rescale_mid, mid=midpoint), **kwargs)


def scale_fill_roygbviz_div(midpoint=0, mode=None, colourblind=None, n=9, **kwargs):
    """Diverging fill scale. See :func:`scale_colour_roygbviz_div`."""
    p = _p(mode, colourblind)
    kwargs.setdefault("na_value", p.neutrals["grey"])
    return scale_fill_gradientn(colors=p.diverging(n), rescaler=partial(rescale_mid, mid=midpoint), **kwargs)


# US spellings, matching plotnine
scale_color_roygbviz_d = scale_colour_roygbviz_d
scale_color_roygbviz_c = scale_colour_roygbviz_c
scale_color_roygbviz_div = scale_colour_roygbviz_div


def roygbviz(mode=None, colourblind=None, order=None, level=0, aesthetics="colour", base_size=11, base_family=None,
             title_family=None, grid=None):
    """Theme plus discrete scales in one list: ``ggplot(...) + roygbviz("dark")``.

    ``aesthetics`` is ``"colour"`` (lines, points), ``"fill"`` (bars, areas) or ``"both"``. Only the scales you
    ask for are added, because plotnine warns about a scale whose aesthetic is not mapped.
    """
    wanted = {"colour": ("colour",), "color": ("colour",), "fill": ("fill",), "both": ("colour", "fill")}
    if aesthetics not in wanted:
        raise ValueError("aesthetics must be 'colour', 'fill' or 'both'")
    out = [theme_roygbviz(mode, colourblind, base_size, base_family, title_family, grid)]
    if "colour" in wanted[aesthetics]:
        out.append(scale_colour_roygbviz_d(mode, colourblind, order, level))
    if "fill" in wanted[aesthetics]:
        out.append(scale_fill_roygbviz_d(mode, colourblind, order, level))
    return out
