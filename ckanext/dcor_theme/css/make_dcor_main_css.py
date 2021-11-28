"""Map CKAN default colors to DCOR colors and generate dcor_theme_colors.css"""
import pathlib

#: Path to CKAN's main.css
ckan_css_path = "/usr/lib/ckan/default/src/ckan/ckan/public/base/css/main.css"

#: Dictionary mapping default colors to DCOR colors
color_map = {
    "#00232e": "#194484",
    "#003647": "#163868",
    "#005d7a": "#163868",
    "#206b82": "#2C55A4",  # btn-primary background and link
    "#1b5a6e": "#1f4d8d",  # btn-primary border
    "#164959": "#194493",  # btn-primary focus background
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
    here = pathlib.Path(__file__).parent
    dcor_css_path = here / "dcor_main.css"

    # replace colors
    main_css_data = pathlib.Path(ckan_css_path).read_text()
    for (old, new) in color_map:
        main_css_data = main_css_data.replace(old, new)

    # add custom css inputs
    css_inputs = sorted(here.glob("*.css"))
    css_inputs = [pp for pp in css_inputs if not pp.samefile(dcor_css_path)]
    for ci in css_inputs:
        main_css_data += "\n"
        main_css_data += ci.read_text()

    dcor_css_path.write_text(main_css_data)

    print(
        f"Make sure to set 'ckan.main_css = {dcor_css_path}' in CKAN config!")


if __name__ == "__main__":
    main()
