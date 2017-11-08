"""
The ENVI Py Engine object selects a task engine to use with ENVI Py
"""

from . import taskengine
from ..decorators import memoize
from .task import Task
from ..engine import Engine as BaseEngine


class Engine(BaseEngine):
    """
    The ENVI Py Engine Class.
    """

    def __init__(self, engine_name, cwd=None):
        """
        Returns an ENVI Py Engine object based on the engine_name.

        :param engine_name: A String specifying the name of the requested engine.
        :return: None
        """
        super(Engine, self).__init__(engine_name)
        self._engine_name = engine_name
        self._cwd = cwd

    def task(self, task_name):
        """
        Returns an ENVI Py Engine Task object. See ENVI Py Engine Task for examples.

        :param task_name: The name of the task to retrieve.
        :return: An ENVI Py Engine Task object.
        """
        return Task(uri=':'.join((self._engine_name, task_name)), cwd=self._cwd)

    @memoize
    def tasks(self):
        """
        Returns a list of all tasks known to the engine.

        :return: A list of task names.
        """
        task_input = {'taskName': 'QueryTaskCatalog'}
        output = taskengine.execute(task_input, self._engine_name, cwd=self._cwd)
        return output['outputParameters']['TASKS']

    @property
    def name(self):
        """
        Returns the name of the task engine associated with the Engine.

        :return: The task engine name (i.e. ENVI, IDL, etc.)
        """
        return self._engine_name
