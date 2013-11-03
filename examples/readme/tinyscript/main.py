#!/usr/env/bin python

import sys

def foo():
    print "I am a mighty foo function!"
    sys.exit(0)

def bar():
    print "Nice to meet you, I am bar."
    sys.exit(1)

if __name__ == "__main__":
    print "Running as a script!"
    sys.exit(2)
