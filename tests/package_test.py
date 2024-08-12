from unittest import TestCase
from models.package import Package
from tests.mock_objects import mock_location


VALID_PACKAGE_WEIGHT = 1.5
INVALID_PACKAGE_WEIGHT_ZERO = 0
INVALID_PACKAGE_WEIGHT_NEGATIVE = -1
INVALID_PACKAGE_WEIGHT_NONNUMBER = 'a'
INVALID_PACKAGE_WEIGHT_EMPTY = ''

VALID_PACKAGE_CUSTOMER_INFO = 'customer info'


class TestPackage(TestCase):
    def setUp(self):
        self.location1 = mock_location('SYD')
        self.location2 = mock_location('PER')
        self.package = Package(self.location1, self.location2, VALID_PACKAGE_WEIGHT, VALID_PACKAGE_CUSTOMER_INFO)

    def testInitialiser_InitialisesSuccessfully(self):
        self.assertEqual(self.package.weight, VALID_PACKAGE_WEIGHT)
        self.assertEqual(self.package.start_location.name, 'SYD')
        self.assertEqual(self.package.end_location.name, 'PER')
        self.assertEqual(self.package.customer_info, VALID_PACKAGE_CUSTOMER_INFO)
        self.assertIsInstance(self.package, Package)

    def testInitialiser_WeightZero_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight cannot be 0 or less'):
            self.package.weight = INVALID_PACKAGE_WEIGHT_ZERO

    def testInitialiser_WeightNegative_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight cannot be 0 or less'):
            self.package.weight = INVALID_PACKAGE_WEIGHT_NEGATIVE

    def testInitialiser_WeightNonNumber_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight must be a number'):
            self.package.weight = INVALID_PACKAGE_WEIGHT_NONNUMBER

    def testInitialiser_WeightEmpty_RaisesError(self):
        with self.assertRaisesRegex(ValueError, 'Weight cannot be empty'):
            self.package.weight = INVALID_PACKAGE_WEIGHT_EMPTY

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

    def testSetter_SetsWeightCorrectly(self):
        self.package.weight = 2.5
        self.assertEqual(self.package.weight, 2.5)

    def testStr_ReturnsCorrectFormat(self):
        self.package._package_id = 'JG5742'
        expected = (
            f'Package ID: JG5742\n'
            f'Weight: 1.5kg\n'
            f'From: SYD\n'
            f'To: PER\n'
            f'Customer: customer info\n'
        )
        self.assertEqual(expected, str(self.package))