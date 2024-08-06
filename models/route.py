from datetime import timedelta
from helpers.functions import get_distance
from models.vehicle import Vehicle

class Route:
    def __init__(self, route_id, locations, departure_time):
        self.route_id = route_id
        self.locations = locations  # List of city names
        self.departure_time = departure_time  # Start time of the route
        self.truck = None
        self.packages = []

    def add_package(self, package):
        if package.start_location == self.locations[0] and self.truck:
            if self.truck.capacity >= package.weight:
                self.packages.append(package)
                self.truck.update_capacity(package.weight)
                package.expected_arrival = self.calculate_arrival_times()[-1]  # Set expected arrival time at destination
                print(f"Package {package.package_id} added to route {self.route_id}.")
            else:
                raise ValueError("Not enough capacity in truck.")
        else:
            raise ValueError("Package start location does not match route start location or no truck assigned.")

    def calculate_travel_time(self, distance):
        average_speed = Vehicle.SPEED_CONSTANT
        return distance / average_speed

    def calculate_arrival_times(self):
        distances = [get_distance(self.locations[i], self.locations[i + 1]) for i in range(len(self.locations) - 1)]
        arrival_times = [self.departure_time]

        current_time = self.departure_time
        for distance in distances:
            travel_time_hours = self.calculate_travel_time(distance)
            travel_time_delta = timedelta(hours=travel_time_hours)
            current_time += travel_time_delta
            arrival_times.append(current_time)

        return arrival_times

    def update_route(self, new_locations):
        self.locations = new_locations
        print(f"Route {self.route_id} updated to new locations: {self.locations}")

    def __str__(self):
        arrival_times = self.calculate_arrival_times()
        stops_with_times = ', '.join(f"{loc} ({time.strftime('%Y-%m-%d %H:%M')})" for loc, time in zip(self.locations, arrival_times))
        return f"Route ID: {self.route_id}, Locations: {stops_with_times}, Truck ID: {self.truck.id_truck if self.truck else 'No truck assigned'}"
