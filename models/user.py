from models.package import Package

class User:
    def __init__(self, user_id, name, contact_info, role='basic'):
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        self.role = role
        self.ordered_packages = []

    def update_contact_info(self, new_contact_info):
        self.contact_info = new_contact_info
        print(f"Contact information for user {self.user_id} updated.")

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Role: {self.role}, Contact Info: {self.contact_info}"

    def order_package(self, package_id, start_location, end_location, weight, application_data):
        package = Package(package_id, start_location, end_location, weight, self.contact_info)
        application_data.packages.append(package)
        self.ordered_packages.append(package)
        print(f"Package {package_id} ordered by user {self.user_id}.")

    def track_package(self, package_id, application_data):
        package = application_data.find_package_by_id(package_id)
        if package and package in self.ordered_packages:
            current_route = application_data.find_route_by_package_id(package_id)
            current_location = current_route.truck.current_location
            # expected_arrival = TODO

            print(f"Package ID: {package.package_id}")
            print(f"Current Location: {current_location}")
            # print(f"Expected Arrival Time: {expected_arrival}") TODO
            print(f"Weight: {package.weight} kg")
            print(f"Start Point: {package.start_location}")
        else:
            print(f"Package {package_id} not found or not ordered by this user.")
