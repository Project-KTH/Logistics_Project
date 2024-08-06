from constants.location_constants import Cities

class Location:
    def __init__(self, city: Cities):
        self.validate_name(city)
        
    
    def validate_name(self, value):
        if not any(char.isalpha() for char in value):
            raise ValueError('Location name cannot contain any digits or symbols')
        elif not isinstance(value, Cities):
            raise ValueError('No office at this location')
        else:
            self._city = value

    @property
    def city(self):
        return self._city

        