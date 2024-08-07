class Cities:

    SYDNEY = 'Sydney'
    BRISBANE = 'Brisbane'
    MELBOURNE = 'Melbourne'
    ADELAIDE = 'Adelaide'
    PERTH = 'Perth'
    DARWIN = 'Darwin'
    ALICE_SPRINGS = 'Alice Springs'

    cities_list = [SYDNEY, BRISBANE, MELBOURNE, ADELAIDE, PERTH, DARWIN, ALICE_SPRINGS]

    distances = {
        SYDNEY: {
            MELBOURNE: 877,
            ADELAIDE: 1376,
            ALICE_SPRINGS: 2762,
            BRISBANE: 909,
            DARWIN: 3935,
            PERTH: 4016
        },
        MELBOURNE: {
            SYDNEY: 877,
            ADELAIDE: 725,
            ALICE_SPRINGS: 2255,
            BRISBANE: 1765,
            DARWIN: 3509,
            PERTH: 2785
        },
        ADELAIDE: {
            SYDNEY: 1376,
            MELBOURNE: 725,
            ALICE_SPRINGS: 1530,
            BRISBANE: 1927,
            DARWIN: 3027,
            PERTH: 2481
        },
        ALICE_SPRINGS: {
            SYDNEY: 2762,
            MELBOURNE: 2255,
            ADELAIDE: 1530,
            BRISBANE: 2993,
            DARWIN: 1497,
            PERTH: 4311
        },
        BRISBANE: {
            SYDNEY: 909,
            MELBOURNE: 1765,
            ADELAIDE: 1927,
            ALICE_SPRINGS: 2993,
            DARWIN: 3426,
            PERTH: 4311
        },
        DARWIN: {
            SYDNEY: 3935,
            MELBOURNE: 3509,
            ADELAIDE: 3027,
            ALICE_SPRINGS: 1497,
            BRISBANE: 3426,
            PERTH: 4025
        },
        PERTH: {
            SYDNEY: 4016,
            MELBOURNE: 2785,
            ADELAIDE: 2481,
            ALICE_SPRINGS: 4311,
            BRISBANE: 4311,
            DARWIN: 4025
        }
    }

    @classmethod
    def from_string(cls, city_string):
        if city_string not in cls.cities_list:
            raise ValueError(f'No office at this location')
        else:
            return city_string

