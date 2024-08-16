from datetime import datetime
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.constants.location_constants import Cities
from models.location import Location
from models.route import Route

class CreateRouteCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        self._params = params
        self._app_data = app_data

    def execute(self):
        input_str, departure_time_str = self._params

        try:
            location_part = input_str.rsplit(' ', 1)[0]
            date_part = input_str.rsplit(' ', 1)[1] + " " + departure_time_str

            location_names = location_part.strip().split(',')
            locations = []
            for name in location_names:
                clean_name = name.strip()
                if any(char.isdigit() for char in clean_name):
                    return f"Invalid location format: {clean_name}. Locations should not contain dates or numbers."
                locations.append(Location(Cities.from_string(clean_name)))
        except ValueError as e:
            return str(e)

        try:
            departure_time = datetime.strptime(date_part.strip(), '%d-%m-%Y %H:%M')
        except ValueError:
            return "Invalid date format. Use 'DD-MM-YYYY HH:MM'."

        new_route = Route(locations=locations, departure_time=departure_time)
        self._app_data.routes.append(new_route)

        return f'Route {new_route.id} was created successfully!'

