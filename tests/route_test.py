from datetime import datetime
from models.location import Location
from unittest import TestCase
from models.route import Route
from tests.mock_objects import mock_location, mock_package

VALID_ROUTE_ID = 1111
VALID_ROUTE_DEPARTURE_TIME = datetime(2024, 8, 10, 10, 45)


class TestRoute(TestCase):
    def setUp(self):
        self.location1 = mock_location('SYD')
        self.location2 = mock_location('PER')
        self.location3 = mock_location('DAR')
        self.location4 = mock_location('MEL')
        self.location5 = mock_location('BRI')
        self.package1 = mock_package('SYD', 'BRI', 1, 'contact info')
        self.package2 = mock_package('PER', 'MEL', 1, 'contact info')
        self.package3 = mock_package('DAR', 'BRI', 1, 'contact info')
        self.route = Route(VALID_ROUTE_ID, ['SYD', 'PER', 'DAR'],
                           VALID_ROUTE_DEPARTURE_TIME)

    def testInitialiser_InitialisesSuccessfully(self):
        self.assertEqual(self.route.route_id, VALID_ROUTE_ID)
        for a_location in self.route.locations:
            self.assertIsInstance(a_location, Location)
        self.assertEqual(self.route.locations[0].name, 'SYD')
        self.assertEqual(self.route.locations[1].name, 'PER')
        self.assertEqual(self.route.locations[2].name, 'DAR')
        self.assertEqual(self.route.departure_time, VALID_ROUTE_DEPARTURE_TIME)
        self.assertIsInstance(self.route, Route)

    def testCalculateTravelTime_WorksCorrectly(self):
        self.assertEqual(self.route.calculate_travel_time(100), 1.1494252873563218)

    def testCalculateArrivalTimes_WorksCorrectly(self):
        # Example expected arrival times, adjust based on your mock data and distance calculations
        expected_arrival_times = ['10-08-2024 10:45', '12-08-2024 08:54', '14-08-2024 07:10']
        self.assertEqual(self.route.calculate_arrival_times(), expected_arrival_times)

    def testCalculateNextStop_WorksCorrectly(self):
        self.assertEqual(self.route.next_stop('SYD'), 'PER')

    def testNextStop_InvalidLocation_(self):
        with self.assertRaisesRegex(ValueError, "Current location MEL not on route."):
            self.route.next_stop(self.location4)

    def testUpdateCurrentLocationsForPackages_UpdatesSuccessfully(self):
        self.route.update_locations_for_packages([self.package1, self.package2, self.package3])
        self.assertEqual(self.route.locations[0].name, 'SYD')
        self.assertEqual(self.route.locations[1].name, 'PER')
        self.assertEqual(self.route.locations[2].name, 'DAR')
        self.assertEqual(self.route.locations[3].name, 'BRI')
        self.assertEqual(self.route.locations[4].name, 'MEL')

    def testStr_ReturnsCorrectFormat(self):
        expected = (f'Route ID: 1111, Locations: SYD (10-08-2024 10:45), PER (12-08-2024 08:54), '
                    f'DAR (14-08-2024 07:10), Truck ID: No truck assigned')
        self.assertEqual(str(self.route), expected)

    def testLen_ReturnCorrectly(self):
        self.assertEqual(len(self.route), 8041)