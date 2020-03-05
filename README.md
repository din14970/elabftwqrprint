# GenQr

Generates a QR code from a string and saves it to a file using the python [qrcode](https://pypi.org/project/qrcode/) package.

Run the script as:

```
$ python3 main.py [options] <string>

usage: main.py [-h] [-o OUTPUT] [-v VERSION] [-e {L,M,Q,H}] [-s BOX_SIZE] [-b BORDER]
               [-p {12,29,38,50,54,62,102,17x54,17x87,23x23,29x42,29x90,39x90,39x48,52x29,62x29,62x100,102x51,102x152,d12,d24,d58}]
               data

positional arguments:
  data                  String to turn into QR code

optional arguments:
  -h, --help
    show this help message and exit
  -o OUTPUT, --output OUTPUT
    Path to output
  -v VERSION, --version VERSION
    Size of QR code (1-40)
  -e {L,M,Q,H}, --error_correction {L,M,Q,H}
    Error correction
  -s BOX_SIZE, --box_size BOX_SIZE
    Number of pixels each box of QR code is
  -b BORDER, --border BORDER
    Number of pixels the border should be
  -p {12,29,38,50,54,62,102,17x54,17x87,23x23,29x42,29x90,39x90,39x48,52x29,62x29,62x100,102x51,102x152,d12,d24,d58}, --printsize {12,29,38,50,54,62,102,17x54,17x87,23x23,29x42,29x90,39x90,39x48,52x29,62x29,62x100,102x51,102x152,d12,d24,d58}
    Sticker dimensions
```
