"""
Tests the GSF Task interface
"""

import unittest
import os


from ..error import NoConfigOptionError
import envipyengine


class TestEngine(unittest.TestCase):
    """
    Test the ENVI Py Engine Config
    """
    def _clean_files(self, filenames):
        """ Convenience method for cleaning up config files """
        for _file in filenames:
            if os.path.exists(_file):
                os.remove(_file)

    @classmethod
    def setUpClass(cls):
        cls.user_file = envipyengine.config._USER_CONFIG_FILE
        if os.path.exists(cls.user_file):
            os.rename(cls.user_file, cls.user_file + '.bak')

        cls.sys_file = envipyengine.config._SYSTEM_CONFIG_FILE
        if os.path.exists(cls.sys_file):
            os.rename(cls.sys_file, cls.sys_file + '.bak')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.user_file + '.bak'):
            os.rename(cls.user_file + '.bak', cls.user_file)

        if os.path.exists(cls.sys_file + '.bak'):
            os.rename(cls.sys_file + '.bak', cls.sys_file)

    def setUp(self):
        self._clean_files([self.user_file, self.sys_file])

    def tearDown(self):
        self._clean_files([self.user_file, self.sys_file])

    def test_set_get_user(self):
        """ Setting property in user config updates correct file """
        value = 'foo'
        envipyengine.config.set('engine', value)
        engine = envipyengine.config.get('engine')

        self.assertEqual(engine, value)
        self.assertTrue(os.path.exists(self.user_file))
        self.assertFalse(os.path.exists(self.sys_file))

    def test_set_get_sys(self):
        """ Setting property in system config updates correct file
            System retrieved if no user setting
        """
        value = 'foo'
        envipyengine.config.set('engine', value, system=True)
        engine = envipyengine.config.get('engine')

        self.assertEqual(engine, value)
        self.assertFalse(os.path.exists(self.user_file))
        self.assertTrue(os.path.exists(self.sys_file))

    def test_get_user(self):
        """ User setting supercedes system setting """
        user_value = 'foo'
        system_value = 'bar'
        envipyengine.config.set('engine', user_value)
        envipyengine.config.set('engine', system_value, system=True)

        engine = envipyengine.config.get('engine')
        self.assertEqual(engine, user_value)
        self.assertTrue(os.path.exists(self.sys_file))
        self.assertTrue(os.path.exists(self.user_file))

    def test_get_invalid(self):
        """ Error thrown when property does not exist """
        with self.assertRaises(NoConfigOptionError):
            envipyengine.config.get('engine')

    def test_remove_user_setting(self):
        """ Remove works as expected with user config """
        value = 'foo'
        envipyengine.config.set('engine', value)

        envipyengine.config.remove('engine')
        with self.assertRaises(NoConfigOptionError):
            envipyengine.config.get('engine')

    def test_remove_sys_setting(self):
        """ Remove works as expected with system config """
        value = 'foo'
        envipyengine.config.set('engine', value, system=True)

        envipyengine.config.remove('engine', system=True)
        with self.assertRaises(NoConfigOptionError):
            envipyengine.config.get('engine')

    def test_set_get_environment_user(self):
        """ Environment values can be set in user config file """
        settings = {'IDL_PATH': '+C:\\', 'IDL_TMP_DIR': 'D:\\'}
        envipyengine.config.set_environment(settings)

        result = envipyengine.config.get_environment()
        self.assertEqual(settings, result)
        self.assertTrue(os.path.exists(self.user_file))
        self.assertFalse(os.path.exists(self.sys_file))

    def test_set_environment_sys(self):
        """ Environment Values can be set in system config file """
        settings = {'IDL_PATH': '+C:\\', 'IDL_TMP_DIR': 'D:\\'}
        envipyengine.config.set_environment(settings, system=True)

        result = envipyengine.config.get_environment()
        self.assertEqual(settings, result)
        self.assertFalse(os.path.exists(self.user_file))
        self.assertTrue(os.path.exists(self.sys_file))

    def test_get_environment_empty(self):
        """ None returned if no environment settings """
        result = envipyengine.config.get_environment()
        self.assertEqual(result, {})

    def test_get_environment_merge(self):
        """
        Settings in user and system config files are merged
        Setting in User file Supercedes setting in system file
        """
        envipyengine.config.set_environment({'IDL_PATH': 'user-path'})
        envipyengine.config.set_environment({'IDL_PATH': 'sys-path'}, system=True)
        envipyengine.config.set_environment({'USER_VAR': 'user-var'})
        envipyengine.config.set_environment({'SYS_VAR': 'sys-var'}, system=True)
        expected = {'IDL_PATH': 'user-path',
                    'USER_VAR': 'user-var',
                    'SYS_VAR': 'sys-var'}
        result = envipyengine.config.get_environment()
        self.assertEqual(result, expected)

    def test_remove_environment_user(self):
        """ Able to remove settings from user config """
        settings = {'IDL_PATH': '+C:\\'}
        envipyengine.config.set_environment(settings)

        envipyengine.config.remove_environment('IDL_PATH')

        result = envipyengine.config.get_environment()
        self.assertEqual(result, {})

    def test_remove_environment_sys(self):
        """ Able to remove setting from sys config """
        settings = {'IDL_PATH': '+C:\\'}
        envipyengine.config.set_environment(settings, system=True)

        envipyengine.config.remove_environment('IDL_PATH', system=True)

        result = envipyengine.config.get_environment()
        self.assertEqual(result, {})
