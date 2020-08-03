from pathlib import Path

import yaml

from . import _global_defaults as gconf

CONFIG_FILENAME = gconf.PRINT_CONFIG_FILENAME


def main():
    conf_path = Path.home().joinpath(gconf.CONFIG_FOLDER)
    conf_file = conf_path.joinpath(CONFIG_FILENAME)
    # create config path
    Path.mkdir(conf_path, exist_ok=True)

    # which server will you connect to?
    printer = input(
        "What printer model do you have? [QL-500, QL-550,"
        " QL-560, QL-570, QL-580N, QL-650TD, QL-700, QL-710W,"
        " QL-720NW, QL-800, QL-810W, QL-820NWB, QL-1050, "
        "QL-1060N]: "
    )
    backend = input(
        "What back-end will you use (i.e. how is the printer"
        "connected) [pyusb, network, linux_kernel]: "
    )
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
    red_label = input(
            "Do you use red tape (for QL-8xx and DK-22251 printers)? "
            "(default = no)(yes|[no])"
            )
    verired = red_label == "yes"
    info = {
        "printer": printer,
        "backend": backend,
        "identifyer": identifyer,
        "labelsize": labelsize,
        "red_tape": verired,
    }

    with conf_file.open("w") as f:
        yaml.dump(info, f)
    print(f"Successfully wrote out config file: {conf_file}")


if __name__ == "__main__":
    main()
