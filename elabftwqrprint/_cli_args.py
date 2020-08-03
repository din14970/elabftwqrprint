from . import _global_defaults as gconf


qr_defaults = {
    "version": gconf.VERSION,
    "error_correction": gconf.ERROR_CORRECTION,
    "border": gconf.BORDER,
    "box_size": gconf.BOX_SIZE,
    "qr_size": gconf.QR_SIZE,
}


save_folder = gconf.DEFAULT_SAVE_LOCATION
save_name = gconf.DEFAULT_SAVE_NAME
defaults = {
    "printsize": gconf.PRINTSIZE,
    "output_path": save_folder.joinpath(save_name),
    "short_text": gconf.SHORT_TEXT,
    "long_text": gconf.LONG_TEXT,
    "font": gconf.FONT,
    "font_size": gconf.FONT_SIZE,
}


def add_args_sticker_basic_content(parser):
    parser.add_argument(
        "-s",
        "--short_text",
        type=str,
        help=(
            "Short text to be printed under QR code. "
            "Overrides any defaults."
            ),
        default=defaults["short_text"],
    )
    parser.add_argument(
        "--no_short_text",
        help=(
            "Don't add any text under QR code. "
            "Overrides the --short_text argument if provided."
            ),
        action="store_true"
    )
    parser.add_argument(
        "-l",
        "--long",
        type=str,
        help=(
            "Long text to print next to QR code "
            "Default is empty. "
            ),
        default=defaults["long_text"],
    )
    return parser


# all arguments associated with how the sticker looks
def add_args_sticker_layout(parser):
    parser.add_argument(
        "-p",
        "--printsize",
        type=str,
        choices=gconf.STICKER_SIZES.keys(),
        help="Sticker dimensions",
        default=defaults["printsize"],
    )
    parser.add_argument(
        "-w",
        "--longwidth",
        type=str,
        help="Maximum width of long text",
        default=gconf.LONG_TEXT_WIDTH
    )
    parser.add_argument(
        "-d",
        "--font_path",
        type=str,
        help="Path to a font file",
        default=defaults["font"],
    )
    parser.add_argument(
        "-f",
        "--fontsize",
        type=int,
        help="Font size of small and big text",
        default=defaults["font_size"],
    )
    parser.add_argument(
        "-q", "--qr_size", type=int, help=("Pixel width of QR code"),
        default=gconf.QR_SIZE
    )
    parser.add_argument(
        "-v",
        "--version",
        type=int,
        help="Size of QR code (1-40). Default optimized.",
        default=qr_defaults["version"],
    )
    parser.add_argument(
        "-e",
        "--error_correction",
        type=str,
        choices=["L", "M", "Q", "H"],
        help="Error correction level",
        default=qr_defaults["error_correction"],
    )
    parser.add_argument(
        "-n",
        "--box_size",
        type=int,
        help=("Number of pixels each box of " "QR code is"),
        default=qr_defaults["box_size"],
    )
    parser.add_argument(
        "-b",
        "--border",
        type=int,
        help=(
            "Number of squares the border of the QR code should be"
            ),
        default=qr_defaults["border"],
    )
    parser.add_argument(
        "--rotate",
        help=("Rotate the final image by 90 degrees"),
        action="store_true",
    )
    return parser


def add_output_args(parser):
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to output file",
        default=defaults["output_path"],
    )
    return parser


def add_args_print(parser):
    parser.add_argument(
            "-m",
            "--rotate_print",
            choices=["auto", "0", "90", "180", "270"],
            default="auto",
            help=(
                "Rotate the print image (counterclock-wise) by this amount"
                " of degrees"
                ))
    return parser
