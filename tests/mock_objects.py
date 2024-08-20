from datetime import timedelta, datetime
from unittest.mock import Mock, PropertyMock, MagicMock

from helpers.distances import distances
from helpers.functions import generate_id
from models.constants.location_constants import Cities
from models.location import Location
from models.route import Route
from models.vehicle import Vehicle
from models.user import User
from tests.location_test import VALID_LOCATION_NAME
from models.package import Package
from core.application_data import ApplicationData


def mock_package(start_location, end_location, weight, customer_info):
    package = Mock(spec=Package)
    package._start_location = start_location
    package._end_location = end_location
    package.customer_info = customer_info
    package.weight = weight
    package._package_id = None

    type(package).package_id = PropertyMock(return_value=package._package_id)

    type(package).start_location = PropertyMock(return_value = package._start_location)

    type(package).end_location = PropertyMock(return_value = package._end_location)

    return package


def mock_location(name):
    location = MagicMock(spec=Location)
    location.name = name
    location.distances = Cities.distances

    def get_distance_to(other_city: str):
        if Cities.from_string(other_city) not in location.distances[location.name]:
            raise ValueError(f"No route between {location.name} and {other_city}")
        return location.distances[location.name][Cities.from_string(other_city)]

    location.get_distance_to.side_effect = get_distance_to

    def custom_str():
        return f'{location.name}'

    location.__str__.side_effect = custom_str

    return location


def mock_route():
    route = MagicMock(spec=Route)
    route.locations = []
    route.truck = None
    route.packages = []

    route.departure_time = datetime(2024, 8, 10, 10, 00)
    def calculate_travel_time(distance):
        average_speed = Vehicle.SPEED_CONSTANT
        return distance / average_speed

    route.calculate_travel_time.side_effect = calculate_travel_time

    def calculate_arrival_times():
        """Calculate estimated arrival times for each location in the route."""
        arrival_times = [route.departure_time]
        current_time = arrival_times[0]

        for i in range(len(route.locations) - 1):
            start = route.locations[i]
            end = route.locations[i + 1]
            distance = start.get_distance_to(end.name)
            travel_time_hours = route.calculate_travel_time(distance)
            travel_time_delta = timedelta(hours=travel_time_hours)
            current_time += travel_time_delta
            arrival_times.append(current_time)

        # Convert datetime objects to strings in desired format
        return [time.strftime('%d-%m-%Y %H:%M') for time in arrival_times]

    route.calculate_arrival_times.side_effect = calculate_arrival_times

    def next_stop(current_location):
        """Determine the next stop based on the current location."""
        if current_location not in route.locations:
            raise ValueError(f"Current location {current_location} not on route.")

        current_index = route.locations.index(current_location)
        if current_index < len(route.locations) - 1:
            return route.locations[current_index + 1]
        return None  # No further stops

    route.next_stop.side_effect = next_stop

    def update_locations_for_packages(packages):

        for package in packages:
            if package.start_location not in route.locations:
                route.locations.append(package.start_location)
            if package.end_location not in route.locations:
                route.locations.append(package.end_location)

    route.update_locations_for_packages.side_effect = update_locations_for_packages

    def custom_str():
        arrival_times = route.calculate_arrival_times()
        stops_with_times = ', '.join(f"{loc} ({time})" for loc, time in zip(route.locations, arrival_times))
        return f"Route ID: {route.id}, Locations: {stops_with_times}, Truck ID: {route.truck.id_truck if route.truck else 'No truck assigned'}"

    route.__str__.side_effect = custom_str

    def custom_len():
        total_distance = 0
        for i in range(len(route.locations) - 1):
            start_location = route.locations[i]
            end_location = route.locations[i + 1]
            total_distance += start_location.get_distance_to(end_location.name)
        return total_distance

    route.__len__.side_effect = lambda: custom_len()

    return route


