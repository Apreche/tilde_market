import unittest

from market import db


class MarketDBTest(unittest.TestCase):

    def setUp(self):
        database = db.get_database(':memory:')
        database.create_schema()

    def tearDown(self):
        db.destroy_database()
