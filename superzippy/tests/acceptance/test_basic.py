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
This module tests basic functionality of Super Zippy (ie: can it make a Super
Zip from a simple pure-Python project with no dependencies?).

"""

# stdlib
import subprocess
import tempfile
import shutil
import os
import sys

# external
import pytest

# internal
from . import sample_info

@pytest.mark.parametrize("sample", sample_info.list_samples())
def test_sample(sample):
    """
    Initiates testing on all of the samples.

    """

    sample_dir = sample_info.get_sample_dir(sample)
    config = sample_info.get_sample_config(sample)

    for i in config.get_entry_points():
        temp_dir = tempfile.mkdtemp()
        try:
            zip_process = subprocess.Popen(
                ["superzippy", "-vvv", sample_dir, i.name],
                cwd = temp_dir
            )
            zip_process.wait()

            superzip_path = \
                os.path.join(temp_dir, config.get_package_name()) + ".sz"

            assert os.path.exists(superzip_path), \
                "%s doesn't exist" % (superzip_path, )

            assert os.access(superzip_path, os.X_OK), \
                "%s is not executable" % (superzip_path, )

            # Check that we get the right output
            for args, output, returncode in i.expected_output:
                test_process = subprocess.Popen(
                    [superzip_path] + args,
                    stdout = subprocess.PIPE,
                    cwd = temp_dir
                )
                test_process.wait()

                decoded_output = test_process.stdout.read()
                decoded_output = \
                    decoded_output.decode(sys.stdout.encoding or "UTF-8")

                assert decoded_output == output
                assert test_process.returncode == returncode
        finally:
            shutil.rmtree(temp_dir)
