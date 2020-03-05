import qrcode
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
import logging

#type of error correction
error_correct = {
    "L" : qrcode.constants.ERROR_CORRECT_L,
    "M" : qrcode.constants.ERROR_CORRECT_M,
    "Q" : qrcode.constants.ERROR_CORRECT_Q,
    "H" : qrcode.constants.ERROR_CORRECT_H,
}

#sticker size dictionary to correspond to brother_ql
sticker_sizes = {
    "12" : (106, None),
    "29" : (306, None),
    "38" : (413, None),
    "50" : (554, None),
    "54" : (590, None),
    "62" : (696, None),
    "102" : (1164, None),
    "17x54" : (165, 566),
    "17x87" :    (165,  956), #    17mm x 87mm die-cut
    "23x23" :    (202,  202), #    23mm x 23mm die-cut
    "29x42" :    (306,  425), #    29mm x 42mm die-cut
    "29x90" :    (306,  991), #    29mm x 90mm die-cut
    "39x90" :    (413,  991), #    38mm x 90mm die-cut
    "39x48" :    (425,  495), #    39mm x 48mm die-cut
    "52x29" :    (578,  271), #    52mm x 29mm die-cut
    "62x29" :    (696,  271), #    62mm x 29mm die-cut
    "62x100" :   (696, 1109), #    62mm x 100mm die-cut
    "102x51" :  (1164,  526), #    102mm x 51mm die-cut
    "102x152" : (1164, 1660), #    102mm x 153mm die-cut
    "d12" :       (94,   94), #    12mm round die-cut
    "d24" :      (236,  236), #    24mm round die-cut
    "d58" :      (618,  618), #    58mm round die-cut
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
    parser.add_argument("-p", "--printsize", type = str, choices = sticker_sizes.keys(),
                        help = "Sticker dimensions", default = "29x90")
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
    #create a white background image
    nh, nw = sticker_sizes[p.printsize]
    #if tape is endless then we cut a square
    if nw is None:
        nw = nh
    background = Image.new('1', (nw, nh), color=1) #one bit pixels
    #does the image fit on the sticker?
    w, h = img.size
    if w<=nw and h<=nh:
        pass
    else:
        #resize the image to the smallest dimension
        sf = min([nh/h, nw/w])
        img = img.resize((int(w*sf), int(h*sf)))
    # paste the new image into the background on 0,0
    background.paste(img)
    # save the image
    background.save(p.output)


if __name__ == "__main__":
    main()
