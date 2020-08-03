import argparse
import logging
import textwrap
import warnings
import sys

from PIL import Image, ImageDraw, ImageFont

import qrcode

from . import _global_defaults as gconf
from . import _cli_args as cli

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
        "%(levelname)s:%(name)s:%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "data",
            type=str,
            help="Text to encode in the QR code")
    parser = cli.add_args_sticker_basic_content(parser)
    parser = cli.add_args_sticker_layout(parser)
    parser = cli.add_output_args(parser)
    p = parser.parse_args()
    if p.no_short_text:
        p.short = ""
    return p


def create_qr_sticker_image(
    data,
    size,
    small_text,
    long_text,
    long_text_width,
    font_path,
    font_size,
    version,
    error_correction,
    box_size,
    border,
    max_qr_size,
    rotate,
):
    """
    Create an image with a QR code and some text

    Parameters
    ----------
    data: str
        The text to encode in the QR code
    size: str
        String encoding the size of the label
        Options: "12", "29", "38", "50", "54", "62", "102",
        "17x54", "17x87", "23x23", "29x42", "29x90", "39x90", "39x48",
        "52x29", "62x29", "62x100", "102x51", "102x152",
        "d12", "d24", "d58"
    small_text: str
        Short string to write below QR code, like
        a sample name
    long_text: str
        Long string to write next to QR code, like a
        description. Will only be used if sticker size
        allows for it
    long_text_width: int
        Width of the long text string in pixels. If it is larger
        than the sticker width, the sticker width will be chosen.
        If none is provided, the full sticker size will be chosen.
    font_path: str
        Path to a font file
    font_size: int
        font size of the long and short text.
    version: int
        Integer from 1-40 that controls number of boxes in the
        QR code. 1 = 21x21. If non, the optimum will be chosen.
    error_correction: str
        Type of error correction to use. Options are L, M, Q, H.
    box_size: int
        How many pixels are in each box
    border: int
        How many boxes does the border consist of.
    max_qr_size: int
        Final max size of qr code in pixels. If None, the best
        fit will be calculated.
    rotate: bool
        whether to rotate the final image by 90 degrees, beyond
        automatic rotation

    Returns
    -------
    image: PIL.Image.Image
        The image object to be written to a file
    """
    nh, nw = gconf.STICKER_SIZES[size]
    logger.debug(f"Sticker size: height {nh} px, width {nw} px")
    # detect whether the image is best rotated 90 degrees
    swapped = False
    # detect the size we need to have for the small text
    logger.debug(f"Using font {font_path} of size {font_size}")
    font = ImageFont.truetype(font_path, font_size)
    if small_text:
        tw, th = font.getsize(small_text)
        logger.debug(f"We have small text of size w {tw} x h {th}")
    else:
        tw = 0
        th = 0
        logger.debug("No small text will be used")
    # on continuous tape make the sticker at least as wide as the height
    # (square) or maximum as wide as the text
    if nw is None:
        # continuous stickers are flipped by default
        swapped = True
        logger.debug("Sticker width undefined")
        if long_text_width is not None:
            nw = max(nh+long_text_width, tw)
            logger.debug(f"Long text width set, width set to {nw}")
        else:
            if not long_text:
                logger.debug(
                        "No long text given. Width appropriately adjusted.")
                nw = max(nh, tw)
            else:
                logger.debug(
                        "Long text given but no long text width set. "
                        "Use default.")
                nw = max(3*nh, tw)
    # for non-continuous tape
    elif nh > nw:
        logger.debug("Height is larger than width, flipping drawing.")
        swapped = True
        nh, nw = nw, nh
    # the default scenario of a rectangle lying down
    else:
        pass
    # on non-continuous tape, warn the user if the text extends
    # beyond the sticker width
    if tw > nw:
        warnings.warn(
            "The small text exceeds the sticker width."
            " Consider using a smaller font size."
        )
    qr_properties = {
        "version": version,
        "error_correction": error_correction,
        "box_size": box_size,
        "border": border,
    }
    qr = qrcode.QRCode(**qr_properties)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # create custom pixel size by padding
    # create a white background image
    background = Image.new('1', (nw, nh), color=1)  # one bit pixels
    logger.debug(f"Created background with size {background.size}")
    # create the text to be added to the images and get their sizes
    draw = ImageDraw.Draw(background)
    # is a qr_size specified explicitly?
    if max_qr_size is not None:
        img = img.resize((max_qr_size, max_qr_size))
    w, h = img.size
    logger.debug(f"QR code created with size w {w} x h {h}")
    # does the image fit on the sticker?
    if h > nh - th:
        logger.debug("QR code is too large for sticker.")
        sf = (nh - th) / h
        newqrw = int(w * sf)
        img = img.resize((newqrw, int(h * sf)))
        logger.debug(f"QR code was resized to {img.size}")
    # paste the new image into the background on 0,0
    background.paste(img)
    if small_text:
        # paste the small text under the QR code
        stx, sty = (0, img.size[1])
        logger.debug(f"There is small text, it is added to x{stx} y{sty}")
        draw.text((stx, sty), small_text, font=font)
    # now paste the long text if possible
    if long_text:
        if long_text_width is None:
            long_text_width = nw - img.size[0]
            logger.debug(
                    f"Long text width not given, setting to {long_text_width}")
        startltx = img.size[0]
        width = min(nw - startltx, long_text_width)
        logger.debug(f"The long text will start at x = {startltx}")
        logger.debug(f"The width of the long text will be {width}")
        offset = 0
        for line in textwrap.wrap(long_text, width // int(0.7*font_size)):
            if offset > nh - th:
                warnings.warn("The long text does not fit the sticker")
                break
            draw.text((startltx, offset), line, font=font)
            offset += font.getsize(line)[1]
    # rotate again if the stickers are to be printed horizontally
    if any([swapped, rotate]) and not all([swapped, rotate]):
        background = background.rotate(90, expand=True)
    return background


def _create_qr_sticker_params(p):
    logger.debug("Arguments:")
    logger.debug(p)
    background = create_qr_sticker_image(
        p.data,
        p.printsize,
        p.short_text,  # small_text
        p.long,  # long_text
        p.longwidth,  # long_text_width
        p.font_path,  # font_path
        p.fontsize,  # font_size
        p.version,  # "version":
        p.error_correction,  # "error_correction":
        p.box_size,  # "box_size":
        p.border,  # "border":
        p.qr_size,
        p.rotate,  # rotate
    )
    # save the image
    background.save(p.output)


def main():
    p = get_args_cli()
    _create_qr_sticker_params(p)
    print(f"Created QR sticker encoding text '{p.data}' at {p.output}")


if __name__ == "__main__":
    main()
