"""The plotnine theme: theme_gray's structure, restyled as cream paper, navy ink, hairline grid and a serif title."""
from __future__ import annotations

from plotnine import element_blank, element_line, element_rect, element_text, theme, theme_gray

from .config import _STATE, pick_font, pick_serif, resolve
from .palettes import get_palette


class theme_roygbviz(theme_gray):
    """Roygbviz theme, built on plotnine's default ``theme_gray``.

    Parameters
    ----------
    mode : {"light", "dark", "cream"}, optional
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
    """

    def __init__(self, mode: str | None = None, colourblind: bool | None = None,
                 base_size: float = 11, base_family: str | None = None,
                 title_family: str | None = None, grid: str | None = None):
        mode, colourblind, _ = resolve(mode, colourblind)
        grid = _STATE["grid"] if grid is None else grid
        if grid not in ("y", "x", "xy", "none"):
            raise ValueError("grid must be 'y', 'x', 'xy' or 'none'")
        n = get_palette(mode, colourblind).neutrals
        body = base_family or pick_font()
        serif = title_family or pick_serif()
        line = element_line(color=n["grid"], size=0.7)
        super().__init__(base_size=base_size, base_family=body)
        self += theme(
            text=element_text(color=n["text"], family=body),
            plot_background=element_rect(fill=n["bg"], color="none"),
            panel_background=element_rect(fill=n["panel"], color="none"),
            panel_border=element_blank(),
            panel_grid_major=line,
            panel_grid_major_x=line if "x" in grid else element_blank(),
            panel_grid_major_y=line if "y" in grid else element_blank(),
            panel_grid_minor=element_blank(),
            axis_line_x=element_line(color=n["rule"], size=0.9),
            axis_line_y=element_blank(),
            axis_ticks=element_blank(),
            axis_text=element_text(color=n["muted"], size=base_size * 0.8),
            axis_title=element_text(color=n["text_2"], size=base_size * 0.85),
            legend_background=element_rect(fill=n["bg"], color="none"),
            legend_key=element_rect(fill="none", color="none"),
            legend_text=element_text(color=n["text_2"], size=base_size * 0.8),
            legend_title=element_text(color=n["muted"], size=base_size * 0.8),
            strip_background=element_blank(),
            strip_text=element_text(color=n["text"], size=base_size * 0.95, weight="bold", ha="left", family=serif),
            plot_title=element_text(color=n["text"], size=base_size * 1.6, weight="bold", ha="left", family=serif),
            plot_subtitle=element_text(color=n["text_2"], size=base_size * 0.95, ha="left"),
            plot_caption=element_text(color=n["muted"], size=base_size * 0.7, ha="left"),
            plot_title_position="plot",
            plot_caption_position="plot",
            plot_margin=0.035,
            panel_spacing=0.035,
        )
