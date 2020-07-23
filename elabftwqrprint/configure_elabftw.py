import yaml
import elabapy
from requests.exceptions import HTTPError
import os
from . import _global_defaults as gconf
from pathlib import Path


def main():
    conf_path = os.path.expanduser(gconf.CONFIG_FOLDER)
    if not os.path.isdir(conf_path):
        os.mkdir(conf_path)
    # which server will you connect to?
    server = input("Which elabFTW server will you connect to (e.g. elab.exampl"
                   "e.org)? ")
    token = input("Enter your API access token (create one in user settings on"
                  " website): ")
    # test the connection
    urlapi = f"https://{server}/api/v1/"
    manager = elabapy.Manager(endpoint=urlapi, token=token)
    try:
        manager.get_items_types()
        success = True
    except HTTPError as e:
        print(e)
        success = False
    if success:
        info = {
                "endpoint": urlapi,
                "token": token,
                "domain_name": server
                }
        with open(str(Path(conf_path+"/elabconfig.yaml")), "w") as f:
            yaml.dump(info, f)
        print("Successfully connected, wrote out config file.")


if __name__ == "__main__":
    main()
