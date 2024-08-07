from datetime import timedelta, datetime
from models.vehicle import Vehicle
from models.route import Route

my_route = Route(15, ["SYD", "MEL", "ADL", "ASP", "BRI", "DAR", "PER"], datetime.now())
print(my_route)
print(len(my_route))