from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.manager import Manager


class CreateManagerCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 3)
        self._params = params
        self._app_data = app_data

    def execute(self):
        # Extract parameters
        name, contact_info, password = self._params
        new_manager = Manager(name=name, contact_info=contact_info, password=password, application_data=self._app_data)
        self._app_data.users.append(new_manager)

        return f'Manager {new_manager.id} was created successfully!'
