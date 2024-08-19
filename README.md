
## OOP Teamwork Workshop - Truck Logistics Management System

### Description
The Truck Logistics Management System is an Object-Oriented Python application designed to manage the logistics of packages and trucks. The system facilitates the creation and management of trucks, routes, and packages. Users can order packages, track their packages, and update contact_info.

In models the main classes are Route, Package, Vehicle, Manager and User.

- Routes have a **id, locations, packages, departure_time, truck, capacity**.
- Packages have a **id, start_location, end_location, weight, customer_info, route, expected_arrival_time**.
- Trucks/Vehicles have a **id, name, capacity, range, current_location, routes: list with all routes**.
- Users have a **id, name, contact_info, password, role and ordered_packages: list**.


#### 1. Route class
Available methods:
- generate_locations_from_packages() - Generate a list of unique locations based on package start and end points.
- assign_truck() - updates self.truck and self.capacity
- add_package() - updates self.packages and self.capacity
- calculate_travel_time() - Calculate travel time based on distance and vehicle speed.
- calculate_arrival_times() - Calculate estimated arrival times for each location in the route.
- next_stop() - Determine the next stop based on the current location.
- update_locations_for_packages() - Update the route's locations to include necessary stops for the packages.
- simulate_route() - Simulate vehicle moving along its route, updating location every 3 seconds.
- __str__() - returns "Route ID: {}, Locations: {stops_with_times}, Truck ID: {}"
- __len__() - Calculate the total length of the route.


#### 2. Package class
Available methods:
- __str__() - returns "Package ID: {}, Weight: {}kg, From: {self.start_location}, To: {self.end_location}, Customer: {self.customer_info}, Assigned Route ID: {}, Expected arrival time: {}"

Constraints:
- weight must be valid positive int or float
- contact_info must not be empty


#### 3. Vehicle class
Available methods:
- find_active_route() - based on a date, gets the active route for a vehicle from a list of all routes. 
- track_location() - based on a date, gets the current location of a vehicle.
- check_schedule() - based on a new route departure_time checks is the vehicle is available.
- check_matching_locations() - based on a new route start location checks for match with vehicle's last route end location.
- check_remaining_range() - checks if vehicle initial_range is >= len(new_route).
- assign_route() - adds new route to the list of all routes for the vehicle. 
- update_capacity() - decreases capacity with package_weight or raises ValueError.
- reset() - resets the vehicle's capacity and range to initial values.
- __str__() - returns "{name} ID:--{}--, location: {}, route: {active_route}, capacity left: {}kg, range to go: {}km"

Constraints:
- name must be from: Scania, Man, Actros
- capacity and range depend on the name
- constant speed: 87km/h
- fixed number of units per name


#### 4. User class
Available methods:
- order_package()
- track_package()
- update_contact_info()
- authenticate()
- hash_password()
- __str__() - returns "User ID: {}, Name: {}, Role: {}, Contact Info: {}"

Constraints:
- name must be min 2 letters
- contact_info must not be empty


#### 5. Manager class
Available methods:
- create_package()
- delete_package()
- add_truck() - adds a new unit to a specific location.
- reset_truck()
- assign_route_to_truck() - assign a route to a truck, ensuring all checks are passed.
- find_suitable_truck() - finds a suitable truck for a given route based on capacity and location.
- create_route()
- get_routes_status()
- remove_user()
- assign_role()


### 6. Commands

- `AddUser` (params: name, contact_info, password) - create a new User and stores it in the AppData. Name must be min 2 letters, contact_info must not be empty.

- `AssignRouteToTruck` (params: route_id, truck_id) - find route and vehicle in app_data, assigns route to truck; assigns truck and capacity to route.

- `AssignPackageToRoute` (params: package_id, route_id) - add package to Route and Route to Package.

- `CreatePackage` (params: start_location, end_location, weight, customer_info) - creates a new Package and stores it in the AppData. Weight must be positive value, customer_info must mot be empty.

- `CreateRoute` (params: locations_str: comma separated, departure_time_str) - creates a new Route and stores it in the AppData.

- `OrderPackage` (params: user_id, start_location, end_location, weight) - creates a new Package and stores it in the AppData, adds the package to the User.

- `DeletePackage` (params: package_id) - find and delete Package from AppData list[Packages].

- `CreateManager` (params: name, contact_info, password) - create and store a new Manager in the AppData list[User]. Name must be min 2 letters, contact_info must not be empty.

- `FindRouteForPackage`(params: package_id)

- `ViewAllPackages`

- `ViewAllUsers`

- `ViewAllVehicles` - view all created vehicles.

- `ViewNotAssignedPackages`

- `ViewNotAssignedPackages`

- `ViewAvailableVehicles`(params: route_id)

- `ViewAvailableVehicles`(params: package_id, customer_info) ViewAllRoutes

- `ViewAllRoutes`

- `ViewRoutesInProgress` compare route start and end date with Now.


### 7. ApplicationData class
Available methods:
- find_package_by_id() - returns Package or None if not found
- find_route_by_package_id() - returns Route or None if not found
- find_vehicle_by_id - returns Vehicle or None if not found
- find_route_for_package - returns Route or None if not 
- find_route_by_id() - returns Route or None if not found
- find_user_by_id() - returns User or None if not found
- find_user_by_contact_info() - returns User or raises ValueError

Attributes:
- self.vehicles: list[Vehicle]
- self.routes: list[Routes]
- self.packages: list[Packages]
- self.users: list[User]

### 8. Unit Tests
Unit tests for the core functionality.


### Input example

```


```

### Output Example

```


```
