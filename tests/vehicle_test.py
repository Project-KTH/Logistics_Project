from unittest import TestCase
from models.vehicle import Vehicle
from mock_objects import mock_package, mock_route, mock_location

VALID_VEHICLE_NAME = 'Truck'
VALID_CAPACITY = 26_000
VALID_TRUCK_RANGE = 13_000


class TestVehicle(TestCase):

    def setUp(self):
        self.adelaide = mock_location('ADL')
        self.sydney = mock_location('SYD')
        self.perth = mock_location('PER')
        self.darwin = mock_location('DAR')
        self.melbourne = mock_location('MEL')
        self.alice_springs = mock_location('ASP')
        self.brisbane = mock_location('BRI')

        self.route1 = mock_route()
        self.route1.locations = [self.adelaide, self.sydney, self.perth, self.darwin]
        self.route1.departure_time = '01-07-2024 11:45'
        self.route1.route_id = 3553

        self.route2 = mock_route()
        self.route2.locations = [self.melbourne, self.alice_springs, self.perth]
        self.route2.departure_time = '10-10-2024 9:15'
        self.route2.route_id = 4751

        self.route3 = mock_route()
        self.route3.locations = [self.sydney, self.darwin, self.brisbane, self.melbourne, self.alice_springs]
        self.route3.departure_time = '11-08-2024 03:34'
        self.route3.route_id = 5634

        self.vehicle = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_TRUCK_RANGE)
        self.vehicle._routes = [self.route1, self.route2, self.route3]

    def testInitialiser_InitialisesCorrectly(self):
        self.assertIsInstance(self.vehicle, Vehicle)
        self.assertEqual(self.vehicle.id_truck, 1001)
        self.assertEqual(self.vehicle.capacity, VALID_CAPACITY)
        self.assertEqual(self.vehicle.name, VALID_VEHICLE_NAME)
        self.assertEqual(self.vehicle.truck_range, VALID_TRUCK_RANGE)
        self.assertEqual(self.vehicle._routes, [self.route1, self.route2, self.route3])

    def testVehicleID_InitialisesCorrectly(self):
        truck2 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_TRUCK_RANGE)
        self.assertEqual(truck2.id_truck, 1002)

    def testFindActiveRoute_FindsRoute(self):
        self.assertEqual(self.vehicle.find_active_route(), self.route3)
        self.assertEqual(self.vehicle.find_active_route('01-07-2024 12:45'), self.route1)
        self.assertEqual(self.vehicle.find_active_route('10-10-2024 10:15'), self.route2)
        self.assertEqual(self.vehicle.find_active_route('10-10-2025 10:15'), None)

