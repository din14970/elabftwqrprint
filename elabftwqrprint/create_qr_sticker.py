import argparse
import logging
import sys

from . import _cli_args as cli
from . import utils as utls

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
    parser = cli.add_arg_sticker_size(parser)
    parser = cli.add_output_args(parser)
    p = parser.parse_args()
    if p.no_short_text:
        p.short = ""
    return p


def _create_qr_sticker_params(p):
    logger.debug("Arguments:")
    logger.debug(p)
    sticker = utls.create_qr_sticker_image(
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
    )
    # save the image
    sticker.save(p.output)


def main():
    p = get_args_cli()
    _create_qr_sticker_params(p)
    print(f"Created QR sticker encoding text '{p.data}' at {p.output}")


if __name__ == "__main__":
    main()
