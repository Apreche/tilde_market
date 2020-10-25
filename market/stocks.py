from market import db
from market import players
from market import companies

COMPANY_STARTING_SHARES = 100


def get_all_company_shares(company_symbol):
    database = db.get_database()
    query = """SELECT * from shares where company = ?"""
    return database.fetchall_as_dict(query, params=(company_symbol,))


def new_company_shares(player_name, num_shares=COMPANY_STARTING_SHARES):
    # Add the shares for a new company to the market
    player = players.get_player(player_name)
    if player is None:
        return False
    company = companies.get_company_by_creator(player_name)
    if company is None:
        return False
    existing_shares = get_all_company_shares(company['symbol'])
    if existing_shares:
        return False

    database = db.get_database()
    query = """
        INSERT INTO shares (
            player, company, quantity
        ) VALUES (?, ?, ?)
    """
    database.query(
        query, params=(
            player['name'],
            company['symbol'],
            COMPANY_STARTING_SHARES
        ), commit=True
    )
    return True
