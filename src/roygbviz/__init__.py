"""Roygbviz (roy-gee-bee-viz): a muted rainbow theme for Python data visualisation, built on plotnine."""
from . import _colour
from .check import Report, check
from .config import resolve as _resolve  # noqa: F401
from . import mpl
from .labels import end_labels, room
from .mpl import cmap, colour, colour_map, group_map, levels, shade, shade_map, stroke, use
from .palettes import ROLES, Palette, get_palette
from .scales import (roygbviz, scale_color_roygbviz_c, scale_color_roygbviz_d, scale_color_roygbviz_div,
                     scale_colour_roygbviz_c, scale_colour_roygbviz_d, scale_colour_roygbviz_groups, scale_fill_roygbviz_groups, scale_colour_roygbviz_div,
                     scale_fill_roygbviz_c, scale_fill_roygbviz_d, scale_fill_roygbviz_div)
from .theme import theme_roygbviz

__version__ = "0.1.0"
__all__ = [
    "ROLES", "Palette", "Report", "check", "cmap", "colour", "colour_map", "end_labels", "get_palette", "group_map", "levels", "shade", "shade_map", "stroke", "room",
    "roygbviz", "theme_roygbviz", "use",
    "scale_colour_roygbviz_d", "scale_fill_roygbviz_d", "scale_colour_roygbviz_c", "scale_fill_roygbviz_c",
    "scale_colour_roygbviz_div", "scale_fill_roygbviz_div", "scale_colour_roygbviz_groups", "scale_fill_roygbviz_groups",
    "scale_color_roygbviz_d", "scale_color_roygbviz_c", "scale_color_roygbviz_div",
]
