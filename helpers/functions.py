def find_suitable_truck(trucks, start_location, required_capacity):
    for truck in trucks:
        if truck.current_location == start_location and truck.current_capacity >= required_capacity and truck.available:
            return truck
    return None

def get_distance(start, end):
    distances = {
        'SYD': {'MEL': 877, 'ADL': 1376, 'ASP': 2762, 'BRI': 909, 'DAR': 3935, 'PER': 4016},
        'MEL': {'ADL': 725, 'ASP': 2255, 'BRI': 1765, 'DAR': 3509},
        # Additional distances
    }
    return distances[start].get(end, float('inf'))  # Returns infinity if no direct route

