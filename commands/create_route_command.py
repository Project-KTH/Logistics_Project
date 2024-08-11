from datetime import datetime

from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.location import Location
from models.route import Route


class CreateRouteCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 3)
        self._params = params
        self._app_data = app_data

    def execute(self):
        route_id, locations_str, departure_time_str = self._params
        locations = [Location(name) for name in locations_str.split(',')]
        departure_time = datetime.strptime(departure_time_str, '%d-%m-%Y %H:%M')
        new_route = Route(route_id, locations, departure_time)
        self._app_data.routes.append(new_route)
        return f'Route {route_id} was created successfully!'