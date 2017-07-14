"""
Defines exceptions for the ENVI Py Engine package.

"""


class TaskEngineNotFoundError(Exception):
    """Exception gets raised when the user has not configured the envi-install-dir.

    :Example:

    >>> import envipyengine
    >>> from envipyengine import Engine
    >>> envipyengine.config.set('envi-install-dir', '')
    >>> envi_engine = Engine('ENVI')
    >>> task_list = envi_engine.tasks()
    # traceback information
    envipyengine.error.TaskEngineNotFoundError: Task Engine executable not found.
    Please verify the 'envi-install-dir' configuration setting.

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
