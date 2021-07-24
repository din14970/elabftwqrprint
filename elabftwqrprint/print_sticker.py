import argparse
import subprocess
import sys


from . import _cli_args as cli
from . import _global_defaults as gconf


def get_args_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Path to the image file")
    parser = cli.add_arg_sticker_size(parser)
    parser = cli.add_args_printer(parser)
    p = parser.parse_args()
    return p


def print_image(p):
    if (p.printer_type is None
        or p.printer_backend is None
        or p.printer_id is None):
        print("No valid printer settings provided or found. Must "
              "at least define printer type, backend and id.")
        sys.exit(1)
    if p.use_red_tape or gconf.PRINT_RED:
        redflag = "--red"
    else:
        redflag = ""
    print_command = (
        f"brother_ql -b {p.printer_backend} -m "
        f"{p.printer_type} -p {p.printer_id} "
        f"print -l {p.printsize} -r {p.rotate_print}"
        f" {redflag} {p.filename}"
    )
    subprocess.run(print_command, shell=True, check=True)
    print("The sticker was printed succesfully")


def main():
    p = get_args_cli()
    print_image(p)


if __name__ == "__main__":
    main()
