from collections import OrderedDict
import logging
import pathlib
import pkg_resources
import subprocess

import babel.messages.pofile
import click


logger = logging.getLogger(__name__)

branding = OrderedDict()
branding["group"] = "collection"
branding["Group"] = "Collection"
branding["an organization"] = "a circle"
branding["an Organization"] = "a Circle"
branding["An organization"] = "A circle"
branding["An Organization"] = "A Circle"
branding["organization"] = "circle"
branding["Organization"] = "Circle"


preserve = [
    "organization_",
    "{organization}",
    "group_",
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
def dcor_theme_i18n_branding():
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
    dest.parent.mkdir(parents=True, exist_ok=True)
    # write .po file for en_US
    with dest.open("wb") as fd:
        babel.messages.pofile.write_po(fd, poin)
    with dest.open("rb") as fd:
        data = fd.readlines()
    data.insert(10, b'"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n')
    with dest.open("wb") as fd:
        fd.writelines(data)

    logger.info(f"Created PO file: {dest}")

    dest_mo = dest.with_suffix(".mo")

    # We cannot run setup.py compile_catalog, because we have no setup.py
    # The arguments for this call I extracted from ckan's setup.cfg.

    # generate custom .po file
    subprocess.check_output(
        f"pybabel compile "
        f"--domain=ckan "
        f"--directory={dest.parent} "
        f"--input-file={dest} "
        f"--output-file={dest_mo} "
        f"--locale=en_US "
        f"--use-fuzzy ",
        shell=True)

    logger.info(f"Created MO file: {dest_mo}")

    print("Make sure to set 'ckan.locale' and 'ckan.locales_offered' to "
          + "'en_US' in your CKAN config.")
