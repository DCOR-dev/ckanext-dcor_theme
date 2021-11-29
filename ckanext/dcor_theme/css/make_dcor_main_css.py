"""Map CKAN default colors to DCOR colors and generate dcor_theme_colors.css"""
import pathlib

#: Path to CKAN's main.css
ckan_css_path = pathlib.Path(
    "/usr/lib/ckan/default/src/ckan/ckan/public/base/css/main.css")

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
}


def main():
    # Notes:
    # - We have to edit webassets.yml: https://github.com/ckan/ckan/issues/6563
    # - We cannot use our own location, we have to use the same.

    # https://github.com/ckan/ckan/issues/6563
    webassets_path = ckan_css_path.with_name("webassets.yml")
    webassets_text = webassets_path.read_text()
    if not webassets_text.count("dcor_main"):
        webassets_text += "dcor_main:\n" \
                          + "  filters: cssrewrite\n" \
                          + "  output: base/%(version)s_dcor_main.css\n" \
                          + "  contents: dcor_main.css\n"
    webassets_path.write_text(webassets_text)

    dcor_css_path = ckan_css_path.with_name("dcor_main.css")
    here = pathlib.Path(__file__).parent

    # replace colors
    main_css_data = ckan_css_path.read_text()
    for color in color_map:
        main_css_data = main_css_data.replace(color, color_map[color])

    # add custom css inputs
    for ci in sorted(here.glob("*.css")):
        main_css_data += "\n"
        main_css_data += ci.read_text()

    dcor_css_path.write_text(main_css_data)

    print("Make sure to set 'ckan.main_css=/base/css/dcor_main.css' "
          + "in the CKAN ini config!")


if __name__ == "__main__":
    main()
