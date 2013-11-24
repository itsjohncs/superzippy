#!/usr/env/bin python

from yaml import load, dump
try:
    # We want this to error because a Super Zip can't have shared libs in it.
    from yaml import CLoader as Loader, CDumper as Dumper
    assert False, "Should not be able to access shared libraries."
except ImportError:
    from yaml import Loader, Dumper

try:
    unicode
except NameError:
    unicode = str

import sys

def parse_list():
    data = load(sys.argv[1])
    for i in data:
        sys.stdout.write(str(i) + "\n")

def parse_tuple_list():
    data = load(sys.argv[1])
    for k, v in data:
        sys.stdout.write(str(k) + " " + str(v) + "\n")

if __name__ == "__main__":
    if sys.argv[2] == "list":
        parse_list()
    else:
        parse_dict()
    sys.exit(1)
