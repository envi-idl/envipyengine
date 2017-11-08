"""
Defines exceptions for the ENVI Py Engine package.

"""


class TaskEngineNotFoundError(Exception):
    """Exception gets raised when the user has not configured the engine.

    :Example:

    >>> import envipyengine
    >>> from envipyengine import Engine
    >>> envipyengine.config.set('engine', '')
    >>> envi_engine = Engine('ENVI')
    >>> task_list = envi_engine.tasks()
    # traceback information
    envipyengine.error.TaskEngineNotFoundError: Task Engine executable not found.
    Please verify the 'engine' configuration setting.

    """
    pass


class TaskEngineExecutionError(Exception):
    """Exception is raised when the Task Engine generates an error.

    :Example:

    >>> from envipyengine import Engine
    >>> envi_engine = Engine('ENVI')
    >>> foo = envi_engine.task('Foo')
    >>> foo.parameters
    # traceback information
    envipyengine.error.TaskEngineExecutionError: ENVITASK: No task matches: foo

    """
    pass

class NoConfigOptionError(Exception):
    """Exception is raised when the config option does not exist.

    :Example:

    >>> from envipyengine import config
    >>> config.get('foo')
    # traceback information
    envipyengine.error.NoConfigOptionError: No option 'foo' in section: 'envipyengine'

    """
    pass