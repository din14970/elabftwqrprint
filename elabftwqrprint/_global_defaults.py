from pathlib import Path

import qrcode

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
VERSION = None
ERROR_CORRECTION = ERROR_CORRECT["M"]
BORDER = 4
BOX_SIZE = 10
PRINTSIZE = "29x90"
OUTPUT_PATH = str(Path("./qrcode.png"))
SHORT_TEXT = ""
LONG_TEXT = ""
FONT = "./Andale Mono.ttf"
FONT_SIZE = 18