def mock_application_data():
    application_data = Mock(spec=ApplicationData)
    application_data.vehicles = []
    application_data.routes = []
    application_data.packages = []
    application_data.users = []

    def find_package_by_id(package_id):
        return next((package for package in application_data.packages if package._package_id == package_id), None)

    application_data.find_package_by_id.side_effect = find_package_by_id

    def find_route_by_package_id(package_id):
        for route in application_data.routes:
            for package in route.packages:
                if package.id == package_id:
                    return route
        return None

    application_data.find_route_by_package_id.side_effect = find_route_by_package_id

    def find_vehicle_by_id(vehicle_id):
        return next((vehicle for vehicle in application_data.vehicles if vehicle.id_truck == vehicle_id), None)

    application_data.find_vehicle_by_id.side_effect = find_vehicle_by_id

    def find_route_for_package(package_id):
        package = application_data.find_package_by_id(package_id)
        if package:
            for route in application_data.routes:
                start_location_match = any(location.name == package.start_location for location in route.locations)
                end_location_match = any(location.name == package.end_location for location in route.locations)
                if start_location_match and end_location_match:
                    return route
        return None

    application_data.find_route_for_package.side_effect = find_route_for_package

    def find_route_by_id(route_id):

        return next((route for route in application_data.routes if route.route_id == route_id), None)

    application_data.find_route_by_id.side_effect = find_route_by_id

    def find_user_by_id(user_id):

        return next((user for user in application_data.users if user.user_id == user_id), None)

    application_data.find_user_by_id.side_effect = find_user_by_id

    def init_vehicles():
        application_data.vehicles: list[Vehicle] = []
        for fleet in Vehicle.vehicle_park.values():
            for _ in range(fleet["units"]):
                new_truck = Vehicle(fleet["name"], fleet["capacity"], fleet["range"])
                application_data.vehicles.append(new_truck)

    application_data.init_vehicles.side_effect = init_vehicles
    application_data.init_vehicles()

    def init_users():
        application_data.users: list[User] = []
        for n in range(5):
            user_id = 1000 + n
            name = "Test_User_0" + str(n)
            contact_info = f"{name}@gmail.com"
            new_user = User(name, contact_info, "password")
            application_data.users.append(new_user)

    application_data.init_users.side_effect = init_users
    application_data.init_users()

    return application_data


def mock_vehicle(name, capacity, truck_range, truck_id=None):
    vehicle = MagicMock(spec=Vehicle)
    vehicle._name = name
    vehicle._capacity = capacity
    vehicle._truck_range = truck_range
    vehicle._initial_capacity = capacity
    vehicle._initial_range = truck_range
    vehicle._routes = []
    vehicle._id_truck = truck_id if truck_id else generate_id(4, 4)  # Ensure truck ID is set
    vehicle._current_location = 'Garage'

    type(vehicle).id_truck = PropertyMock(return_value=vehicle._id_truck)

    def find_active_route(track_date=None):
        if not track_date:
            track_date = datetime.now()
        else:
            if not isinstance(track_date, datetime):
                track_date = datetime.strptime(track_date, '%d-%m-%Y %H:%M')

        active_route = None
        for assigned_route in vehicle._routes:
            assigned_route_start_date = assigned_route.departure_time
            assigned_route_expected_hours = len(assigned_route) / Vehicle.SPEED_CONSTANT
            assigned_route_end_date = assigned_route_start_date + timedelta(hours=assigned_route_expected_hours)

            if assigned_route_start_date <= track_date <= assigned_route_end_date:
                active_route = assigned_route

        return active_route

    vehicle.find_active_route.side_effect = find_active_route

    def track_location(start_time=None):
        if start_time is None:
            start_time = datetime.now()
        else:
            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, '%d-%m-%Y %H:%M')

        location = "Garage"
        for route in vehicle._routes:
            route_start_date = route.departure_time
            if start_time < route_start_date:
                return location
            for n in range(len(route.locations) - 1):
                start_location = route.locations[n]
                end_location = route.locations[n + 1]
                route_distance = distances[start_location.name][end_location.name]
                route_duration = route_distance / Vehicle.SPEED_CONSTANT
                route_delta = timedelta(hours=route_duration)
                route_end_date = route_start_date + route_delta
                if route_start_date <= start_time < route_end_date:
                    return f"In transit to {end_location.name}"
                route_start_date = route_end_date
                location = end_location.name

        return location

    vehicle.track_location.side_effect = track_location

    def check_schedule(new_route):
        if len(vehicle._routes) > 0:
            new_route_start_date = new_route.departure_time

            last_route = vehicle._routes[-1]
            last_route_start_date = last_route.departure_time
            last_route_expected_hours = len(last_route) / Vehicle.SPEED_CONSTANT
            last_route_delta = timedelta(hours=last_route_expected_hours)
            last_route_end_date = last_route_start_date + last_route_delta

            if last_route_end_date < new_route_start_date:
                return True
            else:
                print(f"Vehicle not available before {last_route_end_date}")
                return False
        else:
            return True

    vehicle.check_schedule.side_effect = check_schedule

    def check_matching_locations(new_route):
        """Checks if the route start location is the truck current location"""
        if len(vehicle._routes) > 0:
            last_route = vehicle._routes[-1]
            if last_route.locations[-1].name == new_route.locations[0].name:
                return True
            else:
                raise ValueError(f"Can't assign new route. Route must start from {last_route.locations[-1].name}")
        else:
            return True

    vehicle.check_matching_locations.side_effect = check_matching_locations

    def check_remaining_range(new_route):
        if vehicle._initial_range == vehicle._truck_range and vehicle._initial_range > len(new_route):
            return True
        if vehicle._truck_range > len(new_route):
            return True
        else:
            raise ValueError(f"Range not enough to cover {len(new_route)} km")

    vehicle.check_remaining_range.side_effect = check_remaining_range

    def assign_route(new_route):
        available = vehicle.check_schedule(new_route)
        location = vehicle.check_matching_locations(new_route)
        has_range = vehicle.check_remaining_range(new_route)

        if all([available, location, has_range]):
            vehicle._routes.append(new_route)
            vehicle._truck_range -= len(new_route)

            print(f"Route {new_route.id} added to {vehicle._name} ID: {vehicle.id_truck}")

    vehicle.assign_route.side_effect = assign_route

    def update_capacity(package_weight: float):
        if package_weight <= 0:
            raise ValueError("Package weight is expected to be a positive value")
        if package_weight > vehicle._capacity:
            raise ValueError(f"Free capacity of vehicle: {vehicle.capacity}kg can't load {package_weight}kg")

        vehicle._capacity -= package_weight

    vehicle.update_capacity.side_effect = update_capacity

    def reset():
        """Reset the truck's capacity and range to initial values."""
        vehicle._capacity = vehicle._initial_capacity
        vehicle._truck_range = vehicle._initial_range
        print(f"Vehicle ID: {vehicle._id_truck} has been reset.")

    vehicle.reset.side_effect = reset

    def custom_str():
        return (
            f"{vehicle._name} ID:--{vehicle._id_truck}--\n"
            f"location: {vehicle.track_location()}\n"
            f"route: {vehicle.find_active_route()}\n"
            f"capacity left: {vehicle._capacity}kg\n"
            f"range to go: {vehicle._truck_range}km"
        )

    vehicle.__str__.side_effect = custom_str

    return vehicle

