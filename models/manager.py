from models.route import Route
from models.package import Package
from models.user import User
from models.vehicle import Vehicle
from datetime import datetime

class Manager(User):
    def __init__(self, user_id, name, contact_info, application_data, access_level='basic'):
        super().__init__(user_id, name, contact_info, role='manager')
        self.application_data = application_data
        self.access_level = access_level  # Differentiates permissions among managers

    # Package Management
    def create_package(self, start_location, end_location, weight, customer_info):
        new_package = Package(start_location, end_location, weight, customer_info)
        self.application_data.packages.append(new_package)
        print(f"Package {new_package._package_id} created.")
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
            truck.reset()  # Reset capacity and range
            print(f"Truck {truck_id} reset.")
        else:
            print("Truck not found.")

    def assign_route_to_truck(self, truck, route):
        """Assign a route to a truck, ensuring all checks are passed."""
        if truck.check_schedule(route) and truck.check_matching_locations(route) and truck.check_remaining_range(route):
            truck.assign_route(route)
            route.truck = truck
            print(f"Truck {truck.id_truck} assigned to route {route.route_id}.")
        else:
            print(f"Cannot assign route {route.route_id} to truck {truck.id_truck} due to scheduling, location, or range constraints.")

    def find_suitable_truck(self, route):
        """Find a suitable truck for a given route based on capacity and location."""
        for truck in self.application_data.vehicles:
            if truck.track_location(datetime.now()) == route.locations[0] and truck.capacity >= sum(pkg.weight for pkg in self.application_data.packages):
                return truck
        print(f"No suitable truck found for route {route.route_id}.")
        return None

    # Route Management
    def create_route(self, route_id, locations, departure_time):
        new_route = Route(route_id, locations, departure_time)
        self.application_data.routes.append(new_route)
        print(f"Route {route_id} created.")
        return new_route

    def get_routes_status(self):
        """Get the status of all delivery routes in progress."""
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

    # User Management
    def add_user(self, user_id, name, contact_info, role):
        if role.lower() == "manager":
            new_user = Manager(user_id, name, contact_info, self.application_data, "basic")
        else:
            new_user = User(user_id, name, contact_info)
        self.application_data.users.append(new_user)
        print(f"User {user_id} added with role {role}.")

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
