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
This module tests the file_utilities module which is itself used only in other
tests.

"""

# futures
from __future__ import with_statement

# test helpers
import superzippy.tests.file_utilities as file_utilities

# external
import pytest

# stdlib
import sys
import os
import os.path
import shutil
import tempfile

class TestGetFiles:
    def test_basic(self):
        """
        Create a directory tree and make sure we get the right result.

        """

        temp_dir = tempfile.mkdtemp()
        resolve = lambda *x: os.path.join(temp_dir, *x)
        try:
            os.mkdir(resolve("a"))
            os.mkdir(resolve("b"))
            open(resolve("a", "foo"), "w").close()
            open(resolve("a", "bar"), "w").close()
            desired_tree = set(["a", "b", "a/foo", "a/bar"])

            assert set(file_utilities.get_files(temp_dir)) == desired_tree
        finally:
            shutil.rmtree(temp_dir)

class TestCreateTestDirectory:
    good_cases = [
        ["a", "b", "c", ("a/foo", 1000), ("a/bar", 1000)],
        ["a", ("a/foo", 0)],
        [("bar", 1000)],
        ["bar"]
    ]

    @pytest.mark.parametrize("test_case", good_cases)
    def test_existence(self, test_case):
        """
        Ensure that all the files that were supposed to get created are there,
        and ensure that none were created that weren't supposed to be.

        """

        test_dir = file_utilities.create_test_directory(test_case)
        try:
            real_contents = file_utilities.get_files(test_dir)
            expected_contents = \
                [(i[0] if isinstance(i, tuple) else i) for i in test_case]

            sys.stdout.write("real_contents = %s\n" % (real_contents, ))
            sys.stdout.write(
                "expected_contents = %s\n" % (expected_contents, ))

            assert set(real_contents) == set(expected_contents)
        finally:
            shutil.rmtree(test_dir)

    @pytest.mark.parametrize("test_case", good_cases)
    def test_files_sizes(self, test_case):
        """
        Ensures that the files created are the correct size.

        """

        test_dir = file_utilities.create_test_directory(test_case)
        try:
            for i in test_case:
                if isinstance(i, tuple):
                    sys.stdout.write("checking size of %s\n" % (i[0], ))
                    file_size = os.stat(
                        os.path.join(test_dir, i[0])).st_size
                    assert file_size == i[1]
        finally:
            shutil.rmtree(test_dir)

