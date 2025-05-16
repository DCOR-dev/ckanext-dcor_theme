ckanext-dcor_theme
==================

|PyPI Version| |Build Status| |Coverage Status|

The CKAN theme of DCOR. What this plugin does:

- remove the language selection from footer.html
- remove links from footer.html
- set the title of the page to "DCOR"
- insert a custom about text
- remove social media buttons
- change icons / logo
- use i18n to change the terms "Organization" -> "Circle",
  "Group" -> "Collection", etc.::

     ckan dcor-theme-i18n-branding

- create a custom theme based on the default main.css file
  (hide action buttons (Fullscreen, Embed) in resource view via css,
  change colors) using::

    ckan dcor-theme-main-css-branding


Installation
------------

::

    pip install ckanext-dcor_theme

Edit ckan.ini::

    ckan.plugins = [...] dcor_theme

and run the dcor-i18n-hack command::

    ckan -c /etc/ckan/default/ckan.ini dcor-i18n-hack

Then, edit ckan.ini again::

    ckan.locale_default = en_US


Testing
-------
If CKAN/DCOR is installed and setup for testing, this extension can
be tested with pytest:

::

    pytest ckanext

Testing is implemented via GitHub Actions. You may also set up a local
docker container with CKAN and MinIO. Take a look at the GitHub Actions
workflow for more information.


.. |PyPI Version| image:: https://img.shields.io/pypi/v/ckanext.dcor_theme.svg
   :target: https://pypi.python.org/pypi/ckanext.dcor_theme
.. |Build Status| image:: https://img.shields.io/github/actions/workflow/status/DCOR-dev/ckanext-dcor_theme/check.yml
   :target: https://github.com/DCOR-dev/ckanext-dcor_theme/actions?query=workflow%3AChecks
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/DCOR-dev/ckanext-dcor_theme
   :target: https://codecov.io/gh/DCOR-dev/ckanext-dcor_theme
