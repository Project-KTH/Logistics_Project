from datetime import datetime, timedelta

from core.application_data import ApplicationData
from core.engine import Engine
from models.manager import Manager
from models.user import User

from core.application_data import ApplicationData
from core.command_factory import CommandFactory
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

# from datetime import datetime
# from models.vehicle import Vehicle
# from models.route import Route
# from models.package import Package
# from models.location import Location
#
#
# from datetime import datetime
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
#
#
#     print("\nTest: Update Locations for Packages")
#     test_update_locations_for_packages()
#
#     print("\nTest: Simulate Route")
#     test_simulate_route()


#
# # Create a manager
# manager = Manager(user_id="mgr001", name="Alice", contact_info="alice@example.com", application_data=app_data)
#
# # Add trucks
# truck_models = ["Scania", "Man", "Actros"]
# home_bases = ["SYD", "MEL", "ADL", "BRI", "PER"]
#
# trucks = [manager.add_truck(model, base) for model in truck_models for base in home_bases]
#
# # Create a user
# user = User(user_id="user001", name="John Doe", contact_info="john.doe@example.com")
#
# # User orders packages
# user.order_package("SYD", "MEL", 10000, app_data)
# user.order_package("MEL", "ADL", 5000, app_data)
# user.order_package("SYD", "ADL", 15000, app_data)
#
# # Create and assign routes
# route_data = [
#     ("R001", ["SYD", "MEL", "ADL"], 1),
#     ("R002", ["MEL", "ADL", "PER"], 2),
#     ("R003", ["ADL", "PER", "SYD"], 3),
#     ("R004", ["PER", "SYD", "BRI"], 4),
#     ("R005", ["SYD", "BRI", "DAR"], 5),
#     ("R006", ["BRI", "DAR", "PER"], 6),
#     ("R007", ["DAR", "PER", "SYD"], 7),
#     ("R008", ["PER", "SYD", "MEL"], 8),
#     ("R009", ["SYD", "MEL", "ASP"], 9),
#     ("R010", ["MEL", "ASP", "SYD"], 10),
#     ("R011", ["ASP", "SYD", "ADL"], 11),
#     ("R012", ["SYD", "ADL", "BRI"], 12),
#     ("R013", ["ADL", "BRI", "PER"], 13),
#     ("R014", ["BRI", "PER", "MEL"], 14),
#     ("R015", ["PER", "MEL", "DAR"], 15),
#     ("R016", ["MEL", "DAR", "SYD"], 16),
#     ("R017", ["DAR", "SYD", "ADL"], 17),
#     ("R018", ["SYD", "ADL", "PER"], 18),
#     ("R019", ["ADL", "PER", "BRI"], 19),
#     ("R020", ["PER", "BRI", "SYD"], 20)
# ]
#
# for route_id, locations, hours in route_data:
#     departure_time = datetime.now() + timedelta(hours=hours)
#     route = manager.create_route(route_id, locations, departure_time)
#     suitable_truck = trucks[route_data.index((route_id, locations, hours)) % len(trucks)]
#     manager.assign_route_to_truck(suitable_truck, route)
#
# # User tracks packages
# for package in user.ordered_packages:
#     user.track_package(package._package_id, app_data)
#
# # Print status of all routes
# manager.get_routes_status()
#
# for truck in trucks:
#     for route in truck._routes:
#         route.simulate_route()
from datetime import datetime, timedelta
from models.location import Location
from models.route import Route
from models.vehicle import Vehicle
#
# # Define locations
# sydney = Location("Sydney")
# melbourne = Location("Melbourne")
# adelaide = Location("Adelaide")
# perth = Location("Perth")
#
# # Create a route with defined locations
# route = Route(locations=[sydney, melbourne, adelaide, perth], departure_time=datetime(2024, 8, 17, 10, 0))
#
# # Print route details before simulation
# print("Before simulation:")
# print(route)
#
# # Simulate the route
# print("\nStarting simulation...")
# route.simulate_route()
#
# # Print route details after simulation
# print("\nAfter simulation:")
# print(route)
