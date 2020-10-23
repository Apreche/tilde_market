import os

from market import db
from market import companies
from market import players
from market import userconfig

from market.tests import utils


class UserConfigTest(utils.MarketDBTest):

    def test_validate_good_config_data(self):

        user = 'asdf'
        good_config_data = {
            'symbol': "ASDF",
            'full_name': "A S D F Corp",
        }
        result = userconfig.validate_config_data(user, good_config_data)
        self.assertTrue(result)

    def test_validate_bad_config_data(self):

        user = 'asdf'
        bad_config_data = {}
        result = userconfig.validate_config_data(user, bad_config_data)
        self.assertFalse(result)

        bad_config_data = {
            'full_name': "A S D F Corp",
        }
        result = userconfig.validate_config_data(user, bad_config_data)
        self.assertFalse(result)

        bad_config_data = {
            'symbol': 'ASDFFF',
            'full_name': "A S D F Corp",
        }
        result = userconfig.validate_config_data(user, bad_config_data)
        self.assertFalse(result)

        bad_config_data = {
            'symbol': 'ASDFF',
            'full_name': 3,
        }
        result = userconfig.validate_config_data(user, bad_config_data)
        self.assertFalse(result)

        bad_config_data = {
            'symbol': 'ASDFFFF',
            'full_name': 'hi',
        }
        result = userconfig.validate_config_data(user, bad_config_data)
        self.assertFalse(result)

    def test_process_config_data(self):
        user = 'asdf'
        symbol = "ASDF"
        config_data = {
            'symbol': symbol,
            'full_name': "A S D F Corp",
        }
        userconfig.process_config_data(user, config_data)
        company = companies.get_company_by_symbol(symbol)
        self.assertEqual(company.get('symbol', None), symbol)
        self.assertEqual(company.get('full_name', None), config_data['full_name'])
        self.assertEqual(company.get('creator', None), user)
        player = players.get_player(user)
        self.assertEqual(player.get('name', None), user)
        self.assertEqual(player.get('cash', 0.0), 1000.0)

    def test_process_config_data_already_exists(self):
        user = 'asdf'
        symbol = "ASDF"
        config_data = {
            'symbol': symbol,
            'full_name': "A S D F Corp",
        }
        userconfig.process_config_data(user, config_data)
        userconfig.process_config_data(user, config_data)
        company = companies.get_company_by_symbol(symbol)
        company = companies.get_company_by_symbol(symbol)
        self.assertEqual(company.get('symbol', None), symbol)
        self.assertEqual(company.get('full_name', None), config_data['full_name'])
        self.assertEqual(company.get('creator', None), user)
        player = players.get_player(user)
        self.assertEqual(player.get('name', None), user)
        self.assertEqual(player.get('cash', 0.0), 1000.0)
        player = players.get_player(user)

    def test_process_config_data_player_already_exist(self):
        user = 'asdf'
        players.create_player(user)
        symbol = "ASDF"
        config_data = {
            'symbol': symbol,
            'full_name': "A S D F Corp",
        }
        userconfig.process_config_data(user, config_data)
        company = companies.get_company_by_symbol(symbol)
        self.assertEqual(company.get('symbol', None), symbol)
        self.assertEqual(company.get('full_name', None), config_data['full_name'])
        self.assertEqual(company.get('creator', None), user)
        player = players.get_player(user)
        self.assertEqual(player.get('name', None), user)
        self.assertEqual(player.get('cash', 0.0), 1000.0)
        player = players.get_player(user)

    def test_process_config_data_no_changes(self):
        user = 'asdf'
        players.create_player(user)
        symbol = "ASDF"
        config_data = {
            'symbol': symbol,
            'full_name': "A S D F Corp",
        }
        userconfig.process_config_data(user, config_data)
        new_symbol = 'XXXX'
        new_config_data = {
            'symbol': new_symbol,
            'full_name': "X X X X Corp",
        }
        userconfig.process_config_data(user, new_config_data)
        company = companies.get_company_by_symbol(symbol)
        self.assertEqual(company.get('symbol', None), symbol)
        self.assertEqual(company.get('full_name', None), config_data['full_name'])
        self.assertEqual(company.get('creator', None), user)
        player = players.get_player(user)
        self.assertEqual(player.get('name', None), user)
        self.assertEqual(player.get('cash', 0.0), 1000.0)
        player = players.get_player(user)
        new_company = companies.get_company_by_symbol(new_symbol)
        self.assertEqual(new_company, None)

    def test_process_all_config_files(self):
        test_dir = os.path.dirname(
            os.path.abspath(__file__)
        )
        test_data_dir = os.path.join(
            test_dir, 'testdata'
        )
        userconfig.process_all_config_files(test_data_dir)

        test_companies = [
            {'symbol': "NEWU", 'full_name': "New Corp", 'creator': "newuser"},
            {'symbol': "ACOR", 'full_name': "A Corp", 'creator': "usera"},
            {'symbol': "BMO", 'full_name': "BMO Corp", 'creator': "userb"},
            {'symbol': "CLLC", 'full_name': "C LLC", 'creator': "userc"},
        ]

        database = db.get_database()
        company_count_query = """
            SELECT count(*) as count from companies
        """
        results = database.fetch_as_dict(company_count_query)
        self.assertEqual(results['count'], len(test_companies))

        player_count_query = """
            SELECT count(*) as count from players
        """
        results = database.fetch_as_dict(player_count_query)
        self.assertEqual(results['count'], len(test_companies))

        for test_company in test_companies:
            created_company = companies.get_company_by_symbol(
                test_company['symbol']
            )
            self.assertEqual(test_company, created_company)
            player = players.get_player(test_company['creator'])
            self.assertIsNotNone(player)

        badcorp = companies.get_company_by_symbol('BADU')
        self.assertIsNone(badcorp)
