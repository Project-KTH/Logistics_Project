import hashlib

from helpers.functions import generate_id, calculate_expected_arrival
from models.package import Package


class User:
    id_list = []

    def __init__(self, name, contact_info, password, role='basic'):
        self._user_id = generate_id(existing_ids=self.id_list)
        self._name = self._validate_name(name)
        self.contact_info = self._validate_contact_info(contact_info)
        self.password_hash = self.hash_password(password)
        self.role = role
        self.ordered_packages = []

    @property
    def id(self):
        return self._user_id

    @property
    def name(self):
        return self._name
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, password):
        return self.password_hash == self.hash_password(password)


    def update_contact_info(self, new_contact_info):
        self.contact_info = self._validate_contact_info(new_contact_info)
        print(f"Contact information for user {self._user_id} updated.")

    def _validate_name(self, name):
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return name

    def _validate_contact_info(self, contact_info):
        if len(contact_info) < 5:
            raise ValueError("Contact information must be at least 5 characters long.")
        return contact_info
    def __str__(self):
        return f"User ID: {self._user_id}, Name: {self.name}, Role: {self.role}, Contact Info: {self.contact_info}"

    def order_package(self, start_location, end_location, weight, application_data):
        package = Package(start_location, end_location, weight, self.contact_info)
        application_data.packages.append(package)
        self.ordered_packages.append(package)
        print(f"Package {package.id} ordered by user {self._user_id}.")

    def track_package(self, package_id, application_data):
        package = application_data.find_package_by_id(package_id)
        if package and package in self.ordered_packages:
            current_route = application_data.find_route_for_package(package_id)
            if current_route and current_route.truck:
                current_location = current_route.truck.track_location()
                expected_arrival = calculate_expected_arrival(current_route, package)

                # Using the __str__ format for the package information
                print(package)
                print(f"Current Location: {current_location}")
                print(
                    f"Expected Arrival Time: {expected_arrival.strftime('%Y-%m-%d %H:%M') if not isinstance(expected_arrival, str) else expected_arrival}")
            else:
                print(f"No route or truck found for package {package_id}.")
        else:
            print(f"Package {package_id} not found or not ordered by this user.")

