import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from flask import Blueprint, render_template

from .cli import get_commands


class DCORThemePlugin(p.SingletonPlugin):
    p.implements(p.IBlueprint, inherit=True)
    p.implements(p.IClick, inherit=True)
    p.implements(p.IConfigurer, inherit=True)

    # IBlueprint
    def get_blueprint(self):
        """Return a Flask Blueprint object to be registered by the app."""
        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)

        # Add plugin url rules to Blueprint object
        rules = [
            ('/contact', 'contact', lambda: render_template('contact.html')),
            ('/imprint', 'imprint', lambda: render_template('imprint.html')),
            ('/privacy', 'privacy', lambda: render_template('privacy.html')),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)
        return blueprint

    # IClick
    def get_commands(self):
        return get_commands()

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'dcor_theme')
        toolkit.add_resource('assets_theme', 'dcor_theme_main')
        # Add the custom theme directory to the public directories,
        # so CKAN can find the css file.
        toolkit.add_public_directory(config_, "assets_theme")
