import argparse

from . import _elabftw_interface as elabqr


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--category", type=str, help="Limit results to one category", default=None
    )
    return parser.parse_args()


def main():
    p = get_args_cli()
    elabqr.list_items(category=p.category)


if __name__ == "__main__":
    main()
