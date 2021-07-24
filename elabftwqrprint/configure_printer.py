from pathlib import Path
import sys
import subprocess

import yaml

from . import _global_defaults as gconf
from . import utils as utls

CONFIG_FILENAME = gconf.PRINT_CONFIG_FILENAME


def main():
    conf_path = Path.home().joinpath(gconf.CONFIG_FOLDER)
    conf_file = conf_path.joinpath(CONFIG_FILENAME)
    # create config path
    Path.mkdir(conf_path, exist_ok=True)

    while True:
        while True:
            printer = input(
                f"What printer model do you have? {gconf.SUPPORTED_MODELS}: "
            )
            if printer not in gconf.SUPPORTED_MODELS:
                print("Unsupported model!")
            else:
                break

        while True:
            backend = input(
                "What back-end will you use (i.e. how is the printer"
                f"connected) (default = pyusb) {gconf.PRINTER_BACKENDS}: "
            )
            if backend == "":
                backend = "pyusb"
            if backend not in gconf.PRINTER_BACKENDS:
                print("Unsupported backend!")
            else:
                break

        identifyer = input(
            "What is your printer identifyer? This could be a network"
            " address like tcp://192.168.1.21:9100 or a device address "
            "like usb://0x04f9:0x2015/00M6z401370. (To find out the usb "
            "address, use `lsusb -v` and structure it as "
            "usb://<idVendor>:<idProduct>/<idSerial>.): "
        )

        while True:
            labelsize = input(
                f"What is the size of your labels? {list(gconf.STICKER_SIZES.keys())}: "
            )
            if labelsize not in gconf.STICKER_SIZES:
                print("Label size not recognized!")
            else:
                break

        while True:
            rotate_print = input(
                    f"Rotate images by this amount when you print (default = auto) {gconf.PRINTER_ROTATE_OPTIONS}: "
                    )
            if rotate_print == "":
                rotate_print = "auto"
            if rotate_print not in gconf.PRINTER_ROTATE_OPTIONS:
                print("Unsupported value")
            else:
                break

        verired = input(
                "Do you use red tape (for QL-8xx and DK-22251 printers)? (yes|[no]): "
                ) == "yes"

        info = {
            "printer": printer,
            "backend": backend,
            "identifyer": identifyer,
            "labelsize": labelsize,
            "rotate_print": rotate_print,
            "red_tape": verired,
        }

        testprint = input("Do you want to test the printer? ([yes]|no): " ) != "no"
        if testprint:
            sticker = utls.create_qr_sticker_image(
                "This is a test",
                labelsize,
                "This is a test",  # small_text
                "This is a test",  # long_text
                gconf.LONG_TEXT_WIDTH,  # long_text_width
                gconf.DEFAULT_FONT_PATH,  # font_path
                gconf.FONT_SIZE,  # font_size
                gconf.VERSION,  # "version":
                gconf.ERROR_CORRECTION,  # "error_correction":
                gconf.BOX_SIZE,  # "box_size":
                gconf.BORDER,  # "border":
                gconf.QR_SIZE,
            )
            # save the image
            sticker.save(gconf.DEFAULT_SAVE_PATH)
            if verired:
                redflag = "--red"
            else:
                redflag = ""
            print_command = (
                f"brother_ql -b {backend} -m "
                f"{printer} -p {identifyer} "
                f"print -l {labelsize} -r {rotate_print}"
                f" {redflag} {gconf.DEFAULT_SAVE_PATH}"
            )
            try:
                subprocess.run(print_command, shell=True, check=True)
                print("Printing seems to work!")
            except Exception as e:
                print("An error occured: ")
                print(e)
                redo = input("Do you want to enter a different configuration? ([yes]|no): ") != "no"
                if redo:
                    continue
                else:
                    print("Printer configuration was not successful.")
                    sys.exit(1)
        else:
            print("Configuration will be saved but is not guaranteed to work!")

        with conf_file.open("w") as f:
            yaml.dump(info, f)
        print(f"Successfully wrote out config file: {conf_file}")
        break


if __name__ == "__main__":
    main()
