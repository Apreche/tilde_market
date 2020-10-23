from market import players, companies
from market.tests import utils


class CompanyTest(utils.MarketDBTest):

    def test_create_and_get_by_symbol(self):
        player_name = "joeyjoejoe"
        players.create_player(player_name)
        company_symbol = "ASDF"
        company_name = "All Something Do Fun"
        companies.create_company(company_symbol, company_name, player_name)
        company = companies.get_company_by_symbol(company_symbol)
        self.assertEqual(
            company,
            {
                'symbol': company_symbol,
                'full_name': company_name,
                'creator': player_name,
            }
        )

    def test_create_and_get_by_creator(self):
        player_name = "joeyjoejoe"
        players.create_player(player_name)
        company_symbol = "ASDF"
        company_name = "All Something Do Fun"
        companies.create_company(company_symbol, company_name, player_name)
        company = companies.get_company_by_creator(player_name)
        self.assertEqual(
            company,
            {
                'symbol': company_symbol,
                'full_name': company_name,
                'creator': player_name,
            }
        )

    def test_create_and_get_by_full_name(self):
        player_name = "joeyjoejoe"
        players.create_player(player_name)
        company_symbol = "ASDF"
        company_name = "All Something Do Fun"
        companies.create_company(company_symbol, company_name, player_name)
        company = companies.get_company_by_full_name(company_name)
        self.assertEqual(
            company,
            {
                'symbol': company_symbol,
                'full_name': company_name,
                'creator': player_name,
            }
        )

    def test_create_and_get_exact_company(self):
        player_name = "joeyjoejoe"
        players.create_player(player_name)
        company_symbol = "ASDF"
        company_name = "All Something Do Fun"
        companies.create_company(company_symbol, company_name, player_name)
        company = companies.get_exact_company(player_name, company_symbol, company_name)
        self.assertEqual(
            company,
            {
                'symbol': company_symbol,
                'full_name': company_name,
                'creator': player_name,
            }
        )

    def test_get_null_company(self):
        non_creator = "nonuser"
        company = companies.get_company_by_creator(non_creator)
        self.assertIsNone(company)

        non_symbol = "NOSYM"
        company = companies.get_company_by_symbol(non_symbol)
        self.assertIsNone(company)

        non_name = "NONAME"
        company = companies.get_company_by_full_name(non_name)
        self.assertIsNone(company)

        company = companies.get_exact_company(non_creator, non_symbol, non_name)
        self.assertIsNone(company)
