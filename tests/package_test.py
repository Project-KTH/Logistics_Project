from unittest import TestCase
from models.package import Package

VALID_PACKAGE_START_LOCATION_FULLNAME = 'Sydney'
INVALID_PACKAGE_START_LOCATION = 'Canberra'

VALID_PACKAGE_END_LOCATION_ABBR = 'PER'
INVALID_PACKAGE_END_LOCATION = 'Newcastle'

VALID_PACKAGE_WEIGHT = 1.5
INVALID_PACKAGE_WEIGHT_ZERO = 0
INVALID_PACKAGE_WEIGHT_NEGATIVE = -1
INVALID_PACKAGE_WEIGHT_NONNUMBER = 'a'
INVALID_PACKAGE_WEIGHT_EMPTY = ''

VALID_PACKAGE_CONTACT_INFO = 'contact info'


class TestPackage(TestCase):
    def setUp(self):
        self.package = Package(VALID_PACKAGE_START_LOCATION_FULLNAME, VALID_PACKAGE_END_LOCATION_ABBR,
                               VALID_PACKAGE_WEIGHT, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_InitialisesSuccessfully(self):
        self.assertEqual(self.package.weight, VALID_PACKAGE_WEIGHT)
        self.assertEqual(self.package.start_location, 'SYD')
        self.assertEqual(self.package.end_location, 'PER')
        self.assertEqual(self.package.contact_info, VALID_PACKAGE_CONTACT_INFO)
        self.assertIsInstance(self.package, Package)

    def testInitialiser_InvalidStartLocation_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'No office at this location: Canberra'):
            self.package = Package(INVALID_PACKAGE_START_LOCATION, VALID_PACKAGE_END_LOCATION_ABBR,
                                   VALID_PACKAGE_WEIGHT, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_InvalidEndLocation_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'No office at this location: Newcastle'):
            self.package = Package(VALID_PACKAGE_START_LOCATION_FULLNAME, INVALID_PACKAGE_END_LOCATION,
                                   VALID_PACKAGE_WEIGHT, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_WeightZero_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight cannot be 0 or less'):
            self.package = Package(VALID_PACKAGE_START_LOCATION_FULLNAME, VALID_PACKAGE_END_LOCATION_ABBR,
                                   INVALID_PACKAGE_WEIGHT_ZERO, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_WeightNegative_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight cannot be 0 or less'):
            self.package = Package(VALID_PACKAGE_START_LOCATION_FULLNAME, VALID_PACKAGE_END_LOCATION_ABBR,
                                   INVALID_PACKAGE_WEIGHT_NEGATIVE, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_WeightNonNumber_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight must be a number'):
            self.package = Package(VALID_PACKAGE_START_LOCATION_FULLNAME, VALID_PACKAGE_END_LOCATION_ABBR,
                                   INVALID_PACKAGE_WEIGHT_NONNUMBER, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_WeightEmpty_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight cannot be empty'):
            self.package = Package(VALID_PACKAGE_START_LOCATION_FULLNAME, VALID_PACKAGE_END_LOCATION_ABBR,
                                   INVALID_PACKAGE_WEIGHT_EMPTY, VALID_PACKAGE_CONTACT_INFO)

    def testInitialiser_CreatesIDCorrectly(self):
        def contains_two_letters(value):
            # Count the number of letters in the string
            letter_count = sum(c.isupper() for c in value)
            return letter_count == 2

        def contains_four_digits(value):
            digit_count = sum(c.isdigit() for c in value)
            return digit_count == 4

        self.assertEqual(len(self.package._package_id), 6)
        self.assertTrue(contains_two_letters(self.package._package_id))

    def testStr_ReturnsCorrectFormat(self):
        self.package._package_id = 'JG5742'
        expected = (
            f'Package ID: JG5742\n'
            f'Weight: 1.5kg\n'
            f'From: SYD\n'
            f'To: PER\n'
            f'Customer: contact info\n'
        )
        self.assertEqual(expected, str(self.package))