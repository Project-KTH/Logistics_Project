from datetime import timedelta, datetime, date
from helpers import distances
# vehicle.py


class Vehicle:

    id_vehicle = 1001
    SPEED_CONSTANT = 87

    vehicle_park = {
        "Scania": {"units": 10, "name": "Scania", "capacity": 42_000, "range": 8_000},
        "Man": {"units": 15, "name": "Man", "capacity": 37_000, "range": 10_000},
        "Actros": {"units": 15, "name": "Actros", "capacity": 26_000, "range": 13_000},
    }

    def __init__(self, name, capacity, range):
        self._name = name
        self._capacity = capacity
        self._range = range
        self._initial_capacity = capacity  # Initial capacity to reset to full capacity
        self._initial_range = range  # To reset range

        self._id_truck = Vehicle.id_vehicle
        Vehicle.id_vehicle += 1
        self._routes = [] # List of all routes for a truck.

        # self._current_status = ""
        # self._current_location = ""


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
    def range(self):
        return self._range

    # @property
    # def current_status(self):
    #     return self._current_status

    # @property
    # def current_location(self):
    #     return self._current_location

    # @current_location.setter
    # def current_location(self, new_location):
    #     if new_location not in ("SYD", "MEL", "ADL", "ASP", "BRI", "DAR", "PER"):
    #         raise ValueError(f"Location '{new_location}' not allowed")
    #     self._current_location = new_location

    def find_active_route(self, track_date=None):
        if track_date is None:
            track_date = datetime.now()

        active_route = None
        for assigned_route in self._routes:
            assigned_route_start_date = assigned_route.departure_time
            if track_date < assigned_route_start_date:
                break

            assigned_route_expected_hours = len(assigned_route)/Vehicle.SPEED_CONSTANT
            assigned_route_delta = timedelta(hours=assigned_route_expected_hours)
            assigned_route_end_date = assigned_route_start_date + assigned_route_delta

            if track_date >= assigned_route.departure_time and track_date <= assigned_route_end_date:
                active_route = assigned_route
                break

        return active_route


    def track_location(self, track_date=None):
        if track_date is None:
            track_date = datetime.now()

        location = "Garage"
        for route in self._routes:
            route_start_date = route.departure_time
            if track_date < route_start_date:
                return location
            for n in range(len(route.locations)-1):
                # Iterate through route locations
                start_location = route.locations[n]
                end_location = route.locations[n+1]
                route_distance = distances.distances[start_location][end_location]
                route_duration = route_distance/Vehicle.SPEED_CONSTANT
                route_delta = timedelta(hours=route_duration)
                route_end_date = route_start_date + route_delta
                if route_start_date >= track_date and track_date <= route_end_date:
                    return f"In transit to {end_location}"
                route_start_date = route_end_date
                location = end_location

        return location


        # current_route = self.find_active_route(track_date)

        # current_route_start_date = current_route.departure_time
        # current_route_expected_hours = len(current_route)/Vehicle.SPEED_CONSTANT
        # current_route_delta = timedelta(hours=current_route_expected_hours)
        # current_end_date = current_route_start_date + current_route_delta

        # self._current_location = current_route.locations[0]

        # for n in range(1, len(current_route.locations)-1):
        #     temp_route = current_route.locations[0:n]

        #     expected_hours_to_next_city = len(temp_route)/Vehicle.SPEED_CONSTANT
        #     delta_to_next_city = timedelta(hours=expected_hours_to_next_city)

        #     if current_route_start_date + delta_to_next_city == track_date:
        #         self._current_location = current_route.locations[n]

        #     elif current_route_start_date + delta_to_next_city < track_date:
        #         self._current_location = f"In transit to {current_route.locations[n]}"

        # return self._current_location

    # def advance_route(self):
    #     if self._current_status == "Free":
    #         raise ValueError(f"The truck doesn't have assigned route. Can't advance.")
    #     # change the location to next
    #     inx_location = self.current_route.index(self.current_location)
    #     self.current_location = self.current_route[inx_location+1]
    #     if inx_location + 1 == len(self.current_route):
    #         # complete route, end location
    #         self._complete_route()

    # def _complete_route(self):
    #     self.change_status()
    #     self._current_route = "Not assigned"
    #     self._capacity = Vehicle.vehicle_park[self.name]["capacity"]

    def check_schedule(self, new_route):
        if len(self._routes) > 0:
            new_route_start_date = new_route.departure_time

            last_route = self._routes[-1]
            last_route_start_date = last_route.departure_time
            last_route_expected_hours = len(last_route)/Vehicle.SPEED_CONSTANT
            last_route_delta = timedelta(hours=last_route_expected_hours)
            last_route_end_date = last_route_start_date + last_route_delta

            if last_route_end_date < new_route_start_date:
                return True
            else:
                raise ValueError(f"Vehicle not available before {last_route_end_date}")
        else:
            return True

    def check_matching_locations(self, new_route):
        if len(self._routes) > 0:
            last_route = self._routes[-1]
            if last_route.locations[-1] == new_route.locations[0]:
                return True
            else:
                raise ValueError(f"Can't assign new route. Route must stast from {last_route.locations[-1]}")
        else:
            return True

    def check_remaining_range(self, new_route):
        if self._initial_range == self._range and self._initial_range > len(new_route):
            return True
        if self._range > len(new_route):
            return True
        else:
            raise ValueError(f"Range not enough to cover {len(new_route)} km")

    def assign_route(self, new_route):
        available = self.check_schedule(new_route)
        location = self.check_matching_locations(new_route)
        range = self.check_remaining_range(new_route)

        if all([available, location, range]):
            self._routes.append(new_route)
            self._range -= len(new_route)

            print(f"{new_route} added to {self._name} ID: {self._id_truck}")


    def update_capacity(self, package_weight: float):
        if package_weight <= 0:
            raise ValueError("Package weight is expected to be a positive value")
        if package_weight > self._capacity:
            raise ValueError(f"Free capacity of vehicle: {self.capacity:_}kg can't load {package_weight:_}kg")

        self._capacity = self._capacity - package_weight

    def update_range(self, distance):
        if distance <= 0:
            raise ValueError("Distance is expected to be a positive value")
        if distance > self._range:
            raise ValueError(f"Remaining range is not enough for distance {distance} km")

        self._range -= distance

    def reset(self):
        """Reset the truck's capacity and range to initial values."""
        self._capacity = self._initial_capacity
        self._range = self._initial_range
        print(f"Vehicle ID: {self._id_truck} has been reset.")
    # def change_status(self):
    #     if self._current_status == "Free":
    #         self._current_status = "In transit"
    #     else:
    #         self._current_status = "Free"

    def __str__(self):
        return (
            f"{self.name} ID:--{self.id_truck}-- "
            f"location: {self.track_location()}, "
            f"route: {self.find_active_route()}, "
            f"capacity left: {self.capacity:_}_kg, "
            f"range to go: {self.range:_}_km"
        )

#will move to app_data
all_vehicles: list[Vehicle] = []
for fleet in Vehicle.vehicle_park.values():
    for n in range(fleet["units"]):
        new_truck = Vehicle(fleet["name"], fleet["capacity"], fleet["range"])
        all_vehicles.append(new_truck)

print("------ All vehicles are ready to go ------") #optional, something like system check/the creation is successful.

for each in all_vehicles:
    print(str(each))
