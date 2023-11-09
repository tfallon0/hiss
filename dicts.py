def invert(d: dict) -> dict:
    """Invert the dictionary.

    If the dict is not injective an arbitrary choice is made.

    >>> invert({"one":1, "pi":3, "tau":6.283185307179586})
    {1: 'one', 3: 'pi', 6.283185307179586: 'tau'}
    """
    inv_d = {}
    for elm in d:
        inv_d[d[elm]] = elm
    return inv_d
