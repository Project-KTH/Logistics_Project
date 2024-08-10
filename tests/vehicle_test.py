from unittest import TestCase
from models.vehicle import Vehicle
from mock_objects import mock_package

VALID_VEHICLE_NAME = 'Truck'
VALID_CAPACITY = 26_000
VALID_RANGE = 13_000

class TestVehicle(TestCase):

    def setUp(self):
        self.vehicle = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)

    def testInitialiser_InitialisesSuccessfully(self):
        self.assertEqual(self.vehicle.name, VALID_VEHICLE_NAME)
        self.assertEqual(self.vehicle.capacity, VALID_CAPACITY)
        self.assertEqual(self.vehicle.range, VALID_RANGE)
        self.assertIsInstance(self.vehicle, Vehicle)
    
    def test_create_vehicle_with_increment(self):
        truck1 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)
        truck2 = Vehicle(VALID_VEHICLE_NAME, VALID_CAPACITY, VALID_RANGE)
        
        self.assertEqual(truck1._id_truck, truck2._id_truck-1)