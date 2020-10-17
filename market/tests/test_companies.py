from market import players, companies
from market.tests import utils


class CompanyTest(utils.MarketDBTest):

    def test_create_and_get_company(self):
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
        creator_company = companies.get_company_by_creator(player_name)
        self.assertEqual(company, creator_company)

    def test_get_null_company(self):
        non_creator = "nonuser"
        company = companies.get_company_by_creator(non_creator)
        self.assertIsNone(company)

        non_symbol = "NOSYM"
        company = companies.get_company_by_symbol(non_symbol)
        self.assertIsNone(company)

    def test_process_file(self):
        import ipdb
        ipdb.set_trace()
