"""Map CKAN default colors to DCOR colors and generate dcor_theme_colors.css"""
import pathlib

import tinycss

#: Path to CKAN's main.css
main_css_path = "/usr/lib/ckan/default/src/ckan/ckan/public/base/css/main.css"

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
}


def rewrite_rule(rule):
    """Search for colors in `color_map`, return new css string list"""
    rule_css = []
    colordecs = []
    for dec in rule.declarations:
        val = dec.value.as_css()
        for cc in color_map:
            if cc in val:
                # replace css
                newval = val.replace(cc, color_map[cc])
                colordecs.append("{}: {};".format(dec.name, newval))
    rule_css += rule.selector.as_css().split("\n")
    rule_css.append("{")
    rule_css += ["  " + cd for cd in colordecs]
    rule_css.append("}")
    rule_css.append("")
    return rule_css


# Load CKAN main css
p = tinycss.make_parser("page3")
with open(main_css_path, "br") as fd:
    stylesheet = p.parse_stylesheet_bytes(fd.read())

#: List containing new css file (line-wise)
new_css = []

for rule in stylesheet.rules:  # loop over the rules
    if isinstance(rule, tinycss.css21.RuleSet):  # only deal with rule sets
        new_css += rewrite_rule(rule)
    else:
        # ignore @media (difficult to parse)
        pass

# save color information as new css file
here = pathlib.Path(__file__).parent
with open(here / "dcor_theme_colors.css", "w") as fd:
    for line in new_css:
        fd.write(line + "\n")
