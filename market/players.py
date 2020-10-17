from market import db


def create_player(player_name):
    database = db.get_database()
    player_query = """INSERT INTO players (name) VALUES (?)"""
    database.query(
        player_query, (player_name,), commit=True
    )
    database.connection.commit()


def get_player(player_name):
    database = db.get_database()
    player_query = """
        SELECT * from players where name = ?
    """
    return database.fetch_as_dict(
        player_query, (player_name,),
    )
