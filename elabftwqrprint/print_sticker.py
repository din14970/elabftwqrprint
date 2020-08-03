import argparse
from pathlib import Path
import subprocess
import sys

import yaml

from . import _cli_args as cli
from . import _global_defaults as gconf


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Path to the image file")
    parser = cli.add_args_print(parser)
    p = parser.parse_args()
    return p


def print_image(p):
    conf_path = Path.home().joinpath(gconf.CONFIG_FOLDER)
    print_config_file = conf_path.joinpath(gconf.PRINT_CONFIG_FILENAME)
    try:
        with open(print_config_file) as f:
            print_conf = yaml.load(f, Loader=yaml.FullLoader)
    except Exception:
        print("No printer settings found, run configure_printer first")
        sys.exit(1)
    if print_conf['red_tape']:
        redflag = "--red"
    else:
        redflag = ""
    print_command = (
        f"brother_ql -b {print_conf['backend']} -m "
        f"{print_conf['printer']} -p {print_conf['identifyer']} "
        f"print -l {print_conf['labelsize']} -r {p.rotate_print}"
        f" {redflag} {p.filename}"
    )
    try:
        subprocess.run(print_command, shell=True, check=True)
        print("The sticker was printed succesfully")
    except Exception as e:
        print(e)


def main():
    p = get_args_cli()
    print_image(p)


if __name__ == "__main__":
    main()
