"""
The ENVI Py Engine task object provides task information and can submit a job to the Task Engine with input.
"""
from __future__ import absolute_import
from abc import abstractmethod, abstractproperty
from string import Template
from pprint import PrettyPrinter
from .envipymeta import ENVIPyMeta
from .utils import with_metaclass


class Task(with_metaclass(ENVIPyMeta, object)):
    """
    The ENVI Py Engine Task object represents a Task Engine task and its parameters.

    :Example:

    Import the modules for the example.

    >>> from envipyengine import Engine
    >>> from pprint import pprint

    Create an Engine object for ENVI and get a task

    >>> envi_engine = Engine('ENVI')
    >>> task = envi_engine.task('SpectralIndex')

    Investigate task information.

    >>> print(task.name)
    'SpectralIndex'
    >>> print(task.description, type(task.description))
    ('This task creates a spectral index raster from one pre-defined spectral
    index. Spectral indices are combinations of surface reflectance at two
    or more wavelengths that indicate relative abundance of features of
    interest.', <type 'str'>)
    >>> print(task.display_name, type(task.display_name))
    ('Spectral Index', <type 'str'>)
    >>> task_parameters = task.parameters
    >>> pprint(task_parameters)

    Execute a job using the Task Engine

    >>> input_raster = dict(url='C:\\Program Files\\Harris\\ENVI54\\data\\qb_boulder_msi',
                            factory='URLRaster')
    >>> parameters = dict(INPUT_RASTER=input_raster,
                          INDEX='Normalized Difference Vegetation Index')
    >>> result = task.execute(parameters)


    """

    def __str__(self):
        pretty_print = PrettyPrinter(indent=2)
        props = dict(name=self.name,
                     display_name=self.display_name,
                     description=self.description,
                     parameters=pretty_print.pformat(self.parameters))
        return Template('''
name: ${name}
display_name: ${display_name}
description: ${description}
parameters: ${parameters}
''').substitute(props)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    @abstractmethod
    def __init__(self, uri=None, cwd=None):
        """
        Returns an ENVI Py Engine Task object based on the task name.

        :param uri: A String representing the unique id of the task.
        :param cwd: A String representing the current working directory
                    for the engine execution.
        :return: None
        """
        self._uri = uri
        self._cwd = cwd

    @abstractproperty
    def name(self):
        """
        The name of the task

        :return: a string
        """
        pass

    @abstractproperty
    def display_name(self):
        """
        The display name of the task

        :return: a string
        """
        pass

    @abstractproperty
    def description(self):
        """
        The task description

        :return: a string
        """
        pass

    @abstractproperty
    def uri(self):
        """
        The task unique identifier
        """
        pass

    @abstractproperty
    def parameters(self):
        """
        A list of the task parameter definitions. Each task parameter is a dictionary containing, but not
        limited to, the following keys:

        ================= ========== ================= ==========================================================
        Key               Data Type  Type              Description
        ================= ========== ================= ==========================================================
        name              string     Required          The name of the parameter
        display_name      string     Required          The display name of the parameter
        type              string     Required          The parameter data type
        direction         string     Required          Can be *input* or *output*
        description       string     Required          The parameter description
        required          bool       Required          Indicates if the parameter is required
                                                       on input when submitting a job
        dimensions        string     Optional          Indicates if the parameter is an array if set.  Dimesions
                                                       is of the format *[dim1,dim2,...]*
        choice_list       list       Optional          A list of available choices for the parameter input
        min               type       Optional          The minimum value allowed for the parameter
        max               type       Optional          The maximum value allowed for the parameter
        ================= ========== ================= ==========================================================

        :return: a list of parameter dictionaries
        """
        pass

    @abstractmethod
    def execute(self, parameters, cwd=None):
        """
        Executes a synchronous task using the Task Engine

        :param parameters: A dictionary of key-value pairs of parameter names and values. The dictionary serves as input to the job.
        :param cwd: Set to the current working directory the engine will run in.  Defaults to the python current working directory if none specified.
        :return: A dictionary containing the Task Engine output.
        """
        pass
