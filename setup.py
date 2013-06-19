#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "superzippy",
    version = read("VERSION"),
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
    zip_safe = True,
    data_files = [
        (".", ["LICENSE", "README.rst", "VERSION"])
    ]
)
