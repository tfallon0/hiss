#!/usr/bin/env python

"""Hello World Program Hello =D"""  # noqa: D400 D415

_GREETINGS = ["hel-load world", "hello world"]


def main(*, script=False):
    """
    Print a friendly greeting.

    >>> main(script=False)
    hel-load world

    >>> main(script=True)
    hello world
    """
    print(_GREETINGS[script])


main(script= __name__ == "__main__")
