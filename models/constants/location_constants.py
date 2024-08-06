class Cities:
    pass

    SIDNEY = 'Sydney'
    BRISBANE = 'Brisbane'
    MELBOURNE = 'Melbourne'
    ADELAIDE = 'Adelaide'
    PERTH = 'Perth'
    DARWIN = 'Darwin'
    ALICE_SPRINGS = 'Alice Springs'

    @classmethod
    def from_string(cls, city_string):
        if city_string not in [cls.SIDNEY, cls.BRISBANE, cls.MELBOURNE, cls.ADELAIDE, cls.PERTH, cls.DARWIN, cls.ALICE_SPRINGS]:
            raise ValueError(
                f'No office at that locaation.')

        return city_string

