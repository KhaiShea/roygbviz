import matplotlib

matplotlib.use("Agg")
import pandas as pd
import pytest
from plotnine import aes, geom_col, geom_line, ggplot

import roygbviz as rv


def _lines():
    d = pd.DataFrame({"x": [0, 1, 2] * 3, "y": [1, 2, 3, 2, 3, 4, 3, 4, 5], "g": list("aaabbbccc")})
    return d, ggplot(d, aes("x", "y", colour="g")) + geom_line()


@pytest.mark.parametrize("mode", ["light", "dark"])
def test_use_and_draw(mode, tmp_path):
    rv.use(mode)
    d, g = _lines()
    (g + rv.scale_colour_roygbviz_d() + rv.end_labels(d, "x", "y", "g") + rv.room()).save(
        tmp_path / "a.png", width=4, height=3, verbose=False)
    assert (tmp_path / "a.png").stat().st_size > 1000


def test_bundle_and_level(tmp_path):
    rv.use("light")
    d, g = _lines()
    (g + rv.roygbviz(level=-1)).save(tmp_path / "b.png", width=4, height=3, verbose=False)
    bars = ggplot(d, aes("g", "y", fill="g")) + geom_col() + rv.roygbviz(aesthetics="fill")
    bars.save(tmp_path / "c.png", width=4, height=3, verbose=False)


def test_colour_helpers():
    assert rv.colour("red", "light") == rv.get_palette("light").roles["red"]
    assert rv.colour("grey", "light").startswith("#")
    with pytest.raises(ValueError):
        rv.colour("brown")
    assert len(rv.levels("blue", 5, "dark")) == 5
    cm = rv.colour_map(["a", "b", "Other"], "light")
    assert cm["Other"] == rv.get_palette("light").neutrals["grey"] and cm["a"] != cm["b"]
    with pytest.raises(ValueError):
        rv.colour_map(list("abcdefghij"), "light")


def test_room_validates():
    with pytest.raises(ValueError):
        rv.room(axis="z")
