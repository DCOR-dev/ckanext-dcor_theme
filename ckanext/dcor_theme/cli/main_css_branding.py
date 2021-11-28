import click

from ..css import make_dcor_main_css


@click.command()
def dcor_theme_main_css_branding():
    make_dcor_main_css.main()
