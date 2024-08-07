from constants.location_constants import Cities

class Location:


    def __init__(self, name: str):
        self._name = Cities.from_string(name)
        self._distances = Cities.distances

    @property
    def name(self):
        return self._name

    def get_distance_to(self, other_city: str):
        return self._distances[self._name][other_city]