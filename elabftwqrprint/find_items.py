from . import _elabftw_interface as elabqr
from . import list_elab_items as lei


def main():
    p = lei.get_args_cli()
    val = elabqr.get_item_ids(
            category=p.category,
            match_string=p.search,
            mindate=p.min_date,
            maxdate=p.max_date)
    for i in val:
        print(i)


if __name__ == "__main__":
    main()
