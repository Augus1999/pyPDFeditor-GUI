# test
def test():
    """Import all function and parameters.

    >>> test()
    1
    """
    try:
        from scripts import __main__, __system__, __version__
        __main__(__system__, __version__, test=True)
        return 1
    except Exception:
        return 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()
