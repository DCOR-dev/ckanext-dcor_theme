import re

import pytest

from ckanext.dcor_theme.css import make_dcor_main_css as mdc


def hex_to_rgb(color):
    return tuple(int(color[ii:ii + 2], 16) for ii in (1, 3, 5))


@pytest.mark.parametrize("css,expected", [
    # hex notation (CKAN <= 2.11.6)
    ["color: #1a5668;", f"color: {mdc.color_map['#1a5668']};"],
    # rgb notation with floats (CKAN >= 2.11.7)
    ["color: rgb(25.6, 85.6, 104);", f"color: {mdc.color_map['#1a5668']};"],
    ["color: rgb(0, 34.6844262295, 45.5);",
     f"color: {mdc.color_map['#00232e']};"],
    # a channel exactly 0.5 off (110.5 vs. 111)
    ["color: rgb(27.2, 90.95, 110.5);", f"color: {mdc.color_map['#1b5b6f']};"],
    # other colors are not touched
    ["color: rgb(212.47, 62.50, 58.03);", "color: rgb(212.47, 62.50, 58.03);"],
    ["color: #d43f3a;", "color: #d43f3a;"],
])
def test_replace_colors(css, expected):
    assert mdc.replace_colors(css) == expected


def test_replace_colors_ckan_main_css():
    """No mapped CKAN color remains in the installed CKAN's main.css"""
    css = mdc.replace_colors(mdc.ckan_css_path.read_text())
    for color in mdc.color_map:
        assert color not in css
        ref = hex_to_rgb(color)
        for match in mdc.RGB_RE.finditer(css):
            rgb = [float(value) for value in match.groups()]
            assert not all(abs(a - b) <= 1 for a, b in zip(rgb, ref)), \
                f"{match.group(0)} ({color}) was not replaced"
    # the DCOR colors are there
    assert css.count(mdc.color_map["#1a5668"]) >= 9


def test_rgb_regexp():
    assert re.fullmatch(mdc.RGB_RE, "rgb(1, 2.5, 3)")
