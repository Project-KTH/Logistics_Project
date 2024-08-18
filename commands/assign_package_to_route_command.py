from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class AssignPackageToRouteCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        self._params = params
        self._app_data = app_data

    def execute(self):
        package_id, route_id = self._params
        package = self._app_data.find_package_by_id(package_id)
        route = self._app_data.find_route_by_id(route_id)
        
        if not route:
            return f'Route {route_id} not found!'
        if not package:
            return f'Package {package_id} not found!'

        route.add_package(package) # Adds package to Route and Route to Package.

        return f'Package {package_id} assigned to route {route_id} successfully.'

