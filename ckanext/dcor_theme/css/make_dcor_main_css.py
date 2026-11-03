"""Map CKAN default colors to DCOR colors and generate dcor_theme_colors.css"""
from importlib import resources as importlib_resources
import pathlib
import re

#: Path to CKAN's main.css
ckan_css_path = pathlib.Path(str(
    importlib_resources.files("ckan") / "public" / "base" / "css"
    / "main.css"))

#: Dictionary mapping default colors to DCOR colors
color_map = {
    "#00232e": "#194484",
    "#003647": "#163868",
    "#005d7a": "#163868",
    "#206b82": "#2C55A4",  # btn-primary background and link
    "#1b5a6e": "#1f4d8d",  # btn-primary border
    "#020607": "#1f4d8d",  # btn-primary focus border
    "#164959": "#194493",  # btn-primary hover background
    "#0f323c": "#1f4d8d",  # btn-primary hover border
    "#113845": "#194484",  # pagination active
    "#647A82": "#5D7597",  # nav-item active (resources list in dataset)
    "#30778d": "#3366ac",  # a.tag hover
    "#235767": "#264c82",  # a.tag hover border
    "#3d97b3": "#315484",  # a.tag hover shadow
    "#1b5b6f": "#1B2E6F",  # a hover
    "#1a5668": "#1A3168",  # a hover border
    "#185062": "#181A62",  # a active
}


#: Regular expression for colors in `rgb(r, g, b)` notation
RGB_RE = re.compile(r"rgb\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\)")


def replace_colors(css_data):
    """Replace CKAN default colors with DCOR colors

    Since CKAN 2.11.7, `main.css` contains some colors in `rgb(r, g, b)`
    notation with floating point values instead of hex notation, e.g.
    `rgb(25.6, 85.6, 104)` instead of `#1a5668`. These are replaced as
    well if all channels are within 1 of a color in :const:`color_map`.
    If several colors match, the closest one is used.
    """
    for color in color_map:
        css_data = css_data.replace(color, color_map[color])

    rgb_map = {tuple(int(color[ii:ii + 2], 16) for ii in (1, 3, 5)): new
               for color, new in color_map.items()}

    def replace_rgb(match):
        rgb = [float(value) for value in match.groups()]
        candidates = []
        for key, new in rgb_map.items():
            diffs = [abs(a - b) for a, b in zip(rgb, key)]
            if max(diffs) <= 1:
                candidates.append((sum(d ** 2 for d in diffs), new))
        if candidates:
            return min(candidates)[1]
        return match.group(0)

    return RGB_RE.sub(replace_rgb, css_data)


def main():
    here = pathlib.Path(__file__).parent.resolve()
    # The webassets_dcor.yml file is already present in the public/base/css
    # directory (https://github.com/ckan/ckan/pull/6817).
    base_css = here.parent / "assets_theme"

    # Create a patched CSS file with the colors replaced.
    dcor_css_path = base_css / "dcor_main.css"

    # replace colors
    main_css_data = replace_colors(ckan_css_path.read_text())

    # add custom css inputs
    for ci in sorted(here.glob("*.css")):
        main_css_data += "\n"
        main_css_data += ci.read_text()

    dcor_css_path.write_text(main_css_data)

    print("Make sure to set 'ckan.theme=dcor_theme_main/dcor_theme_main' "
          + "in the CKAN ini config!")


if __name__ == "__main__":
    main()
