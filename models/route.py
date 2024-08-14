from datetime import timedelta, datetime

from helpers.distances import distances
from helpers.functions import generate_id
from models.location import Location
from models.vehicle import Vehicle
from models.location import Location
import time

class Route:
    def __init__(self, location_names, departure_time):
        # Convert location names to Location objects
        self._package_id = generate_id()
        self.locations = [Location(name) for name in location_names]
        if isinstance(departure_time, datetime):
            self.departure_time = departure_time  # Ensure this is a datetime object
        else:
            self.departure_time = datetime.strptime(departure_time, '%d-%m-Y %H:%M')
        self.truck = None

    @property
    def id(self):
        return self._package_id

    def calculate_travel_time(self, distance):
        """Calculate travel time based on distance and vehicle speed."""
        average_speed = Vehicle.SPEED_CONSTANT
        return distance / average_speed

    def calculate_arrival_times(self):
        """Calculate estimated arrival times for each location in the route."""
        arrival_times = [self.departure_time]  # Use the departure_time directly as a datetime object
        current_time = arrival_times[0]

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
        if current_location not in [loc.name for loc in self.locations]:
            raise ValueError(f"Current location {current_location} not on route.")

        current_index = [loc.name for loc in self.locations].index(current_location)
        if current_index < len(self.locations) - 1:
            return self.locations[current_index + 1].name
        return None  # No further stops

    def update_locations_for_packages(self, packages):
        """Update the route's locations to include necessary stops for the packages."""
        # Add start and end locations for each package, ensuring order
        for package in packages:
            start_location = Location(package.start_location)
            end_location = Location(package.end_location)
            if not any(location.name == start_location.name for location in self.locations):
                self.locations.append(start_location)
            if not any(location.name == end_location.name for location in self.locations):
                self.locations.append(end_location)


    def simulate_route(self):
        """Simulate vehicle moving along its route, updating location every 3 seconds."""
        current_time = self.departure_time
        print(f"Starting route simulation for route {self.route_id}.")

        for n in range(len(self.locations) - 1):
            start_location = self.locations[n].name
            end_location = self.locations[n + 1].name
            route_distance = distances[start_location][end_location]
            route_duration = route_distance / Vehicle.SPEED_CONSTANT
            accelerated_seconds = route_duration * 3600  # Accelerate by treating hours as seconds
            arrival_time = current_time + timedelta(seconds=accelerated_seconds)
            print(
                f"Traveling from {start_location} to {end_location}, will arrive by {arrival_time.strftime('%H:%M:%S')}"
            )

            while current_time < arrival_time:
                time_to_arrival = (arrival_time - current_time).total_seconds()
                if time_to_arrival > 3:
                    print(f"Time: {current_time.strftime('%H:%M:%S')} - In transit to {end_location}")
                    time.sleep(0.5)  # Sleep less time to accelerate simulation
                    current_time += timedelta(seconds=accelerated_seconds / 10)  # Simulate a faster passage
                else:
                    current_time += timedelta(seconds=time_to_arrival)
                    break

            print(f"Arrived at {end_location} at {current_time.strftime('%H:%M:%S')}.")

        print(f"Route simulation for route {self.route_id} completed.")


    def __str__(self):
        arrival_times = self.calculate_arrival_times()
        stops_with_times = ', '.join(f"{loc.name} ({time})" for loc, time in zip(self.locations, arrival_times))
        return f"Route ID: {self.route_id}, Locations: {stops_with_times}, Truck ID: {self.truck.id_truck if self.truck else 'No truck assigned'}"

    def __len__(self):
        """Calculate the total length of the route."""
        total_distance = 0
        for i in range(len(self.locations) - 1):
            start_location = self.locations[i]
            end_location = self.locations[i + 1]
            total_distance += start_location.get_distance_to(end_location.name)
        return total_distance