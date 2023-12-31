#!/usr/bin/env python

"""Script to read names from input and emit greetings as output."""

import contextlib
import sys


def greet(name, *, file=None):
    R"""
    Greet someone by name.

    >>> greet('Alice Bobson')
    Hello, Alice Bobson!

    >>> import io
    >>> outfile = io.StringIO()
    >>> greet('Bob Alistair', file=outfile)
    >>> outfile.getvalue()
    'Hello, Bob Alistair!\n'
    """
    print(f'Hello, {name}!', file=file)


def greetall(infile, outfile):
    R"""
    Read names, one per line, from infile, and greet them to outfile.

    >>> import io
    >>> infile = io.StringIO('Alice Bobson \n\t\nBob Alistair\nAlice Bobson\n')
    >>> outfile = io.StringIO()
    >>> greetall(infile, outfile)
    >>> outfile.getvalue()
    'Hello, Alice Bobson!\nHello, Bob Alistair!\n'
    """
    names = set()
    for line in infile:
        name = line.strip()
        if not name or name in names:
            continue
        names.add(name)
        greet(name, file=outfile)


def die(status, message):
    """Fail with an error."""
    print(f'{sys.argv[0]}: error: {message}', file=sys.stderr)
    sys.exit(status)


def main():
    """Run the over-glorified hello-world program."""
    if len(sys.argv) > 3:
        die(2, 'too many arguments')

    try:
        with contextlib.ExitStack() as stack:
            def enter_open(path, mode):
                return stack.enter_context(
                    open(path, mode=mode, encoding='utf-8'),
                )

            infile = sys.stdin
            outfile = sys.stdout
            if len(sys.argv) > 1:
                infile = enter_open(sys.argv[1], 'r')
            if len(sys.argv) > 2:
                outfile = enter_open(sys.argv[2], 'x')
            greetall(infile, outfile)
    except OSError as error:
        die(1, str(error))


if __name__ == '__main__':
    main()
