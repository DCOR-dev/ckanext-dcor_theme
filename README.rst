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

- create a new version of the main.css file using
  (hide action buttons (Fullscreen, Embed) in resource view via css,
  change colors)::

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

Testing can also be done via vagrant in a virtualmachine using the
`dcor-test <https://app.vagrantup.com/paulmueller/boxes/dcor-test/>` image.
Make sure that `vagrant` and `virtualbox` are installed and run the
following commands in the root of this repository:

::

    # Setup virtual machine using `Vagrantfile`
    vagrant up
    # Run the tests
    vagrant ssh -- sudo bash /testing/vagrant-run-tests.sh


.. |PyPI Version| image:: https://img.shields.io/pypi/v/ckanext.dcor_theme.svg
   :target: https://pypi.python.org/pypi/ckanext.dcor_theme
.. |Build Status| image:: https://img.shields.io/github/actions/workflow/status/DCOR-dev/ckanext-dcor_theme/check.yml
   :target: https://github.com/DCOR-dev/ckanext-dcor_theme/actions?query=workflow%3AChecks
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/DCOR-dev/ckanext-dcor_theme
   :target: https://codecov.io/gh/DCOR-dev/ckanext-dcor_theme
