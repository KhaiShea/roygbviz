# API reference

Generated from the docstrings in the installed package. Import with `import roygbviz as rv`.

## `rv.use(mode: 'str' = 'light', colourblind: 'bool' = False, order: 'str' = 'series', plotnine: 'bool' = True, base_size: 'float' = 11, grid: 'str' = 'y')`

Make Roygbviz the default for the whole session: matplotlib rcParams, colormaps, and plotnine's theme.

``grid`` is ``"y"`` (horizontal hairlines, the default), ``"x"``, ``"xy"`` or ``"none"``.
Returns the active :class:`~roygbviz.palettes.Palette`.

## `rv.colour(role: 'str', mode=None, colourblind=None) -> 'str'`

One hex colour by name: ``"red"``, ``"orange"``, ``"yellow"``, ``"green"``, ``"teal"``, ``"blue"``,
``"indigo"``, ``"violet"``, ``"pink"``, a stage (``"STT"``, ``"LLM"``, ``"TTS"``), or ``"grey"`` for the neutral.

## `rv.colour_map(levels, mode=None, colourblind=None, order=None) -> 'dict'`

Pin each level to one colour so it looks the same in every figure: ``scale_colour_manual(values=colour_map(MODELS))``.

Up to nine levels. A level called ``"Other"`` gets the neutral grey and does not use up a colour.

## `rv.levels(role: 'str', n: 'int' = 5, mode=None, colourblind=None) -> 'list[str]'`

``n`` (3, 5 or 7) lightness levels of one colour, deepest first. Handy for stacked bars or one family of series.

## `rv.group_map(mode=None, colourblind=None) -> 'dict'`

The stage colours, ``{"STT": ..., "LLM": ..., "TTS": ...}``, for top-level comparisons.
Use with ``scale_fill_manual(values=rv.group_map())``, or the ``scale_*_roygbviz_groups`` scales.

## `rv.shade(colour: 'str', steps: 'int' = 1, mode=None, colourblind=None) -> 'str'`

The shading colour for a fill: ``steps`` levels lighter than ``colour`` (default one).

``colour`` is a role or stage name (``"blue"``, ``"STT"``) or any hex. Use it for areas, bands, ribbons and the
bodies of outlined marks, and keep the line or outline in the default colour, so the shade reads as the same
colour, one step softer::

    geom_area(fill=rv.shade("blue")) + geom_line(colour=rv.colour("blue"))

## `rv.shade_map(mapping: 'dict', steps: 'int' = 1, mode=None, colourblind=None) -> 'dict'`

:func:`shade` applied to every value of a ``{level: colour}`` map, for ``scale_fill_manual``.

## `rv.stroke(size: 'float' = 1.0, base_size: 'float | None' = None) -> 'float'`

Scale a line width or marker size with the text size, so a figure grows or shrinks as one.

``size`` is the width you would use at the default base size (11). ``base_size`` defaults to the one set by ``use()``.

## `rv.cmap(kind: 'str' = 'blue', mode=None, colourblind=None, n: 'int' = 256) -> 'LinearSegmentedColormap'`

Matplotlib colormap. ``kind``: a role name, ``"spectrum"``, or ``"diverging"``.

## `rv.end_labels(data, x: 'str', y: 'str', group: 'str', label: 'str | None' = None, *, dot: 'bool' = True, size: 'float' = 3.4, text_size: 'float' = 9, gap: 'float' = 0.025, bold: 'bool | str' = False, ink: 'bool' = True)`

Layers that put a dot and the group's name at the last point of each line.

``data`` is the DataFrame behind the plot, ``x``, ``y`` and ``group`` are column names (``x`` must be numeric).
``label`` is a column to print instead of the group name, for example ``"Netherlands  182.5 cm"``.
The dots take the colour of the group. Label text is in the ink colour (``ink=True``) because pale colours fail as text; pass ``ink=False`` to colour it. Add
:func:`room` so there is space to the right::

    ggplot(df, aes("year", "cm", colour="country")) + geom_line() + rv.end_labels(df, "year", "cm", "country") + rv.room()

