"""
ENVI Metaclass for overriding string representations.
"""
from abc import ABCMeta


class ENVIPyMeta(ABCMeta):
    """
    ENVI Metaclass for overriding string representations.
    """
    def __repr__(cls):
        return '{0}.{1}'.format(__package__, cls.__name__)
