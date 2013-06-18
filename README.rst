Super Zippy
===========

I have a dream that python package distribution is super easy and super zippy, and I will make this dream a reality.

Todo
----

Chris hacked together something that will work for the Galah API Client, which is the intended user of this library, so in the spirit of not draining tons of time into something that's not too important, I'm going to shelf this project. Hopefully it'll come off the shelf one day though. Here's my current status:

The zipsite module seems to work fully as a replacement to the standard site module. This is great and it means that the Python path is now automatically modified by zipsite to include any modules in the zip file.

What needs to be done from here is add in Python import hooks to make it so we can import from the new paths easily, because it seems that by default, just adding the modules in the zip file to the path is not sufficient.

Once that is done, we just need to add a bootstrapping sort of file template that will automatically call zipsite, add the import hooks, then execute whatever script file the user provided. This should complete the effort.

Of course we also need to create a script that will use distibute or w/e to install everything into a single directory (use the ``--home`` command line option and friends). Then just pointing zipsite at the correct place will make the magic happen.

It may be worthwhile to try and get this into the Python standard library as well as this could be fairly useful, but I'm not sure what Python 3 has in store for this (hell, maybe they already do this.. might be worth verifying one way or the other).

May your day be super zippy!

Authors
-------

John Sullivan

License
-------

None yet, you have no license to use this O.O. I'll stick licensing around when I'm ready, it'll be under Apache v2.0. If you're impatient badger me with emails.

Delicious
---------

Yes it is.
