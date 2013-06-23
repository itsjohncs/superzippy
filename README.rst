Super Zippy
===========

Super Zippy takes a Python package and its pure Python dependencies and transforms them all into a single executable file.

This is similar to `cx_Freeze <http://cx-freeze.sourceforge.net/>`_ except that it does not attempt to deal with non-pure Python dependencies and thus is much lighter weight and easier to use.

Examples
--------

Let's say we want to user Super Zippy on itself to create a single file containing all of Super Zippy's dependencies and code.

.. code-block:: bash

	$ superzippy superzippy superzippy.packaging:run
	$ ./superzippy
	Usage: superzippy [options] [PACKAGE1 PACKAGE2 ...] [ENTRY POINT]

	superzippy: error: 1 or more arguments must be supplied.

We can send this single file (called ``superzippy`` above) to anyone and as long as they already have Python installed they can just run the file.

How it Works
------------

It installs the Python package you specify into a ``virtualenv`` using ``pip`` (so anything you can tell ``pip`` to install can be given to ``superzippy``), then grabs the site-packages directory out of the virtual environment and sticks it into a zip file along with some [super bootstrapping code](https://github.com/brownhead/superzippy/tree/master/superzippy/bootstrapper). Then it just [makes the zip file executable](http://sayspy.blogspot.com/2010/03/various-ways-of-distributing-python.html) by adding a proper shebang to it and flipping its executable bit.

Motivation
----------

I created this for a tool called the `Galah API Client <https://www.github.com/galah-group/galah-apiclient>`_ which is a simple tool that has only pure Python dependencies. It is basically a script but since it is a little complex I didn't want everything to be in a single file as that gets tedious fast... But I still wanted a good way to distribute it to my users who are not Python developers, may not have root access, and don't want to deal with ``virtualenv`` and ``pip``.

Installing
----------

To install Super Zippy, just run

.. code-block:: shell

	$ pip install superzippy

You can also install from the ``setup.py`` script yourself of course, or you can even create a super zipped up version of Super Zippy using Super Zippy. ``pip`` is probably the easiest way to go though if you're already familiar with Python packages.

Authors
-------

`John Sullivan <http://brownhead.github.io>`_

License
-------

Apache License v2.0 (see LICENSE)
