from models.location import Location


class Package:
    def __init__(self, package_id: str, start_location, end_location, weight: float, contact_info: str):
        self.validate_id(package_id)
        self._start_location = start_location
        self._end_location = end_location
        self.weight = weight
        self.customer_info = contact_info
        self.distance = self.calculate_distance()
        
    def validate_id(self, value):
        if not value.isalnum():
            raise ValueError('Package ID should contain letters and digits only')
        elif not any(char.isdigit() for char in value):
            raise ValueError('Package ID should contain at least one digit')
        elif not any(char.isalpha() for char in value):
            raise ValueError('Package ID should contain at least one letter')
        elif len(value) < 3:
            raise ValueError('Package ID should be at least 3 characters long')
        else:
            self._package_id = value

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

    def __str__(self) -> str:
        return (
            f'Package N: {self.id}\n'
            f'Weight: {self.weight}'
            f'From: {self.start_location}'
            f'To: {self.end_location}'
            f'Customer: {self.customer_info}'
        )