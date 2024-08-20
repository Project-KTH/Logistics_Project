from datetime import datetime
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.constants.location_constants import Cities
from models.location import Location
from models.route import Route


class CreateAndAssignRouteCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        self._params = params
        self._app_data = app_data

    def execute(self):
        locations_list = self._params[0].split(",")
        departure_time_str = self._params[1] + " " + self._params[2]
        package_weight_threshold = float(self._params[3])

        if len(locations_list) < 2:
            raise ValueError(f"Ensure locations are at least two: {locations_list}.")

        locations = [Location(Cities.from_string(name.strip())) for name in locations_list]

        try:
            departure_time = datetime.strptime(departure_time_str, "%d-%m-%Y %H:%M")
        except ValueError:
            raise ValueError("Invalid date format. Use 'DD-MM-YYYY HH:MM'.")

        new_route = Route(locations=locations, departure_time=departure_time)
        route_distance = len(new_route)
        self._app_data.routes.append(new_route)

        arrival_times = new_route.calculate_arrival_times()
        print(f"Route created with ID: {new_route.id}")
        print(f"Total route distance: {route_distance} km")
        print(f"Estimated arrival times at each stop:")
        for location, arrival_time in zip(locations_list, arrival_times):
            print(f"{location}: {arrival_time}")

        suitable_truck = next(
            (truck for truck in self._app_data.vehicles if
             (truck.capacity >= package_weight_threshold and truck.truck_range >= route_distance
              and truck.track_location(datetime.now()) == 'Garage')
             ),
            None
        )

        if not suitable_truck:
            raise ValueError("No suitable truck available with enough capacity and range.")

        print(f"Truck {suitable_truck.id_truck} assigned to the route.")
        new_route.assign_truck(suitable_truck)
        total_assigned_weight = 0

        def can_add_package(package, total_assigned_weight):
            return (
                    (package.start_location.name in locations_list) and (package.end_location.name in locations_list)
                    and (total_assigned_weight + package.weight <= suitable_truck.capacity)
            )

        for package in self._app_data.packages:
            if can_add_package(package, total_assigned_weight):
                new_route.add_package(package)
                total_assigned_weight += package.weight
                print(f"Package {package.id} added to the route. Total assigned weight: {total_assigned_weight} kg.")
            else:
                print(f"Package {package.id} cannot be added. Either exceeds truck capacity or locations not in route.")

        suitable_truck.assign_route(new_route)
        print(f"Truck {suitable_truck.id_truck} has been assigned to route {new_route.id}")

        for package in new_route.packages:
            print(f"Package {package.id} assigned to the route.")

        return f"Route {new_route.id} created and packages assigned successfully!"
