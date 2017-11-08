"""
Implements the Task Engine task class.
"""

from ..task import Task as BaseTask
# from gsfcommon.error import TaskNotFoundError
from ..decorators import memoize
from . import taskengine

class Task(BaseTask):
    """
    Creates a Task Engine task that can submit jobs and list task parameters.
    """
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self._engine, self._name = self._uri.split(':')

    @property
    def name(self):
        info = self.taskinfo()
        return str(info['name'])

    @property
    def display_name(self):
        info = self.taskinfo()
        return str(info['displayName'])

    @property
    def description(self):
        info = self.taskinfo()
        return str(info['description'])

    @property
    def uri(self):
        return ':'.join((self._engine, self._name))

    @property
    def engine(self):
        """ Return the Engine object for this Task object """
        return self._engine

    @property
    def parameters(self):
        info = self.taskinfo()
        return info['parameters']

    def execute(self, parameters, cwd=None):
        task_input = {'taskName': self._name,
                      'inputParameters': parameters}

        # cwd passed in takes precedence over task cwd
        if not cwd:
            cwd = self._cwd
        return taskengine.execute(task_input, self._engine, cwd=cwd)

    @memoize
    def taskinfo(self):
        """ Retrieve the Task Information
        """

        task_input = {'taskName': 'QueryTask',
                      'inputParameters': {"Task_Name": self._name}}

        info = taskengine.execute(task_input, self._engine, cwd=self._cwd)

        task_def = info['outputParameters']['DEFINITION']

        task_def['name'] = str(task_def.pop('NAME'))
        task_def['description'] = str(task_def.pop('DESCRIPTION'))
        task_def['displayName'] = str(task_def.pop('DISPLAY_NAME'))

        if 'COMMUTE_ON_SUBSET' in task_def:
            task_def['commute_on_subset'] = task_def.pop('COMMUTE_ON_SUBSET')
        if 'COMMUTE_ON_DOWNSAMPLE' in task_def:
            task_def['commute_on_downsample'] = task_def.pop('COMMUTE_ON_DOWNSAMPLE')

        # Convert PARAMETERS into a list instead of a dictionary
        # which matches the gsf side things
        task_def['parameters'] = \
            [v for v in task_def['PARAMETERS'].values()]
        task_def.pop('PARAMETERS')

        parameters = task_def['parameters']
        for parameter in parameters:
            parameter['name'] = str(parameter.pop('NAME'))
            parameter['description'] = str(parameter.pop('DESCRIPTION'))
            parameter['display_name'] = str(parameter.pop('DISPLAY_NAME'))
            parameter['required'] = bool(parameter.pop('REQUIRED'))

            if 'MIN' in parameter:
                parameter['min'] = parameter.pop('MIN')

            if 'MAX' in parameter:
                parameter['max'] = parameter.pop('MAX')

            if parameter['TYPE'].count('['):
                parameter['type'], parameter['dimensions'] = parameter.pop('TYPE').split('[')
                parameter['dimensions'] = '[' + parameter['dimensions']
                parameter['type'] = str(parameter['type'])
            else:
                parameter['type'] = str(parameter.pop('TYPE').split('ARRAY')[0])

            if 'DIMENSIONS' in parameter:
                parameter['dimensions'] = parameter.pop('DIMENSIONS')

            if 'DIRECTION' in parameter:
                parameter['direction'] = parameter.pop('DIRECTION').lower()

            if 'DEFAULT' in parameter:
                if parameter['DEFAULT'] is not None:
                    parameter['default_value'] = parameter.pop('DEFAULT')
                else:
                    parameter.pop('DEFAULT')

            if 'CHOICE_LIST' in parameter:
                if parameter['CHOICE_LIST'] is not None:
                    parameter['choice_list'] = parameter.pop('CHOICE_LIST')
                else:
                    parameter.pop('CHOICE_LIST')

            if 'FOLD_CASE' in parameter:
                parameter['fold_case'] = parameter.pop('FOLD_CASE')

            if 'AUTO_EXTENSION' in parameter:
                parameter['auto_extension'] = parameter.pop('AUTO_EXTENSION')

            if 'IS_TEMPORARY' in parameter:
                parameter['is_temporary'] = parameter.pop('IS_TEMPORARY')

            if 'IS_DIRECTORY' in parameter:
                parameter['is_directory'] = parameter.pop('IS_DIRECTORY')

        return task_def
