"""Small, dependency-free colour maths (OKLab/OKLCH, WCAG contrast, CVD simulation)."""
from __future__ import annotations

import math

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied in linear RGB.
_MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def _s2lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin2s(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_linear(hex_: str) -> tuple[float, float, float]:
    h = hex_.strip().lstrip("#")
    return tuple(_s2lin(int(h[i : i + 2], 16) / 255) for i in (0, 2, 4))  # type: ignore[return-value]


def linear_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#%02X%02X%02X" % tuple(round(_lin2s(c) * 255) for c in rgb)


def to_oklab(hex_: str, cvd: str | None = None) -> tuple[float, float, float]:
    r, g, b = hex_to_linear(hex_)
    if cvd:
        m = _MACHADO[cvd]
        r, g, b = (max(0.0, min(1.0, m[k][0] * r + m[k][1] * g + m[k][2] * b)) for k in range(3))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (
        0.2104542553 * l + 0.7936177850 * m_ - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m_ + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m_ - 0.8086757660 * s,
    )


def to_oklch(hex_: str) -> tuple[float, float, float]:
    L, a, b = to_oklab(hex_)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def _lab_to_linear(L: float, a: float, b: float) -> tuple[float, float, float]:
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_hex(L: float, C: float, h: float) -> str:
    """OKLCH to hex. Chroma is reduced (hue and lightness kept) until the colour fits sRGB."""
    hr = math.radians(h)

    def rgb(c: float):
        return _lab_to_linear(L, c * math.cos(hr), c * math.sin(hr))

    def fits(v) -> bool:
        return all(-1e-6 <= x <= 1 + 1e-6 for x in v)

    if not fits(rgb(C)):
        lo, hi = 0.0, C
        for _ in range(32):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if fits(rgb(mid)) else (lo, mid)
        C = lo
    return linear_to_hex(rgb(C))


def delta_e(a: str, b: str, cvd: str | None = None) -> float:
    """Euclidean distance in OKLab x100, optionally after simulating colour vision deficiency."""
    return 100 * math.dist(to_oklab(a, cvd), to_oklab(b, cvd))


def luminance(hex_: str) -> float:
    r, g, b = hex_to_linear(hex_)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def mix(a: str, b: str, t: float) -> str:
    """Interpolate two hex colours in OKLab."""
    la, lb = to_oklab(a), to_oklab(b)
    L, A, B = (x + (y - x) * t for x, y in zip(la, lb))
    return linear_to_hex(_lab_to_linear(L, A, B))
