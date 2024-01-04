#!/usr/bin/env python

"""Line numbering program."""

import sys


def main():
    """Open file and display numbered lines."""
    if len(sys.argv) != 2:
        _die(f"Usage: {sys.argv[0]} filename", 2)

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                print(f"{i}: {line}", end="")
    except OSError as err:
        _die(f"{sys.argv[0]}: {err}", 1)


def _die(message, error):
    print(message, file=sys.stderr)
    sys.exit(error)


if __name__ == "__main__":
    main()
