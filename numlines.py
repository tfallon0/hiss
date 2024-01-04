#!/usr/bin/env python

"""Line numbering program."""

import sys


def main():
    """Open file and display numbered lines."""
    if len(sys.argv) != 2:
        print("Usage: numlines.py filename", file=sys.stderr)
        sys.exit(2)

    file = open(sys.argv[1], "r", encoding="utf-8")
    try:
        i = 0
        for line in file:
            print(f"{i}: {line}", end="")
            i += 1
    finally:
        file.close()


if __name__ == "__main__":
    main()
