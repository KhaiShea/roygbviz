"""Roygbviz colour data: nine muted hues (ROYGBIV plus teal and pink), neutrals and ramps, in light and dark."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from . import _colour as C

ROLES: tuple[str, ...] = ("red", "orange", "yellow", "green", "teal", "blue", "indigo", "violet", "pink")
"""The nine hues in rainbow order."""

LEVEL_STEP = 0.09
"""Lightness step (OKLCH L) between neighbouring levels of one colour."""

DEFAULT_LEVEL = {"light": 0, "dark": 0}
"""Where the default colour sits among the levels: the middle one, in both modes. Change a value (for example -1 for
light) to move the default one level deeper or lighter; ``levels()`` follows."""

# --- twelve colours from one rainbow -----------------------------------------------------------------
# After Kate Morley's 12-bit rainbow (iamkate.com/data/12-bit-rainbow): twelve hues evenly spaced round the wheel
# (30 degrees apart, offset so the first hue is coral-crimson), near-constant chroma, and
# lightness that rises smoothly to a peak at yellow so yellow still reads as yellow. Tone and saturation match the
# earlier muted nine (mean chroma 0.13, mean lightness 0.67). Small per-hue lightness and chroma nudges lift the
# worst neighbouring pair from about 7 to about 11 (OKLab x100). Nine of the twelve are model colours and three
# are the stage colours (STT, LLM, TTS), so a stage and a model never share a hue.
_COLOURS: dict[tuple[str, str], dict[str, str]] = {
    ("standard", "light"): dict(red="#C46246", orange="#E69D49", yellow="#F1DE8A", green="#46CB87", teal="#00AEA3", blue="#0089A2", indigo="#626ACE", violet="#7844A3", pink="#B365A0"),
    ("standard", "dark"): dict(red="#CC6749", orange="#E69D49", yellow="#F3DE83", green="#47CB87", teal="#13B0A6", blue="#008DA7", indigo="#6C75D9", violet="#834FAF", pink="#B2679F"),
}

# --- stage (group) colours -------------------------------------------------------------------------
# For top-level STT / LLM / TTS comparisons: crimson, lime and deep blue from the same rainbow. Each stage leads a block of four
# neighbouring hues: STT with red, orange, yellow; LLM with green, teal, blue; TTS with indigo, violet, pink.
GROUPS: tuple[str, ...] = ("STT", "LLM", "TTS")
_GROUPS: dict[str, dict[str, str]] = {
    "light": dict(STT="#AC3E5C", LLM="#ABD865", TTS="#0062A1"),
    "dark": dict(STT="#AC415D", LLM="#ACD768", TTS="#006AAE"),
}

# Series order: the order model colours are handed out in plots. Each new colour is the one furthest from those
# already used, so any first-k set is as distinct as the nine allow. Shared by light and dark. "rainbow" is ROYGBIV.
_SERIES_ORDER: tuple[str, ...] = ("red", "yellow", "teal", "violet", "orange", "pink", "blue", "green", "indigo")

DIVERGING_MID: dict[str, str] = {"light": "#FFFFFF", "dark": "#F3EEE3"}
"""The zero point of the diverging ramp: white on cream paper, and the cream-white ink colour in dark mode."""

# --- neutrals (cream paper and navy ink; dark mode swaps them) ---------------------------------------
_NEUTRALS: dict[str, dict[str, str]] = {
    "light": dict(bg="#FAF6EF", panel="#FAF6EF", grid="#E9E2D4", grid_minor="#F1EBDF", strip="#EFE8D9",
                  rule="#C9C1B0", tick="#756F61", muted="#756F61", text_2="#4D5466", text="#1B2A41",
                  grey="#8E897C", mid="#ECE6D8"),
    "dark": dict(bg="#141A29", panel="#141A29", grid="#232B40", grid_minor="#1B2235", strip="#1D2538",
                 rule="#3A4560", tick="#9AA1B3", muted="#9AA1B3", text_2="#C4C0B3", text="#F3EEE3",
                 grey="#8A90A0", mid="#2E3441"),
}

# --- ramps ----------------------------------------------------------------------------------------
_SPECTRUM = {  # (s, L, C, h) from the surface-like end (s=0) to the emphasis end (s=1)
    "light": [(0.0, 0.955, 0.030, 95), (0.2, 0.890, 0.090, 95), (0.4, 0.800, 0.120, 65),
              (0.6, 0.660, 0.140, 25), (0.8, 0.500, 0.130, 335), (1.0, 0.330, 0.110, 275)],
    "dark": [(0.0, 0.250, 0.060, 275), (0.2, 0.370, 0.110, 295), (0.4, 0.500, 0.130, 340),
             (0.6, 0.640, 0.140, 25), (0.8, 0.790, 0.120, 70), (1.0, 0.930, 0.100, 100)],
}


def _shift(hex_: str, steps: float, span: int = 3) -> str:
    """Move a colour ``steps`` levels lighter (positive) or deeper (negative), keeping its hue.

    A step is ``LEVEL_STEP`` of lightness, but never more than ``1/span`` of the room left before near-white (0.96) or
    near-black (0.22) divided over ``span`` steps, so a pale colour like yellow still gets distinct soft levels instead of clipping.
    """
    L, c, h = C.to_oklch(hex_)
    room = (0.96 - L) if steps > 0 else (L - 0.22)
    step = min(LEVEL_STEP, room / span)
    c *= 0.92 ** steps if steps > 0 else 0.97 ** -steps
    return C.oklch_to_hex(L + steps * step if steps > 0 else L - (-steps) * step, c, h)


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _hue_lerp(a: float, b: float, t: float) -> float:
    d = ((b - a + 180) % 360) - 180
    return (a + d * t) % 360


def _check_mode(mode: str) -> str:
    if mode not in ("light", "dark"):
        raise ValueError(f"mode must be 'light' or 'dark', not {mode!r}")
    return mode


@dataclass(frozen=True)
class Palette:
    """Every colour for one mode and one vision family."""

    mode: str
    colourblind: bool
    roles: dict[str, str]
    neutrals: dict[str, str]

    @property
    def groups(self) -> dict[str, str]:
        """The three stage colours for top-level comparisons: ``{"STT": ..., "LLM": ..., "TTS": ...}``."""
        return {k: _shift(v, DEFAULT_LEVEL[self.mode]) if DEFAULT_LEVEL[self.mode] else v for k, v in _GROUPS[self.mode].items()}

    # ---- categorical ----
    def levels(self, role: str, n: int = 5) -> list[str]:
        """``n`` (3, 5 or 7) lightness levels of one colour, deepest first. The default colour is the middle one.

        With ``n=7`` the softest levels of pale colours (yellow) can clip at near-white, so prefer 3 or 5."""
        base = self.roles.get(role) or self.groups.get(role)
        if base is None:
            raise ValueError(f"role must be one of {ROLES + GROUPS}")
        if n not in (3, 5, 7):
            raise ValueError("n must be 3, 5 or 7")
        idx = n // 2 - DEFAULT_LEVEL[self.mode]  # the default sits at index n // 2 unless DEFAULT_LEVEL moves it
        up, down = max(3, n - 1 - idx), max(3, idx)
        return [_shift(base, k, up if k > 0 else down) if k else base for k in range(-idx, n - idx)]

    def series(self, n: int | None = None, order: str = "series", level: int = 0) -> list[str]:
        """Colours in hand-out order. ``order="series"`` is the validated order, ``"rainbow"`` is ROYGBIV.

        ``level`` shifts every colour lighter (positive) or deeper (negative) by that many steps, for example
        ``level=-1`` for thin lines that need more contrast.
        """
        if order == "rainbow":
            names: Sequence[str] = ROLES
        elif order == "series":
            names = _SERIES_ORDER
        else:
            raise ValueError("order must be 'series' or 'rainbow'")
        cols = [_shift(self.roles[r], level) if level else self.roles[r] for r in names]
        return cols if n is None else cols[:n]

    def rainbow(self) -> list[str]:
        return self.series(order="rainbow")

    @property
    def surface(self) -> str:
        return self.neutrals["bg"]

    # ---- continuous ----
    def sequential(self, hue: str = "blue", n: int = 9) -> list[str]:
        """One-hue ramp, from the surface-like end to the emphasis end. ``hue="spectrum"`` gives a multi-hue ramp."""
        if hue == "spectrum":
            return self._spectrum(n)
        if hue not in self.roles:
            raise ValueError(f"hue must be one of {ROLES} or 'spectrum'")
        _, c_base, h = C.to_oklch(self.roles[hue])
        out = []
        for i in range(n):
            s = i / (n - 1)
            L = 0.935 - 0.635 * s if self.mode == "light" else 0.27 + 0.62 * s
            chroma = 1.05 * c_base * (min(1.0, 0.2 + 1.6 * s) if s <= 0.5 else 1.0 - 0.35 * (s - 0.5) / 0.5)
            out.append(C.oklch_to_hex(L, chroma, h))
        return out

    def _spectrum(self, n: int) -> list[str]:
        stops = _SPECTRUM[self.mode]
        out = []
        for i in range(n):
            s = i / (n - 1)
            k = max(j for j in range(len(stops) - 1) if stops[j][0] <= s or j == 0)
            (s0, L0, C0, h0), (s1, L1, C1, h1) = stops[k], stops[k + 1]
            t = (s - s0) / (s1 - s0)
            out.append(C.oklch_to_hex(_lerp(L0, L1, t), _lerp(C0, C1, t), _hue_lerp(h0, h1, t)))
        return out

    def diverging(self, n: int = 9) -> list[str]:
        """Cold to hot: +1 is the STT stage colour (crimson), 0 is white, -1 is the TTS stage colour (deep blue), with a straight gradient between.

        Returned cold to hot (index 0 is -1, the last is +1). ``n`` is forced odd so the midpoint is exactly white.
        """
        n += (n + 1) % 2
        cold, hot, mid = self.groups["TTS"], self.groups["STT"], DIVERGING_MID[self.mode]
        out = []
        for i in range(n):
            u = (i - (n - 1) / 2) / ((n - 1) / 2)  # -1 (cold) .. 1 (hot)
            if abs(u) < 1e-9:
                out.append(mid)
            else:
                out.append(C.mix(mid, hot if u > 0 else cold, abs(u)))
        return out


def get_palette(mode: str = "light", colourblind: bool = False) -> Palette:
    """Return the :class:`Palette` for a mode ('light' or 'dark').

    The colourblind-safe set is planned but not built yet, so ``colourblind=True`` raises for now.
    """
    _check_mode(mode)
    if colourblind:
        raise NotImplementedError("the colourblind-safe palette is not built yet; use colourblind=False")
    roles = {r: _shift(h, DEFAULT_LEVEL[mode]) if DEFAULT_LEVEL[mode] else h for r, h in _COLOURS[("standard", mode)].items()}
    return Palette(mode, False, roles, dict(_NEUTRALS[mode]))
