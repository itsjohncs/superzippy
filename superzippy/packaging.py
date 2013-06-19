#!/usr/bin/env python
from optparse import OptionParser, make_option
import subprocess
import logging
import sys
import tempfile
import os, os.path
import zipdir
import pkg_resources
import shutil

DEVNULL = open(os.devnull, "w")

_dirty_files = []
def destroy_dirty_files():
    global _dirty_files

    log = logging.getLogger("superzippy")

    for i in _dirty_files:
        log.debug("Deleting %s.", i)
        shutil.rmtree(i)

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
        ),
        make_option(
            "-c", "--config", action = "store", default = "superconfig.py",
            help =
                "The configuration file to use when creating the archive. "
                "Defaults to %default."
        ),
        make_option(
            "-o", "--output", action = "store", default = None,
            help =
                "The name of the output file. Defaults to the name of the "
                "package."
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

    #### Create virtual environment

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

    ##### Install package and dependencies

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

    ##### Install bootstrapper

    log.debug("Adding bootstrapper to the archive.")

    bootstrap_files = {
        "bootstrapper.py": "__main__.py",
        "zipsite.py": "zipsite.py",
        "module_locator.py": "module_locator.py"
    }

    for k, v in bootstrap_files.items():
        source = pkg_resources.resource_stream("superzippy.bootstrapper", k)
        dest = open(os.path.join(temp_dir, v), "w")

        shutil.copyfileobj(source, dest)

        source.close()
        dest.close()

    ##### Install configuration

    log.debug("Copying configuration file to archive.")

    shutil.copyfile(options.config, os.path.join(temp_dir, "superconfig.py"))

    ##### Zip everything up into final file

    log.debug("Zipping up %s.", temp_dir)

    output_file = options.output if options.output else package_to_install

    zipdir.zipdir(
        temp_dir,
        output_file
    )

    #### Make that file executable

    with file(output_file, "r") as f:
        data = f.read()

    with file(output_file, "w") as f:
        f.write("#!/usr/bin/env python\n" + data)

    os.chmod(output_file, 0755)

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
