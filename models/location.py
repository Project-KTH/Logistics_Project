from models.constants.location_constants import Cities


class Location:
    def __init__(self, name: str):
        self._name = Cities.from_string(name)
        self.distances = Cities.distances

    @property
    def name(self):
        return self._name

    def get_distance_to(self, other_city: str):
        """Gets the distance from the current object to another location"""
        if Cities.from_string(other_city) not in self.distances[self.name]:
            raise ValueError(f"No route between {self.name} and {other_city}")
        return self.distances[self.name][Cities.from_string(other_city)]

    def __str__(self):
        return f'{self.name}'
    
    def __eq__(self, other):
        return self._name == other._name