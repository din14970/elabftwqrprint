import argparse

from . import _elabftw_interface as elabqr
from . import _global_defaults as gconf
from . import _cli_args as cli
from . import create_qr_sticker as cqs


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "id_no",
            type=int,
            help="Database item to create QR-sticker for")
    parser = cli.add_args_sticker_basic_content(parser)
    parser = cli.add_args_sticker_layout(parser)
    parser = cli.add_output_args(parser)
    parser = cli.add_args_elab_connection(parser)
    p = parser.parse_args()
    return p


def _create_qr_elab_sticker(p):
    if not p.do_not_verify:
        verify = gconf.VERIFY
    manager = elabqr.initialize(url=p.url, token=p.token, verify=verify)
    item = manager.get_item(p.id_no)
    link = f"{p.url}/database.php?mode=view&id={p.id_no}"
    p.data = link
    print(item['title'])
    print(item['date'])
    short_desc = f"{item['date']} {item['title']}"
    if not p.short_text:
        p.short_text = short_desc
    if p.no_short_text:
        p.short_text = ""
    print(f"Will create QR sticker for link {link} and label with: {p.short_text}")
    cqs._create_qr_sticker_params(p)
    print(f"Created QR sticker for item {p.id_no} at {p.output}")


def main():
    p = get_args_cli()
    _create_qr_elab_sticker(p)


if __name__ == "__main__":
    main()
