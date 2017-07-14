"""
Contains utility decorator objects
"""
import functools


def memoize(obj):
    """Decorator function caches the return value of a function based on its input arguments."""
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        """Decorator function caches the return value of a function based on its input arguments."""
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer
