from models.route import Route
from models.package import Package
from models.user import User
from models.vehicle import Vehicle


class Manager(User):
    def __init__(self, user_id, name, contact_info, application_data, access_level='basic'):
        super().__init__(user_id, name, contact_info, role='manager')
        self.application_data = application_data
        self.access_level = access_level  # Differentiates permissions among managers

    # Package Management
    def create_package(self, package_id, start_location, end_location, weight, customer_info):
        new_package = Package(package_id, start_location, end_location, weight, customer_info)
        self.application_data.packages.append(new_package)
        print(f"Package {package_id} created.")
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
        new_truck = Vehicle(name=fleet_info["name"], capacity=fleet_info["capacity"], range=fleet_info["range"])
        new_truck.current_location = home_base
        self.application_data.vehicles.append(new_truck)
        print(f"Truck {new_truck.id_truck} ({new_truck.name}) added at location {home_base}.")
        return new_truck

    def reset_truck(self, truck_id):
        truck = self.application_data.find_vehicle_by_id(truck_id)
        if truck:
            truck.current_location = "Garage"
            truck._capacity = truck._initial_capacity  # Reset capacity to full
            truck._range = truck._initial_range  # Reset range
            truck.change_status()
            print(f"Truck {truck_id} reset.")
        else:
            print("Truck not found.")

    def assign_truck(self, truck_id, route_id):
        truck = self.application_data.find_vehicle_by_id(truck_id)
        route = self.application_data.find_route_by_id(route_id)
        if truck and route:
            if truck.current_status == "Free" and truck.current_location == route.locations[0]:
                route.truck = truck
                truck.assign_route(*route.locations)
                print(f"Truck {truck_id} assigned to route {route_id}.")
            else:
                print("Truck not available or not at the starting location of the route.")
        else:
            print("Truck or route not found.")

    # Route Management
    def create_route(self, route_id, locations, departure_time):
        new_route = Route(route_id, locations, departure_time)
        self.application_data.routes.append(new_route)
        print(f"Route {route_id} created.")
        return new_route

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
