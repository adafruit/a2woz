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
@click.version_option(version=__version__)
@click.option("--debug", "-d", is_flag="True", help="print debugging information while processing")
@click.option("--output", "-o", "output_file", type=click.Path(), default=None, help="Output path, defaults to the input with the extension replaced with .woz. When multiple input files are specified, --output may not be used.")
@click.option("--overwrite/--no-overwrite", "-f/-n", default=False, help="Controls whether to overwrite an output file. Files are not overwritten by default.")
@click.argument("input-files", type=click.Path(exists=True), nargs=-1)
def main(debug, input_files, output_file, overwrite):
    "Convert a disk image to .woz format with minimal processing"
    logger = debug and DebugLogger or DefaultLogger
    
    if len(input_files) == 1:
        if output_file is None:
            output_file = os.path.splitext(input_files[0])[0] + ".woz"

        if not overwrite:
            if os.path.exists(output_file):
                raise SystemExit(f"Use --overwrite to overwrite {output_file}.")
    elif output_file is not None:
        raise SystemExit(f"--output is only valid with one input file")

    for input_file in input_files:
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
