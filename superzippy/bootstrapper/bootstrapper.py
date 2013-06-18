#!/usr/bin/env python

import zipsite
import superconfig
import module_locator
import os.path

zipsite.addsitedir(
	os.path.abspath(os.path.join(
		module_locator.module_path(), "lib", "python2.7", "site-packages"
	)),
	prepend_mode = True
)

# Entry point is expected to be in the form module:function
load_module, run_func = superconfig.entry_point.split(":")

module = __import__(load_module, fromlist = [run_func])

getattr(module, run_func)()
