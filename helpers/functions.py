import random
import string


def find_suitable_truck(trucks, start_location, required_capacity):
    for truck in trucks:
        if truck.current_location == start_location and truck.current_capacity >= required_capacity and truck.available:
            return truck
    return None

def get_distance(start, end):
    distances = {
        'SYD': {'SYD': 0, 'MEL': 877, 'ADL': 1376, 'ASP': 2762, 'BRI': 909, 'DAR': 3935, 'PER': 4016},
        'MEL': {'SYD': 877, 'MEL': 0, 'ADL': 725, 'ASP': 2255, 'BRI': 1765, 'DAR': 3752, 'PER': 3509},
        'ADL': {'SYD': 1376, 'MEL': 725, 'ADL': 0, 'ASP': 1530, 'BRI': 1927, 'DAR': 3027, 'PER': 2785},
        'ASP': {'SYD': 2762, 'MEL': 2255, 'ADL': 1530, 'ASP': 0, 'BRI': 2993, 'DAR': 1497, 'PER': 2481},
        'BRI': {'SYD': 909, 'MEL': 1765, 'ADL': 1927, 'ASP': 2993, 'BRI': 0, 'DAR': 3426, 'PER': 4311},
        'DAR': {'SYD': 3935, 'MEL': 3752, 'ADL': 3027, 'ASP': 1497, 'BRI': 3426, 'DAR': 0, 'PER': 4025},
        'PER': {'SYD': 4016, 'MEL': 3509, 'ADL': 2785, 'ASP': 2481, 'BRI': 4311, 'DAR': 4025, 'PER': 0},
    }
    return distances[start].get(end, float('inf'))  # Returns infinity if no direct route
distances = {
        'SYD': {'SYD': 0, 'MEL': 877, 'ADL': 1376, 'ASP': 2762, 'BRI': 909, 'DAR': 3935, 'PER': 4016},
        'MEL': {'SYD': 877, 'MEL': 0, 'ADL': 725, 'ASP': 2255, 'BRI': 1765, 'DAR': 3752, 'PER': 3509},
        'ADL': {'SYD': 1376, 'MEL': 725, 'ADL': 0, 'ASP': 1530, 'BRI': 1927, 'DAR': 3027, 'PER': 2785},
        'ASP': {'SYD': 2762, 'MEL': 2255, 'ADL': 1530, 'ASP': 0, 'BRI': 2993, 'DAR': 1497, 'PER': 2481},
        'BRI': {'SYD': 909, 'MEL': 1765, 'ADL': 1927, 'ASP': 2993, 'BRI': 0, 'DAR': 3426, 'PER': 4311},
        'DAR': {'SYD': 3935, 'MEL': 3752, 'ADL': 3027, 'ASP': 1497, 'BRI': 3426, 'DAR': 0, 'PER': 4025},
        'PER': {'SYD': 4016, 'MEL': 3509, 'ADL': 2785, 'ASP': 2481, 'BRI': 4311, 'DAR': 4025, 'PER': 0},
    }



def generate_id(num_letters=2, num_digits=4, existing_ids=None):
    """Generates unique ID for each package"""
    if existing_ids is None:
        existing_ids = []

    letters = string.ascii_uppercase
    numbers = string.digits

    while True:
        first_two_characters = ''.join(random.choices(letters, k=num_letters))
        rest_characters = ''.join(random.choices(numbers, k=num_digits))
        the_id = first_two_characters + rest_characters

        if the_id not in existing_ids:
            return the_id



def calculate_expected_arrival(route, package):
    arrival_times = route.calculate_arrival_times()
    end_location_index = route.locations.index(package.end_location)
    return arrival_times[end_location_index]
