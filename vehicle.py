class Vehicle:

    id_vehicle = 1
    SPEED_CONSTANT = 87

    vehicle_park = {
        "Scania": {"units": 10, "name": "Scania", "capacity": 42_000, "range": 8_000},
        "Man": {"units": 15, "name": "Man", "capacity": 37_000, "range": 10_000},
        "Actros": {"units": 15, "name": "Actros", "capacity": 26_000, "range": 13_000},
    }
    # Vehicle_park could be in another class like Inventory if needed.

    def __init__(self, name, capacity, range):
        self._name = name
        self._capacity = capacity
        self._range = range

        self._id_truck = Vehicle.id_vehicle
        Vehicle.id_vehicle += 1
        self._current_status = "Free"
        self._current_location = "Garage"
        self._current_route = "Not assigned"
    
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
            raise ValueError(f"The truck doesn't have assigned route. Can't advance.")
        # change the location to next
        inx_location = self.current_route.index(self.current_location)
        self.current_location = self.current_route[inx_location+1]
        if inx_location + 1 == len(self.current_route):
            # complete route, end location
            self._complete_route()
    
    def _complete_route(self):
        self.change_status()
        self._current_route = "Not assigned"
        self._capacity = Vehicle.vehicle_park[self.name]["capacity"]

    def assign_route(self, *new_route):
        # add if in transit - can't assign route
        if not all(city in ("SYD", "MEL", "ADL", "ASP", "BRI", "DAR", "PER") for city in new_route):
            raise ValueError(f"Route {new_route} out of coverage")
        self._current_route = new_route
        self.change_status()
    
    def update_capacity(self, package_weight: float):
        if package_weight <= 0:
            raise ValueError("Package weight is expected to be positive value")
        if package_weight > self._capacity:
            raise ValueError(f"Free capacity of vehicle: {self.capacity:_}kg can't load {package_weight:_}kg")
        
        self._capacity = self._capacity - package_weight
    
    def update_range(self, distance):
        if distance <= 0:
            raise ValueError("Distance is expected to be positive value")
        if distance > self._range:
            raise ValueError(f"Remaining range is not enough for distance {distance} km")
        
        self._range -= distance
    
    def change_status(self):
        if self._current_status == "Free":
            self._current_status = "In transit"
        else:
            self._current_status = "Free"

    def __str__(self):

        return (
            f"{self.name} ID:--{self.id_truck}-- "
            f"status: {self.current_status}, "
            f"location: {self.current_location}, "
            f"route: {self._current_route}, "
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

all_vehicles[5].update_capacity(15.5)
all_vehicles[5].current_location = "BRI"
all_vehicles[5].assign_route("BRI", "MEL", "ADL")
all_vehicles[5].advance_route()
print(all_vehicles[5])