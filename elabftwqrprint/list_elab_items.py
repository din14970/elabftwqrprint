import argparse
import sys

from . import _elabftw_interface as elabqr
from . import _cli_args as cli


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--category", type=str, help="Limit results to one category",
        default=None
    )
    parser.add_argument(
            "-s",
            "--search",
            type=str,
            help="Search substring that the database item titles must contain",
            default=None,
            )
    parser.add_argument(
            "-m",
            "--min_date",
            type=int,
            help="Minimum date for database items. Must be in form YYYYMMDD.",
            )
    parser.add_argument(
            "-M",
            "--max_date",
            type=int,
            help="Maximum date for database items. Must be in form YYYYMMDD.",
            )
    parser = cli.add_args_elab_connection(parser)
    return parser.parse_args()


def main():
    p = get_args_cli()
    elabqr.list_items(
            category=p.category,
            match_string=p.search,
            mindate=p.min_date,
            maxdate=p.max_date,
            url=p.url,
            token=p.token,
            verify=p.do_not_verify==False,
            )


if __name__ == "__main__":
    main()
