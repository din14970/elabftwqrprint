from pathlib import Path

import elabapy
import yaml

from tabulate import tabulate

from . import _global_defaults as gconf
from . import create_qr_sticker as main

conf_path = Path.home().joinpath(gconf.CONFIG_FOLDER)
configfile = conf_path.joinpath(gconf.CONFIG_FILENAME)

def initialize():
    try:
        with open(configfile) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception:
        print("Unable to find or open config file. Run configure_elabftw first.")
        return

    manager = elabapy.Manager(endpoint=config["endpoint"], token=config["token"])
    return manager


def list_items(category=None):
    manager = initialize()
    if manager:
        all_items = manager.get_all_items()
        table = [["ID", "Date", "Category", "Name"]]
        for i in all_items:
            if category is not None:
                if i["category"] != category:
                    continue
            table.append([i["id"], i["date"], i["category"], i["title"]])
        print(tabulate(table, headers="firstrow"))


def _get_domain_name():
    try:
        with open(configfile) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        domain = config["domain_name"]
    except Exception:
        print("Unable to find or open config file. Run configure_elabftw first.")
        return
    return domain


def make_qrcode_item(id_no, filename, **kwargs):
    manager = initialize()
    if not manager:
        return
    item = manager.get_item(id_no)
    servname = _get_domain_name()
    link = f"https://{servname}/database.php?mode=view&id={id_no}"
    short_desc = f"{item['date']} {item['title']}"
    print(f"Will create QR sticker for link {link} and title {short_desc}")
    sticker = main.create_qr_sticker_image(link, small_text=short_desc, **kwargs)
    sticker.save(filename)
