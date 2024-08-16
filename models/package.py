import random
import string

from helpers.functions import generate_id


class Package:

    id_list = []

    def __init__(self, start_location, end_location, weight: float, customer_info: str):
        self._start_location = start_location
        self._end_location = end_location
        self.weight = weight
        self.customer_info = customer_info
        self._package_id = generate_id(existing_ids=self.id_list)


    @property
    def id(self):
        return self._package_id

    @property
    def start_location(self):
        return self._start_location
    
    @property
    def end_location(self):
        return self._end_location
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, value):
        if value == '':
            raise ValueError('Weight cannot be empty')
        elif not isinstance(value, (float, int)):
            raise ValueError('Weight must be a number')
        elif value <= 0:
            raise ValueError('Weight cannot be 0 or less')
        else:
            self._weight = value

    @property
    def customer_info(self):
        return self._customer_info

    @customer_info.setter
    def customer_info(self, value):
        if not value or value.strip() == '':
            raise ValueError('Customer info cannot be an empty string')
        self._customer_info = value

    def generate_id(self):
        """Generates unique ID for each package"""
        letters = string.ascii_uppercase
        numbers = string.digits

        while True:

            first_two_characters = ''.join(random.choices(letters, k=2))
            rest_characters = ''.join(random.choices(numbers, k=4))
            the_id = first_two_characters + rest_characters

            if the_id not in self.id_list:
                self.id_list.append(the_id)
                return the_id

    def __str__(self) -> str:
        return (
            f'Package ID: {self._package_id}\n'
            f'Weight: {self.weight}kg\n'
            f'From: {self.start_location}\n'
            f'To: {self.end_location}\n'
            f'Customer: {self.customer_info}\n'
        )