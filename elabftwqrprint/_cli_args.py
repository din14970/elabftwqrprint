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


def add_arg_sticker_size(parser):
    parser.add_argument(
        "-p",
        "--printsize",
        type=str,
        choices=gconf.STICKER_SIZES.keys(),
        help="Sticker dimensions",
        default=defaults["printsize"],
    )
    return parser


# all arguments associated with how the sticker looks
def add_args_sticker_layout(parser):
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
        choices=gconf.ERROR_CORRECT.keys(),
        help="Error correction level",
        default=qr_defaults["error_correction"],
    )
    parser.add_argument(
        "-n",
        "--box_size",
        type=int,
        help=("Number of pixels each box of QR code is"),
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


def add_args_printer(parser):
    parser.add_argument(
            "--printer_type",
            default=gconf.PRINTER_TYPE,
            choices=gconf.SUPPORTED_MODELS,
            help=(
                "Type of Brother label printer (see brother_ql documentation)"
                ))
    parser.add_argument(
            "--printer_backend",
            default=gconf.PRINTER_BACKEND,
            choices=gconf.PRINTER_BACKENDS,
            help=(
                "Printer backend (see brother_ql documentation)"
                ))
    parser.add_argument(
            "--printer_id",
            default=gconf.PRINTER_ID,
            help=(
                "Printer identifyer (see brother_ql documentation)"
                ))
    parser.add_argument(
            "--rotate_print",
            choices=gconf.PRINTER_ROTATE_OPTIONS,
            default=gconf.ROTATE_PRINT,
            help=(
                "Rotate the print image (counterclock-wise) by this amount"
                " of degrees. With auto it is automatically adjusted."
                ))
    parser.add_argument(
        "--use_red_tape",
        action="store_true",
        help=("Print as red tape"),
    )
    return parser


def add_args_elab_connection(parser):
    parser.add_argument(
            "--url",
            default=gconf.URL,
            help=(
                "URL to the eLabFTW instance (e.g. https://elab.example.com)"
                ))
    parser.add_argument(
            "--token",
            default=gconf.TOKEN,
            help=(
                "Token to access the eLabFTW instance"
                ))
    parser.add_argument(
            "--do_not_verify",
            action="store_true",
            help=(
                "Don't verify the certificate, overriding any default."
                ))
    return parser
