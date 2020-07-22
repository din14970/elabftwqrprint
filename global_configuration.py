import qrcode
from pathlib import Path
# type of error correction
error_correct = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}
CONFIG_FOLDER = "~/.elabftwqrprint"
VERSION = None
ERROR_CORRECTION = error_correct["M"]
BORDER = 4
BOX_SIZE = 10
PRINTSIZE = "29x90"
OUTPUT_PATH = str(Path("./qrcode.png"))
SHORT_TEXT = ""
LONG_TEXT = ""
FONT_SIZE = 18
