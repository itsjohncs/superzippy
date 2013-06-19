Super Zippy
===========

Super Zippy takes a Python package and its pure Python dependencies and transforms them all into a single executable file.

This is similar to [cx_Freeze](http://cx-freeze.sourceforge.net/) except that it does not attempt to deal with non-pure Python dependencies and thus is much lighter weight and easier to use.

Examples
--------

.. code-block:: bash

	$ superzippy superzippy superzippy.packaging:run
	$ ./superzippy
	Usage: superzippy [options] [PACKAGE] [ENTRY POINT]

	superzippy: error: Exactly two arguments must be supplied.

And now we have a single file containing all of Super Zippy's dependencies and code. We can send this single file (called ``superzippy`` above) to anyone and as long as they already have Python installed they can just run the file.

How it Works
------------

It installs the Python package you specify into a ``virtualenv`` using ``pip`` (so anything you can tell ``pip`` to install can be given to ``superzippy``), then grabs the site-packages directoy out of the virtual environment and sticks it in a zip file along with some super bootstrapping code. Then it just makes the zip file executable.

Motivation
----------

I created this for a tool called the `Galah API Client <https://www.github.com/galah-group/galah-apiclient>`_ which is a simple tool that has only pure Python dependencies. It is basically a script but since it is a little complex I didn't want everything to be in a single file as that gets tedious fast... But I still wanted a good way to distribute it to my users who are not Python developers, may not have root access, and don't want to deal with ``virtualenv`` and ``pip``.

Authors
-------

`John Sullivan <http://brownhead.github.io>`_

License
-------

Apache License v2.0 (see LICENSE)
