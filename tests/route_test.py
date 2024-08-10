from datetime import datetime
from unittest import TestCase
from models.route import Route
from tests.mock_objects import mock_location, mock_package

VALID_ROUTE_ID = 1111
VALID_ROUTE_DEPARTURE_TIME = '10:45'


class TestRoute(TestCase):
    def setUp(self):
        self.location1 = mock_location()
        self.location1.name = 'SYD'
        self.location2 = mock_location()
        self.location2.name = 'PER'
        self.location3 = mock_location()
        self.location3.name = 'DAR'
        self.location4 = mock_location()
        self.location4.name = 'MEL'
        self.location5 = mock_location()
        self.location5.name = 'BRI'
        self.package1 = mock_package()
        self.package1.start_location = self.location1
        self.package1.end_location = self.location5
        self.package2 = mock_package()
        self.package2.start_location = self.location2
        self.package2.end_location = self.location4
        self.package3 = mock_package()
        self.package3.start_location = self.location3
        self.package3.end_location = self.location5
        self.route = Route(VALID_ROUTE_ID, [self.location1, self.location2, self.location3],
                           VALID_ROUTE_DEPARTURE_TIME)

    def testInitialiser_InitialisesSuccessfully(self):
        self.assertEqual(self.route.route_id, VALID_ROUTE_ID)
        self.assertEqual(self.route.locations, [self.location1, self.location2, self.location3])
        self.assertEqual(self.route.departure_time, VALID_ROUTE_DEPARTURE_TIME)
        self.assertIsInstance(self.route, Route)

    def testCalculateTravelTime_WorksCorrectly(self):
        self.assertEqual(self.route.calculate_travel_time(100), 1.1494252873563218)

    def testCalculateArrivalTimes_WorksCorrectly(self):
        # Example expected arrival times, adjust based on your mock data and distance calculations
        expected_arrival_times = ['10:45', '08:54', '07:10']
        self.assertEqual(self.route.calculate_arrival_times(), expected_arrival_times)

    def testCalculateNextStop_WorksCorrectly(self):
        self.assertEqual(self.route.next_stop(self.location2), self.location3)

    def testNextStop_InvalidLocation_(self):
        with self.assertRaisesRegex(ValueError, "Current location MEL not on route."):
            self.route.next_stop(self.location4)

    def testUpdateCurrentLocationsForPackages_UpdatesSuccessfully(self):
        self.route.update_locations_for_packages([self.package1, self.package2, self.package3])
        self.assertEqual(self.route.locations, [self.location1, self.location2, self.location3, self.location5,
                                                self.location4])

    def testStr_ReturnsCorrectFormat(self):
        expected = f'Route ID: 1111, Locations: SYD (10:45), PER (08:54), DAR (07:10), Truck ID: No truck assigned'
        self.assertEqual(str(self.route), expected)