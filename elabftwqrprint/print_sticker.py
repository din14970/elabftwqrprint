import argparse
import os
from . import _global_defaults as gconf
import yaml


def print_image(filename):
    conf_path = os.path.expanduser(gconf.CONFIG_FOLDER)
    if not os.path.isdir(conf_path):
        os.mkdir(conf_path)
    print_config_file = conf_path+"/printerconfig.yaml"
    try:
        with open(print_config_file) as f:
            print_conf = yaml.load(f)
    except Exception:
        print("No printer settings found, run configure_printer first")
        return
    print_command = (f"brother_ql -b {print_conf['backend']} -m "
                     f"{print_conf['printer']} -p {print_conf['identifyer']} "
                     f"print -l {print_conf['labelsize']} {filename}")
    os.system(print_command)
    print("The sticker was printed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str,
                        help="Path to the image file"
                        )
    p = parser.parse_args()
    print_image(p.filename)


if __name__ == "__main__":
    main()
