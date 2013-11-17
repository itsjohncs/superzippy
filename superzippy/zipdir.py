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

"""
Module that provides a useful function that can be used to zip up an entire
directory.

"""

# future
from __future__ import with_statement

# stdlib
from contextlib import closing
import zipfile
import os

def zip_directory(path, output_file, compression = zipfile.ZIP_DEFLATED):
    """
    Compresses the directory at ``path`` into a zip file at ``output_file``.

    .. note::

        Empty directories are not added to the zip file.

    .. note::

        Creating empty zip files is not supported on version < 2.7.1.

    """

    with closing(zipfile.ZipFile(output_file, "w", compression)) as f:
        for dir_path, dir_names, file_names in os.walk(path):
            for i in file_names:
                file_path = os.path.join(dir_path, i)
                f.write(file_path, os.path.relpath(file_path, path))
