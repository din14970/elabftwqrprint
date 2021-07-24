from pathlib import Path
import warnings
import os
import yaml
import qrcode


def get_endpoint(URL):
    return f"{URL}/api/v1/"


folder = os.path.split(__file__)[0]
DEFAULT_FONT_PATH = os.path.join(folder, "defaultfont.ttf")

SUPPORTED_MODELS = ["QL-500",
                    "QL-550",
                    "QL-560",
                    "QL-570",
                    "QL-580N",
                    "QL-650TD",
                    "QL-700",
                    "QL-710W",
                    "QL-720NW",
                    "QL-800",
                    "QL-810W",
                    "QL-820NWB",
                    "QL-1050",
                    "QL-1060N",
                    ]

PRINTER_BACKENDS = ["pyusb", "network", "linux_kernel"]
PRINTER_ROTATE_OPTIONS = ["auto", "0", "90", "180", "270"]

STICKER_SIZES = {
    "12": (106, None),
    "29": (306, None),
    "38": (413, None),
    "50": (554, None),
    "54": (590, None),
    "62": (696, None),
    "102": (1164, None),
    "17x54": (165, 566),
    "17x87": (165, 956),  # 17mm x 87mm die-cut
    "23x23": (202, 202),  # 23mm x 23mm die-cut
    "29x42": (306, 425),  # 29mm x 42mm die-cut
    "29x90": (306, 991),  # 29mm x 90mm die-cut
    "39x90": (413, 991),  # 38mm x 90mm die-cut
    "39x48": (425, 495),  # 39mm x 48mm die-cut
    "52x29": (578, 271),  # 52mm x 29mm die-cut
    "62x29": (696, 271),  # 62mm x 29mm die-cut
    "62x100": (696, 1109),  # 62mm x 100mm die-cut
    "102x51": (1164, 526),  # 102mm x 51mm die-cut
    "102x152": (1164, 1660),  # 102mm x 153mm die-cut
    "d12": (94, 94),  # 12mm round die-cut
    "d24": (236, 236),  # 24mm round die-cut
    "d58": (618, 618),  # 58mm round die-cut
}
# type of error correction
ERROR_CORRECT = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}
CONFIG_FOLDER = ".elabftwqrprint"
CONFIG_FILENAME = "elabconfig.yaml"
PRINT_CONFIG_FILENAME = "printerconfig.yaml"
FORMAT_CONFIG_FILENAME = "formatting.yaml"

# mutable defaults - if they are in a config file it is read,
# otherwise a reasonable default is given
conf_path = Path.home().joinpath(CONFIG_FOLDER)

try:
    configfile = conf_path.joinpath(CONFIG_FILENAME)
    with open(configfile) as f:
        connection_config = yaml.load(f, Loader=yaml.FullLoader)
except Exception as e:
    warnings.warn(f"Could not load eLabFTW config file: {e}. If this is unintentional make sure you run the 'configure_elabftw' script.")
    connection_config = {}

URL = connection_config.get("url", None)
TOKEN = connection_config.get("token", None)
VERIFY = connection_config.get("verify", None)

try:
    print_conf_file = conf_path.joinpath(PRINT_CONFIG_FILENAME)
    with open(print_conf_file) as f:
        print_config = yaml.load(f, Loader=yaml.FullLoader)
except Exception as e:
    warnings.warn(f"Could not load printer config file: {e}. If this is unintentional make sure you run the 'configure_printer' script.")
    print_config = {}

PRINTER_TYPE = print_config.get("printer", None)
PRINTER_BACKEND = print_config.get("backend", None)
PRINTER_ID = print_config.get("identifyer", None)
PRINTSIZE = print_config.get("labelsize", "29x90")
PRINT_RED = print_config.get("red_tape", False)
ROTATE_PRINT = print_config.get("rotate_print", "auto")

try:
    format_config_file = conf_path.joinpath(FORMAT_CONFIG_FILENAME)
    with open(format_config_file) as f:
        format_config = yaml.load(f, Loader=yaml.FullLoader)
except Exception:
    format_config = {}

# Image saving defaults
DEFAULT_SAVE_NAME = format_config.get("default_save_name", "last_sticker.png")
DEFAULT_SAVE_LOCATION = Path(format_config.get("default_save_folder",
                                               conf_path))
DEFAULT_SAVE_PATH = Path.joinpath(DEFAULT_SAVE_LOCATION, DEFAULT_SAVE_NAME)

# QR code defaults
VERSION = format_config.get("version")
ERROR_CORRECTION = format_config.get("error_correction", ERROR_CORRECT["M"])
BORDER = format_config.get("border", 4)
BOX_SIZE = format_config.get("box_size", 10)
# sticker layout defaults
SHORT_TEXT = format_config.get("short_text", "")
LONG_TEXT = format_config.get("long_text", "")
FONT = format_config.get("font", DEFAULT_FONT_PATH)
FONT_SIZE = format_config.get("font_size", 18)
LONG_TEXT_WIDTH = format_config.get("long_text_width")
QR_SIZE = format_config.get("max_qr_size")
