# vehicle.py

from helpers.linked_list import LinkedList


class Vehicle:
    id_vehicle = 1
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
        self._initial_range = range  # To reset range Kristin added it

        self._id_truck = Vehicle.id_vehicle
        Vehicle.id_vehicle += 1
        self._current_status = "Free"
        self._current_location = "Garage"
        self._current_route = LinkedList()

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

    @property
    def current_status(self):
        return self._current_status

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, new_location):
        if new_location not in ("SYD", "MEL", "ADL", "ASP", "BRI", "DAR", "PER"):
            raise ValueError(f"Location '{new_location}' not allowed")
        self._current_location = new_location

    @property
    def current_route(self):
        return self._current_route

    def advance_route(self):
        if self._current_status == "Free":
            raise ValueError(f"The truck doesn't have an assigned route. Can't advance.")

        # Retrieve the current route as a list of locations
        current_route_list = self._current_route.get_route()
        print(f"Advancing route. Current route: {current_route_list}")

        try:
            inx_location = current_route_list.index(self.current_location)
        except ValueError:
            raise ValueError(f"Current location '{self.current_location}' is not in the route.")

        self.current_location = current_route_list[inx_location + 1]
        if inx_location + 1 == len(current_route_list) - 1:
            self._complete_route()

    def _complete_route(self):
        self.change_status()
        self._current_route = LinkedList()
        self._capacity = Vehicle.vehicle_park[self.name]["capacity"]

    def assign_route(self, new_route: LinkedList):
        # Directly assign the new route
        self._current_route = new_route
        self.change_status()

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

    def change_status(self):
        if self._current_status == "Free":
            self._current_status = "In transit"
        else:
            self._current_status = "Free"

    def __str__(self):
        # Ensure the route is printed as a string
        route_str = " -> ".join(self._current_route.get_route())
        return (
            f"{self.name} ID:--{self.id_truck}-- "
            f"status: {self.current_status}, "
            f"location: {self.current_location}, "
            f"route: {route_str}, "
            f"capacity left: {self.capacity:_}kg, "
            f"range to go: {self.range:_}km"
        )
