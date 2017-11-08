"""
The Taskengine module provides functions for querying and running tasks.
"""

import sys
import os

from subprocess import Popen, PIPE
import subprocess
import json
from collections import OrderedDict
from .. import config
from ..error import TaskEngineNotFoundError
from ..error import TaskEngineExecutionError
from ..error import NoConfigOptionError

def execute(input_params, engine, cwd=None):
    """
    Execute a task with the provided input parameters

    :param input_params: Python dictionary containg all input parameters.
                         This will be converted to JSON before being passed
                         to the task engine.
    :param engine: String specifying Task Engine type to run (ENVI, IDL, etc.)
    :param cwd: Optionally specify the current working directory to be used
                when spawning the task engine.
    :return: A python dictionary representing the results JSON string generated
             by the Task Engine.
    """

    try:
        taskengine_exe = config.get('engine')
    except NoConfigOptionError:
        raise TaskEngineNotFoundError(
            "Task Engine config option not set." +
            "\nPlease verify the 'engine' configuration setting.")

    if not os.path.exists(taskengine_exe):
        raise TaskEngineNotFoundError(
            "Task Engine executable not found." +
            "\nPlease verify the 'engine' configuration setting.")

    # Get any arguments for the taskengine
    engine_args = None
    try:
        engine_args = config.get('engine-args')
    except NoConfigOptionError:
        pass

    # Get environment overrides if they exist
    environment = None
    config_environment = config.get_environment()
    if config_environment:
        environment = os.environ.copy()
        environment.update(config_environment)

    # Build up the args vector for popen
    args = [taskengine_exe, engine]
    if engine_args:
        args.append(engine_args)

    # Hide the Console Window on Windows OS
    startupinfo = None
    if sys.platform.startswith('win'):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    input_json = json.dumps(input_params)
    process = Popen(args,
                    stdout=PIPE,
                    stdin=PIPE,
                    stderr=PIPE,
                    universal_newlines=True,
                    cwd=cwd,
                    env=environment,
                    startupinfo=startupinfo)
    stdout, stderr = process.communicate(input=input_json)
    if process.returncode != 0:
        if stderr != '':
            raise TaskEngineExecutionError(stderr)
        else:
            raise TaskEngineExecutionError(
                'Task Engine exited with code: ' + str(process.returncode))
    else:
        return json.loads(stdout, object_pairs_hook=OrderedDict)

