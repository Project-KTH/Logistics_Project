from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData

class ViewAllVehicles:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        self._params = params
        self._app_data = app_data
    
    def execute(self):
        return "\n----------------------\n".join(
            str(vehicle) 
            for vehicle in self._app_data.vehicles
        )
