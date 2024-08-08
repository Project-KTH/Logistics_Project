import itertools



class Cities:
    # Define full city names
    SYDNEY = 'Sydney'
    BRISBANE = 'Brisbane'
    MELBOURNE = 'Melbourne'
    ADELAIDE = 'Adelaide'
    PERTH = 'Perth'
    DARWIN = 'Darwin'
    ALICE_SPRINGS = 'Alice Springs'

    # Mapping of full city names to abbreviations
    abbreviation_map = {
        'Sydney': 'SYD',
        'Brisbane': 'BRI',
        'Melbourne': 'MEL',
        'Adelaide': 'ADL',
        'Alice Springs': 'ASP',
        'Darwin': 'DAR',
        'Perth': 'PER'
    }

    # Distances using abbreviations
    distances = {
        'SYD': {'MEL': 877, 'ADL': 1376, 'ASP': 2762, 'BRI': 909, 'DAR': 3935, 'PER': 4016},
        'MEL': {'SYD': 877, 'ADL': 725, 'ASP': 2255, 'BRI': 1765, 'DAR': 3752, 'PER': 3509},
        'ADL': {'SYD': 1376, 'MEL': 725, 'ASP': 1530, 'BRI': 1927, 'DAR': 3027, 'PER': 2785},
        'ASP': {'SYD': 2762, 'MEL': 2255, 'ADL': 1530, 'BRI': 2993, 'DAR': 1497, 'PER': 2481},
        'BRI': {'SYD': 909, 'MEL': 1765, 'ADL': 1927, 'ASP': 2993, 'DAR': 3426, 'PER': 4311},
        'DAR': {'SYD': 3935, 'MEL': 3752, 'ADL': 3027, 'ASP': 1497, 'BRI': 3426, 'PER': 4025},
        'PER': {'SYD': 4016, 'MEL': 3509, 'ADL': 2785, 'ASP': 2481, 'BRI': 4311, 'DAR': 4025},
    }

    @classmethod
    def from_string(cls, city_string):
        # Check if the city_string is an abbreviation and map it to the full name
        if city_string in cls.abbreviation_map:
            return cls.abbreviation_map[city_string]
        # If city_string is not an abbreviation, check against full city names
        elif city_string in cls.abbreviation_map.values():
            return city_string
        else:
            raise ValueError(f'No office at this location: {city_string}')

    @classmethod
    def get_abbreviation(cls, city_name):
        # Return the abbreviation for the full city name
        for abbr, full_name in cls.abbreviation_map.items():
            if full_name == city_name:
                return abbr
        return None


