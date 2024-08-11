# from models.location import Location
import random
import string

class Package:

    id_list = []

    def __init__(self, start_location, end_location, weight: float, contact_info: str):
        self._start_location = start_location
        self._end_location = end_location
        self.weight = weight
        self.customer_info = contact_info
        self._package_id = self.generate_id()

    # def validate_id(self, value):
    #     if not value.isalnum():
    #         raise ValueError('Package ID should contain letters and digits only')
    #     elif not any(char.isdigit() for char in value):
    #         raise ValueError('Package ID should contain at least one digit')
    #     elif not any(char.isalpha() for char in value):
    #         raise ValueError('Package ID should contain at least one letter')
    #     elif len(value) < 3:
    #         raise ValueError('Package ID should be at least 3 characters long')
    #     else:
    #         self._package_id = value

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
        if not value:
            raise ValueError('Weight cannot be empty')
        elif not isinstance(value, (float, int)):
            raise ValueError('Weight must be a number')
        elif value <= 0:
            raise ValueError('Weight cannot be 0 or less')
        else:
            self._weight = value

    @property
    def contact_info(self):
        return self._contact_info
    
    @contact_info.setter
    def contact_info(self, value):
        self._contact_info = value

    # def calculate_distance(self):
    #     distance = self.start_location.get_distance_to(self.end_location.name)
    #     return distance

    def generate_id(self):

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