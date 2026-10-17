"""Check any list of colours against the same gates Roygbviz was built to pass."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import _colour as C
from .palettes import _family, get_palette

BAND = {"light": (0.43, 0.77), "dark": (0.48, 0.67)}  # OKLCH lightness band for categorical marks
CHROMA_FLOOR = 0.09   # slightly below the usual 0.10: this palette is deliberately muted
CVD_TARGET = 8.0      # protan / deutan, OKLab x100 (informational until the colourblind set is built)
NORMAL_FLOOR = 10.0   # normal vision, OKLab x100; twelve evenly spaced hues, worst pair about 10.5
CONTRAST_MIN = 3.0    # WCAG, mark against surface


@dataclass
class Report:
    lightness_ok: bool
    chroma_ok: bool
    cvd_min: float
    normal_min: float
    contrast_min: float
    low_contrast: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Hard gates: chroma and normal-vision separation. Lightness band, CVD and low contrast are reported only
        (the soft nine-colour set sits above the usual band, CVD is parked, and pale colours need labels or outlines)."""
        return self.chroma_ok and self.normal_min >= NORMAL_FLOOR

    def __str__(self) -> str:
        return (f"lightness band {'ok' if self.lightness_ok else 'outside (info)'} | chroma {'ok' if self.chroma_ok else 'FAIL'} | "
                f"CVD min {self.cvd_min:.1f} (info) | normal min {self.normal_min:.1f} (>= {NORMAL_FLOOR:g}) | "
                f"contrast min {self.contrast_min:.2f} (>= {CONTRAST_MIN:g})"
                + (f" | below 3:1: {', '.join(self.low_contrast)}" if self.low_contrast else ""))


def check(colours: list[str], mode: str = "light", surface: str | None = None, pairs: str = "all") -> Report:
    """Check ``colours`` (in the order they will be used) for a mode.

    ``pairs="all"`` (default) compares every pair, which is what nine colours on one chart need; ``"adjacent"`` only compares neighbours.
    """
    surface = surface or get_palette(mode).surface
    lo, hi = BAND[_family(mode)]
    lch = [C.to_oklch(c) for c in colours]
    n = len(colours)
    idx = [(i, j) for i in range(n) for j in range(i + 1, n)] if pairs == "all" else [(i, i + 1) for i in range(n - 1)]
    cvd = min(min(C.delta_e(colours[i], colours[j], k) for k in ("protan", "deutan")) for i, j in idx)
    nor = min(C.delta_e(colours[i], colours[j]) for i, j in idx)
    cons = [C.contrast(c, surface) for c in colours]
    return Report(
        lightness_ok=all(lo <= round(L, 3) <= hi for L, _, _ in lch),
        chroma_ok=all(c >= CHROMA_FLOOR for _, c, _ in lch),
        cvd_min=cvd, normal_min=nor, contrast_min=min(cons),
        low_contrast=[c for c, k in zip(colours, cons) if k < CONTRAST_MIN],
    )
