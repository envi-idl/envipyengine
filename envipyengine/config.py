"""
The config module is used to configure settings for ENVI Py Engine.

The following properties are currently supported:

==================== ========== ==================================================
Property Name        Data Type  Description
==================== ========== ==================================================
engine               string     The full path to the engine executable. Example:
                                "C:\\\\Program Files\\\\Harris\\\\ENVI54\\\\IDL86\\\\bin\\\\bin.x86_64\\\\taskengine.exe"
engine-args          string     Any additional command line arguments that will be
                                passed to the taskengine executable.
Environment Variable string     Any valid environment variable and value pairs.
Names                           All name/value pairs specified in this
                                section will be interpreted as environment variables
                                for use when running the Engine.
==================== ========== ==================================================

Please refer to the following examples of setting configuration values.

Set the Engine Executable path for the current user:
 >>> import envipyengine
 >>> envipyengine.config.set('engine', <executable-path>)

Set the ENVI Engine Executable path for all users.
 >>> import envipyengine
 >>> envipyengine.config.set('engine', <install-dir>, system=True)

Specify additional arguments for the Task Engine:
 >>> import envipyengine
 >>> envipyengine.config.set('engine-args', '--compile')

Specify an environment variable to be used when running the task engine:
 >>> import envipyengine
 >>> envipyengine.config.set_environment(dict('IDL_PATH'=<path-to-idl-code>)

The locations of the configuration files are:

============================== ===================================================================
OS and Configuration Type      Configuration File
============================== ===================================================================
Windows User Configuration     C:\\\\Users\\\\<user>\\\\AppData\\\\Local\\\\envipyengine\\\\settings.cfg
Windows System Configuration   C:\\\\ProgramData\\\\envipyengine\\\\settings.cfg
Mac OS X User Configuration    /Users/<user>/Library/Preferences/envipyengine/settings.cfg
Max OS X System Configuration  /Library/Preferences/envipyengine/settings.cfg
Linux User Configuration       /home/<user>/.envipyengine/settings.cfg
Linux System Configuration     /var/lib/envipyengine/settings.cfg
============================== ===================================================================


"""
import os
import sys

import ctypes

if sys.platform == 'win32':
    from ctypes import wintypes, windll


try:
    from ConfigParser import ConfigParser  # Python 2
    from ConfigParser import NoOptionError
    from ConfigParser import NoSectionError
except ImportError:
    from configparser import ConfigParser  # Python 3
    from configparser import NoOptionError
    from configparser import NoSectionError

from .error import NoConfigOptionError

_APP_DIRNAME = 'envipyengine'
_CONFIG_FILENAME = 'settings.cfg'
_MAIN_SECTION_NAME = 'envipyengine'
_ENVIRONMENT_SECTION_NAME = 'engine-environment'


def _user_config_file():
    """
    Returns the path to the settings.cfg file. On Windows the file is
    located in the AppData/Local/envipyengine directory. On Unix, the file
    will be located in the ~/.envipyengine directory.

    :return: String specifying the full path to the settings.cfg file
    """
    if sys.platform == 'win32':
        if 'LOCALAPPDATA' in os.environ:
            user_dir = os.getenv('LOCALAPPDATA')
        else:
            user_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local')
        config_path = os.path.join(user_dir, _APP_DIRNAME, _CONFIG_FILENAME)
    elif sys.platform.startswith('darwin'):
        user_dir = os.path.expanduser('~')
        config_path = os.path.sep.join([user_dir, 'Library', 'Preferences',
                                        _APP_DIRNAME, _CONFIG_FILENAME])
    else:
        user_dir = os.path.expanduser('~')
        config_path = os.path.sep.join([user_dir, '.' + _APP_DIRNAME,
                                        _CONFIG_FILENAME])
    return config_path


def _system_config_file():
    """
    Returns the path to the settings.cfg file. On Windows the file is
    located in the AppData/Local/envipyengine directory. On Unix, the file
    will be located in the ~/.envipyengine directory.

    :return: String specifying the full path to the settings.cfg file
    """
    if sys.platform == 'win32':
        config_path = os.path.sep.join([_windows_system_appdata(),
                                        _APP_DIRNAME,
                                        _CONFIG_FILENAME])
    elif sys.platform.startswith('darwin'):
        config_path = os.path.sep.join([os.path.sep + 'Library', 'Preferences',
                                        _APP_DIRNAME, _CONFIG_FILENAME])
    else:
        config_path = os.path.sep.join(['', 'var', 'lib', _APP_DIRNAME,
                                        _CONFIG_FILENAME])
    return config_path


