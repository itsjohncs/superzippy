#!/usr/env/bin python

from clint.textui import puts, colored
import sys

def foo():
    puts(colored.red("I am a mighty foo function!"))
    sys.exit(0)

def bar():
    puts(colored.blue("Nice to meet you, I am bar."))
    sys.exit(1)

if __name__ == "__main__":
    puts("Running as a script!")
    sys.exit(2)
