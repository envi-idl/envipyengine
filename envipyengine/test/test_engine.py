"""
Tests the GSF Task interface
"""

import unittest

from envipyengine import Engine
from envipyengine import Task
from envipyengine.error import TaskEngineExecutionError


class TestEngine(unittest.TestCase):
    """
    Test the ENVI Py Engine
    """

    def test_name(self):
        """Verify Engine.name returns a string."""
        engine = Engine('ENVI')
        self.assertIsInstance(engine.name, str)

    def test_invalid_engine(self):
        """Verify Invalid Engine Name Raises an Exception when used"""
        with self.assertRaises(TaskEngineExecutionError):
            engine = Engine('FOO')
            # pylint: disable=unused-variable
            task_list = engine.tasks()

    def test_tasks_method(self):
        """Verify Engine.tasks() returns a list of strings"""
        engine = Engine('ENVI')
        tasks = engine.tasks()
        self.assertIsInstance(tasks, list)

    def test_task_method(self):
        """Verify Engine.task() returns a Task object"""
        engine = Engine('ENVI')
        task = engine.task('SpectralIndex')
        self.assertIsInstance(task, Task)
