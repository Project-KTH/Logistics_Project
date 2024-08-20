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
        self.package4 = mock_package('PER', 'DAR', 1, 'contact info')
        self.route = Route([self.location1, self.location2, self.location3, self.location4, self.location5], VALID_ROUTE_DEPARTURE_TIME)

    def testInitialiser_InitialisesSuccessfully(self):
        self.assertIsInstance(self.route.id, str)

        self.assertEqual(self.route.locations[0].name, 'SYD')
        self.assertEqual(self.route.locations[1].name, 'PER')
        self.assertEqual(self.route.locations[2].name, 'DAR')
        self.assertEqual(self.route.locations[3].name, 'MEL')
        self.assertEqual(self.route.locations[4].name, 'BRI')

        self.assertEqual(self.route.departure_time, VALID_ROUTE_DEPARTURE_TIME)
        self.assertIsInstance(self.route, Route)
    def testCalculateTravelTime_WorksCorrectly(self):
        self.assertEqual(self.route.calculate_travel_time(100), 1.1494252873563218)

    def testCalculateArrivalTimes_WorksCorrectly(self):

        expected_arrival_times = ['10-08-2024 10:45', '12-08-2024 08:54',
                                  '14-08-2024 07:10', '16-08-2024 02:18',
                                  '16-08-2024 22:35']
        self.assertEqual(self.route.calculate_arrival_times(), expected_arrival_times)

    def testCalculateNextStop_WorksCorrectly(self):
        self.assertEqual(self.route.next_stop('SYD'), 'PER')

    def testNextStop_InvalidLocation_(self):
        with self.assertRaisesRegex(ValueError, "Current location MEL not on route."):
            self.route.next_stop(self.location4)


    def testStr_ReturnsCorrectFormat(self):
        expected = (f'Route ID: {self.route.id}, Locations: SYD (10-08-2024 10:45), PER (12-08-2024 08:54), '
                    f'DAR (14-08-2024 07:10), MEL (16-08-2024 02:18), BRI (16-08-2024 22:35), Truck ID: No truck assigned')
        self.assertEqual(str(self.route), expected)
    def testLen_ReturnCorrectly(self):
        self.assertEqual(len(self.route), 13558)