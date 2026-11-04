"""Tests for plugin.py."""
import re

import pytest

import ckanext.dcor_theme.plugin as plugin  # noqa: F401


class BlueprintChecker:
    def add_url_rule(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_plugin_get_blueprint():
    p = plugin.DCORThemePlugin()
    blueprint = p.get_blueprint()
    funcs = blueprint.deferred_functions
    endpoints = []
    for func in funcs:
        checker = BlueprintChecker()
        func(checker)
        endpoints.append(checker.args[1])
    assert "contact" in endpoints
    assert "imprint" in endpoints
    assert "privacy" in endpoints


def test_plugin_get_commands():
    p = plugin.DCORThemePlugin()
    names = [c.name for c in p.get_commands()]
    assert names == ["dcor-patch-ckan-templates",
                     "dcor-theme-i18n-branding",
                     "dcor-theme-main-css-branding"]


@pytest.mark.ckan_config('ckan.plugins', 'dcor_theme')
@pytest.mark.usefixtures('with_plugins')
@pytest.mark.parametrize("page,title", [
    ("contact", "Contact"),
    ("imprint", "Imprint"),
    ("privacy", "Privacy"),
])
def test_plugin_pages(app, page, title):
    resp = app.get(f"/{page}")
    assert resp.status_code == 200
    assert re.search(rf"<title>\s*{title}", resp.body)
