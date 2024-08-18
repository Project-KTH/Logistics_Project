from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class ViewSinglePackage:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        self._params = params
        self._app_data = app_data

    def execute(self):
        package_id = self._params[0]
        customer_info = self._params[1]

        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ValueError(f"Package ID {package_id} not found")
        
        if customer_info != package.customer_info:
            raise ValueError(f"Wrong customer info: {customer_info}") 

        return str(package)
