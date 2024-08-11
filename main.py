from datetime import timedelta, datetime
import random

from core.application_data import ApplicationData
from models.location import Location
from models.manager import Manager
from models.route import Route
from models.user import User

from core.command_factory import CommandFactory
from core.engine import Engine


# app_data = ApplicationData()
# cmd_factory = CommandFactory(app_data)
# engine = Engine(cmd_factory)
#
# engine.start()
#










# Helper function to format datetime
def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M")

# Set up the application data
app_data = ApplicationData()

# Create a manager
manager = Manager(user_id="mgr001", name="Alice", contact_info="alice@example.com", application_data=app_data)

# Add trucks
truck1 = manager.add_truck("Scania", "SYD")
truck2 = manager.add_truck("Man", "MEL")

# Create packages
package1 = manager.create_package("SYD", "MEL", 10000, "john@example.com")
package2 = manager.create_package( "MEL", "ADL", 5000, "jane@example.com")
package3 = manager.create_package( "SYD", "ADL", 15000, "bob@example.com")

# Create routes and assign them to trucks
departure_time1 = datetime.now() + timedelta(hours=1)  # 1 hour from now
route1 = manager.create_route("R001", ["SYD", "MEL", "ADL"], departure_time1)
manager.assign_route_to_truck(truck1, route1)

departure_time2 = datetime.now() + timedelta(hours=2)  # 2 hours from now
route2 = manager.create_route("R002", ["MEL", "ADL"], departure_time2)
manager.assign_route_to_truck(truck2, route2)

# Track packages
def track_package(package_id):
    package = app_data.find_package_by_id(package_id)
    if package:
        current_route = app_data.find_route_for_package(package_id)
        if current_route and current_route.truck:
            current_location = current_route.truck.track_location(datetime.now())
            arrival_times = current_route.calculate_arrival_times()

            print(f"Package ID: {package.id}")
            print(f"Weight: {package.weight} kg")
            print(f"Start Point: {package.start_location}")
            print(f"End Point: {package.end_location}")
            print(f"Current Location: {current_location}")
            print(f"Route ID: {current_route.route_id}")
            print("Route Details:")
            for loc, arrival in zip(current_route.locations, arrival_times):
                print(f" - {loc}: Expected Arrival at {format_datetime(arrival)}")
            print("-" * 40)
        else:
            print(f"Package {package_id} is not currently on a route.")
    else:
        print(f"Package {package_id} not found.")

# Print information for all packages
track_package("PKG001")
track_package("PKG002")
track_package("PKG003")

# Print status of all routes
manager.get_routes_status()