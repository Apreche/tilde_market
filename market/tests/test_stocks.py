from market import companies
from market import players
from market import stocks
from market.tests import utils


class StocksTest(utils.MarketDBTest):

    def test_new_company_shares(self):
        player_name = "joeyjoejoe"
        company_name = "joecorp"
        company_symbol = "joe"
        players.create_player(player_name)
        companies.create_company(company_symbol, company_name, player_name)
        stocks.new_company_shares(player_name)
        shares = stocks.get_all_company_shares(company_symbol)
        self.assertEqual(
            shares, [
                {
                    'company': company_symbol,
                    'player': player_name,
                    'quantity': stocks.COMPANY_STARTING_SHARES,
                }
            ]
        )
