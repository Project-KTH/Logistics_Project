from models.route import Route
from models.package import Package
from models.user import User
from models.vehicle import Vehicle
from datetime import datetime

class Manager(User):
    def __init__(self, name, contact_info, password, application_data, access_level='basic'):
        super().__init__(name, contact_info, password, role='manager')
        self.application_data = application_data
        self.access_level = access_level

    # Package Management
    def create_package(self, start_location, end_location, weight, customer_info):
        new_package = Package(start_location, end_location, weight, customer_info)
        self.application_data.packages.append(new_package)
        print(f"Package {new_package.id} created.")
        return new_package

    def delete_package(self, package_id):
        package = self.application_data.find_package_by_id(package_id)
        if package:
            self.application_data.packages.remove(package)
            print(f"Package {package_id} deleted.")
        else:
            print("Package not found.")

    # Vehicle Management
    def add_truck(self, name, home_base):
        if name not in Vehicle.vehicle_park:
            raise ValueError(f"Model name '{name}' is not available in the vehicle park.")

        fleet_info = Vehicle.vehicle_park[name]
        new_truck = Vehicle(name=fleet_info["name"], capacity=fleet_info["capacity"], truck_range=fleet_info["range"])
        self.application_data.vehicles.append(new_truck)
        print(f"Truck {new_truck.id_truck} ({new_truck.name}) added at location {home_base}.")
        return new_truck

    def reset_truck(self, truck_id):
        truck = self.application_data.find_vehicle_by_id(truck_id)
        if truck:
            truck.reset()
            print(f"Truck {truck_id} reset.")
        else:
            print("Truck not found.")

    def assign_route_to_truck(self, truck, route):
        """Assign a route to a truck, ensuring all checks are passed."""
        if truck.check_schedule(route) and truck.check_matching_locations(route) and truck.check_remaining_range(route):
            truck.assign_route(route)
            route.truck = truck
            print(f"Truck {truck.id_truck} assigned to route {route.id}.")
        else:
            print(f"Cannot assign route {route.id} to truck {truck.id_truck} due to scheduling, location, or range constraints.")

    def find_suitable_truck(self, route):
        """Find a suitable truck for a given route based on capacity and location."""
        for truck in self.application_data.vehicles:
            if truck.track_location(datetime.now()) == route.locations[0] and truck.capacity >= sum(pkg.weight for pkg in self.application_data.packages):
                return truck
        print(f"No suitable truck found for route {route.id}.")
        return None

        # Route Management

    def create_route(self, locations=None, departure_time=None):
        if not locations:
            locations = self.generate_locations_from_packages(self.application_data.packages)

        if not departure_time:
            departure_time = datetime.now()

        new_route = Route(locations, departure_time)
        self.application_data.routes.append(new_route)
        print(f"Route {new_route.id} created.")
        return new_route

    def generate_locations_from_packages(self, packages):
        unique_locations = set()
        for package in packages:
            unique_locations.add(package.start_location)
            unique_locations.add(package.end_location)
        return list(unique_locations)

    def get_routes_status(self):
        now = datetime.now()

        for route in self.application_data.routes:
            if route.truck:
                current_stop = route.truck.track_location(now)
                delivery_weight = sum(package.weight for package in self.application_data.packages if package.start_location in route.locations)
                location_names = [loc.name for loc in route.locations]
                print(f"Route ID: {route.route_id}")
                print(f"Stops: {', '.join(location_names)}")
                print(f"Delivery Weight: {delivery_weight} kg")
                print(f"Current Location: {current_stop}")
                print("-" * 40)

    def remove_user(self, user_id):
        user = self.application_data.find_user_by_id(user_id)
        if user:
            self.application_data.users.remove(user)
            print(f"User {user_id} removed.")
        else:
            print("User not found.")

    def assign_role(self, user_id, new_role):
        user = self.application_data.find_user_by_id(user_id)
        if user:
            user.role = new_role
            print(f"User {user_id} role updated to {new_role}.")
        else:
            print("User not found.")
