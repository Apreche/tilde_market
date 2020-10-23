from market import players
from market.tests import utils


class PlayerTest(utils.MarketDBTest):

    def test_create_get_player(self):
        player_name = "joeyjoejoe"
        players.create_player(player_name)
        player = players.get_player(player_name)
        self.assertEqual(player['name'], player_name)
