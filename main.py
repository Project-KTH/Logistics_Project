from datetime import datetime, timedelta

from core.application_data import ApplicationData
from models.manager import Manager
from models.user import User

# Set up the application data
app_data = ApplicationData()

# Create a manager
manager = Manager(user_id="mgr001", name="Alice", contact_info="alice@example.com", application_data=app_data)

# Add trucks
truck_models = ["Scania", "Man", "Actros"]
home_bases = ["SYD", "MEL", "ADL", "BRI", "PER"]

trucks = [manager.add_truck(model, base) for model in truck_models for base in home_bases]

# Create a user
user = User(user_id="user001", name="John Doe", contact_info="john.doe@example.com")

# User orders packages
user.order_package("SYD", "MEL", 10000, app_data)
user.order_package("MEL", "ADL", 5000, app_data)
user.order_package("SYD", "ADL", 15000, app_data)

# Create and assign routes
route_data = [
    ("R001", ["SYD", "MEL", "ADL"], 1),
    ("R002", ["MEL", "ADL", "PER"], 2),
    ("R003", ["ADL", "PER", "SYD"], 3),
    ("R004", ["PER", "SYD", "BRI"], 4),
    ("R005", ["SYD", "BRI", "DAR"], 5),
    ("R006", ["BRI", "DAR", "PER"], 6),
    ("R007", ["DAR", "PER", "SYD"], 7),
    ("R008", ["PER", "SYD", "MEL"], 8),
    ("R009", ["SYD", "MEL", "ASP"], 9),
    ("R010", ["MEL", "ASP", "SYD"], 10),
    ("R011", ["ASP", "SYD", "ADL"], 11),
    ("R012", ["SYD", "ADL", "BRI"], 12),
    ("R013", ["ADL", "BRI", "PER"], 13),
    ("R014", ["BRI", "PER", "MEL"], 14),
    ("R015", ["PER", "MEL", "DAR"], 15),
    ("R016", ["MEL", "DAR", "SYD"], 16),
    ("R017", ["DAR", "SYD", "ADL"], 17),
    ("R018", ["SYD", "ADL", "PER"], 18),
    ("R019", ["ADL", "PER", "BRI"], 19),
    ("R020", ["PER", "BRI", "SYD"], 20)
]

for route_id, locations, hours in route_data:
    departure_time = datetime.now() + timedelta(hours=hours)
    route = manager.create_route(route_id, locations, departure_time)
    suitable_truck = trucks[route_data.index((route_id, locations, hours)) % len(trucks)]
    manager.assign_route_to_truck(suitable_truck, route)

# User tracks packages
for package in user.ordered_packages:
    user.track_package(package._package_id, app_data)

# Print status of all routes
manager.get_routes_status()

for truck in trucks:
    for route in truck._routes:
        route.simulate_route()
