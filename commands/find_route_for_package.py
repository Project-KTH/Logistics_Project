from datetime import datetime
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.constants.location_constants import Cities
from models.location import Location
from models.route import Route

class FindRouteForPackage:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        self._params = params
        self._app_data = app_data
    
    def execute(self):
        package_id = self._params[0]
        
        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ValueError(f"Package ID {package_id} not found")
        
        routes = []
        for route in self._app_data.routes:
            if package.start_location in route.locations and package.end_location in route.locations:
                start_index = route.locations.index(package.start_location)
                end_index = route.locations.index(package.end_location)
                if start_index < end_index:
                    routes.append(route)
        
        if routes:
            return "\n----------------------\n".join(str(route) for route in routes)
        else:
            return "No suitable route found"
        
    