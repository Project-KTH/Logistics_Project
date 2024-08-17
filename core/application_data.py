from models.vehicle import Vehicle
from models.user import User


class ApplicationData:
    def __init__(self):
        self.init_vehicles()
        self.routes = []
        self.packages = []
        self.init_users()

    def find_package_by_id(self, package_id):
        return next((package for package in self.packages if package._package_id == package_id), None)

    def find_route_by_package_id(self, package_id):
        for route in self.routes:
            for package in route.packages:
                if package.id == package_id:
                    return route
        return None

    def find_vehicle_by_id(self, vehicle_id):
        return next((vehicle for vehicle in self.vehicles if vehicle.id_truck == vehicle_id), None)

    def find_route_for_package(self, package_id):
        package = self.find_package_by_id(package_id)
        if package:
            for route in self.routes:
                if package.start_location in route.locations and package.end_location in route.locations:
                    return route
        return None

    def find_route_by_id(self, route_id):
        return next((route for route in self.routes if route.id == route_id), None)

    def find_user_by_id(self, user_id):
        return next((user for user in self.users if user.user_id == user_id), None)
    
    def find_user_by_contact_info(self, contact_info):
        for user in self.users:
            if user.contact_info == contact_info:
                return user
        
        raise ValueError(f'User with {contact_info} contact info does not exist!')

    def init_vehicles(self):
        self.vehicles: list[Vehicle] = []
        for fleet in Vehicle.vehicle_park.values():
            for _ in range(fleet["units"]):
                new_truck = Vehicle(fleet["name"], fleet["capacity"], fleet["range"])
                self.vehicles.append(new_truck)

    def init_users(self):
        self.users: list[User] = []
        for n in range(5):
            password = "001234kthabC"
            name = "Test_User_0" + str(n)
            contact_info = f"{name}@gmail.com"
            new_user = User(name, contact_info, password)
            self.users.append(new_user)
