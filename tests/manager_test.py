from datetime import datetime
from unittest import TestCase
from models.manager import Manager
from models.package import Package
from models.vehicle import Vehicle
from tests.mock_objects import mock_application_data, mock_package, mock_vehicle, mock_location, mock_route


class TestManager(TestCase):
    def setUp(self):

        self.sydney = mock_location('SYD')
        self.perth = mock_location('PER')
        self.brisbane = mock_location('BRI')
        self.alice_springs = mock_location('ASP')
        self.melbourne = mock_location('MEL')
        self.darwin = mock_location('DAR')
        self.adelaide = mock_location('ADL')

        self.test_application_data = mock_application_data()
        self.manager = Manager('manager', 'contact info', 'password', self.test_application_data)

        self.package1 = mock_package('SYD', 'PER', 4.5, 'customer_info')
        self.package1._package_id = 'FR4567'

        self.route1 = mock_route()
        self.route1.id = 1000
        self.route1.locations = [self.melbourne, self.brisbane]

        self.route2 = mock_route()
        self.route2.id = 1001
        self.route2.locations = [self.alice_springs, self.darwin]
        self.route2.departure_time = datetime.strptime('11-05-2024 03:34', '%d-%m-%Y %H:%M')

        self.route3 = mock_route()
        self.route3.id = 1002
        self.route3.locations = [self.sydney, self.adelaide]  # Route from Sydney to Adelaide
        self.route3.departure_time = datetime.strptime('01-05-2024 08:00', '%d-%m-%Y %H:%M')

        self.route4 = mock_route()
        self.route4.id = 1003
        self.route4.locations = [self.adelaide, self.sydney]
        self.route4.departure_time = datetime.strptime('14-12-2024 06:00', '%d-%m-%Y %H:%M')

        self.truck = mock_vehicle('Truck', 10000, 10000, truck_id=2000)
        self.truck._routes = [self.route2]

        self.truck2 = mock_vehicle('Truck2', 100000, 10000, truck_id=3000)
        self.truck2._current_location = self.melbourne

        self.truck4 = mock_vehicle('Truck4', 15000, 2000, truck_id=5000)
        self.truck4._routes = [self.route3]

    def testInitialiser_InitialisesOK(self):
        self.assertEqual(self.manager.access_level, 'basic')
        self.assertEqual(self.manager.application_data, self.test_application_data)
        self.assertEqual(self.manager.name, 'manager')
        self.assertEqual(self.manager.id, self.manager.id)
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

    def testAssignRouteToTruck_AvailableTruck_OK(self):
        self.manager.assign_route_to_truck(self.truck2, self.route1)
        self.assertEqual(self.route1.truck, self.truck2)

    def testAssignRouteToTruck_UnavailableTruck_DoesNothing(self):
        self.manager.assign_route_to_truck(self.truck, self.route2)
        self.assertIsNone(self.route2.truck)

    def testFindSuitableTruck_OK(self):
        self.test_application_data.vehicles.extend([
            self.truck, self.truck2, self.truck4])
        self.manager.find_suitable_truck(self.route4)
