from .i18n_branding import dcor_theme_i18n_branding
from .main_css_branding import dcor_theme_main_css_branding
from .patch_ckan_templates import dcor_patch_ckan_templates


def get_commands():
    return [
        dcor_patch_ckan_templates,
        dcor_theme_i18n_branding,
        dcor_theme_main_css_branding,
        ]
