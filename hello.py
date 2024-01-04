#!/usr/bin/env python
"""Hello World Program Hello =D"""  # noqa: D400 D415


def main(*, script=False):
    """Print a friendly greeting."""
    print("hello world" if script else "hel-load world")


main(script= __name__ == "__main__")
