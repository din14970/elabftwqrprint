from pathlib import Path
import os
import yaml
import qrcode


folder = os.path.split(__file__)[0]
default_font_path = os.path.join(folder, "defaultfont.ttf")

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
try:
    conf_path = Path.home().joinpath(CONFIG_FOLDER)
    print_conf_file = conf_path.joinpath(PRINT_CONFIG_FILENAME)
    with open(print_conf_file) as f:
        print_config = yaml.load(f, Loader=yaml.FullLoader)
except Exception:
    print_config = None
try:
    conf_path = Path.home().joinpath(CONFIG_FOLDER)
    format_config_file = conf_path.joinpath(FORMAT_CONFIG_FILENAME)
    with open(format_config_file) as f:
        format_config = yaml.load(f, Loader=yaml.FullLoader)
except Exception:
    format_config = None

# saving images
try:
    DEFAULT_SAVE_NAME = format_config["default_save_name"]
except Exception:
    DEFAULT_SAVE_NAME = "last_sticker.png"
try:
    DEFAULT_SAVE_LOCATION = Path(format_config["default_save_folder"])
except Exception:
    DEFAULT_SAVE_LOCATION = conf_path
# QR code defaults
try:
    VERSION = format_config["version"]
except Exception:
    VERSION = None
try:
    ERROR_CORRECTION = format_config["error_correction"]
except Exception:
    ERROR_CORRECTION = ERROR_CORRECT["M"]
try:
    BORDER = format_config["border"]
except Exception:
    BORDER = 4
try:
    BOX_SIZE = format_config["box_size"]
except Exception:
    BOX_SIZE = 10
# layout defaults
try:
    SHORT_TEXT = format_config["short_text"]
except Exception:
    SHORT_TEXT = ""
try:
    LONG_TEXT = format_config["long_text"]
except Exception:
    LONG_TEXT = ""
try:
    FONT = format_config["font"]
except Exception:
    FONT = default_font_path
try:
    FONT_SIZE = format_config["font_size"]
except Exception:
    FONT_SIZE = 18
try:
    LONG_TEXT_WIDTH = format_config["long_text_width"]
except Exception:
    LONG_TEXT_WIDTH = None
try:
    QR_SIZE = format_config["max_qr_size"]
except Exception:
    QR_SIZE = None

try:
    PRINTSIZE = print_config["labelsize"]
except Exception:
    PRINTSIZE = "29x90"
