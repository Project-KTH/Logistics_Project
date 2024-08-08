from datetime import timedelta, datetime

from core.application_data import ApplicationData
from helpers.linked_list import LinkedList
from helpers.rootmanager import RouteManager, print_route
from models.location import Location
from models.manager import Manager
from models.vehicle import Vehicle
from models.route import Route

my_route = Route(15, ["SYD","PER"], datetime(2024, 8, 7, 10, 10))
future_route = Route(105, ["PER", "MEL", "ADL"], datetime(2024, 8, 15, 10, 10))
print(my_route)
print(future_route)
print(len(my_route))
print(len(future_route))
print(type(my_route.departure_time))
print(all_vehicles[5])
print(all_vehicles[10])
print()
print(all_vehicles[5].assign_route(my_route))
print(all_vehicles[5].assign_route(future_route))
print()
print(all_vehicles[5].find_active_route())
print(all_vehicles[5].track_location())

from core.application_data import ApplicationData
from helpers.linked_list import LinkedList
from helpers.rootmanager import RouteManager, print_route
from models.location import Location
from models.manager import Manager
from models.vehicle import Vehicle
from models.route import Route

# my_route = Route(15, ["SYD", "MEL", "ADL", "ASP", "BRI", "DAR", "PER"], datetime.now())
# print(my_route)
# print(len(my_route))
# # Create a Location instance to manage routes




def test_route_assignments():
    # Setup application data
    app_data = ApplicationData()

    # Create a Manager
    manager = Manager(user_id=1, name="Alice", contact_info="alice@example.com", application_data=app_data)

    # Create a RouteManager
    route_manager = RouteManager()

    # Test 1: Direct route assignment within main route 1 (Adelaide to Brisbane)
    print("\nTest 1: Direct Route (Adelaide to Brisbane)")
    try:
        route_adl_bri = route_manager.determine_route("ADL", "BRI")
        print_route("ADL", "BRI", route_adl_bri)
    except ValueError as e:
        print(e)

    # Test 2: Direct route assignment within main route 2 (Perth to Darwin)
    print("\nTest 2: Direct Route (Perth to Darwin)")
    try:
        route_per_dar = route_manager.determine_route("PER", "DAR")
        print_route("PER", "DAR", route_per_dar)
    except ValueError as e:
        print(e)

    # Test 3: Hub route using Alice Springs from Brisbane to Perth
    print("\nTest 3: Hub Route (Brisbane to Perth via Alice Springs)")
    try:
        route_bri_per = route_manager.determine_route("BRI", "PER")
        print_route("BRI", "PER", route_bri_per)
    except ValueError as e:
        print(e)

    # Test 4: Hub route using Alice Springs from Darwin to Adelaide
    print("\nTest 4: Hub Route (Darwin to Adelaide via Alice Springs)")
    try:
        route_dar_adl = route_manager.determine_route("DAR", "ADL")
        print_route("DAR", "ADL", route_dar_adl)
    except ValueError as e:
        print(e)

    # Test 5: Hub route using Alice Springs from Sydney to Darwin
    print("\nTest 5: Hub Route (Sydney to Darwin via Alice Springs)")
    try:
        route_syd_dar = route_manager.determine_route("SYD", "DAR")
        print_route("SYD", "DAR", route_syd_dar)
    except ValueError as e:
        print(e)

    print("\nTest 5: Hub Route (Sydney to BRI TO SYD)")
    try:
        route_syd_dar = route_manager.determine_route("BRI", "SYD")
        print_route("BRI", "SYD", route_syd_dar)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    test_route_assignments()



#expected output: Test 1: Direct Route (Adelaide to Brisbane)
# Route from ADL to BRI: ADL -> MEL -> SYD -> BRI
#
# Test 2: Direct Route (Perth to Darwin)
# Route from PER to DAR: PER -> ASP -> DAR
#
# Test 3: Hub Route (Brisbane to Perth via Alice Springs)
# Route from BRI to PER: BRI -> ASP -> PER
#
# Test 4: Hub Route (Darwin to Adelaide via Alice Springs)
# Route from DAR to ADL: DAR -> ASP -> BRI -> SYD -> MEL -> ADL
#
# Test 5: Hub Route (Sydney to Darwin via Alice Springs)
# Route from SYD to DAR: SYD -> BRI -> ASP -> DAR
