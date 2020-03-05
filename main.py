import qrcode
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
import logging

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
    parser.add_argument("-r", "--wpixels", type = int,
                        help = "Width in pixels of the saved image", default = 991)
    parser.add_argument("-c", "--hpixels", type = int,
                        help = "Height in pixels of the saved image", default = 306)
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

    #create custom pixel size by padding
    #first resize the image to the minimum dimension
    nw = p.wpixels
    nh = p.hpixels
    pix = np.array(img)
    h, w = pix.shape
    if w>nw and h<=nh:
        img = img.resize((nw, nw))
    elif h>nh and w<=nw:
        img = img.resize((nh, nh))
    elif h>nh and w>nw:
        if h/nh > w/nw:
            nd = nw
        else:
            nd = nh
        img = img.resize((nd, nd))
    else:
        pass #no resizing necessary
    #then make the resized image into an array
    pix = np.array(img, dtype="uint8")*255
    h, w = pix.shape
    #padd this array
    newpix = np.full((nh, nw), 255, dtype='uint8')
    newpix[0:h, 0:w]=pix
    img = Image.fromarray(newpix)

    img.save(p.output)


if __name__ == "__main__":
    main()
