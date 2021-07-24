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
    while True:
        server = input(
            "What is the URL to your eLab instance? (e.g. https://elab.example.org)? "
        )
        if not (server.startswith("https://") or server.startswith("http://")):
            print("Please enter a valid URL")
            continue
        token = input(
            "Enter your API access token (create one in user settings on the web interface): "
        )
        verify = input(
            "Verify the certificate when connecting? (default: yes) ([yes]/no) "
        )
        veriflag = verify != "no"

        # test the connection
        urlapi = gconf.get_endpoint(server)
        manager = elabapy.Manager(endpoint=urlapi, token=token, verify=veriflag)
        try:
            manager.get_status()
        except HTTPError as e:
            print("Could not connect to server: ")
            print(e)
            retry = input("Retry entering info? ([yes]/no)") != "no"
            if retry:
                continue
            else:
                sys.exit(1)

        info = {"token": token,
                "url": server,
                "verify": veriflag,
                }
        with conf_file.open("w") as f:
            yaml.dump(info, f)
        print(f"Successfully connected, wrote out config file: {conf_file}")
        break


if __name__ == "__main__":
    main()
