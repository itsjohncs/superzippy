# This file contains code primarily found from stack overflow, see there for
# licensing terms.

"""
Module for finding out where the current script is being executed from.

.. author: Daniel Stutzbach, http://stackoverflow.com/a/2632297/1989056

"""

import os, os.path
import sys


try:
    unicode
except NameError:
    unicode = str


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        try:
            filename = unicode(sys.executable, encoding)
        except TypeError:
            filename = sys.executable
    else:
        try:
            filename = unicode(__file__, encoding)
        except TypeError:
            filename = __file__
    return os.path.dirname(filename)
