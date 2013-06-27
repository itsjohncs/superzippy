#!/usr/bin/env python

# Copyright (c) 2013 John Sullivan
# Copyright (c) 2013 Other contributers as noted in the CONTRIBUTERS file
#
# This file is part of superzippy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from optparse import OptionParser, make_option
import subprocess
import logging
import sys
import tempfile
import os, os.path
from . import zipdir
import pkg_resources
import shutil
import shlex
import errno

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
            "-v", "--verbose", action = "count", default=0,
            help =
                "May be specified thrice. If specified once, INFO messages and "
                "above are output. If specified twice, DEBUG messages and "
                "above are output. If specified thrice, DEBUG messages and "
                "above are output, along with the output from any invoked "
                "programs."
        ),
        make_option(
            "-q", "--quiet", action = "store_true",
            help = "Only CRITICAL log messages will be output."
        ),
        make_option(
            "-o", "--output", action = "store", default = None,
            help =
                "The name of the output file. Defaults to the name of the "
                "last package specified on the command line."
        ),
        make_option(
            "-r", "--requirements", action = "append", default = [],
            help =
                "A path to a requirements.txt file to parse and install from. "
                "This option may be specified multiple times."
        ),
        make_option(
            "-c", "--raw-copy", action = "append", default = [],
            dest = "raw_copy",
            help =
                "A path to a file or directory to copy into the created "
                "executable directly. Useful when you don't have a setup.py "
                "for your project."
        ),
        make_option(
            "--raw-copy-rename", action = "append", default = [],
            dest = "raw_copy_rename",
            help =
                "Takes 2 arguments, first a path to a file or directory to "
                "copy into the zuper zip directly, and second the name that "
                "file should have (this name will be importable from within "
                "the executable."
        )
    ]

    parser = OptionParser(
        usage = "usage: %prog [options] [PACKAGE1 PACKAGE2 ...] [ENTRY POINT]",
        description =
            "Zips up a package and adds superzippy's super bootstrap logic to "
            "it. ENTRY POINT should be in the format module:function. Just "
            "like the entry_point option for distutils. Each PACKAGE string "
            "will be passed directly to pip so you may use options and expect "
            "normal results (ex: 'PyYAML --without-libyaml').",
        option_list = option_list
    )

    options, args = parser.parse_args(args)

    if len(args) < 1:
        parser.error("1 or more arguments must be supplied.")

    return (options, args)

def setup_logging(options, args):
    if options.verbose >= 2:
        log_level = logging.DEBUG
    elif options.verbose == 1:
        log_level = logging.INFO
    elif options.quiet:
        log_level = logging.CRITICAL
    else:
        log_level = logging.WARN

    format = "[%(levelname)s] %(message)s"

    logging.basicConfig(level = log_level, format = format)

    logging.getLogger("superzippy").debug("Logging initialized.")

def main(options, args):
    log = logging.getLogger("superzippy")

    packages = args[0:-1]
    entry_point = args[-1]

    # Append any requirements.txt files to the packages list.
    packages += ["-r %s" % i for i in options.requirements]

    # Create the virtualenv directory
    virtualenv_dir = tempfile.mkdtemp()
    _dirty_files.append(virtualenv_dir)

    #### Create virtual environment

    log.debug("Creating virtual environment at %s.", virtualenv_dir)
    output_target = None if options.verbose >= 3 else DEVNULL

    return_value = subprocess.call(
        ["virtualenv", virtualenv_dir],
        stdout = output_target,
        stderr = subprocess.STDOUT
    )

    if return_value != 0:
        log.critical(
            "virtualenv returned non-zero exit status (%d).", return_value
        )

        return 1

    ##### Install package and dependencies

    pip_path = os.path.join(virtualenv_dir, "bin", "pip")

    for i in packages:
        log.debug("Installing package with `pip install %s`.", i)

        command = [pip_path, "install"] + shlex.split(i)
        return_value = subprocess.call(
            command,
            stdout = output_target,
            stderr = subprocess.STDOUT
        )

        if return_value != 0:
            log.critical("pip returned non-zero exit status (%d).", return_value)

            return 1

    if not packages:
        log.warn("No packages specified.")

    #### Move site packages over to build directory

    # TODO: We should look at pip's source code and figure out how it decides
    # where site-packages is and use the same algorithm.

    build_dir = tempfile.mkdtemp()
    _dirty_files.append(build_dir)

    site_package_dir = None
    for root, dirs, files in os.walk(virtualenv_dir):
        if "site-packages" in dirs:
            found = os.path.join(root, "site-packages")

            # We'll only use the first one, but we want to detect them all.
            if site_package_dir is not None:
                log.warn(
                    "Multiple site-packages directories found. `%s` will be "
                    "used. `%s` was found afterwards.",
                    site_package_dir,
                    found
                )
            else:
                site_package_dir = found

    shutil.move(site_package_dir, build_dir)

    #### Perform any necessary raw copies.
    raw_copies = options.raw_copy_rename

    for i in options.raw_copy:
        if i[-1] == "/":
            i = i[0:-1]

        raw_copies.append((i, os.path.basename(i)))

    for file_path, dest_name in raw_copies:
        log.debug(
            "Performing raw copy of `%s`, destination name: `%s`.",
            file_path,
            dest_name
        )

        dest = os.path.join(build_dir, "site-packages", dest_name)

        try:
            shutil.copytree(file_path, dest)
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(file_path, dest)
            else:
                raise

    ##### Install bootstrapper

    log.debug("Adding bootstrapper to the archive.")

    bootstrap_files = {
        "__init__.py": "__init__.py",
        "bootstrapper.py": "__main__.py",
        "zipsite.py": "zipsite.py",
        "module_locator.py": "module_locator.py"
    }

    for k, v in bootstrap_files.items():
        source = pkg_resources.resource_stream("superzippy.bootstrapper", k)
        dest = open(os.path.join(build_dir, v), "wb")

        shutil.copyfileobj(source, dest)

        source.close()
        dest.close()

    ##### Install configuration

    log.debug("Adding configuration file to archive.")

    with open(os.path.join(build_dir, "superconfig.py"), "w") as f:
        f.write("entry_point = '%s'" % entry_point)

    ##### Zip everything up into final file

    log.debug("Zipping up %s.", build_dir)

    if options.output:
        output_file = options.output
    elif packages:
        output_file = shlex.split(packages[-1])[0]

        for k, c in enumerate(output_file):
            if c in ("=", ">", "<"):
                output_file = output_file[0:k]
    else:
        log.critical("No output file or packages specified.")

        return 1

    try:
        zipdir.zipdir(
            build_dir,
            output_file
        )
    except IOError:
        log.critical(
            "Could not write to output file at '%s'.",
            output_file,
            exc_info = sys.exc_info()
        )

        return 1

    #### Make that file executable

    with open(output_file, "rb") as f:
        data = f.read()

    with open(output_file, "wb") as f:
        f.write(b"#!/usr/bin/env python\n" + data)

    os.chmod(output_file, 0o755)

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
