"""Tests for plugin.py."""
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
