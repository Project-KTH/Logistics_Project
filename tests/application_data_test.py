from unittest import TestCase
from core.application_data import ApplicationData
from mock_objects import mock_package, mock_vehicle, mock_route, mock_user, mock_location


class ApplicationDataTest(TestCase):
    def setUp(self):
        self.application_data = ApplicationData()

        self.location1 = mock_location("SYD")
        self.location2 = mock_location("BRI")
        self.location3 = mock_location("PER")
        self.location4 = mock_location("MEL")
        self.location5 = mock_location("DAR")

        self.package1 = mock_package(self.location1.name, self.location2.name, 1, 'contact1')
        self.package2 = mock_package(self.location3.name, self.location4.name, 1, 'contact2')
        self.package3 = mock_package(self.location5.name, self.location2.name, 1, 'contact3')
        self.package4 = mock_package(self.location3.name, self.location5.name, 1, 'contact4')

        self.route1 = mock_route()
        self.route1.locations = [self.location1, self.location2]
        self.route2 = mock_route()
        self.route2.locations = [self.location3, self.location4]
        self.route3 = mock_route()
        self.route3.locations = [self.location5, self.location2]
        self.route4 = mock_route()
        self.route4.locations = [self.location3, self.location5]

        self.vehicle1 = mock_vehicle("Truck1", 1000, 500)
        self.vehicle2 = mock_vehicle("Truck2", 1500, 800)

        self.user1 = mock_user( "User1", "user1@example.com", "password12")
        self.user2 = mock_user( "User2", "user2@example.com", "password12")

        self.application_data.packages = [self.package1, self.package2, self.package3, self.package4]
        self.application_data.routes = [self.route1, self.route2, self.route3, self.route4]
        self.application_data.vehicles = [self.vehicle1, self.vehicle2]
        self.application_data.users = [self.user1, self.user2]

    def testFindPackageById(self):
        self.package1._package_id = 1
        self.package2._package_id = 2
        self.assertEqual(self.application_data.find_package_by_id(1), self.package1)
        self.assertEqual(self.application_data.find_package_by_id(2), self.package2)
        self.assertIsNone(self.application_data.find_package_by_id(3))

    # def testFindRouteByPackageId(self):
    #     self.package1.package_id = '1'
    #     self.package2.package_id = '2'
    #     self.route1.packages = [self.package1]
    #     self.route2.packages = [self.package2]
    #     self.assertEqual(self.application_data.find_route_by_package_id('1'), self.route1)
    #     self.assertEqual(self.application_data.find_route_by_package_id('2'), self.route2)