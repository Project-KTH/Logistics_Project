from datetime import datetime
from unittest import TestCase
from models.user import User
from tests.mock_objects import mock_application_data, mock_package, mock_location, mock_route, mock_vehicle
from unittest.mock import patch
from io import StringIO

VALID_USER_NAME = 'User'
VALID_USER_CONTACT_INFO = 'contact info'
VALID_USER_PASSWORD = 'password123'

class TestUser(TestCase):

    @patch('helpers.functions.generate_id', return_value=1000)
    def setUp(self, mock_generate_id):
        self.user = User(VALID_USER_NAME, VALID_USER_CONTACT_INFO, VALID_USER_PASSWORD)
        self.application_data = mock_application_data()

        self.package1 = mock_package("PER", 'DAR', 10.5, "user1@example.com")
        self.package1._package_id = 'PKG001'
        self.package2 = mock_package("MEL", "BRI", 5.0, "user2@example.com")
        self.package2._package_id = 'FY8475'
        self.package3 = mock_package("PER", "MEL", 8.0, "user4@example.com")
        self.package3._package_id = 'RT3564'
        self.package4 = mock_package("BRI", "ADL", 7.5, "user5@example.com")
        self.package4._package_id = 'DK6435'

        self.sydney = mock_location('SYD')
        self.perth = mock_location('PER')
        self.brisbane = mock_location('BRI')
        self.alice_springs = mock_location('ASP')
        self.melbourne = mock_location('MEL')
        self.darwin = mock_location('DAR')
        self.adelaide = mock_location('ADE')

        self.scania = mock_vehicle("Scania", 42_000, 8_000)
        self.man = mock_vehicle("Man", 37_000, 10_000)
        self.actros = mock_vehicle("Actros", 26_000, 13_000)
        self.scania2 = mock_vehicle("Scania", 42_000, 8_000)
        self.man2 = mock_vehicle("Man", 37_000, 10_000)
        self.actros2 = mock_vehicle("Actros", 26_000, 13_000)

        self.route1 = mock_route()
        self.route1.locations = [self.melbourne, self.brisbane]
        self.actros2._routes = [self.route1]
        self.route1.truck = self.actros2
        self.route1.departure_time = datetime(year=2024, month=8, day=12, hour=10, minute=0)
        self.route2 = mock_route()
        self.route2.locations = [self.sydney, self.brisbane, self.perth]
        self.route2.truck = self.man
        self.route2.departure_time = datetime(year=2024, month=8, day=12, hour=10, minute=0)
        self.route3 = mock_route()
        self.route3.locations = [self.adelaide, self.melbourne, self.sydney]
        self.route3.truck = self.actros
        self.route3.departure_time = datetime(year=2024, month=8, day=12, hour=10, minute=0)
        self.route4 = mock_route()
        self.route4.locations = [self.alice_springs, self.darwin, self.brisbane, self.perth]
        self.route4.truck = self.man2
        self.route4.departure_time = datetime(year=2024, month=8, day=12, hour=10, minute=0)
        self.route5 = mock_route()
        self.route5.locations = [self.sydney, self.adelaide, self.melbourne, self.darwin]
        self.route5.truck = self.scania2
        self.route5.departure_time = datetime(year=2024, month=8, day=12, hour=10, minute=0)

        self.route_for_package2 = mock_route()
        self.route_for_package2.locations = [self.brisbane, self.perth]
        self.route_for_package2.departure_time = datetime(2024, 8, 10,  10, 00)

        self.user = User(VALID_USER_NAME, VALID_USER_CONTACT_INFO, VALID_USER_PASSWORD)
        self.application_data = mock_application_data()

    def testInitialiser_OK(self):
        self.assertEqual(self.user.name, VALID_USER_NAME)
        self.assertEqual(self.user.contact_info, VALID_USER_CONTACT_INFO)
        self.assertIsInstance(self.user, User)
        self.assertTrue(self.user.authenticate(VALID_USER_PASSWORD))  # Test password hashing


    def testUpdateContactInfo_OK(self):
        self.user.update_contact_info('New contact info')
        self.assertEqual(self.user.contact_info, 'New contact info')

    def testStr_OK(self):
        expected = (
            f'User ID: {self.user.id}, Name: {VALID_USER_NAME}, Role: basic, Contact Info: {VALID_USER_CONTACT_INFO}'
        )

        self.assertEqual(str(self.user), expected)

    @patch('sys.stdout', new_callable=StringIO)
    def testOrderPackage_OK(self, mock_stdout):
        self.user.order_package('SYD', 'PER', 100, application_data=self.application_data)
        self.assertEqual(len(self.application_data.packages), 1)
        self.assertEqual(len(self.user.ordered_packages), 1)

        printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Package {self.user.ordered_packages[0]._package_id} ordered by user {self.user.id}.")

    def testTrackPackage_NoRoute_OK(self):
        self.user.ordered_packages = [self.package1, self.package2, self.package3, self.package4]
        self.application_data.routes = [mock_route() for _ in range(5)]
        self.application_data.packages = [self.package1, self.package2, self.package3, self.package4]
        self.user.track_package('RT3564', self.application_data)

    def testTrackPackage_OnTheWay_OK(self):
        def calculate_expected_arrival(route, package):
            """Calculate the expected arrival time at the package's end location."""
            arrival_times = route.calculate_arrival_times()
            end_location = package.end_location
            end_location_index = next(
                (i for i, loc in enumerate(route.locations)
                 if loc.name == end_location),
                None
            )
            if end_location_index is None:
                raise ValueError(f"End location '{end_location}' not found in route locations.")
            return arrival_times[end_location_index]

        self.user.calculate_expected_arrival = calculate_expected_arrival

        self.user.ordered_packages = [self.package1, self.package2, self.package3, self.package4]
        self.application_data.routes = [mock_route()]
        self.application_data.packages = [self.package1, self.package2, self.package3, self.package4]
        self.user.track_package('FY8475', self.application_data)
    def testCalculateExpectedArrival_OK(self):
        def calculate_expected_arrival(route, package):
            """Calculate the expected arrival time at the package's end location."""
            arrival_times = route.calculate_arrival_times()
            end_location = package.end_location
            end_location_index = next(
                (i for i, loc in enumerate(route.locations)
                 if loc.name == end_location),
                None
            )
            if end_location_index is None:
                raise ValueError(f"End location '{end_location}' not found in route locations.")
            return arrival_times[end_location_index]

        route = mock_route()
        route.locations = [self.melbourne, self.brisbane]  # Ensure the end location 'BRI' is in the route
        route.departure_time = datetime(year=2024, month=8, day=12, hour=10, minute=0)

        self.user.calculate_expected_arrival = calculate_expected_arrival
        self.assertEqual(self.user.calculate_expected_arrival(route, self.package2), '13-08-2024 06:17')