def _windows_system_appdata():
    """
    Return the path to the Windows Common App Data folder.
    On Windows 7, for example, this is C:\\ProgramData

    :return: String reprsentation the path to the Windows Common
             App Data folder
    """
    # Could also use os.environ['ALLUSERSPROFILE'] - maybe?
    csidl_common_appdata = 35
    sh_get_folder_path = windll.shell32.SHGetFolderPathW
    sh_get_folder_path.argtypes = [wintypes.HWND,
                                   ctypes.c_int,
                                   wintypes.HANDLE,
                                   wintypes.DWORD,
                                   wintypes.LPCWSTR]
    path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    result = sh_get_folder_path(0, csidl_common_appdata, 0, 0, path_buf)
    return str(path_buf.value)


def _read_config(cfg_file):
    """
    Return a ConfigParser object populated from the settings.cfg file.

    :return: A Config Parser object.
    """
    config = ConfigParser()
    # maintain case of options
    config.optionxform = lambda option: option
    if not os.path.exists(cfg_file):
        # Create an empty config
        config.add_section(_MAIN_SECTION_NAME)
        config.add_section(_ENVIRONMENT_SECTION_NAME)
    else:
        config.read(cfg_file)
    return config


def _write_config(config, cfg_file):
    """
    Write a config object to the settings.cfg file.

    :param config: A ConfigParser object to write to the settings.cfg file.
    """
    directory = os.path.dirname(cfg_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(cfg_file, "w+") as output_file:
        config.write(output_file)


def get_environment():
    """
    Return all environment values from the config files. Values
    stored in the user configuration file will take precedence
    over values stored in the system configuration file.

    :return: A dictionary containing the name/value pairs of all
             environment settings in the config file.
    """
    section = _ENVIRONMENT_SECTION_NAME
    # Read system
    sys_cfg = _read_config(_SYSTEM_CONFIG_FILE)
    sys_env = \
        dict(sys_cfg.items(section)) if sys_cfg.has_section(section) else {}

    # Read user
    usr_cfg = _read_config(_USER_CONFIG_FILE)
    usr_env = \
        dict(usr_cfg.items(section)) if usr_cfg.has_section(section) else {}

    # Merge user into system
    for k in usr_env.keys():
        sys_env[k] = usr_env[k]
    return sys_env


def set_environment(environment, system=False):
    """
    Set engine environment values in the config file.

    :param environment: A dictionary containing the environment variable
                        settings as key/value pairs.
    :keyword system: Set to True to modify the system configuration file.
                     If not set, the user config file will be modified.
    """
    config_filename = \
        _SYSTEM_CONFIG_FILE if system is True else _USER_CONFIG_FILE
    config = _read_config(config_filename)

    section = _ENVIRONMENT_SECTION_NAME
    for key in environment.keys():
        config.set(section, key, environment[key])
    _write_config(config, config_filename)


def remove_environment(environment_var_name, system=False):
    """
    Remove the specified environment setting from the appropriate config file.

    :param environment_var_name: The name of the environment setting to remove.
    :keyword system: Set to True to modify the system configuration file.
                     If not set, the user config file will be modified.
    """
    config_filename = \
        _SYSTEM_CONFIG_FILE if system is True else _USER_CONFIG_FILE
    config = _read_config(config_filename)

    section = _ENVIRONMENT_SECTION_NAME
    config.remove_option(section, environment_var_name)
    _write_config(config, config_filename)


def get(property_name):
    """
    Returns the value of the specified configuration property.
    Property values stored in the user configuration file take
    precedence over values stored in the system configuration
    file.

    :param property_name: The name of the property to retrieve.
    :return: The value of the property.
    """
    config = _read_config(_USER_CONFIG_FILE)
    section = _MAIN_SECTION_NAME
    try:
        property_value = config.get(section, property_name)
    except (NoOptionError, NoSectionError) as error:

        # Try the system config file
        try:
            config = _read_config(_SYSTEM_CONFIG_FILE)
            property_value = config.get(section, property_name)
        except (NoOptionError, NoSectionError) as error:
            raise NoConfigOptionError(error)

    return property_value


def set(property_name, value, system=False):
    """
    Sets the configuration property to the specified value.

    :param property_name: The name of the property to set.
    :param value: The value for the property.
    :keyword system: Set to True to modify the system configuration file.
                     If not set, the user config file will be modified.
    """
    config_filename = \
        _SYSTEM_CONFIG_FILE if system is True else _USER_CONFIG_FILE
    config = _read_config(config_filename)

    section = _MAIN_SECTION_NAME
    config.set(section, property_name, value)
    _write_config(config, config_filename)


def remove(property_name, system=False):
    """
    Remove a configuration property/value setting from the config file.

    :param property_name: The name of the property to remove.
    :keyword system: Set to True to modify the system configuration file.
                     If not set, the user config file will be modified.
    """
    config_filename = \
        _SYSTEM_CONFIG_FILE if system is True else _USER_CONFIG_FILE
    config = _read_config(config_filename)

    section = _MAIN_SECTION_NAME
    config.remove_option(section, property_name)
    _write_config(config, config_filename)


# Set up some module globals so they only need to be
# calculated once
_USER_CONFIG_FILE = _user_config_file()
_SYSTEM_CONFIG_FILE = _system_config_file()
