"""
Tests the ENVI Py Task interface
"""

import unittest
import tempfile
import os
import shutil
import inspect

from envipyengine import Engine
from envipyengine.error import TaskEngineExecutionError

from .. import test

class TestTask(unittest.TestCase):
    """
    Test the ENVI Py Engine Task interface
    """
    @classmethod
    def setUpClass(cls):
        cls.engine = Engine('ENVI')
        cls.task = cls.engine.task('SpectralIndex')

    def test_uri(self):
        """Verify task.uri returns a string."""
        self.assertIsInstance(self.task.uri, str)

    def test_name(self):
        """Verify task.name returns a string."""
        self.assertIsInstance(self.task.name, str)

    def test_display_name(self):
        """Verify task display name returns a string."""
        self.assertIsInstance(self.task.display_name, str)

    def test_description(self):
        """Verify task description returns a string."""
        self.assertIsInstance(self.task.description, str)

    def test_parameters(self):
        """Verify task parameters returns a list with a parameter dictionary."""
        parameters = self.task.parameters
        self.assertIsInstance(parameters, list)
        for parameter in parameters:
            self.assertIsInstance(parameter['name'], str)
            self.assertIsInstance(parameter['display_name'], str)
            self.assertIsInstance(parameter['type'], str)
            self.assertRegexpMatches(parameter['direction'], '(input|output)')
            self.assertIsInstance(parameter['description'], str)
            self.assertIsInstance(parameter['required'], bool)

    def test_execute(self):
        """Verify an envipy task can be executed successfully."""

        # Create a temp directory
        tempdir = os.sep.join([tempfile.gettempdir(), 'envipy_test_execute'])
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)
        os.makedirs(tempdir)

        # Input test file is checked into the 'test/data' directory
        input_raster_url = os.path.join(test.data_dir(), 'checkerboard.dat')
        
        input_raster = dict(
            url=input_raster_url,
            factory='URLRaster')
        parameters = dict(INPUT_RASTER=input_raster,
                          INDEX='Normalized Difference Vegetation Index')
        result = self.task.execute(parameters, cwd=tempdir)
        self.assertIsInstance(result, dict)

        # Assert that the output files are there
        result_file = \
            result['outputParameters']['OUTPUT_RASTER']['url']
        self.assertTrue(os.path.exists(result_file))

        result_aux_files = \
            result['outputParameters']['OUTPUT_RASTER']['auxiliary_url']
        for aux_file in result_aux_files:
            self.assertTrue(os.path.exists(aux_file))

        # Verify that the cwd was honored in execute call
        self.assertEqual(os.path.dirname(result_file), tempdir)
        shutil.rmtree(tempdir)

    def test_invalid_task(self):
        """Verify an invalid task name throws an exception."""
        task = self.engine.task('InvalidTaskName')
        with self.assertRaises(TaskEngineExecutionError):
            # pylint: disable=unused-variable
            parameters = task.parameters

    def test_multidim_task(self):
        """Verify multidimensional datatype is handled."""
        task = self.engine.task('ClassificationToShapefile')
        parameters = task.parameters
        for parameter in parameters:
            if parameter['name'] == 'EXPORT_CLASSES':
                self.assertEqual(parameter['type'], 'STRING')
                self.assertEqual(parameter['dimensions'], '[*]')
