import sys
import operator
import functools

import elabapy
from requests.exceptions import HTTPError

from tabulate import tabulate

from . import _global_defaults as gconf


def initialize(url=None, token=None, verify=True):
    if url is None:
        url = gconf.URL
    if token is None:
        token = gconf.TOKEN
    if verify:
        verify = gconf.VERIFY
    if url is None or token is None:
        print("Unable to find URL or token in config file"
              "Run 'configure_elabftw' first.")
        sys.exit(1)
    manager = elabapy.Manager(
            endpoint=gconf.get_endpoint(url),
            token=token,
            verify=verify,
            )
    try:
        manager.get_status()
    except HTTPError as e:
        print(e)
        sys.exit(1)
    return manager


def _filter_item_info(items,
                      columns=None,
                      category=None,
                      match_string=None,
                      mindate=None,
                      maxdate=None):
    if columns is not None:
        table = [list(columns)]
    else:
        table = []
    for i in items:
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
        if columns is not None:
            table.append([i[j] for j in columns])
        else:
            table.append(i)
    return table


def get_items(category=None, match_string=None, mindate=None, maxdate=None, **kwargs):
    manager = initialize(**kwargs)
    all_items = manager.get_all_items()
    return _filter_item_info(all_items,
                             category=category,
                             match_string=match_string,
                             mindate=mindate,
                             maxdate=maxdate,
            )


def list_items(category=None, match_string=None, mindate=None, maxdate=None,
               **kwargs):
    manager = initialize(**kwargs)
    all_items = manager.get_all_items()
    table = _filter_item_info(all_items,
                              columns=["id", "date", "category", "title"],
                              category=category,
                              match_string=match_string,
                              mindate=mindate,
                              maxdate=maxdate,
                              )
    print(tabulate(table, headers="firstrow"))


def get_item_ids(category=None, match_string=None, mindate=None, maxdate=None,
                 **kwargs):
    manager = initialize(**kwargs)
    all_items = manager.get_all_items()
    ids = _filter_item_info(all_items,
                            columns=["id"],
                            category=category,
                            match_string=match_string,
                            mindate=mindate,
                            maxdate=maxdate,
                            )[1:]
    return functools.reduce(operator.add, ids)


def _get_domain_name(url=None):
    if url is None:
        url = gconf.URL
    try:
        _, domain = url.split("://")
        return domain
    except Exception:
        print("Could not identify a valid URL. "
              "Run configure_elabftw first.")
        sys.exit(1)
