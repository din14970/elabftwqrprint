import textwrap
import qrcode
import argparse
import warnings
from PIL import Image, ImageDraw, ImageFont
import logging
from . import _global_defaults as gconf


# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# type of error correction
error_correct = gconf.ERROR_CORRECTION

# sticker size dictionary to correspond to brother_ql
sticker_sizes = gconf.STICKER_SIZES


qr_defaults = {
        "version": gconf.VERSION,
        "error_correction": gconf.ERROR_CORRECTION,
        "border": gconf.BORDER,
        "box_size": gconf.BOX_SIZE,
        }


defaults = {
        "printsize": gconf.PRINTSIZE,
        "output_path": gconf.OUTPUT_PATH,
        "short_text": gconf.SHORT_TEXT,
        "long_text": gconf.LONG_TEXT,
        "font": gconf.FONT,
        "font_size": gconf.FONT_SIZE,
        }


def create_qr_sticker_image(link,
                            size=defaults["printsize"],
                            small_text=defaults["short_text"],
                            long_text=defaults["long_text"],
                            long_text_width=None,
                            font_path=defaults["font"],
                            font_size=defaults["font_size"],
                            qr_properties=None,
                            qr_size=None,
                            ):
    """
    Create an image with a QR code and some text

    Parameters
    ----------
    link: str
        The text to encode in the QR code
    size: str
        String encoding the size of the string
        Options: "12", "29", "38", "50", "54", "62", "102",
        "17x54", "17x87", "23x23", "29x42", "29x90", "39x90", "39x48",
        "52x29", "62x29", "62x100", "102x51", "102x152",
        "d12", "d24", "d58"
    small_text: str, optional
        Short string to write below QR code, like
        a sample name
    long_text: str, optional
        Long string to write next to QR code, like a
        description. Will only be used if sticker size
        allows for it
    long_text_width: float, optional
        Width of the long text string in pixels. If it is larger
        than the sticker width, the sticker width will be chosen.
        If none is provided, the full sticker size will be chosen.
        If the width is less than 2x the height, the long text will
        not be printed even if provided. On an unbounded sticker,
        the text will by default be 2x wider than the QR code.
    font_path: str, optional
        Path to a font file
    font_size: int, optional
        font size of the long and short text. Default is 8 (pt).
    max_long_text_width: float, optional
        Must be between 0-1. The fraction of the width of the
        sticker that is reserved for tex
    qr_properties: dict, optional
        Dictionary of options to define how the QR code is made.
        Default is the defaults provided by the qrcode package.
        See the documentation on the qrcode package
    qr_size: int, optional
        Final size of qr code in pixels. If not defined the best
        fit will be calculated.

    Returns
    -------
    image: PIL.Image.Image
        The image object to be written to a file
    """
    nh, nw = sticker_sizes[size]
    logger.debug(f"Sticker size: height {nh} px, width {nw} px")
    # detect whether the image is best rotated 90 degrees
    swapped = False
    # if tape is endless then we cut a square
    if nw is None:
        logger.debug("Sticker width undefined")
        if long_text_width is None:
            logger.debug("No long text width defined. "
                         "Taking tape height.")
            long_text_width = nh
        if long_text:
            nw = nh + long_text_width
            logger.debug(f"Long text given. Setting width h + tw : {nw}")
        else:
            logger.debug("No long text given. Set dimensions square.")
            nw = nh
    elif nh > nw:
        logger.debug("Height is larger than width, flipping drawing.")
        swapped = True
        nh, nw = nw, nh
    else:
        # a regular bounded sticker with nh<nw
        pass
    if qr_properties is None:
        qr_properties = qr_defaults
    qr = qrcode.QRCode(**qr_properties)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # create custom pixel size by padding
    # create a white background image
    background = Image.new('1', (nw, nh), color=1)  # one bit pixels
    logging.debug(f"Created background with size {background.size}")
    # create the text to be added to the images and get their sizes
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(font_path, font_size)
    if small_text:
        tw, th = draw.textsize(small_text, font)
        logger.debug(f"We have small text of size w {tw} x h {th}")
    else:
        tw = 0
        th = 0
        logging.debug("No small text is given")
    # check if the small text is not wider than the sticker
    if tw > nw:
        warnings.warn("The small text exceeds the sticker width."
                      " Consider using a smaller font size.")
    # does the image fit on the sticker?
    if qr_size is not None:
        img = img.resize((qr_size, qr_size))
    w, h = img.size
    logger.debug(f"QR code created with size w {w} x h {h}")
    if h > nh-th:
        logger.debug("QR code is too large for sticker.")
        sf = (nh-th)/h
        newqrw = int(w*sf)
        img = img.resize((newqrw, int(h*sf)))
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
            long_text_width = nh
            logger.debug(f"Long text width not given, setting to nh {nh}")
        startltx = img.size[0]
        width = max(nw-startltx, long_text_width)
        logger.debug(f"The long text will start at x = {startltx}")
        logger.debug(f"The width of the long text will be {width}")
        if width >= nh:
            logger.debug(f"The text width {width} is at least the height {nh}")
            offset = 0
            for line in textwrap.wrap(long_text, width//int(0.7*font_size)):
                if offset > nh-th:
                    warnings.warn("The long text does not fit the sticker")
                    break
                draw.text((startltx, offset), line, font=font)
                offset += font.getsize(line)[1]
        else:
            warnings.warn("There is insufficient space "
                          "for long text.")
    # rotate again if the stickers are to be printed horizontally
    if swapped:
        background = background.rotate(90, expand=True)
    return background


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str,
                        help="String to turn into QR code")
    parser.add_argument("-p", "--printsize", type=str,
                        choices=sticker_sizes.keys(),
                        help="Sticker dimensions",
                        default=defaults["printsize"])
    parser.add_argument("-o", "--output", type=str,
                        help="Path to output file",
                        default=defaults["output_path"])
    parser.add_argument("-s", "--short", type=str,
                        help="Short text printed under QR code",
                        default=defaults["short_text"])
    parser.add_argument("-l", "--long", type=str,
                        help="Long text to print next to QR code",
                        default=defaults["long_text"])
    parser.add_argument("-w", "--longwidth", type=str,
                        help="Width of long text",
                        default=None)
    parser.add_argument("-d", "--font_path", type=str,
                        help="Path to a font file",
                        default=defaults["font"])
    parser.add_argument("-f", "--fontsize", type=int,
                        help="Font size of small and big text",
                        default=defaults["font_size"])
    parser.add_argument("-q", "--qr_size", type=int,
                        help=("Pixel width of QR code"),
                        default=None)
    parser.add_argument("-v", "--version", type=int,
                        help="Size of QR code (1-40). Default optimized.",
                        default=qr_defaults["version"])
    parser.add_argument("-e", "--error_correction", type=str,
                        choices=["L", "M", "Q", "H"],
                        help="Error correction level",
                        default=qr_defaults["error_correction"])
    parser.add_argument("-n", "--box_size", type=int,
                        help=("Number of pixels each box of "
                              "QR code is"),
                        default=qr_defaults["box_size"])
    parser.add_argument("-b", "--border", type=int,
                        help=("Number of pixels the border "
                              "should be"),
                        default=qr_defaults["border"])
    return parser.parse_args()


def main():
    p = get_args_cli()
    extraparams = {
        "version": p.version,
        "error_correction": p.error_correction,
        "box_size": p.box_size,
        "border": p.border,
    }
    background = create_qr_sticker_image(
            p.data, p.printsize, small_text=p.short,
            long_text=p.long, long_text_width=None, font_size=p.fontsize,
            qr_properties=extraparams, font_path=p.font_path)
    # save the image
    background.save(p.output)


if __name__ == "__main__":
    main()
