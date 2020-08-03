import argparse

from . import _cli_args as cli
from . import create_sticker_elab_item as crstelab
from . import print_sticker as print_image


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "id_no",
            type=int,
            help="Database item to create QR-sticker for")
    parser = cli.add_args_sticker_basic_content(parser)
    parser = cli.add_args_sticker_layout(parser)
    parser = cli.add_output_args(parser)
    parser = cli.add_args_print(parser)
    p = parser.parse_args()
    return p


def main():
    p = get_args_cli()
    crstelab._create_qr_elab_sticker(p)
    p.filename = p.output
    print_image.print_image(p)


if __name__ == "__main__":
    main()
