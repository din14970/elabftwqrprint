from pathlib import Path
import sys

import elabapy
from requests.exceptions import HTTPError
import yaml

from tabulate import tabulate

from . import _global_defaults as gconf

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


def list_items(category=None, match_string=None, mindate=None, maxdate=None):
    manager = initialize()
    all_items = manager.get_all_items()
    table = [["ID", "Date", "Category", "Name"]]
    for i in all_items:
        if category is not None:
            if i["category"] != category:
                continue
        if match_string is not None:
            if match_string not in i["title"]:
                continue
        if mindate is not None:
            if int(i["date"]) < mindate:
                continue
        if maxdate is not None:
            if int(i["date"]) > maxdate:
                continue
        table.append([i["id"], i["date"], i["category"], i["title"]])
    print(tabulate(table, headers="firstrow"))


def get_item_ids(category=None, match_string=None, mindate=None, maxdate=None):
    manager = initialize()
    all_items = manager.get_all_items()
    ids = []
    for i in all_items:
        if category is not None:
            if i["category"] != category:
                continue
        if match_string is not None:
            if match_string not in i["title"]:
                continue
        if mindate is not None:
            if int(i["date"]) < mindate:
                continue
        if maxdate is not None:
            if int(i["date"]) > maxdate:
                continue
        ids.append(i["id"])
    return ids


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
