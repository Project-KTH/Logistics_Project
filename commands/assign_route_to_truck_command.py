from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class AssignRouteToTruckCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        self._params = params
        self._app_data = app_data

    def execute(self):
        route_id, truck_id = self._params
        route = self._app_data.find_route_by_id(route_id)
        truck = self._app_data.find_vehicle_by_id(truck_id)

        if not route:
            return f'Route {route_id} not found!'
        if not truck:
            return f'Truck {truck_id} not found!'

        truck.assign_route(route)
        route.truck = truck

        return f'Route {route_id} assigned to truck {truck_id} successfully.'

