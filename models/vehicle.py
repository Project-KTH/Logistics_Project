from datetime import timedelta, datetime, date
from helpers import distances
import time


class Vehicle:
    id_vehicle = 1001  # Class variable

    SPEED_CONSTANT = 87

    vehicle_park = {
        "Scania": {"units": 10, "name": "Scania", "capacity": 42_000, "range": 8_000},
        "Man": {"units": 15, "name": "Man", "capacity": 37_000, "range": 10_000},
        "Actros": {"units": 15, "name": "Actros", "capacity": 26_000, "range": 13_000},
    }

    def __init__(self, name, capacity, truck_range):
        self._name = name
        self._capacity = capacity
        self._truck_range = truck_range
        self._initial_capacity = capacity  # Initial capacity to reset to full capacity
        self._initial_range = truck_range  # To reset truck range
        self._id_truck = Vehicle.id_vehicle
        Vehicle.id_vehicle += 1
        self._routes = []  # List of all routes for a truck.
        self._current_location = "Garage"

    @property
    def name(self):
        return self._name

    @property
    def id_truck(self):
        return self._id_truck

    @property
    def capacity(self):
        return self._capacity

    @property
    def truck_range(self):
        return self._truck_range

    def find_active_route(self, track_date=None):
        if not track_date:
            track_date = datetime.now()
        else:
            if not isinstance(track_date, datetime):
                track_date = datetime.strptime(track_date, '%d-%m-%Y %H:%M')


        active_route = None
        for assigned_route in self._routes:
            assigned_route_start_date = assigned_route.departure_time
            assigned_route_expected_hours = len(assigned_route) / Vehicle.SPEED_CONSTANT
            assigned_route_end_date = assigned_route_start_date + timedelta(hours=assigned_route_expected_hours)

            if assigned_route_start_date <= track_date <= assigned_route_end_date:
                active_route = assigned_route

        return active_route

    def track_location(self, start_time=None):
        if start_time is None:
            start_time = datetime.now()
        else:
            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, '%d-%m-%Y %H:%M')

        location = "Garage"
        for route in self._routes:
            route_start_date = route.departure_time
            if start_time < route_start_date:
                return location
            for n in range(len(route.locations) - 1):
                start_location = route.locations[n]
                end_location = route.locations[n + 1]
                route_distance = distances.distances[start_location.name][end_location.name]
                route_duration = route_distance / Vehicle.SPEED_CONSTANT
                route_delta = timedelta(hours=route_duration)
                route_end_date = route_start_date + route_delta
                if route_start_date <= start_time < route_end_date:
                    return f"In transit to {end_location.name}"
                route_start_date = route_end_date
                location = end_location.name

        return location

    def simulate_route(self):
        """Simulate vehicle moving along its route, updating location every 3 seconds."""
        for route in self._routes:
            route_start_date = route.departure_time
            current_time = route_start_date
            print(f"Starting route simulation for vehicle {self._id_truck} on route {route.route_id}.")

            for n in range(len(route.locations) - 1):
                start_location = route.locations[n].name
                end_location = route.locations[n + 1].name
                route_distance = distances.distances[start_location][end_location]
                route_duration = route_distance / Vehicle.SPEED_CONSTANT
                route_delta = timedelta(hours=route_duration)

                # Calculate an accelerated arrival time for faster simulation
                accelerated_seconds = route_duration * 3600  # Accelerate by treating hours as seconds
                arrival_time = current_time + timedelta(seconds=accelerated_seconds)
                print(
                    f"Traveling from {start_location} to {end_location}, will arrive by {arrival_time.strftime('%H:%M:%S')}")

                while current_time < arrival_time:
                    time_to_arrival = (arrival_time - current_time).total_seconds()
                    if time_to_arrival > 3:
                        print(f"Time: {current_time.strftime('%H:%M:%S')} - In transit to {end_location}")
                        time.sleep(0.5)  # Sleep less time to accelerate simulation
                        current_time += timedelta(seconds=accelerated_seconds / 10)  # Simulate a faster passage
                    else:
                        current_time += timedelta(seconds=time_to_arrival)
                        break

                self._current_location = end_location
                print(f"Arrived at {end_location} at {current_time.strftime('%H:%M:%S')}.")

        print(f"Route simulation for vehicle {self._id_truck} completed.")

    def check_schedule(self, new_route):
        if len(self._routes) > 0:
            new_route_start_date = new_route.departure_time

            last_route = self._routes[-1]
            last_route_start_date = last_route.departure_time
            last_route_expected_hours = len(last_route) / Vehicle.SPEED_CONSTANT
            last_route_delta = timedelta(hours=last_route_expected_hours)
            last_route_end_date = last_route_start_date + last_route_delta

            if last_route_end_date < new_route_start_date:
                return True
            else:
                print(f"Vehicle not available before {last_route_end_date}")
                return False
        else:
            return True

    def check_matching_locations(self, new_route):
        """Checks if the route start location is the truck current location"""
        if len(self._routes) > 0:
            last_route = self._routes[-1]
            if last_route.locations[-1].name == new_route.locations[0].name:
                return True
            else:
                raise ValueError(f"Can't assign new route. Route must start from {last_route.locations[-1].name}")
        else:
            return True

    def check_remaining_range(self, new_route):
        if self._initial_range == self._truck_range and self._initial_range > len(new_route):
            return True
        if self._truck_range > len(new_route):
            return True
        else:
            raise ValueError(f"Range not enough to cover {len(new_route)} km")

    def assign_route(self, new_route):
        available = self.check_schedule(new_route)
        location = self.check_matching_locations(new_route)
        has_range = self.check_remaining_range(new_route)

        if all([available, location, has_range]):
            self._routes.append(new_route)
            self._truck_range -= len(new_route)

            print(f"Route {new_route.route_id} added to {self._name} ID: {self._id_truck}")

    def update_capacity(self, package_weight: float):
        if package_weight <= 0:
            raise ValueError("Package weight is expected to be a positive value")
        if package_weight > self._capacity:
            raise ValueError(f"Free capacity of vehicle: {self.capacity:_}kg can't load {package_weight:_}kg")

        self._capacity -= package_weight

    def update_range(self, distance):
        if distance <= 0:
            raise ValueError("Distance is expected to be a positive value")
        if distance > self._truck_range:
            raise ValueError(f"Remaining range is not enough for distance {distance} km")

        self._truck_range -= distance

    def reset(self):
        """Reset the truck's capacity and range to initial values."""
        self._capacity = self._initial_capacity
        self._truck_range = self._initial_range
        print(f"Vehicle ID: {self._id_truck} has been reset.")

    def __str__(self):
        return (
            f"{self.name} ID:--{self.id_truck}--\n"
            f"location: {self.track_location()}\n"
            f"route: {self.find_active_route()}\n"
            f"capacity left: {self.capacity}kg\n"
            f"range to go: {self.truck_range}km"
        )
# will move to app_data
# all_vehicles: list[Vehicle] = []
# for fleet in Vehicle.vehicle_park.values():
#     for n in range(fleet["units"]):
#         new_truck = Vehicle(fleet["name"], fleet["capacity"], fleet["range"])
#         all_vehicles.append(new_truck)
#
# print("------ All vehicles are ready to go ------") #optional, something like system check/the creation is successful.
#
# for each in all_vehicles:
#     print(str(each))