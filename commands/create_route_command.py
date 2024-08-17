from datetime import datetime
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.constants.location_constants import Cities
from models.location import Location
from models.route import Route

class CreateRouteCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 3)
        self._params = params
        self._app_data = app_data

    def execute(self):
        locations_list = self._params[0].split(",")
        departure_time_str = self._params[-2] + " " + self._params[-1]

        if len(locations_list) < 2:
            raise ValueError(f"Ensure locations are at least two: {locations_list}.")

        locations = [Location(Cities.from_string(name)) for name in locations_list]
    
        try:
            departure_time = datetime.strptime(departure_time_str, '%d-%m-%Y %H:%M')
        except ValueError:
            raise ValueError("Invalid date format. Use 'DD-MM-YYYY HH:MM'.")

        new_route = Route(locations=locations, departure_time=departure_time)
        self._app_data.routes.append(new_route)

        return f'Route {new_route.id} was created successfully!'
