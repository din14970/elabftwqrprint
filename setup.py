from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="elabftwqrprint",
    version="0.0.6",
    description=("Make QR code stickers for elabFTW database"
                 " entries and print them with Brother label "
                 "printers."),
    url='https://github.com/din14970/elabftwqrprint',
    author='Niels Cautaerts',
    author_email='nielscautaerts@hotmail.com',
    license='GPL-3.0',
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=['Topic :: Scientific/Engineering',
                 'Intended Audience :: Science/Research',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.8'],
    keywords=[
        'e-lab',
        'provenance',
        'lab management',
    ],
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'configure_elabftw = elabftwqrprint.configure_elabftw:main',
              'configure_printer = elabftwqrprint.configure_printer:main',
              'create_qr_sticker = elabftwqrprint.create_qr_sticker:main',
              'create_sticker_elab_item = elabftwqrprint.create_sticker_elab_item:main',
              'list_elab_items = elabftwqrprint.list_elab_items:main',
              'print_sticker_elab_item = elabftwqrprint.print_sticker_elab_item:main',
              'print_sticker = elabftwqrprint.print_sticker:main',
              'find_items = elabftwqrprint.find_items:main'
          ],
      },
    package_data={'': ['elabftwqrprint/defaultfont.ttf']},
    include_package_data=True,
    install_requires=[
        'brother-ql>=0.9.4',
        'elabapy>=0.6.1',
        'pyyaml>=5.1',
        'Pillow>=7.2.0',
        'tabulate>=0.8.7',
        'qrcode>=6.1',
    ],
)