def mock_user(name, contact_info, password, role='basic'):
    user = MagicMock(spec = User)
    user.name = name
    user.contact_info = contact_info
    user.role = role

    def update_contact_info(new_contact_info):
        user.contact_info = new_contact_info
        print(f"Contact information for user {user.id} updated.")

    user.update_contact_info.side_effect = update_contact_info

    def custom_str():
        return f"User ID: {user.id}, Name: {user.name}, Role: {user.role}, Contact Info: {user.contact_info}"

    user.__str__.side_effect = custom_str

    def order_package(start_location, end_location, weight, application_data):
        package = Package(start_location, end_location, weight, user.contact_info)
        application_data.packages.append(package)
        user.ordered_packages.append(package)
        print(f"Package {package.id} ordered by user {user.id}.")

    user.order_package.side_effect = order_package

    def track_package(package_id, application_data):
        package = application_data.find_package_by_id(package_id)
        if package and package in user.ordered_packages:
            current_route = application_data.find_route_for_package(package_id)
            if current_route and current_route.truck:
                current_location = current_route.truck.track_location()
                expected_arrival = user.calculate_expected_arrival(current_route, package)
                print(f"Package ID: {package._package_id}")
                print(f"Current Location: {current_location}")
                print(
                    f"Expected Arrival Time: {expected_arrival.strftime('%Y-%m-%d %H:%M') if not isinstance(expected_arrival, str) else expected_arrival}")
                print(f"Weight: {package.weight} kg")
                print(f"Start Point: {package.start_location}")
            else:
                print(f"No route or truck found for package {package_id}.")
        else:
            print(f"Package {package_id} not found or not ordered by this user.")

    user.track_package.side_effect = track_package

    # def calculate_expected_arrival(route, package):
    #     """Calculate the expected arrival time at the package's end location."""
    #     arrival_times = route.calculate_arrival_times()
    #     # Find the index of the package's end location in the route's location list
    #     end_location_index = route.locations.index(package.end_location)
    #     # Return the expected arrival time at the package's end location
    #     return arrival_times[end_location_index]
    #
    # user.calculate_expected_arrival.side_effect = calculate_expected_arrival

    return user
