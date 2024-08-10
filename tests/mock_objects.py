from datetime import timedelta
from unittest.mock import Mock, PropertyMock, MagicMock
from models.constants.location_constants import Cities
from models.location import Location
from models.route import Route
from models.vehicle import Vehicle
from tests.location_test import VALID_LOCATION_NAME


from models.package import Package


def mock_package():
    package = Mock(spec=Package)
    package.contact_info = 'contact info'
    package.weight = '1.5'

    return package


def mock_location():
    location = MagicMock(spec=Location)
    location.name = Cities.from_string(VALID_LOCATION_NAME)
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

    def calculate_time():
        average_speed = Vehicle.SPEED_CONSTANT
        return route.distance / average_speed

    route.calculate_time.side_effect = calculate_time

    def calculate_arrival_times():
        """Calculate estimated arrival times for each location in the route."""
        arrival_times = [route.departure_time]
        current_time = route.departure_time

        for i in range(len(route.locations) - 1):
            start = route.locations[i]
            end = route.locations[i + 1]
            distance = start.get_distance_to(end.name)
            travel_time_hours = route.calculate_travel_time(distance)
            travel_time_delta = timedelta(hours=travel_time_hours)
            current_time += travel_time_delta
            arrival_times.append(current_time)

        # Convert datetime objects to strings in desired format
        return [time.strftime('%H:%M') for time in arrival_times]

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
        """Update the route's locations to include necessary stops for the packages."""
        # Add start and end locations for each package, ensuring order
        for package in packages:
            if package.start_location not in route.locations:
                route.locations.append(package.start_location)
            if package.end_location not in route.locations:
                route.locations.append(package.end_location)

    route.update_locations_for_packages.side_effect = update_locations_for_packages

    def custom_str():
        arrival_times = route.calculate_arrival_times()
        stops_with_times = ', '.join(f"{loc} ({time})" for loc, time in zip(route.locations, arrival_times))
        return f"Route ID: {route.route_id}, Locations: {stops_with_times}, Truck ID: {route.truck.id_truck if route.truck else 'No truck assigned'}"

    route.__str__.side_effect = custom_str

    def custom_len():
        total_distance = 0
        for i in range(len(route.locations) - 1):
            start_location = route.locations[i]
            end_location = route.locations[i + 1]
            total_distance += start_location.get_distance_to(end_location.name)
        return total_distance

    route.__len__.side_effect = custom_len

    return route

