from importlib import resources as importlib_resources
import pathlib

import pytest

from ckan.cli.cli import ckan as ckan_cli

from ckanext.dcor_theme.cli.i18n_branding import replace_branding


@pytest.mark.parametrize("msgid,expected", [
    ("Create an Organization", "Create a Circle"),
    ("organization", "circle"),
    ("Add to group", "Add to collection"),
    # placeholders and identifiers are preserved
    ("{organization} was deleted", "{organization} was deleted"),
    ("organization_id", "organization_id"),
    ("Group {group}", "Collection {group}"),
    # unrelated strings are not modified
    ("Dataset", "Dataset"),
    # plural forms
    (("organization", "organizations"), ("circle", "circles")),
])
def test_replace_branding(msgid, expected):
    assert replace_branding(msgid) == expected


@pytest.mark.ckan_config('ckan.plugins', 'dcor_theme')
@pytest.mark.usefixtures('with_plugins')
def test_cli_i18n_branding(cli):
    result = cli.invoke(ckan_cli, ["dcor-theme-i18n-branding"])
    assert result.exit_code == 0, result.output
    path_po = (pathlib.Path(str(importlib_resources.files("ckan.i18n")))
               / "en_US" / "LC_MESSAGES" / "ckan.po")
    assert path_po.exists()
    assert path_po.with_suffix(".mo").exists()
    data = path_po.read_text(encoding="utf-8")
    assert 'msgstr "Circle"' in data
    assert "Plural-Forms" in data
