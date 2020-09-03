ckanext-dcor_theme
==================

The CKAN theme of DCOR. What this plugin does:


- remove the language selection from footer.html
- remove links from footer.html
- set the title of the page to "DCOR"
- insert a custom about text
- hide action buttons (Fullscreen, Embed) in resource view via css
- use i18n to change the terms "Organization" -> "Circle",
  "Group" -> "Collection", etc.

  .. code::

     ckan -c /etc/ckan/default/ckan.ini dcor-i18n-hack



Installation
------------

::

    pip install ckanext-dcor_theme

Edit ckan.ini
```
ckan.plugins = [...] dcor_theme
ckan.favicon = /base/images/favicon.ico
```
and run the dcor-i18n-hack command above.

Then, edit ckan.ini again:
```
ckan.locale_default = en_US
```
