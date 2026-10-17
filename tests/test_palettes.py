import pytest

import roygbviz as rv
from roygbviz import _colour as C
from roygbviz.palettes import _SERIES_ORDER

MODES = ("light", "dark", "cream")


@pytest.mark.parametrize("mode", MODES)
def test_nine_distinct_colours(mode):
    p = rv.get_palette(mode)
    assert list(p.roles) == list(rv.ROLES) and len(rv.ROLES) == 9
    cols = p.series()
    assert len(set(cols)) == 9
    assert rv.check(cols, mode, pairs="all").normal_min >= 10.0


@pytest.mark.parametrize("mode", MODES)
def test_series_order_is_a_permutation_shared_by_modes(mode):
    assert sorted(_SERIES_ORDER) == sorted(rv.ROLES)
    p = rv.get_palette(mode)
    assert p.series(order="rainbow") == [p.roles[r] for r in rv.ROLES]


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("role", rv.ROLES)
def test_levels_are_monotone_in_lightness(mode, role):
    p = rv.get_palette(mode)
    for n in (3, 5, 7):
        lv = p.levels(role, n)
        assert len(lv) == n and lv[n // 2] == p.roles[role]  # default is the middle level in both modes
        L = [C.to_oklch(h)[0] for h in lv]
        assert L == sorted(L)
        assert len(set(lv)) == n


def test_levels_validation():
    p = rv.get_palette()
    with pytest.raises(ValueError):
        p.levels("red", 4)
    with pytest.raises(ValueError):
        p.levels("brown")


def test_series_level_shifts_lightness():
    p = rv.get_palette()
    deep, base, soft = p.series(3, level=-1), p.series(3), p.series(3, level=1)
    for d, b, s in zip(deep, base, soft):
        assert C.to_oklch(d)[0] < C.to_oklch(b)[0] < C.to_oklch(s)[0]


@pytest.mark.parametrize("mode", MODES)
def test_sequential_ramps_monotone(mode):
    p = rv.get_palette(mode)
    for hue in ("blue", "violet", "green", "spectrum"):
        L = [C.to_oklch(h)[0] for h in p.sequential(hue, 9)]
        assert L == sorted(L) or L == sorted(L, reverse=True)
    assert len(p.diverging(9)) == 9 and len(p.diverging(8)) == 9  # forced odd


def test_colourblind_is_parked():
    with pytest.raises(NotImplementedError):
        rv.get_palette("light", colourblind=True)


def test_bad_mode():
    with pytest.raises(ValueError):
        rv.get_palette("sepia")


def test_text_contrast_on_surface():
    for mode in MODES:
        n = rv.get_palette(mode).neutrals
        assert C.contrast(n["text"], n["bg"]) >= 7
        assert C.contrast(n["muted"], n["bg"]) >= 4.5


@pytest.mark.parametrize("mode", MODES)
def test_stage_colours(mode):
    import itertools
    p = rv.get_palette(mode)
    g = p.groups
    assert set(g) == {"STT", "LLM", "TTS"}
    assert min(C.delta_e(a, b) for a, b in itertools.combinations(g.values(), 2)) >= 15
    assert rv.group_map(mode) == g


@pytest.mark.parametrize("mode", MODES)
def test_diverging_runs_cold_to_hot(mode):
    from roygbviz.palettes import DIVERGING_MID
    p = rv.get_palette(mode)
    div = p.diverging(9)
    assert div[0] == p.groups["TTS"] and div[-1] == p.groups["STT"]  # -1 TTS colour, +1 STT colour
    assert div[4] == DIVERGING_MID["dark" if mode == "dark" else "light"]                              # 0 is white
    L = [C.to_oklch(h)[0] for h in div]
    # lightness rises from the blue end to the white middle and falls to the red end
    assert all(a <= b + 1e-6 for a, b in zip(L[:5], L[1:5])) and all(a >= b - 1e-6 for a, b in zip(L[4:], L[5:]))
    assert C.to_oklch(div[4])[1] < 0.03


def test_shade_is_lighter_than_default():
    from roygbviz import _colour as C
    import roygbviz as rv
    rv.use("light")
    for name in ("red", "yellow", "blue", "STT", "LLM", "TTS"):
        base = rv.colour(name)
        assert C.to_oklch(rv.shade(name))[0] > C.to_oklch(base)[0]
    assert rv.shade("#336699") != "#336699"
    assert C.to_oklch(rv.shade("red", 2))[0] > C.to_oklch(rv.shade("red", 1))[0]
    m = rv.shade_map({"a": "red", "b": "teal"})
    assert set(m) == {"a", "b"}


def test_stroke_scales_with_base_size():
    import roygbviz as rv
    rv.use("light", base_size=11)
    assert rv.stroke(1.2) == 1.2
    rv.use("light", base_size=14)
    assert abs(rv.stroke(1.0) - 14 / 11) < 1e-9
    assert rv.stroke(1.0, base_size=9) < 1
    rv.use("light")


def test_light_is_white_and_cream_is_the_old_paper():
    assert rv.get_palette("light").neutrals["bg"] == "#FFFFFF"
    assert rv.get_palette("cream").neutrals["bg"] == "#FAF6EF"
    assert rv.get_palette("dark").neutrals["bg"] == "#141A29"


def test_light_and_cream_share_their_colours():
    a, b = rv.get_palette("light"), rv.get_palette("cream")
    assert a.roles == b.roles and a.groups == b.groups


def test_light_is_the_default_mode():
    import subprocess
    import sys

    out = subprocess.run([sys.executable, "-c", "import roygbviz as rv; from roygbviz.config import _STATE; print(_STATE['mode'])"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert out == "light"
