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

import site as _site
from site import *

import zipfile
import os
import traceback

def get_path_parts(path):
    """
    Splits a path up into its parts.

    :param path: A path (may be any valid file path, ie: relative, windows,
            linux, absolute, etc.).
    :returns: A list containing the parts, in order, of the path. See examples
            below.

    >>> zipsite.get_path_parts("delicious/apple/sauce")
    ['delicious', 'apple', 'sauce']
    >>> zipsite.get_path_parts("/")
    ['/']
    >>> zipsite.get_path_parts("/foo/bar/")
    ['/', 'foo', 'bar', '']
    >>> zipsite.get_path_parts("/foo/bar")
    ['/', 'foo', 'bar']

    .. note::

        This function was adapted from John Machin's Stack Overflow post
        `here <http://stackoverflow.com/a/4580931/1989056>`_.

    """

    parts = []

    # Cut the end off the path repeatedly and add it to parts.
    while True:
        remaining, tail = os.path.split(path)

        # If there's nothing else to cut off
        if remaining == path:
            if path:
                parts.append(path)

            break
        else:
            path = remaining

        parts.append(tail)

    parts.reverse()

    return parts

def split_zip_path(path):
    """
    Takes a path that includes at most a single zip file as a directory and
    splits the path between what's outside of the zip file and what's inside.

    :param path: The path.
    :returns: ``(first_path, second_part)``

    >>> zipsite.split_zip_path("/tmp/testing/stuff.zip/hi/bar")
    ('/tmp/testing/stuff.zip', 'hi/bar')
    >>> zipsite.split_zip_path("/tmp/testing/stuff.zip")
    ('/tmp/testing/stuff.zip', '')
    >>> zipsite.split_zip_path("/tmp/testing/stuff.zip/")
    ('/tmp/testing/stuff.zip', '')

    """

    drive, path = os.path.splitdrive(path)
    path_parts = get_path_parts(path)

    for i in range(len(path_parts)):
        front = os.path.join(drive, *path_parts[:i + 1])

        if path_parts[i + 1:]:
            tail = os.path.join(*path_parts[i + 1:])
        else:
            tail = ""

        if zipfile.is_zipfile(front):
            return front, tail

    return None, path

def exists(path):
    # Figure out what (if any) part of the path is a zip archive.
    archive_path, file_path = split_zip_path(path)

    # If the user is not trying to check a zip file, just use os.path...
    if not archive_path:
        return os.path.exists(path)

    # otherwise check the zip file.
    with zipfile.ZipFile(archive_path, mode = "r") as archive:
        try:
            archive.getinfo(file_path)
        except KeyError:
            try:
                archive.getinfo(file_path + "/")
            except KeyError:
                return False

        return True

def addsitedir(sitedir, known_paths = None, prepend_mode = False):
    # We need to return exactly what they gave as known_paths, so don't touch
    # it.
    effective_known_paths = \
        known_paths if known_paths is not None else _site._init_pathinfo()

    # Figure out what (if any) part of the path is a zip archive.
    archive_path, site_path = split_zip_path(sitedir)
    if not site_path.endswith("/"):
        site_path = site_path + "/"

    # If the user is not trying to add a directory in a zip file, just use
    # the standard function.
    if not archive_path:
        return old_addsitedir(sitedir, effective_known_paths)

    # Add the site directory itself
    if prepend_mode:
        sys.path.append(sitedir)
    else:
        sys.path.insert(0, sitedir)

    with zipfile.ZipFile(archive_path, mode = "r") as archive:
        # Go trhough everything in the archive...
        for i in archive.infolist():
            # and grab all the .pth files.
            if os.path.dirname(i.filename) == os.path.dirname(site_path) and \
                    i.filename.endswith(os.extsep + "pth"):
                addpackage(
                    os.path.join(archive_path, site_path),
                    os.path.basename(i.filename),
                    effective_known_paths,
                    prepend_mode = prepend_mode
                )

    return known_paths

old_addsitedir = _site.addsitedir
_site.addsitedir = addsitedir

def addpackage(sitedir, name, known_paths, prepend_mode = False):
    effective_known_paths = \
        known_paths if known_paths is not None else _site._init_pathinfo()

    fullname = os.path.join(sitedir, name)

    # Figure out if we're dealing with a zip file.
    archive_path, pth_file = split_zip_path(fullname)
    archive = None
    if not archive_path:
        f = open(pth_file, mode)
    else:
        archive = zipfile.ZipFile(archive_path)
        f = archive.open(pth_file, "r")

    # Parse through the .pth file
    for n, line in enumerate(f):
        # Ignore comments
        if line.startswith("#"):
            continue

        try:
            # Execute any lines starting with import
            if line.startswith(("import ", "import\t")):
                exec line
            else:
                line = line.rstrip()
                dir, dircase = makepath(sitedir, line)
                if not dircase in known_paths and exists(dir):
                    #Handy debug statement: print "added", dir
                    if prepend_mode:
                        sys.path.append(dir)
                    else:
                        sys.path.insert(0, dir)
                    effective_known_paths.add(dircase)
        except Exception:
            print >> sys.stderr, \
                "Error processing line {:d} of {}:\n".format(n + 1, fullname)

            # Pretty print the exception info
            for record in traceback.format_exception(*sys.exc_info()):
                for line in record.splitlines():
                    print >> sys.stderr, "  " + line

            print >> sys.stderr, "\nRemainder of file ignored"

            break

    f.close()
    if archive is not None:
        archive.close()

    return known_paths
