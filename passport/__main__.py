#!/usr/bin/env python3

# (c) 2018-9 by 4am
# MIT-licensed

import click

from passport import eddimage, wozardry, a2rimage
from passport.loggers import DefaultLogger, DebugLogger
from passport import RawConvert
from passport.strings import __date__, STRINGS
import argparse
import os.path

__version__ = "0.2" # https://semver.org/
__progname__ = "passport"

@click.command()
@click.help_option()
@click.version_option(version=STRINGS["header"])
@click.option("--debug", "-d", is_flag="True", help="print debugging information while processing")
@click.argument("input-file", type=click.Path(exists=True))
@click.argument("output-file", type=click.Path())
def main(debug, input_file, output_file):
    "Convert a disk image to .woz format with minimal processing"
    logger = debug and DebugLogger or DefaultLogger
    
    base, ext = os.path.splitext(input_file)
    ext = ext.lower()
    if ext == ".edd":
        reader = eddimage.EDDReader
    elif ext == ".a2r":
        reader = a2rimage.A2RImage
    else:
        raise SystemExit("unrecognized file type")

    logger = debug and DebugLogger or DefaultLogger
    with open(input_file, "rb") as f:
        RawConvert(input_file, reader(f), logger, output_file)

if __name__ == '__main__':
    main()
