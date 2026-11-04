import pathlib

import ckan
from ckan.cli.cli import ckan as ckan_cli
import pytest

from ckanext.dcor_theme.css import make_dcor_main_css as mdc


@pytest.mark.ckan_config('ckan.plugins', 'dcor_theme')
@pytest.mark.usefixtures('with_plugins')
def test_cli_main_css_branding(cli):
    result = cli.invoke(ckan_cli, ["dcor-theme-main-css-branding"])
    assert result.exit_code == 0, result.output
    path_css = (pathlib.Path(mdc.__file__).parent.parent
                / "assets_theme" / "dcor_main.css")
    assert path_css.exists()
    css = path_css.read_text()
    # the custom CSS files are appended
    css_theme = (pathlib.Path(mdc.__file__).parent
                 / "dcor_theme.css").read_text()
    assert css_theme in css
    # CKAN colors are replaced
    for color in mdc.color_map:
        assert color not in css


@pytest.mark.ckan_config('ckan.plugins', 'dcor_theme')
@pytest.mark.usefixtures('with_plugins')
def test_cli_patch_ckan_templates(cli):
    for _ in range(2):  # patching twice must not break anything
        result = cli.invoke(ckan_cli, ["dcor-patch-ckan-templates"])
        assert result.exit_code == 0, result.output
    path_templates = pathlib.Path(ckan.__file__).parent / "templates"
    res_item = (path_templates / "package" / "snippets"
                / "resource_item.html").read_text()
    assert "| truncate(50)" not in res_item
    assert 'style="overflow-wrap: break-word" class="heading"' in res_item
    resources = (path_templates / "package" / "snippets"
                 / "resources.html").read_text()
    assert "|truncate(25)" not in resources
    assert "overflow-wrap" in resources
