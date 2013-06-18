#!/usr/bin/env python
from optparse import OptionParser, make_option
import subprocess
import logging
import sys
import tempfile
import os, os.path
import zipdir

DEVNULL = open(os.devnull, "w")

_dirty_files = []
def destroy_dirty_files():
    global _dirty_files

    log = logging.getLogger("superzippy")

    for i in _dirty_files:
        log.debug("Deleting %s.", i)

    _dirty_files = []

def parse_arguments(args = sys.argv[1:]):
    option_list = [
        make_option(
            "-v", "--verbose", action = "store_true",
            help = "INFO level log messages and above will be output."
        ),
        make_option(
            "-d", "--debug", action = "store_true",
            help = "DEBUG level log messages and above will be output."
        ),
        make_option(
            "-q", "--quiet", action = "store_true",
            help = "No log messages will be output."
        )
    ]

    parser = OptionParser(
        usage = "usage: %prog [options] [PACKAGE]",
        description =
            "Zips up a package and adds superzippy's super bootstrap logic to "
            "it.",
        option_list = option_list
    )

    options, args = parser.parse_args(args)

    if len(args) != 1:
        parser.error("Exactly one argument must be supplied.")

    return (options, args)

def setup_logging(options, args):
    log_level = logging.WARN
    if options.debug:
        log_level = logging.DEBUG
    elif options.verbose:
        log_level = logging.INFO
    elif options.quiet:
        log_level = sys.maxint

    format = "[%(levelname)s] %(message)s"

    logging.basicConfig(level = log_level, format = format)

def main(options, args):
    log = logging.getLogger("superzippy")

    # Create the virtualenv directory
    temp_dir = tempfile.mkdtemp()
    _dirty_files.append(temp_dir)

    log.debug("Creating virtual environment at %s.", temp_dir)
    output_target = None if options.debug else DEVNULL

    return_value = subprocess.call(
        ["virtualenv", temp_dir],
        stdout = output_target,
        stderr = subprocess.STDOUT
    )

    if return_value != 0:
        log.critical(
            "virtualenv returned non-zero exit status (%d).", return_value
        )

        return 1

    package_to_install = args[0]
    pip_path = os.path.join(temp_dir, "bin", "pip")

    log.debug("Installing the package %s.", package_to_install)
    return_value = subprocess.call(
        [pip_path, "install", package_to_install],
        stdout = output_target,
        stderr = subprocess.STDOUT
    )

    if return_value != 0:
        log.critical("pip returned non-zero exit status (%d).", return_value)

        return 1

    log.debug("Zipping up %s.", temp_dir)
    zipdir.zipdir(temp_dir, package_to_install)

    return 0

def run():
    options, args = parse_arguments()
    setup_logging(options, args)
    try:
        main(options, args)
    finally:
        destroy_dirty_files()

if __name__ == "__main__":
    run()
