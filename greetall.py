#!/usr/bin/env python

"""Greet all script."""

import contextlib
import sys

from supply import distinct_gen


def greet_all(names_file, greet_file):
    for name in distinct_gen(filter(None, map(str.strip, names_file))):
        print(f"Hello, {name}!", file=greet_file)


def main():
    if len(sys.argv) > 3:
        _die(f"{sys.argv[0]}: error: too many arguments", 2)
    try:
        if len(sys.argv) < 2:
            ncm = contextlib.nullcontext(sys.stdin)
        else:
            ncm = open(sys.argv[1], "r", encoding="utf-8")
        with ncm as file:
            if len(sys.argv) < 3:
                gcm = contextlib.nullcontext(sys.stdout)
            else:
                gcm = open(sys.argv[2], "a", encoding="utf-8")
            with gcm as greetings:
                greet_all(file, greetings)
    except OSError as err:
        _die(f"{sys.argv[0]}: error: {err}", 1)


def _die(message, error):
    print(message, file=sys.stderr)
    sys.exit(error)


if __name__ == "__main__":
    main()
