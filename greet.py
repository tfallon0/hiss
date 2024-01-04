#!/usr/bin/env python

"""Greeting script."""

from sys import argv


def main():
    """Run the greeting program."""
    if len(argv) == 1:
        try:
            name = input("Hello, who are you? ")
        except EOFError:
            name = "World"
        greet(name)
    else:
        for name in argv[1:]:
            greet(name)


def greet(name):
    """Greet by name."""
    print(f"Hello {name}!")


if __name__ == "__main__":
    main()
