# Elabftwqrprint

[elabFTW](https://www.elabftw.net/) is a free and open source electronic lab notebook which can be used not only to log scientific activities in a lab, but also to keep track of physical and digital objects. Each object in the database can be accessed via a unique URL. To link the physical objects to the digital database entries, encoding these URL's into QR codes which can be printed on a sticker is very convenient. [Brother](www.brother.com) makes a series of (semi-)professional label printers which are well suited for this purpose, and there is [a python library](https://github.com/pklaus/brother_ql) that sends direct print instructions to these types of printers.  This repository is a collection of command line tools for linking up the elabFTW API to create QR codes from database objects and the brother-ql printer library to print them out.

# Installation

```
$ pip install elabftwqrprint
```

Pro-tip: for safety it's always best to install things in a virtual environment

# Useage

First you must configure the elabftw server information and the printer information with:

```
$ configure_elabftw
```

and

```
$ configure_printer
```
respectively. You will be guided through a number of prompts to enter the url to your elabFTW instance, your access token, your printer model, etc. The information you provide is stored in `~/.elabftwqrprint/elabconfig.yaml` and `~/.elabftwqrprint/printerconfig.yaml` respectively. These are different config files because you might want to create sticker images without having a Brother printer, or you might want to print stickers separate from elabFTW. For each PC you install this package on, you only have to do this once. If you change some settings you can directly edit the config files or re-run these config scripts.

After successfully creating the configuration, you can use the following commands:

```
$ create_qr_sticker [TEXT]  # turn any string into a QR code sticker of a dimension suitable for the Brother printers
$ create_sticker_elab_item [ID]  # create a QR code sticker image from a database item in your elabFTW instance and save to a file
$ list_elab_items  # view a table of your database items in the command line
$ print_sticker_elab_item [ID]  # directly print a QR code sticker from a database item in your elabFTW instance
$ print_sticker [FILENAME]  # print a sticker from a file
```

Each command has a number of options to control how the sticker looks, e.g. font, font size, QR code size, longer description to print next to the QR code... You can check the different options with the `-h` or `--help` flags.
