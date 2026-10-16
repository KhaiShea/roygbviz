"""Active defaults. ``roygbviz.use()`` sets them; everything else reads them when no argument is given."""
from __future__ import annotations

from functools import lru_cache

_STATE = {"mode": "light", "colourblind": False, "order": "series", "grid": "y", "base_size": 11.0}


def resolve(mode: str | None = None, colourblind: bool | None = None, order: str | None = None):
    """Fill in anything left as None from the active defaults."""
    return (
        _STATE["mode"] if mode is None else mode,
        _STATE["colourblind"] if colourblind is None else colourblind,
        _STATE["order"] if order is None else order,
    )


def _first_installed(names: tuple[str, ...], fallback: str) -> str:
    """First font in ``names`` that matplotlib can actually draw (static TrueType or OpenType, not Type 1)."""
    from matplotlib import font_manager as fm

    for name in names:
        try:
            path = fm.findfont(name, fallback_to_default=False)
        except ValueError:
            continue
        if path.lower().endswith((".ttf", ".otf", ".ttc")):
            return name
    return fallback


@lru_cache(maxsize=1)
def pick_font() -> str:
    """Body font: first installed from a friendly fallback chain, so matplotlib never warns about a missing one."""
    return _first_installed(("Inter", "Helvetica Neue", "Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"),
                            "DejaVu Sans")


@lru_cache(maxsize=1)
def pick_serif() -> str:
    """Title font: an editorial serif if one is installed."""
    return _first_installed(("Source Serif 4", "Georgia", "Iowan Old Style", "Palatino", "TeX Gyre Pagella",
                             "Caladea", "Liberation Serif", "DejaVu Serif"), "DejaVu Serif")
