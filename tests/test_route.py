from unittest import TestCase
from models.route import Route

VALID_ROUTE_ID = 1111 # some numbers, just not to stay empty

class TestRoute(TestCase):
    def setUp(self):
        self.route = Route()