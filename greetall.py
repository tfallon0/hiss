#!/usr/bin/env python

"""Greet all script."""

import sys
from contextlib import ExitStack

from supply import distinct_gen


def greet_all(names_file, greet_file):
    """Output a greeting to greet_file for each unique name that appears in names_file."""
    for name in distinct_gen(filter(None, map(str.strip, names_file))):
        print(f"Hello, {name}!", file=greet_file)


def main():
    """Run the program."""
    if len(sys.argv) > 3:
        _die(f"{sys.argv[0]}: error: too many arguments", 2)
    names = sys.stdin
    greetings = sys.stdout
    try:
        with ExitStack() as stack:
            def opener(arg_index, mode):
                return stack.enter_context(open(sys.argv[arg_index], mode, encoding="utf-8"))

            if len(sys.argv) > 1:
                names = opener(1, "r")
                if len(sys.argv) > 2:
                    greetings = opener(2, "a")

            greet_all(names, greetings)
    except OSError as err:
        _die(f"{sys.argv[0]}: error: {err}", 1)


def _die(message, error):
    print(message, file=sys.stderr)
    sys.exit(error)


if __name__ == "__main__":
    main()
