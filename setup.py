#!/usr/bin/env python
import os
from setuptools import setup, find_packages

def read(fname):
    """
    Returns the contents of the file in the top level directory with the name
    ``fname``.

    """

    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_files(path):
    relative_to = os.path.dirname(path)
    result = []
    for dirpath, dirnames, filenames in os.walk(path):
        result += [os.path.relpath(os.path.join(dirpath, i), relative_to)
            for i in filenames]
    return result

setup(
	name = "superzippy",
    version = read("VERSION").strip(),
    author = "John Sullivan and other contributers",
    author_email = "john@galahgroup.com",
    description = (
        "A Python utility for packaging up multi-file Python scripts into a "
        "single file, dependencies and all."
    ),
    license = "Apache v2.0",
    keywords = "python packaging",
    url = "https://www.github.com/brownhead/superzippy",
    long_description = read("README.rst"),
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License"
    ],
    packages = find_packages(),
    entry_points = {
        "console_scripts": [
            "superzippy = superzippy.packaging:run"
        ]
    },
    # This ensures that the MANIFEST.IN file is used for both binary and source
    # distributions.
    include_package_data = True,
    zip_safe = True,
    data_files = [
        (".", ["LICENSE", "README.rst", "VERSION"])
    ]
)
