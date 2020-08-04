import argparse
import sys

from . import _cli_args as cli
from . import create_sticker_elab_item as crstelab
from . import print_sticker as print_image


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "id_no",
            type=str,
            nargs="*",
            help=(
                "Id(s) of database item or items to "
                "create QR-sticker for"),
            default=sys.stdin,
    )
    parser = cli.add_args_sticker_basic_content(parser)
    parser = cli.add_args_sticker_layout(parser)
    parser = cli.add_output_args(parser)
    parser = cli.add_args_print(parser)
    p = parser.parse_args()
    return p


def main():
    p = get_args_cli()
    # if a short text is provided it overrides the default
    override_short_text = False
    if p.short_text:
        override_short_text = True
    all_stickers = p.id_no
    for i in all_stickers:
        p.id_no = i
        if not override_short_text:
            p.short_text = ""
        crstelab._create_qr_elab_sticker(p)
        p.filename = p.output
        print_image.print_image(p)
        print(f"Printed item {i}")


if __name__ == "__main__":
    main()
