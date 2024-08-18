from models.constants.location_constants import Cities


class Location:
    def __init__(self, name: str):
        self._name = Cities.from_string(name) if isinstance(name, str) else name.name
        self.distances = Cities.distances

    @property
    def name(self):
        return self._name

    def get_distance_to(self, other_city: str):
        other_city_abbr = Cities.from_string(other_city)
        if other_city_abbr not in self.distances[self.name]:
            raise ValueError(f"No route between {self.name} and {other_city}")
        return self.distances[self.name][other_city_abbr]

    def __str__(self):
        return f'{self.name}'
    
    def __eq__(self, other):
        return self._name == other._name