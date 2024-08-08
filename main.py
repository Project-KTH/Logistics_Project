from datetime import timedelta, datetime
from models.vehicle import Vehicle, all_vehicles
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