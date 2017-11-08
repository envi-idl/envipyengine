"""
Tests the tasks running through the config environment
"""

import unittest
import os
import shutil


import envipyengine
from envipyengine import Engine
from envipyengine.error import NoConfigOptionError

from .. import test

class TestTaskEnv(unittest.TestCase):
    """
    Test the Task Engine environment options.
    """

    @classmethod
    def setUpClass(cls):

        cls.user_file = envipyengine.config._USER_CONFIG_FILE


        #backup exsisting config files on the machine
        if os.path.exists(cls.user_file):
            # Only save the engine path
            engine_path = None
            try:
                engine_path = envipyengine.config.get('engine')
            except NoConfigOptionError: 
                pass
            os.rename(cls.user_file, cls.user_file + '.bak')
            envipyengine.config.set('engine', engine_path)

        cls.sys_file = envipyengine.config._SYSTEM_CONFIG_FILE
        if os.path.exists(cls.sys_file):
            engine_path = None
            try:
                engine_path = envipyengine.config.get('engine')
            except NoConfigOptionError:
                pass
            os.rename(cls.sys_file, cls.sys_file + '.bak')
            envipyengine.config.set('engine', engine_path, system=True)

        envipyengine.config.set_environment({'IDL_PATH': '%s;<IDL_DEFAULT>' % test.task_dir()})

    @classmethod
    def tearDownClass(cls):
        cls._clean_files([cls.user_file, cls.sys_file])
        #replace backup files on the machine
        if os.path.exists(cls.user_file + '.bak'):
            os.rename(cls.user_file + '.bak', cls.user_file)

        if os.path.exists(cls.sys_file + '.bak'):
            os.rename(cls.sys_file + '.bak', cls.sys_file)

    def test_cwd_execute(self):
        """
        Verify the engine gets the current working directory from the task.execute.
        Also verifies environment variables are set by the engine.
        """
        python_cwd = os.getcwd()
        expected_dir = test.workspace_dir()
        # Running this test from the workspace defeats the purpose of this test
        self.assertNotEqual(python_cwd.lower(), expected_dir.lower(),
                            'cwd cannot be the workspace dir')


        getcwd_task = Engine('IDL').task('getcwd')
        actual = getcwd_task.execute({}, cwd=expected_dir)
        self.assertEqual(actual['outputParameters']['CWD'], expected_dir)

    def test_cwd_engine(self):
        """
        Verify the engine gets the current working directory from the Engine object.
        """
        python_cwd = os.getcwd()
        expected_dir = test.workspace_dir()
        # Running this test from the workspace defeats the purpose of this test
        self.assertNotEqual(python_cwd.lower(), expected_dir.lower(),
                            'cwd cannot be the workspace dir')

        getcwd_task = Engine('IDL', cwd=expected_dir).task('getcwd')
        actual = getcwd_task.execute({})
        self.assertEqual(actual['outputParameters']['CWD'], expected_dir)

    @classmethod
    def _clean_files(cls, filenames):
        """ Convenience method for cleaning up config files """
        for _file in filenames:
            if os.path.exists(_file):
                os.remove(_file)
