import yaml
import os
from . import _global_defaults as gconf
from pathlib import Path


def main():
    conf_path = os.path.expanduser(gconf.CONFIG_FOLDER)
    if not os.path.isdir(conf_path):
        os.mkdir(conf_path)
    # which server will you connect to?
    printer = input("What printer model do you have? [QL-500, QL-550,"
                    " QL-560, QL-570, QL-580N, QL-650TD, QL-700, QL-710W,"
                    " QL-720NW, QL-800, QL-810W, QL-820NWB, QL-1050, "
                    "QL-1060N]: ")
    backend = input("What back-end will you use (i.e. how is the printer"
                    "connected) [pyusb, network, linux_kernel]: ")
    identifyer = input(
            "What is your printer identifyer? This could be a network"
            " address like tcp://192.168.1.21:9100 or a device address "
            "like usb://0x04f9:0x2015/00M6z401370. (To find out the usb "
            "address, use `lsusb -v` and structure it as "
            "usb://<idVendor>:<idProduct>/<idSerial>.): "
            )
    labelsize = input(
            "What is the size of your labels? [12, 29, 38, 50, 54, 62, "
            "102, 17x54, 17x87, 23x23, 29x42, 29x90, 39x90, 39x48, 52x29, "
            "62x29, 62x100, 102x51, 102x152, d12, d24, d58]: "
            )
    info = {
            "printer": printer,
            "backend": backend,
            "identifyer": identifyer,
            "labelsize": labelsize
            }
    config_created = str(Path(conf_path+"/printerconfig.yaml"))
    with open(config_created, "w") as f:
        yaml.dump(info, f)
    print(f"Successfully wrote out config file {config_created}.")


if __name__ == "__main__":
    main()
