from datetime import timedelta, datetime
from models.location import Location
from models.vehicle import Vehicle
from models.location import Location


class Route:
    def __init__(self, route_id, locations, departure_time):
        self.route_id = route_id
        self.locations = locations  # Ordered list of locations to visit
        self.departure_time = datetime.strptime(departure_time, '%d-%m-%Y %H:%M')
        self.truck = None

    def calculate_travel_time(self, distance):
        """Calculate travel time based on distance and vehicle speed."""
        average_speed = Vehicle.SPEED_CONSTANT
        return distance / average_speed

    def calculate_arrival_times(self):
        """Calculate estimated arrival times for each location in the route."""
        arrival_times = [self.departure_time]
        current_time = self.departure_time

        for i in range(len(self.locations) - 1):
            start = self.locations[i]
            end = self.locations[i + 1]
            distance = start.get_distance_to(end.name)
            travel_time_hours = self.calculate_travel_time(distance)
            travel_time_delta = timedelta(hours=travel_time_hours)
            current_time += travel_time_delta
            arrival_times.append(current_time)

        # Convert datetime objects to strings in desired format
        return [time.strftime('%d-%m-%Y %H:%M') for time in arrival_times]

    def next_stop(self, current_location):
        """Determine the next stop based on the current location."""
        if current_location not in self.locations:
            raise ValueError(f"Current location {current_location} not on route.")

        current_index = self.locations.index(current_location)
        if current_index < len(self.locations) - 1:
            return self.locations[current_index + 1]
        return None  # No further stops

    def update_locations_for_packages(self, packages):
        """Update the route's locations to include necessary stops for the packages."""
        # Add start and end locations for each package, ensuring order
        for package in packages:
            if package.start_location not in self.locations:
                self.locations.append(package.start_location)
            if package.end_location not in self.locations:
                self.locations.append(package.end_location)

    def __str__(self):
        arrival_times = self.calculate_arrival_times()
        stops_with_times = ', '.join(f"{loc} ({time})" for loc, time in zip(self.locations, arrival_times))
        return f"Route ID: {self.route_id}, Locations: {stops_with_times}, Truck ID: {self.truck.id_truck if self.truck else 'No truck assigned'}"

    def __len__(self):
        """Calculate the total length of the route."""
        total_distance = 0
        for i in range(len(self.locations) - 1):
            start_location = self.locations[i]
            end_location = self.locations[i + 1]
            total_distance += start_location.get_distance_to(end_location.name)
        return total_distance

