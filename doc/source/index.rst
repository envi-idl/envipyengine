.. _envipyengine:

***********************
ENVI Py Engine
***********************

ENVI Py Engine provides a client Python package, named envipyengine, to run ENVI analytics provided by ENVI Desktop.
The Python package provides the ability to query for available tasks, retrieve task information, and execute tasks on the desktop.

There is an additional client Python package available, named envipyarc, to provide the ability to run ENVI analytics through ArcMap and ArcGIS Pro.  

See https://www.nv5geospatialsoftware.com/ for more details on product offerings.


Usage
=====

Before using ENVI Py Engine, you must first configure the package so it can find your Engine executable within your ENVI/IDL installation. To do this make sure the "engine" config option is set::

    >>> import envipyengine
    >>> engine = envipyengine.config.get('engine')
    
If the above command throws an error, then you will need to set the 'engine' property to the the full path of the 'taskengine' executable in your ENVI installation::

    >>> envipyengine.config.set('engine', <path-to-executable>)

When specifying paths in Python strings on Windows, be sure to use two backslashes as your directory separator.

To connect to the ENVI Task Engine and list the available tasks, create a new instance of the Engine class with the engine name from the Python command line::

    >>> from envipyengine import Engine
    >>> envi_engine = Engine('ENVI')
    >>> envi_engine.tasks()

You must have write permissions for Python's current working directory in order to run the examples.

To get an ENVI task object, use the :code:`task()` method on the Engine object::

    >>> task = envi_engine.task('SpectralIndex')
	
To get a list of task parameter information, use the :code:`parameters` property on the Task object::
	
    >>> task.parameters

To execute a task, use the :code:`execute()` method on the Task object. A GSF Job object is returned after the job has been submitted::

    >>> input_raster = dict(url='<path_to_input_raster>', factory='URLRaster')
    >>> parameters = dict(INPUT_RASTER=input_raster, 
                          INDEX='Normalized Difference Vegetation Index')
    >>> task.execute(parameters)


API Documentation
=================

.. toctree::
   :maxdepth: 2

   envipyengine_api
