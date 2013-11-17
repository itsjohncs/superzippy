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

# test helpers
from . import file_utilities

# external
import pytest

# internal
from .. import zipdir

# stdlib
from contextlib import closing
import zipfile
import tempfile
import shutil
import os
import sys

class TestZipDir:
    good_cases = [
        ["a", "b", ("a/foo", 1000), ("a/bar", 1000), ("b/baz", 1000)],
        ["a", ("a/foo", 0)],
        [("bar", 1000)]
    ]

    @pytest.fixture
    def zip_tree(self, request, test_case):
        try:
            # We must create these variables up front for our finally
            # statement to work correctly.
            test_dir = zip_file = unzip_dir = None

            # Create some files and directories to zip up
            test_dir = file_utilities.create_test_directory(test_case)

            # Get a temporary file that will become our zip file
            zip_file_handle = tempfile.NamedTemporaryFile(delete = False)
            zip_file_handle.close()
            zip_file = zip_file_handle.name

            # Zip up our directory tree
            zipdir.zip_directory(test_dir, zip_file)

            # Unzip our directory tree
            unzip_dir = tempfile.mkdtemp()
            with closing(zipfile.ZipFile(zip_file, "r")) as f:
                f.extractall(unzip_dir)
        except:
            if test_dir is not None:
                shutil.rmtree(test_dir)

            if zip_file is not None:
                os.remove(zip_file)

            if unzip_dir is not None:
                shutil.rmtree(unzip_dir)

            raise

        def cleanup():
            shutil.rmtree(test_dir)
            os.remove(zip_file)
            shutil.rmtree(unzip_dir)
        request.addfinalizer(cleanup)

        return test_dir, zip_file, unzip_dir

    @pytest.mark.parametrize("test_case", good_cases)
    def test_existence(self, zip_tree, test_case):
        """
        Ensure that all the files that were supposed to get zipped up make it
        it into the archive, and ensure that none got in that were not
        supposed to.

        """

        test_dir, zip_file, unzip_dir = zip_tree

        real_contents = file_utilities.get_files(unzip_dir)
        expected_contents = file_utilities.get_files(test_dir)

        sys.stdout.write("real_contents = %s\n" % (str(real_contents), ))
        sys.stdout.write(
            "expected_contents = %s\n" % (str(expected_contents), ))

        assert set(real_contents) == set(expected_contents)


    @pytest.mark.parametrize("test_case", good_cases)
    def test_files_sizes(self, zip_tree, test_case):
        """
        Ensures that the files created are the correct size.

        """

        test_dir, zip_file, unzip_dir = zip_tree

        for i in test_case:
            if isinstance(i, tuple):
                sys.stdout.write("checking size of %s\n" % (i[0], ))
                file_size = os.stat(
                    os.path.join(test_dir, i[0])).st_size
                assert file_size == i[1]
