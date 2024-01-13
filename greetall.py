#!/usr/bin/env python

"""Greet all script."""

from contextlib import nullcontext, ExitStack
import sys

from supply import distinct_gen


def greet_all(names_file, greet_file):
    for name in distinct_gen(filter(None, map(str.strip, names_file))):
        print(f"Hello, {name}!", file=greet_file)


def main():
    if len(sys.argv) > 3:
        _die(f"{sys.argv[0]}: error: too many arguments", 2)
    file = sys.stdin
    greetings = sys.stdout
    try:
        with ExitStack() as stack:
            if len(sys.argv) > 1:
                file = stack.enter_context(open(sys.argv[1], "r", encoding="utf-8"))
                if len(sys.argv) > 2:
                    greetings = stack.enter_context(open(sys.argv[2], "a", encoding="utf-8"))
            greet_all(file, greetings)
    except OSError as err:
        _die(f"{sys.argv[0]}: error: {err}", 1)


def _die(message, error):
    print(message, file=sys.stderr)
    sys.exit(error)


if __name__ == "__main__":
    main()
