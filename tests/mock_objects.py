from unittest.mock import Mock, PropertyMock, MagicMock
from models.constants.location_constants import Cities
from models.location import Location
from tests.location_test import VALID_LOCATION_NAME


from models.package import Package


def mock_package():
    package = Mock(spec=Package)
    package.contact_info = 'contact info'
    package.weight = '1.5'

    return package


def mock_location():
    location = MagicMock(spec=Location)
    location.name = Cities.from_string(VALID_LOCATION_NAME)
    location.distances = Cities.distances

    def get_distance_to(other_city: str):
        if Cities.from_string(other_city) not in location.distances[location.name]:
            raise ValueError(f"No route between {location.name} and {other_city}")
        return location.distances[location.name][Cities.from_string(other_city)]

    location.get_distance_to.side_effect = get_distance_to

    def custom_str():
        return f'{location.name}'

    location.__str__.side_effect = custom_str

    return location


