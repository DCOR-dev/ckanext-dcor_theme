"""Map CKAN default colors to DCOR colors and generate dcor_theme_colors.css"""
import pkg_resources
import pathlib

#: Path to CKAN's main.css
ckan_css_path = pathlib.Path(
    pkg_resources.resource_filename("ckan", "public/base/css/main.css"))

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


def main():
    here = pathlib.Path(__file__).parent.resolve()
    # The webassets_dcor.yml file is already present in the public/base/css
    # directory (https://github.com/ckan/ckan/pull/6817).
    base_css = here.parent / "assets_theme"

    # Create a patched CSS file with the colors replaced.
    dcor_css_path = base_css / "dcor_main.css"

    # replace colors
    main_css_data = ckan_css_path.read_text()
    for color in color_map:
        main_css_data = main_css_data.replace(color, color_map[color])

    # add custom css inputs
    for ci in sorted(here.glob("*.css")):
        main_css_data += "\n"
        main_css_data += ci.read_text()

    dcor_css_path.write_text(main_css_data)

    print("Make sure to set 'ckan.theme=dcor_theme_main/dcor_theme_main' "
          + "in the CKAN ini config!")


if __name__ == "__main__":
    main()
