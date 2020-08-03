from pathlib import Path
import sys

import elabapy
from requests.exceptions import HTTPError
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
        print("Unable to find or open config file. "
              "Run configure_elabftw first.")
        sys.exit(1)
    manager = elabapy.Manager(
            endpoint=config["endpoint"],
            token=config["token"])
    try:
        manager.get_items_types()
    except HTTPError as e:
        print(e)
        sys.exit(1)
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
    except Exception:
        print("Unable to find or open config file. "
              "Run configure_elabftw first.")
        sys.exit(1)
    try:
        domain = config["domain_name"]
    except Exception as e:
        print(e)
        sys.exit(1)
    return domain
