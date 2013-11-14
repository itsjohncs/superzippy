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

# futures
from __future__ import with_statement

# stdlib
import shutil
import tempfile
import os.path
import random
import string

try:
    unicode
except NameError:
    unicode = str

try:
    xrange
except NameError:
    xrange = range

def create_test_directory(tree):
    """
    Creates a temporary directory with the given file tree in it.

    :param tree: A list of strings and tuples where each string is a path to
        a directory that should exist within the temporary directory (relative
        to the root of the directory) and each tuple is a file that should
        exist within the temporary directory represented as ``(path, size)``,
        the file will be created and filled with ``size`` bytes of data.
    :returns: A path to the temporary directory.

    .. note::

        The files and directories are created in the order they appear in the
        list. If a file is specfied in a directory that has not previously been
        created an exception will be thrown.

    >>> create_test_directory(["a", ("a/bla", 12)])
    "/tmp/asdf"
    >>> print list(os.walk("/tmp/asdf"))

    """

    # Note: This will create a directory with permissions 0o700
    temp_dir = tempfile.mkdtemp()

    resolve_path = lambda x: os.path.join(temp_dir, x)

    for i in tree:
        if isinstance(i, str) or isinstance(i, unicode):
            os.mkdir(resolve_path(i), 0o700)
        elif isinstance(i, tuple) and len(i) == 2:
            path, size = i
            with open(resolve_path(path), "w") as f:
                symbols = string.ascii_letters + string.digits
                for i in xrange(size):
                    f.write(random.choice(symbols))
        else:
            raise TypeError("All items in list must be string or two-tuple.")

    return temp_dir

def get_files(path):
    """
    Returns a list of all the files under the given directory. Directories are
    not marked by a trailing slash (so the directory `bar/` would be listed as
    `bar`).

    For example, given a directory tree as below.

    .. code-block::

        + path/
        |    + foo.txt
        |    + bar/
        |        + baz.txt
        |        + qux.txt

    >>> get_files("path")
    ["foo.txt", "bar", "bar/baz.txt", "bar/qux.txt"]

    """

    if not os.path.isdir(path):
        raise TypeError("%s is not a directory." % (path, ))

    test_files = []
    for dir_path, dir_names, file_names in os.walk(path):
        # Iterate through every file and directory in dir_path
        for i in file_names + dir_names:
            # Figure out the full path of i
            cur_path = os.path.join(dir_path, i)

            # Cut off the first part of it (that includes path). So if path
            # is foo, then `foo/bla.txt` becomes `bla.txt`.
            cur_path = os.path.relpath(cur_path, path)

            test_files.append(cur_path)
    return test_files
