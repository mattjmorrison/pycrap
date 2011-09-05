def partial(func, *args, **keywords):
    """
    Taken from http://docs.python.org/library/functools.html
    because functools is not available for Python2.4
    """
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc