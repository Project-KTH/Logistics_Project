from unittest.mock import Mock
from unittest import TestCase
from tests.package_test import (VALID_PACKAGE_WEIGHT, VALID_PACKAGE_CONTACT_INFO, VALID_PACKAGE_END_LOCATION_ABBR,
                                VALID_PACKAGE_START_LOCATION_FULLNAME, INVALID_PACKAGE_END_LOCATION)
from models.package import Package


def mock_package():
    package = Mock(spec=Package)
    package._start_location = VALID_PACKAGE_START_LOCATION_FULLNAME
    package._end_location = VALID_PACKAGE_END_LOCATION_ABBR
    package.contact_info = VALID_PACKAGE_CONTACT_INFO
    package.weight = VALID_PACKAGE_WEIGHT

    return package



