Super Zippy
===========

Super Zippy will take a Python package and create a single executable file out of it that you can distribute to all your Linux user friends.

.. code-block:: bash

	$ echo "entry_point = 'superzippy.packaging:run'" > superconfig.py
	$ superzippy superzippy

And now we have a single file containing all of Super Zippy's dependencies and code. No installation necessary.

Authors
-------

John Sullivan

License
-------

Apache License v2.0
