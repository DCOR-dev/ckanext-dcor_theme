import os
import pathlib
import pkg_resources
import shutil
import subprocess
import babel.messages.pofile

import ckan
import click


branding = {
    "group": "collection",
    "Group": "Collection",
    "organization": "circle",
    "Organization": "Circle",
    "an organization": "a circle",
    "an Organization": "a Circle",
}

preserve = [
    "{organization}",
    "organization_name",
    "group_name",
    "{group}",
]


def replace_branding(msgid):
    if isinstance(msgid, tuple):
        return tuple([replace_branding(m) for m in list(msgid)])
    else:
        for pp in preserve:
            msgid = msgid.replace(pp, pp.upper())
        for bb in branding:
            msgid = msgid.replace(bb, branding[bb])
        for pp in preserve:
            msgid = msgid.replace(pp.upper(), pp)
        return msgid


@click.command()
def dcor_i18n_hack():
    src = pathlib.Path(pkg_resources.resource_filename("ckan.i18n",
                                                       "ckan.pot"))
    # load file and replace known strings
    with src.open("r", encoding="utf-8") as fd:
        poin = babel.messages.pofile.read_po(fd)

    for msg in poin:
        msg.string = replace_branding(msg.id)
    # file structure
    dest = src.parent / "en_US" / "LC_MESSAGES" / "ckan.po"
    # create parent directories
    parents = list(dest.parents)
    parents.reverse()
    for pp in parents:
        if not pp.exists():
            pp.mkdir()
    with dest.open("wb") as fd:
        babel.messages.pofile.write_po(fd, poin)

    with dest.open("rb") as fd:
        data = fd.readlines()
    data.insert(10, b'"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n')
    with dest.open("wb") as fd:
        data = fd.writelines(data)

    # for some reason we also need this .js file:
    sjs = pathlib.Path(
        pkg_resources.resource_filename("ckan", "public/base/i18n/en_GB.js"))
    shutil.copy(str(sjs), str(sjs.with_name("en_US.js")))

    # Readup:
    # https://docs.ckan.org/en/2.8/maintaining/configuration.html#config-i18n

    # generate custom .po file
    cpath = pathlib.Path(ckan.__file__).parent.parent
    os.chdir(str(cpath))
    subprocess.check_output(
        "python setup.py compile_catalog --locale en_US --use-fuzzy",
        shell=True)

    print("Make sure to set 'ckan.locale' and 'ckan.locales_offered' to "
          + "'en_US' in your CKAN config.")


def get_commands():
    return [dcor_i18n_hack]
