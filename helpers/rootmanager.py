from helpers.linked_list import LinkedList


class RouteManager:
    def __init__(self):
        self.main_route_1 = self._initialize_route_1()
        self.main_route_2 = self._initialize_route_2()

    def _initialize_route_1(self) -> LinkedList:
        # Route 1: Adelaide -> Melbourne -> Sydney -> Brisbane -> Alice Springs
        route = LinkedList()
        route.append("ADL")
        route.append("MEL")
        route.append("SYD")
        route.append("BRI")
        route.append("ASP")  # Alice Springs as a central hub
        return route

    def _initialize_route_2(self) -> LinkedList:
        # Route 2: Perth -> Alice Springs -> Darwin
        route = LinkedList()
        route.append("PER")
        route.append("ASP")  # Alice Springs as a central hub
        route.append("DAR")
        return route

    def determine_route(self, start: str, destination: str) -> LinkedList:
        """Determine the best route between two locations using Alice Springs as a hub."""
        if self.main_route_1.contains(start) and self.main_route_2.contains(destination):
            # Route packages through Alice Springs
            return self.create_hub_route(start, destination, self.main_route_1, self.main_route_2)
        elif self.main_route_2.contains(start) and self.main_route_1.contains(destination):
            # Route packages through Alice Springs
            return self.create_hub_route(start, destination, self.main_route_2, self.main_route_1)
        elif self.main_route_1.contains(start) and self.main_route_1.contains(destination):
            return self.extract_subroute(self.main_route_1, start, destination)
        elif self.main_route_2.contains(start) and self.main_route_2.contains(destination):
            return self.extract_subroute(self.main_route_2, start, destination)
        else:
            raise ValueError(f"No route available from {start} to {destination}")

    def extract_subroute(self, route: LinkedList, start: str, destination: str) -> LinkedList:
        """Extract a subroute from a given main route."""
        subroute = LinkedList()
        found_start = False
        current_node = route.head

        while current_node:
            if current_node.location == start:
                found_start = True
            if found_start:
                subroute.append(current_node.location)
            if current_node.location == destination:
                break
            current_node = current_node.next

        # Validate that the subroute contains the start and destination
        if not subroute.contains(start) or not subroute.contains(destination):
            raise ValueError(f"Subroute from {start} to {destination} could not be created.")

        if subroute.get_route().index(start) > subroute.get_route().index(destination):
            subroute.reverse()

        return subroute

    def create_hub_route(self, start: str, destination: str, start_route: LinkedList, destination_route: LinkedList) -> LinkedList:
        """Create a route that goes from start to Alice Springs and then to the destination."""
        hub_route = LinkedList()

        # Route from start to Alice Springs
        if start_route.contains(start):
            hub_route = self.extract_subroute(start_route, start, 'ASP')
        else:
            raise ValueError(f"Subroute from {start} to ASP could not be created.")




        # Route from Alice Springs to destination
        if destination_route.contains('ASP') and destination_route.contains(destination):
            continuation_route = self.extract_subroute(destination_route, 'ASP', destination)
        else:
            raise ValueError(f"Continuation route from ASP to {destination} could not be created.")

        # Append continuation_route to hub_route
        current_node = hub_route.head
        while current_node and current_node.next:
            current_node = current_node.next

        # Append the continuation route from ASP onwards
        if current_node:
            current_node.next = continuation_route.head.next  # Skip the 'ASP' node to avoid duplication

        return hub_route

def print_route(start: str, destination: str, route: LinkedList):
    """Helper function to print the route in a readable format."""
    route_str = " -> ".join(route.get_route())
    print(f"Route from {start} to {destination}: {route_str}")



#IDEA HOW WORKS
#Initializes two main routes: main_route_1 and main_route_2.
# Calls helper methods _initialize_route_1() and _initialize_route_2() to set up these routes.
# _initialize_route_1():
#
#     Creates a LinkedList object representing the first main route.
#     Adds nodes to the linked list in the order: Adelaide (ADL), Melbourne (MEL), Sydney (SYD), Brisbane (BRI), and Alice Springs (ASP).
#     Returns the linked list representing the first main route.
#
# _initialize_route_2():
#
#     Creates a LinkedList object representing the second main route.
#     Adds nodes to the linked list in the order: Perth (PER), Alice Springs (ASP), and Darwin (DAR).
#     Returns the linked list representing the second main route.

# determine_route(start: str, destination: str):
#
#     Determines the best route between two locations.
#     Condition 1: If start is on main_route_1 and destination is on main_route_2, calls create_hub_route() with main_route_1 and main_route_2.
#     Condition 2: If start is on main_route_2 and destination is on main_route_1, calls create_hub_route() with main_route_2 and main_route_1.
#     Condition 3: If both start and destination are on main_route_1, calls extract_subroute() on main_route_1.
#     Condition 4: If both start and destination are on main_route_2, calls extract_subroute() on main_route_2.
#     Raises a ValueError if no valid route is found.

# extract_subroute(route: LinkedList, start: str, destination: str):
#
#     Extracts a subroute from a given route between two locations.
#     Initializes an empty LinkedList called subroute.
#     Iterates over the nodes of the given route, starting from the head.
#     Once the start location is found, begins appending locations to subroute.
#     Continues appending locations until the destination is reached.
#     Validates that both start and destination are included in the subroute.
#     Returns the extracted subroute or raises an error if the subroute cannot be created.

# create_hub_route(start: str, destination: str, start_route: LinkedList, destination_route: LinkedList):
#
#     Creates a route that transitions through Alice Springs (the hub).
#     Step 1: Extracts a subroute from the start_route that leads to Alice Springs (ASP).
#     Step 2: Extracts a subroute from destination_route starting from Alice Springs (ASP) to the destination.
#     Appends the continuation subroute to the hub route, ensuring the ASP node is not duplicated.
#     Returns the complete hub route that transitions through Alice Springs.