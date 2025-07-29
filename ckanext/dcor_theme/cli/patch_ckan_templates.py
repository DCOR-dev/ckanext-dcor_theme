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

    # patch resource listing template
    path_template_res = ckan_path / "templates/package/snippets/resources.html"
    data_res = path_template_res.read_text()
    # This makes the browser force a line-break even inside a word,
    # which means that it breaks long filenames.
    st = 'style="word-wrap: break-word"'
    for old, new in [
        # remove the truncate filter for file names
        ("|truncate(25)", ""),
        # force word wrap of the file names
        ('<a href="',
         f'<a {st} href="'),
        ('<a class="flex-fill" href="',
         f'<a class="flex-fill" {st} href="'),
    ]:
        data_res = data_res.replace(old, new)
    path_template_res.write_text(data_res)
