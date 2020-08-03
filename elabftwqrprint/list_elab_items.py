import argparse
import sys

from . import _elabftw_interface as elabqr


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
    return parser.parse_args()


def main():
    p = get_args_cli()
    elabqr.list_items(
            category=p.category,
            match_string=p.search,
            mindate=p.min_date,
            maxdate=p.max_date)


if __name__ == "__main__":
    main()
