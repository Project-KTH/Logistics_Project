import random
import string
from models.location import Location

from helpers.functions import generate_id


class Package:

    id_list = []

    def __init__(self, start_location, end_location, weight: float, customer_info: str):
        self.start_location = start_location
        self.end_location = end_location
        self.weight = weight
        self.customer_info = customer_info
        self._package_id = generate_id(existing_ids=self.id_list)
        self.route = None

    @property
    def id(self):
        return self._package_id
    
    @property
    def expected_arrival_time(self):
        if self.route:
            end_location_index = self.route.locations.index(self.end_location)
            arrival_time = self.route.calculate_arrival_times()[end_location_index]
            return arrival_time
        else:
            return "No route assigned."


    @property
    def start_location(self):
        return self._start_location
    
    @start_location.setter
    def start_location(self, value):
        if isinstance(value, str):
            self._start_location = Location(value)
        elif isinstance(value, Location):
            self._start_location = value
        else:
            raise ValueError(f"Invalid start location {value}.")

    @property
    def end_location(self):
        return self._end_location
    
    @end_location.setter
    def end_location(self, value):
        if isinstance(value, str):
            self._end_location = Location(value)
        elif isinstance(value, Location):
            self._end_location = value
        else:
            raise ValueError(f"Invalid end location {value}.")
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError("Invalid weight format. Please provide a numeric value.")
        if value <= 0:
            raise ValueError('Weight cannot be 0 or less')
        self._weight = value

    @property
    def customer_info(self):
        return self._customer_info

    @customer_info.setter
    def customer_info(self, value):
        if not value or value.strip() == '':
            raise ValueError('Customer info cannot be an empty string')
        self._customer_info = value


    def __str__(self) -> str:
        return (
            f'Package ID: {self._package_id}\n'
            f'Weight: {self.weight}kg\n'
            f'From: {self.start_location}\n'
            f'To: {self.end_location}\n'
            f'Customer: {self.customer_info}\n'
            f'Assigned Route ID: {self.route.id if self.route else "No route assigned"}\n'
            f'Expected arrival time: {self.expected_arrival_time}\n'
        )