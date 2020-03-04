import qrcode
import argparse
from pathlib import Path
from PIL import Image


error_correct = {
    "L" : qrcode.constants.ERROR_CORRECT_L,
    "M" : qrcode.constants.ERROR_CORRECT_M,
    "Q" : qrcode.constants.ERROR_CORRECT_Q,
    "H" : qrcode.constants.ERROR_CORRECT_H,
}

def get_args_cli():

    parser = argparse.ArgumentParser()
    parser.add_argument("data", type = str,
                        help = "String to turn into QR code")
    parser.add_argument("-o", "--output", type = str,
                        help = "Path to output", default = str(Path("./qrcode.png")))
    parser.add_argument("-v", "--version", type = int,
                        help = "Size of QR code (1-40)", default = None)
    parser.add_argument("-e", "--error_correction", type = str, choices = ["L", "M", "Q", "H"],
                        help = "Error correction", default = "M")
    parser.add_argument("-s", "--box_size", type = int,
                        help = "Number of pixels each box of QR code is", default = 10)
    parser.add_argument("-b", "--border", type = int,
                        help = "Number of pixels the border should be", default = 4)
    return parser.parse_args()

def main():
    p = get_args_cli()
    extraparams = {
        "version":p.version,
        "error_correction": error_correct[p.error_correction],
        "box_size":p.box_size,
        "border":p.border,
    }
    qr = qrcode.QRCode(**extraparams)
    qr.add_data(p.data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(p.output)


if __name__ == "__main__":
    main()
