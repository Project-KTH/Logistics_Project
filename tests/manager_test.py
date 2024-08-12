from unittest import TestCase
from models.manager import Manager
from models.package import Package
from models.vehicle import Vehicle
from tests.mock_objects import mock_application_data, mock_package, mock_vehicle


class TestManager(TestCase):
    def setUp(self):
        self.test_application_data = mock_application_data()
        self.manager = Manager(1000, 'manager', 'contact info', self.test_application_data)
        self.package1 = mock_package('SYD', 'PER', 4.5, 'customer_info')
        self.package1._package_id = 'FR4567'
        self.truck = mock_vehicle('Truck', 10000, 10000, truck_id=2000)

    def testInitialiser_InitialisesOK(self):
        self.assertEqual(self.manager.access_level, 'basic')
        self.assertEqual(self.manager.application_data, self.test_application_data)
        self.assertEqual( self.manager.name, 'manager')
        self.assertEqual(self.manager.user_id, 1000)
        self.assertEqual(self.manager.role, 'manager')
        self.assertEqual(self.manager.contact_info, 'contact info')
        self.assertIsInstance(self.manager, Manager)

    def testCreatePackage_OK(self):
        package = self.manager.create_package('SYD', 'PER', 1.5, 'customer info')
        self.assertIsInstance(package, Package)
        self.assertEqual(package.start_location, 'SYD')
        self.assertEqual(package.end_location, 'PER')
        self.assertEqual(package.weight, 1.5)
        self.assertEqual(package.customer_info, 'customer info')
        self.assertEqual(self.test_application_data.packages, [package])

    def testDeletePackage_OK(self):
        self.test_application_data.packages = [self.package1]
        self.manager.delete_package('FR4567')
        self.assertEqual(self.test_application_data.packages, [])

    def testAddTruck_OK(self):
        truck = self.manager.add_truck('Scania', 'SYD')
        self.assertIsInstance(truck, Vehicle)
        self.assertEqual(truck.name, 'Scania')
        self.assertEqual(truck.truck_range, 8000)
        self.assertEqual(truck.capacity, 42000)
        self.assertEqual(self.test_application_data.vehicles[40], truck)

    def testResetTruck_OK(self):
        self.test_application_data.vehicles.append(self.truck)
        self.assertEqual(self.test_application_data.vehicles[40], self.truck)
        self.truck.capacity, self.truck.truck_range = 1, 1
        self.manager.reset_truck(2000)
        self.truck.capacity, self.truck.truck_range = 10000, 10000
