"""
Module for finding out where the current script is being executed from.

.. author: Daniel Stutzbach, http://stackoverflow.com/a/2632297/1989056

"""

import os, os.path
import sys

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))
