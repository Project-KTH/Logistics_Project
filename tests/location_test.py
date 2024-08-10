from unittest import TestCase
from models.location import Location

VALID_LOCATION_NAME = 'Sydney'
INVALID_LOCATION_NAME = 'Canberra'


class TestLocation(TestCase):

    def setUp(self):
        self.location = Location(VALID_LOCATION_NAME)

    def testInitialiser_InitialisesCorrectly(self):
        self.assertEqual(self.location.name, 'SYD')
        self.assertIsInstance(self.location, Location)

    def testInitialiser_InvalidName_ReturnsError(self):
        with self.assertRaisesRegex(ValueError, 'No office at this location: Canberra'):
            self.location = Location(INVALID_LOCATION_NAME)

    def testGetDistanceTo_FullName_Works(self):
        self.assertEqual(self.location.get_distance_to('Perth'), 4016)

    def testGetDistanceTo_Abbr_Works(self):
        self.assertEqual(self.location.get_distance_to('PER'), 4016)

    def testGetDistanceTo_InvalidLocation_RaisesError(self):
        with self.assertRaisesRegex(ValueError, "No office at this location: Canberra"):
            self.assertEqual(self.location.get_distance_to(INVALID_LOCATION_NAME), 4016)

