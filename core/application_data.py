from models.vehicle import Vehicle
from models.user import User

class ApplicationData:
    def __init__(self):
        self.init_vehicles()
        self.routes = []
        self.packages = []
        self.init_users()

    def find_package_by_id(self, package_id):
        """
        Find a package by its unique ID.

        :param package_id: Unique identifier for the package.
        :return: Package object if found, otherwise None.
        """
        return next((package for package in self.packages if package._package_id == package_id), None)

    def find_route_by_package_id(self, package_id):
        # Iterate through routes to find the one containing the package
        for route in self.routes:
            for package in route.packages:
                if package.id == package_id:
                    return route
        return None
    def find_vehicle_by_id(self, vehicle_id):
        """
        Find a vehicle by its unique ID.

        :param vehicle_id: Unique identifier for the vehicle.
        :return: Vehicle object if found, otherwise None.
        """
        return next((vehicle for vehicle in self.vehicles if vehicle.id_truck == vehicle_id), None)

    def find_route_for_package(self, package_id):
        # Finds the route that includes the package's start and end location
        package = self.find_package_by_id(package_id)
        if package:
            for route in self.routes:
                if package.start_location in route.locations and package.end_location in route.locations:
                    return route
        return None

    def find_route_by_id(self, route_id):
        """
        Find a route by its unique ID.

        :param route_id: Unique identifier for the route.
        :return: Route object if found, otherwise None.
        """
        return next((route for route in self.routes if route.route_id == route_id), None)

    def find_user_by_id(self, user_id):
        """
        Find a user by their unique ID.

        :param user_id: Unique identifier for the user.
        :return: User object if found, otherwise None.
        """
        return next((user for user in self.users if user.user_id == user_id), None)
    
    def init_vehicles(self):
        self.vehicles: list[Vehicle] = []
        for fleet in Vehicle.vehicle_park.values():
            for _ in range(fleet["units"]):
                new_truck = Vehicle(fleet["name"], fleet["capacity"], fleet["range"])
                self.vehicles.append(new_truck)
    
    def init_users(self):
        self.users: list[User] = []
        for n in range(5):
            user_id = 1000 + n
            name = "Test_User_0" + str(n)
            contact_info = f"{name}@gmail.com"
            new_user = User(user_id, name, contact_info)
            self.users.append(new_user)

