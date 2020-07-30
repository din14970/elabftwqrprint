import sys
from pathlib import Path

import elabapy
import yaml
from requests.exceptions import HTTPError

from . import _global_defaults as gconf

CONFIG_FILENAME = gconf.CONFIG_FILENAME

def main():
    conf_path = Path.home().joinpath(gconf.CONFIG_FOLDER)
    conf_file = conf_path.joinpath(CONFIG_FILENAME)

    # create config path
    Path.mkdir(conf_path, exist_ok=True)

    # ask info to user before creating the config file
    server = input(
        "Which elabFTW server will you connect to (e.g. elab.example.org)? "
    )
    token = input(
        "Enter your API access token (create one in user settings on website): "
    )
    verify = input(
        "Verify the certificate? (default: yes) ([yes]/no) "
    )
    veriflag = verify != "no"

    # test the connection
    urlapi = f"https://{server}/api/v1/"
    manager = elabapy.Manager(endpoint=urlapi, token=token, verify=veriflag)
    try:
        manager.get_items_types()
    except HTTPError as e:
        print(e)
        sys.exit(1)

    info = {"endpoint": urlapi, "token": token, "domain_name": server}
    with conf_file.open("w") as f:
        yaml.dump(info, f)
    print(f"Successfully connected, wrote out config file: {conf_file}")


if __name__ == "__main__":
    main()
