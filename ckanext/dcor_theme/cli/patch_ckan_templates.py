import logging
import pathlib

import ckan
import click


logger = logging.getLogger(__name__)


@click.command()
def dcor_patch_ckan_templates():
    """
    patch CKAN templates with minor changes that would be too complicated to
    implement with jinja templating
    """
    click.secho("Patching templates to improve resource listing")
    patch_wider_resource_listing()


def patch_wider_resource_listing():
    """Make sure the full filename is visible in the resource view"""
    ckan_path = pathlib.Path(ckan.__file__).parent

    # patch page to increase resource file listing width
    path_template_page = ckan_path / "templates/page.html"
    data_page = path_template_page.read_text()
    for old, new in [
        ('<aside class="secondary col-md-3">',
         '<aside class="secondary col-md-5">'),
        ('<div class="primary col-md-9 col-xs-12" role="main">',
         '<div class="primary col-md-7 col-xs-12" role="main">')
    ]:
        data_page = data_page.replace(old, new)
    path_template_page.write_text(data_page)

    # patch resource listing template, removing the truncate filter
    path_template_res = ckan_path / "templates/package/snippets/resources.html"
    data_res = path_template_res.read_text()
    data_res = data_res.replace("|truncate(25)", "")
    path_template_res.write_text(data_res)
