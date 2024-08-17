from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData

class ViewAvailableVehicles:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        self._params = params
        self._app_data = app_data
    
    def execute(self):
        route_id = self._params[0]

        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ValueError(f"Route ID {route_id} not found")
        
        vehicles = []
        for vehicle in self._app_data.vehicles:
            try:
                vehicle.check_matching_locations(route)
            except ValueError:
                pass
            else:
                vehicles.append(vehicle)
        
        if vehicles:
            return "\n----------------------\n".join(str(vehicle) for vehicle in vehicles)
        else:
            return "No available vehicle found"
