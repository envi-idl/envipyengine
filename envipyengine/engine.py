"""
The ENVI Py Engine object selects a task engine to use with ENVI Py
"""

from __future__ import absolute_import
from abc import abstractmethod, abstractproperty
from string import Template
from .envipymeta import ENVIPyMeta
from .utils import with_metaclass


class Engine(with_metaclass(ENVIPyMeta, object)):
    """
    The ENVI Py Engine Class.

    :Example:

    Import the module for the example

    >>> from envipyengine import Engine
    >>> from pprint import pprint

    Create an ENVI Engine and print a list of available tasks.

    >>> envi_engine = Engine('ENVI')
    >>> tasks = envi_engine.tasks()
    >>> pprint(tasks)
    ['AdditiveLeeAdaptiveFilter',
     'AdditiveMultiplicativeLeeAdaptiveFilter',
     'ApplyGainOffset',
     ...

    """

    @abstractmethod
    def __init__(self, engine_name, cwd=None):
        """
        Returns an ENVI Py Engine object based on the engine_name.

        :param engine_name: A String specifying the name of the requested engine.
        :param cwd: A String representing the current working directory
                    for the engine execution.
        :return: None
        """
        pass

    @abstractmethod
    def task(self, task_name):
        """
        Returns an ENVI Py Engine Task object. See ENVI Py Engine Task for examples.

        :param task_name: The name of the task to retrieve.
        :return: An ENVI Py Engine Task object.
        """
        pass

    @abstractmethod
    def tasks(self):
        """
        Returns a list of all tasks known to the engine.

        :return: A list of task names.
        """
        pass

    @abstractproperty
    def name(self):
        """
        Returns the name of the task engine associated with the Engine.

        :return: The task engine name (i.e. ENVI, IDL, etc.)
        """
        pass

    def __str__(self):
        props = dict(name=self.name)
        return Template('''Engine (${name})''').substitute(props)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()
