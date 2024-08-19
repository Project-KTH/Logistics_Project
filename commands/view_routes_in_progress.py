from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from datetime import datetime


class ViewRoutesInProgress:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        self._params = params
        self._app_data = app_data

    def execute(self):
        current_time = datetime.now()
        return "\n----------------------\n".join(
            str(route) 
            for route in self._app_data.routes 
            if route.departure_time <= current_time 
            and current_time <= datetime.strptime(
                route.calculate_arrival_times()[-1], '%d-%m-%Y %H:%M'
                )
        )
