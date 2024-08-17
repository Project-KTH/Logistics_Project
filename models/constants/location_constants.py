

class Cities:
    SYDNEY = 'Sydney'
    BRISBANE = 'Brisbane'
    MELBOURNE = 'Melbourne'
    ADELAIDE = 'Adelaide'
    PERTH = 'Perth'
    DARWIN = 'Darwin'
    ALICE_SPRINGS = 'Alice Springs'

    abbreviation_map = {
        'Sydney': 'SYD',
        'Brisbane': 'BRI',
        'Melbourne': 'MEL',
        'Adelaide': 'ADL',
        'Alice Springs': 'ASP',
        'Darwin': 'DAR',
        'Perth': 'PER'
    }

    distances = {
            'SYD': {'SYD': 0, 'MEL': 877, 'ADL': 1376, 'ASP': 2762, 'BRI': 909, 'DAR': 3935, 'PER': 4016},
            'MEL': {'SYD': 877, 'MEL': 0, 'ADL': 725, 'ASP': 2255, 'BRI': 1765, 'DAR': 3752, 'PER': 3509},
            'ADL': {'SYD': 1376, 'MEL': 725, 'ADL': 0, 'ASP': 1530, 'BRI': 1927, 'DAR': 3027, 'PER': 2785},
            'ASP': {'SYD': 2762, 'MEL': 2255, 'ADL': 1530, 'ASP': 0, 'BRI': 2993, 'DAR': 1497, 'PER': 2481},
            'BRI': {'SYD': 909, 'MEL': 1765, 'ADL': 1927, 'ASP': 2993, 'BRI': 0, 'DAR': 3426, 'PER': 4311},
            'DAR': {'SYD': 3935, 'MEL': 3752, 'ADL': 3027, 'ASP': 1497, 'BRI': 3426, 'DAR': 0, 'PER': 4025},
            'PER': {'SYD': 4016, 'MEL': 3509, 'ADL': 2785, 'ASP': 2481, 'BRI': 4311, 'DAR': 4025, 'PER': 0},
        }

    @classmethod
    def from_string(cls, city_string: str):
        if city_string.title() in cls.abbreviation_map:
            return cls.abbreviation_map[city_string.title()]
        elif city_string.upper() in cls.abbreviation_map.values():
            return city_string.upper()
        else:
            raise ValueError(f'No office at this location: {city_string}')

    @classmethod
    def get_abbreviation(cls, city_name):
        for abbr, full_name in cls.abbreviation_map.items():
            if full_name == city_name:
                return abbr
        return None


