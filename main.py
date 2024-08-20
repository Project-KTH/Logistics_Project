from datetime import datetime, timedelta

from core.application_data import ApplicationData
from core.engine import Engine
from models.location import Location
from models.manager import Manager
from models.package import Package
from models.route import Route
from models.user import User

from core.application_data import ApplicationData
from core.command_factory import CommandFactory
from models.vehicle import Vehicle


#
#
if __name__ == "__main__":
    # Initialize Application Data
    app_data = ApplicationData()

    # Create a CommandFactory with the application data
    command_factory = CommandFactory(app_data)

    # Initialize the engine with the command factory
    engine = Engine(command_factory)

    # Start the terminal interface
    engine.start()

#
#
# # Test the generate_locations_from_packages method
# def test_generate_locations_from_packages():
#     # Create test packages
#     package1 = Package("Sydney", "Melbourne", 20, "Customer 1")
#     package2 = Package("Melbourne", "Adelaide", 30, "Customer 2")
#     package3 = Package("Adelaide", "Perth", 40, "Customer 3")
#
#     # Create a route from packages
#     route = Route(departure_time="17-08-2024 09:00")
#     route.generate_locations_from_packages([package1, package2, package3])
#
#     # Print the generated locations
#     print("Generated Locations from Packages:")
#     for location in route.locations:
#         print(location.name)
#
# def test_assign_truck():
#     # Create test packages
#     package1 = Package("Sydney", "Melbourne", 20, "Customer 1")
#     package2 = Package("Melbourne", "Adelaide", 30, "Customer 2")
#
#     # Create a route
#     route = Route(departure_time="17-08-2024 09:00")
#     route.generate_locations_from_packages([package1, package2])
#
#     # Create a vehicle
#     vehicle = Vehicle(name="Scania", capacity=42000, truck_range=8000)
#
#     # Assign the truck to the route
#     route.assign_truck(vehicle)
#
#     # Print assigned truck info
#     print(f"Truck {route.truck.name} has been assigned to route {route.id}")
#
# def test_calculate_travel_time():
#     route = Route(locations=[Location("Sydney"), Location("Melbourne")], departure_time="17-08-2024 09:00")
#     distance = route.locations[0].get_distance_to(route.locations[1].name)
#
#     travel_time = route.calculate_travel_time(distance)
#     print(f"Travel time from Sydney to Melbourne: {travel_time:.2f} hours")
#
# def test_calculate_arrival_times():
#     # Create test packages
#     package1 = Package("Sydney", "Melbourne", 20, "Customer 1")
#     package2 = Package("Melbourne", "Adelaide", 30, "Customer 2")
#
#     # Create a route
#     route = Route(departure_time="17-08-2024 09:00")
#     route.generate_locations_from_packages([package1, package2])
#
#     # Print calculated arrival times
#     arrival_times = route.calculate_arrival_times()
#     print("Arrival times for each stop:")
#     for time in arrival_times:
#         print(time)
#
#
# def next_stop(self, current_location):
#     location_names = [loc.name for loc in self.locations]
#
#     if current_location not in location_names:
#         raise ValueError(
#             f"Current location {current_location} not on route. Available locations: {', '.join(location_names)}")
#
#     current_index = location_names.index(current_location)
#
#     if current_index < len(self.locations) - 1:
#         return self.locations[current_index + 1].name
#     return None  # No further stops
#
#
# def test_update_locations_for_packages():
#     # Create test packages
#     package1 = Package("Sydney", "Melbourne", 20, "Customer 1")
#     package2 = Package("Melbourne", "Adelaide", 30, "Customer 2")
#
#     # Create a route
#     route = Route(locations=[Location("Sydney"), Location("Melbourne")], departure_time="17-08-2024 09:00")
#
#     # Update locations with new packages
#     route.update_locations_for_packages([package2])
#
#     # Print updated locations
#     print("Updated Locations:")
#     for location in route.locations:
#         print(location.name)
#
# def test_simulate_route():
#     # Create test packages
#     package1 = Package("Sydney", "Melbourne", 20, "Customer 1")
#     package2 = Package("Melbourne", "Adelaide", 30, "Customer 2")
#
#     # Create a route
#     route = Route(departure_time="17-08-2024 09:00")
#     route.generate_locations_from_packages([package1, package2])
#
#     # Simulate the route
#     route.simulate_route()
#
# if __name__ == "__main__":
#     print("\nTest: Generate Locations from Packages")
#     test_generate_locations_from_packages()
#
#     print("\nTest: Assign Truck to Route")
#     test_assign_truck()
#
#     print("\nTest: Calculate Travel Time")
#     test_calculate_travel_time()
#
#     print("\nTest: Calculate Arrival Times")
#     test_calculate_arrival_times()
#
#     print("\nTest: Update Locations for Packages")
#     test_update_locations_for_packages()
#
#     print("\nTest: Simulate Route")
#     test_simulate_route()
#
