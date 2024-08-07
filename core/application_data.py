class ApplicationData:
    def __init__(self):
        self.vehicles = []
        self.routes = []
        self.packages = []
        self.users = []

    def find_package_by_id(self, package_id):
        """
        Find a package by its unique ID.

        :param package_id: Unique identifier for the package.
        :return: Package object if found, otherwise None.
        """
        return next((package for package in self.packages if package.package_id == package_id), None)

    def find_vehicle_by_id(self, vehicle_id):
        """
        Find a vehicle by its unique ID.

        :param vehicle_id: Unique identifier for the vehicle.
        :return: Vehicle object if found, otherwise None.
        """
        return next((vehicle for vehicle in self.vehicles if vehicle.id_truck == vehicle_id), None)

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