## `rv.room(right: 'float' = 0.18, left: 'float' = 0.02, axis: 'str' = 'x', breaks=None)`

Extra space around an axis so end labels fit inside the plot. ``right`` is a fraction of the data range.

``breaks`` sets the tick positions so no tick lands in the empty space. Add it like any scale. If you already set your own x scale, pass ``expand=(left, 0, right, 0)`` to it instead.

## `rv.check(colours: 'list[str]', mode: 'str' = 'light', surface: 'str | None' = None, pairs: 'str' = 'all') -> 'Report'`

Check ``colours`` (in the order they will be used) for a mode.

``pairs="all"`` (default) compares every pair, which is what nine colours on one chart need; ``"adjacent"`` only compares neighbours.

## `rv.theme_roygbviz(mode: 'str | None' = None, colourblind: 'bool | None' = None, base_size: 'float' = 11, base_family: 'str | None' = None, title_family: 'str | None' = None, grid: 'str | None' = None)`

Roygbviz theme, built on plotnine's default ``theme_gray``.

Parameters
----------
mode : {"light", "dark"}, optional
    Defaults to whatever :func:`roygbviz.use` last set (``"light"`` if never called).
colourblind : bool, optional
    Only the neutrals matter to the theme, so this is here for symmetry with the scales.
base_size : float
    Body text size in points. Title, subtitle and ticks scale from it.
base_family, title_family : str, optional
    Body and title fonts. ``None`` picks Inter and an editorial serif (Source Serif, Georgia, Palatino, ...),
    whichever is installed first.
grid : {"y", "x", "xy", "none"}, optional
    Which hairline gridlines to draw. ``"y"`` (horizontal) is the default; use ``"xy"`` for scatter plots.

## `rv.roygbviz(mode=None, colourblind=None, order=None, level=0, aesthetics='colour', base_size=11, base_family=None, title_family=None, grid=None)`

Theme plus discrete scales in one list: ``ggplot(...) + roygbviz("dark")``.

``aesthetics`` is ``"colour"`` (lines, points), ``"fill"`` (bars, areas) or ``"both"``. Only the scales you
ask for are added, because plotnine warns about a scale whose aesthetic is not mapped.

## `rv.scale_colour_roygbviz_d(mode=None, colourblind=None, order=None, level=0, **kwargs)`

Discrete colour scale. Up to nine levels; fold the tail into "Other" or facet for more.

``level`` shifts all colours lighter (+) or deeper (-), e.g. ``level=-1`` for thin lines.

## `rv.scale_fill_roygbviz_d(mode=None, colourblind=None, order=None, level=0, **kwargs)`

Discrete fill scale. See :func:`scale_colour_roygbviz_d`.

## `rv.scale_colour_roygbviz_c(hue='blue', mode=None, colourblind=None, n=9, **kwargs)`

Sequential colour scale. ``hue`` is any of the nine colour names, ``"spectrum"`` for a multi-hue ramp.

## `rv.scale_fill_roygbviz_c(hue='blue', mode=None, colourblind=None, n=9, **kwargs)`

Sequential fill scale. See :func:`scale_colour_roygbviz_c`.

## `rv.scale_colour_roygbviz_div(midpoint=0, mode=None, colourblind=None, n=9, **kwargs)`

Diverging colour scale: cold to hot (indigo and blue, neutral, orange and red), centred on ``midpoint``.

## `rv.scale_fill_roygbviz_div(midpoint=0, mode=None, colourblind=None, n=9, **kwargs)`

Diverging fill scale. See :func:`scale_colour_roygbviz_div`.

## `rv.scale_colour_roygbviz_groups(mode=None, colourblind=None, **kwargs)`

Colour scale for the three stages: STT, LLM, TTS. Different in kind from the nine model colours.

## `rv.scale_fill_roygbviz_groups(mode=None, colourblind=None, **kwargs)`

Fill scale for the three stages: STT, LLM, TTS.

**Back to the [home page](index.md).**
