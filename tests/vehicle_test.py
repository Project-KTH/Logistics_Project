from datetime import datetime
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
        self.route1.departure_time = datetime.strptime('01-07-2024 11:45', '%d-%m-%Y %H:%M')
        self.route1.route_id = 3553
        self.route1.truck = None

        self.route2 = mock_route()
        self.route2.locations = [self.melbourne, self.alice_springs, self.perth]
        self.route2.departure_time = datetime.strptime('10-10-2024 9:15', '%d-%m-%Y %H:%M')
        self.route2.route_id = 4751
        self.route2.truck = None

        self.route3 = mock_route()
        self.route3.locations = [self.sydney, self.darwin, self.brisbane, self.melbourne, self.alice_springs]
        self.route3.departure_time = datetime.strptime('11-08-2024 03:34', '%d-%m-%Y %H:%M')
        self.route3.route_id = 5634
        self.route3.truck = None

        self.route4 = mock_route()
        self.route4.locations = [self.alice_springs, self.darwin]
        self.route4.departure_time = datetime.strptime('11-09-2024 03:34', '%d-%m-%Y %H:%M')
        self.route4.route_id = 5623
        self.route4.truck = None

        self.route5 = mock_route()
        self.route5.locations = [self.alice_springs, self.darwin, self.brisbane, self.alice_springs, self.melbourne, self.perth, self.darwin]
        self.route5.departure_time = datetime.strptime('13-08-2024 03:34', '%d-%m-%Y %H:%M')
        self.route5.route_id = 4564
        self.route5.truck = None

        self.vehicle = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_TRUCK_RANGE)
        self.vehicle._routes = [self.route1, self.route2, self.route3]

    def testInitialiser_InitialisesCorrectly(self):
        self.assertIsInstance(self.vehicle, Vehicle)
        self.assertEqual(self.vehicle.id_truck, self.vehicle.id_truck)
        self.assertEqual(self.vehicle.capacity, VALID_CAPACITY)
        self.assertEqual(self.vehicle.name, VALID_VEHICLE_NAME)
        self.assertEqual(self.vehicle.truck_range, VALID_TRUCK_RANGE)
        self.assertEqual(self.vehicle._routes, [self.route1, self.route2, self.route3])

    def testVehicleID_InitialisesCorrectly(self):
        truck2 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_TRUCK_RANGE)
        self.assertEqual(truck2.id_truck, truck2.id_truck)

    def testFindActiveRoute_FindsRoute(self):
        self.assertEqual(self.vehicle.find_active_route(), None)
        self.assertEqual(self.vehicle.find_active_route(datetime(2024, 7, 1, 12, 45)), self.route1)
        self.assertEqual(self.vehicle.find_active_route(datetime(2024, 10, 10, 10, 15)), self.route2)
        self.assertEqual(self.vehicle.find_active_route(datetime(2025, 10, 10, 10, 15)), None)

    def testTrackLocation_Works(self):
        self.assertEqual(self.vehicle.track_location(), 'DAR')
        self.assertEqual(self.vehicle.track_location('12-08-2024 05:34'), 'DAR')
        self.assertEqual(self.vehicle.track_location('10-10-2024 9:15'), 'In transit to ASP')
        self.assertEqual(self.vehicle.track_location('10-10-2010 9:15'), 'Garage')

    def testCheckSchedule_Available_ReturnsTrue(self):
        self.assertTrue(self.vehicle.check_schedule(self.route4))

    def testCheckSchedule_Unavailable_ReturnsFalse(self):
        with self.assertRaises(ValueError, msg=f"Vehicle not available before {self.route3.departure_time}"):
            self.vehicle.check_schedule(self.route5)

    def testCheckMatchingLocations_NonMatchingLocations_RaisesError(self):
        with self.assertRaisesRegex(ValueError, "Can't assign new route. Route must start from ASP"):
            self.vehicle.check_matching_locations(self.route1)

    def testCheckMatchingLocations_MatchingLocations_RaisesError(self):
        self.assertTrue(self.vehicle.check_matching_locations(self.route4))

    def testCheckRemainingRange_EnoughRange_ReturnsTrue(self):
        self.vehicle._routes = [self.route2]
        self.vehicle._truck_range = VALID_TRUCK_RANGE - len(self.route2)
        self.assertTrue(self.vehicle.check_remaining_range(self.route2))

    # def testCheckRemainingRange_NotEnoughRange_ReturnsError(self):
    #     self.vehicle._truck_range -= 100_000
    #     with self.assertRaisesRegex(ValueError, f"Range not enough to cover 4736 km"):
    #         self.vehicle.check_remaining_range(self.route2)
    #         # error not raised

    def testAssignRoute_PossibleRoute_AppendsToRoutes(self):
        self.assertEqual(len(self.vehicle._routes), 3)
        self.vehicle.assign_route(self.route4)
        self.assertEqual(len(self.vehicle._routes), 4)

    def testAssignRoute_ImpossibleRoute_DoesNotAppend(self):
        with self.assertRaises(ValueError):
            self.vehicle.assign_route(self.route5)

    def testUpdateCapacity_OK(self):
        self.vehicle.update_capacity(1456.43)
        self.assertEqual(self.vehicle._capacity, 24543.57)

    def testUpdateCapacity_WeightNegative_RaisesError(self):
        with self.assertRaisesRegex(ValueError, "Package weight is expected to be a positive value"):
            self.vehicle.update_capacity(-1)

    def testUpdateCapacity_NotEnoughCapacity(self):
        with self.assertRaisesRegex(ValueError, "Free capacity of vehicle: 26_000kg can't load 30_000kg"):
            self.vehicle.update_capacity(30_000)

    # def testUpdateRange_NegativeDistance_RaisesError(self):
    #     with self.assertRaisesRegex(ValueError, 'Distance is expected to be a positive value'):
    #         self.vehicle.update_range(-1)
    #
    # def testUpdateRange_InsufficientRange_RaisesError(self):
    #     with self.assertRaisesRegex(ValueError, 'Remaining range is not enough for distance 100000 km'):
    #         self.vehicle.update_range(100_000)
    #
    # def testUpdate_SufficientRange_UpdatesRange(self):
    #     self.vehicle.update_range(10_000)
    #     self.assertEqual(self.vehicle.truck_range, 3000)
    #
    # def testUpdateRange_DistanceNegative_RaisesError(self):
    #     with self.assertRaisesRegex(ValueError, 'Distance is expected to be a positive value'):
    #         self.vehicle.update_range(-1)

    def testReset_OK(self):
        self.vehicle.update_capacity(1000)
        self.assertEqual(self.vehicle.capacity, 25000)
        self.assertEqual(self.vehicle.truck_range, 13000)
        self.vehicle.reset()
        self.assertEqual(self.vehicle.capacity, 26000)
        self.assertEqual(self.vehicle.truck_range, 13000)

    def testStr_OK(self):
        expected = (
            f'{self.vehicle.name} ID: {self.vehicle.id_truck}\n'
            f'current location: DAR\n'
            f'current route: None\n'
            f'all assigned routes: \n'
            f'  1. {self.route1}\n'
            f'  2. {self.route2}\n'
            f'  3. {self.route3}\n'
            f'\n'
            f'capacity: {self.vehicle.capacity}kg\n'
            f'range: {self.vehicle.truck_range}km\n'
        )
        self.assertEqual(str(self.vehicle), expected)
