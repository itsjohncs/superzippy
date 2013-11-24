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

# stdlib
import pkg_resources
import os
import re
try:
    import ConfigParser as configparser # Python 2.x
except ImportError:
    import configparser # Python 3.x

def get_sample_dir(name = None):
    """
    Returns a path containing the sample ``name``. Will extract the sample
    directory if necessary (if we're in a zip file). If ``None`` is given for
    ``name``, a path to the ``samples/`` directory will be returned.

    """

    samples_dir = pkg_resources.resource_filename(
        "superzippy.tests.acceptance", "samples")
    if not os.path.exists(samples_dir):
        raise RuntimeError("Could not retrieve samples directory.")

    if name is None:
        return samples_dir
    else:
        result = os.path.join(samples_dir, name)
        if not os.path.exists(result):
            raise ValueError("Could not find sample %s." % (name, ))

        return result

def list_samples():
    """
    Returns a list of all of the samples available.

    >>> list_samples()
    ["simple", "readme"]

    """

    samples_dir = get_sample_dir()

    def is_sample(name):
        "Returns True if name is a valid sample."

        return (os.path.isdir(os.path.join(samples_dir, name)) and
            os.path.isfile(os.path.join(samples_dir, name, "testing.ini")))

    open("/tmp/outputbla.txt", "w").write(
        str(os.listdir(samples_dir)) + "\n" + str(filter(is_sample, os.listdir(samples_dir))))

    return filter(is_sample, os.listdir(samples_dir))

class SampleConfig:
    def __init__(self, sample_name, parser):
        self.sample_name = sample_name
        self._parser = parser

    def get_package_name(self):
        return self._parser.get("info", "name")

    def is_python_supported(self, version_string):
        try:
            regex = self._parser.get("info", "supports_python")
        except:
            return True

        return re.match(regex, version_string) is not None

    class EntryPoint:
        def __init__(self, name, expected_output, options):
            self.name = name
            self.expected_output = expected_output
            self.options = options

    def get_entry_points(self):
        sections = [i for i in self._parser.sections() if
            i.startswith("entry_point")]

        result = []
        for i in sections:
            try:
                expected_output = eval(self._parser.get(i, "expected_output"))
            except configparser.NoOptionError:
                expected_output = []

            try:
                options = eval(self._parser.get(i, "options"))
            except configparser.NoOptionError:
                options = []

            result.append(SampleConfig.EntryPoint(
                name = self._parser.get(i, "name"),
                expected_output = expected_output,
                options = options
            ))

        return result

def get_sample_config(name):
    """
    Returns a dict containing the configuration of the given sample project.
    The configuration will be pulled from the sample's ``testing.ini`` file.

    """

    parser = configparser.SafeConfigParser()
    parser.read(os.path.join(get_sample_dir(name), "testing.ini"))

    return SampleConfig(name, parser)
