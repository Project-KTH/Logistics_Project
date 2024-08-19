from models.route import Route


class SimulateRouteCommand():
    def __init__(self, params, app_data):
        self.route_id = params[0]
        self.app_data = app_data

    def execute(self):
        route = self.app_data.find_route_by_id(self.route_id)
        if not route:
            return f"Route with ID {self.route_id} not found."

        simulation_result = route.simulate_route()
        return f"Simulation for route {self.route_id} completed.\nDetails:\n{simulation_result}"
