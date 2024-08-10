from unittest import TestCase
from models.vehicle import Vehicle
from mock_objects import mock_package, mock_route, mock_location

VALID_VEHICLE_NAME = 'Truck'
VALID_CAPACITY = 26_000
VALID_RANGE = 13_000


class TestVehicle(TestCase):

    def setUp(self):
        self.adelaide = mock_location()
        self.adelaide.name = 'ADE'
        self.sydney = mock_location()
        self.sydney.name = 'SYD'
        self.perth = mock_location()
        self.perth.name = 'PER'
        self.darwin = mock_location()
        self.darwin.name = 'DAR'
        self.melbourne = mock_location()
        self.melbourne.name = 'MEL'
        self.alice_springs = mock_location()
        self.alice_springs.name = 'ASP'
        self.brisbane = mock_location()
        self.brisbane.name = 'BRI'

        self.route1 = mock_route()
        self.route1.locations = [self.adelaide, self.sydney, self.perth, self.darwin]
        self.route1.departure_time = '11:45'
        self.route1.route_id = 3553

        self.route2 = mock_route()
        self.route2.location = [self.melbourne, self.alice_springs, self.perth]
        self.route2.departure_time = '9:15'
        self.route2.route_id = 4751

        self.route3 = mock_route()
        self.route3.location = [self.sydney, self.darwin, self.brisbane, self.melbourne, self.alice_springs]
        self.route3.departure_time = '16:34'
        self.route3.route_id = 5634

        self.vehicle = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)

    def test_create_vehicle_with_increment(self):
        truck1 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)
        self.assertEqual(truck1._id_truck, 1001)
        truck2 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)
        self.assertEqual(truck2._id_truck, 1002)

    def testVehicleID_InitialiserCorrectly(self):
        self.assertEqual(self.vehicle._id_truck, 1001)
        truck2 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)
        self.assertEqual(truck2._id_truck, 1002)