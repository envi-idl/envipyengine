"""

"""

import os
from distutils.core import Command as BaseCommand
from unittest import TestLoader, TextTestRunner
from setuptools import setup


class TestCommand(BaseCommand):
    """Runs the package tests."""
    description = 'Runs all package tests.'

    user_options = [
        ('junit=', None,
         'outputs results to an xml file.')
    ]

    def initialize_options(self):
        self.junit = None

    def finalize_options(self):
        pass

    def run(self):
        # Import xmlrunner here so it's not a setup requirement
        import xmlrunner
        test_suite = TestLoader().discover('.')
        if self.junit:
            with open(self.junit, 'wb') as output:
                runner = xmlrunner.XMLTestRunner(output)
                runner.run(test_suite)
        else:
            runner = TextTestRunner(verbosity=2)
            runner.run(test_suite)

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(name='envipyengine',
      version='1.0.8',
      description='ENVI Python Engine',
      long_description=long_description,
      url='https://github.com/envi-idl/envipyengine',
      author='Harris Geospatial Solutions, Inc.',
      packages=['envipyengine',
                'envipyengine.taskengine'],
      scripts=['scripts/envipyengineconfig.py'],
      extras_require={
        'dev': [
            'coverage',
            'pylint',
            'Sphinx',
            'Sphinx-PyPI-upload',
            'sphinx_rtd_theme',
            'twine',
            'unittest-xml-reporting',
            'wheel'
        ]
      },
      cmdclass=dict(test=TestCommand),
      license='MIT',
      keywords='envi idl'
      )
