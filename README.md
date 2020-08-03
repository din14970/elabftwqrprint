# Elabftwqrprint

## Description

[eLabFTW](https://www.elabftw.net/) is a free and open source electronic lab notebook which can be used not only to log scientific activities in a lab, but also to keep track of physical and digital objects. Each object in the database can be accessed via a unique URL. To link the physical objects to the digital database entries, encoding these URL's into QR codes which can be printed on a sticker is very convenient. [Brother](www.brother.com) makes a series of (semi-)professional label printers which are well suited for this purpose, and there is [a python library](https://github.com/pklaus/brother_ql) that sends direct print instructions to these types of printers.  This repository is a collection of command line tools for linking up the eLabFTW API to create QR codes from database objects and the brother-ql printer library to print them out.

## Installation

```bash
$ pip install --user elabftwqrprint
```

Pro-tip: for safety it's always best to install things in a virtual environment

### Note for Linux
It seems that when installing on Linux, the scripts are stored in `~/.local/bin` or `/user/local/bin`. These may not be on the path, meaning that the scripts are not directly accessible through the shell. To add these locations to the path do

```bash
$ export PATH=$PATH:$HOME/.local/bin
```

To make this a permanent thing whenever you open up a new shell add it to your shell config file, e.g. `~/.bashrc`.

## Usage

First you must configure the elabftw server information and the printer information with:

```bash
$ configure_elabftw
```

and

```bash
$ configure_printer
```
respectively. You will be guided through a number of prompts to enter the url to your elabFTW instance, your access token, your printer model, etc. The information you provide is stored in `~/.elabftwqrprint/elabconfig.yaml` and `~/.elabftwqrprint/printerconfig.yaml` respectively. These are different config files because you might want to create sticker images without having a Brother printer, or you might want to print stickers separate from elabFTW. For each PC you install this package on, you only have to do this once. If you change some settings you can directly edit the config files or re-run these config scripts.

After successfully creating the configuration, you can use the following commands:

```bash
$ list_elab_items  # view a table of your database items in the command line

$ create_qr_sticker [TEXT]  # turn any string into a QR code sticker of a dimension suitable for the Brother printers
$ create_sticker_elab_item [ID]  # create a QR code sticker image from a database item in your elabFTW instance and save to a file

$ print_sticker_elab_item [ID]  # directly print a QR code sticker from a database item in your elabFTW instance
$ print_sticker [FILENAME]  # print a sticker from a file
```

Each command has a number of options to control how the sticker looks, e.g. font, font size, QR code size, longer description to print next to the QR code... You can check the different options with the `-h` or `--help` flags.

In addition, you can manually create the config file `~/.elabftwqrprint/formatting.yaml`, with which you can override a number of defaults. The following options are recognized:
```yaml
default_save_name: # name of file commands write image to by default
default_save_folder: # directory where default image is written to
version: # the version of QR code used, see documentation of qrcode package
error_correction: # error correction level, see documentation of qrcode package and help in commands
border: # number of squares for QR code border, see documentation of qrcode package
box_size: # number of pixels per box in the QR code, see documentation of qrcode package
short_text: # default short text written below QR code. Will override <date> <title> label used by default in create_sticker_elab_item, but will be overridden by -s flag.
long_text: # default long text written to the right of the QR code. Will be overridden by -l flag.
font: # path to truetype font file
font_size: # default font size
long_text_width: # approximate number of pixels occupied by long text line. If None, a best guess is estimated.
max_qr_size: # maximum side length of QR code in pixels.
```

## Changelog

### v0.0.3
* fixed some bugs related to sticker rotation
* added more options for creating all stickers
* improved inheritance of arguments between various scripts
* added more user configurability with an extra config file
