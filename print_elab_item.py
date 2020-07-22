import argparse
import elabqr
import os
import global_configuration as gconf
import yaml


def main():
    conf_path = os.path.expanduser(gconf.CONFIG_FOLDER)
    if not os.path.isdir(conf_path):
        os.mkdir(conf_path)
    default_path = conf_path+"/last_sticker.png"
    try:
        print_conf = yaml.load(conf_path+"/printerconfig.yaml")
    except Exception:
        print("No printer settings found, run configure_printer first")
        return
    parser = argparse.ArgumentParser()
    parser.add_argument("id_no", type=str,
                        help="Database item to create QR-sticker for")
    parser.add_argument("-l", "--long", type=str,
                        help="Long text to print next to QR code",
                        default=gconf.LONG_TEXT)
    parser.add_argument("-f", "--fontsize", type=int,
                        help="Font size of small and big text",
                        default=gconf.FONT_SIZE)
    p = parser.parse_args()
    elabqr.make_qrcode_item(p.id_no, default_path, long_text=p.long,
                            font_size=p.fontsize)
    print(f"Created QR sticker for item {p.id_no} at {default_path}")
    os.system(
             f"brother_ql -b {print_conf['backend']} -m "
             f"{print_conf['printer']} -p {print_conf['identifyer']} "
             f"print -l {print_conf['labelsize']} {default_path}"
             )
    print("The sticker was printed")


if __name__ == "__main__":
    main()
