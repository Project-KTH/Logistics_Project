from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.package import Package


class CreatePackageCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        self._params = params
        self._app_data = app_data

    def execute(self):
        start_location, end_location, weight, customer_info = self._params
        weight = float(weight)
        new_package = Package(start_location, end_location, weight, customer_info)
        self._app_data.packages.append(new_package)
        return f'Package {new_package.id} was created successfully!'