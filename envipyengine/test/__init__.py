"""
Contains the test suite for the envipyengine.  Helper methods are avaible here.
"""
import os

def task_dir():
    """Returns the directory containing IDL/ENVI tasks for testing"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')

def data_dir():
    """Returns the directory containing test data"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def workspace_dir():
    """
    Returns the workspace directory for holding temporary data. Directory is created if
    it doesn't exist.
    """
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workspace')
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
    return temp_dir
