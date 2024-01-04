#!/usr/bin/env python

"""Line numbering program."""

import sys


def main():
    """Open file and display numbered lines."""
    if len(sys.argv) != 2:
        print("Usage: numlines.py filename", file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1], "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            print(f"{i}: {line}", end="")


if __name__ == "__main__":
    main()
