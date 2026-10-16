"""Direct labels: name a line at its right-hand end instead of sending the reader to a legend."""
from __future__ import annotations

from plotnine import aes, geom_point, geom_text, scale_x_continuous, scale_y_continuous


def room(right: float = 0.18, left: float = 0.02, axis: str = "x", breaks=None):
    """Extra space around an axis so end labels fit inside the plot. ``right`` is a fraction of the data range.

    ``breaks`` sets the tick positions so no tick lands in the empty space. Add it like any scale. If you already set your own x scale, pass ``expand=(left, 0, right, 0)`` to it instead.
    """
    if axis not in ("x", "y"):
        raise ValueError("axis must be 'x' or 'y'")
    make = scale_x_continuous if axis == "x" else scale_y_continuous
    return make(expand=(left, 0, right, 0), breaks=breaks) if breaks is not None else make(expand=(left, 0, right, 0))


def end_labels(data, x: str, y: str, group: str, label: str | None = None, *, dot: bool = True,
               size: float = 3.4, text_size: float = 9, gap: float = 0.025, bold: bool | str = False, ink: bool = True):
    """Layers that put a dot and the group's name at the last point of each line.

    ``data`` is the DataFrame behind the plot, ``x``, ``y`` and ``group`` are column names (``x`` must be numeric).
    ``label`` is a column to print instead of the group name, for example ``"Netherlands  182.5 cm"``.
    The dots take the colour of the group. Label text is in the ink colour (``ink=True``) because pale colours fail as text; pass ``ink=False`` to colour it. Add
    :func:`room` so there is space to the right::

        ggplot(df, aes("year", "cm", colour="country")) + geom_line() + rv.end_labels(df, "year", "cm", "country") + rv.room()
    """
    last = data.loc[data.groupby(group, observed=True)[x].idxmax()]
    span = float(data[x].max() - data[x].min()) or 1.0
    layers = []
    if dot:
        layers.append(geom_point(aes(x=x, y=y, colour=group), data=last, size=size, show_legend=False))
    from .config import resolve
    from .palettes import get_palette
    mode, cb, _ = resolve(None, None, None)
    text_col = get_palette(mode, cb).neutrals["text"]
    mapping = aes(x=x, y=y, label=label or group) if ink else aes(x=x, y=y, label=label or group, colour=group)
    kw = dict(colour=text_col) if ink else {}
    layers.append(geom_text(mapping, data=last, ha="left", nudge_x=gap * span, size=text_size,
                            fontweight=("bold" if bold is True else bold) or "normal", show_legend=False, **kw))
    return layers
