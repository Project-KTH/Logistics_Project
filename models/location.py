from models.constants.location_constants import Cities


class Location:
    def __init__(self, name: str):
        self._name = Cities.from_string(name)
        self.distances = Cities.distances

    @property
    def name(self):
        return self._name

    def get_distance_to(self, other_city: str):
        if Cities.from_string(other_city) not in self.distances[self.name]:
            raise ValueError(f"No route between {self.name} and {other_city}")
        return self.distances[self.name][Cities.from_string(other_city)]
