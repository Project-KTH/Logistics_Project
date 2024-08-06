class Package:
    def __init__(self, id: str, start_location, end_location, weight: float, customer_info: dict):
        self.validate_id(id)
        self._start_location = start_location
        self._end_location = end_location
        self.weight = weight
        self.customer_info = customer_info
        
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
            self._id = value

    @property
    def id(self):
        return self._id

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
        elif value > 1000:
            raise ValueError('Weight cannot more than 1000')
        else:
            self._weight = value

    @property
    def customer_info(self):
        return self._customer_info
    
    @customer_info.setter
    def customer_info(self, value):
        if not isinstance(value, dict):
            raise ValueError('Customer info must be a dictionary')
        else:
            self._customer_info = value

