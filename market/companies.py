from market import db


def create_company(company_symbol, company_name, player_name):
    database = db.get_database()
    company_query = """
        INSERT INTO companies (
            symbol, full_name, creator
        ) VALUES (
           ?, ?, ?
        )
    """
    query_params = (company_symbol, company_name, player_name)
    database.query(company_query, query_params, commit=True)


def get_company_by_symbol(company_symbol):
    database = db.get_database()
    company_query = """
        SELECT * from companies WHERE symbol = ?
    """
    query_params = (company_symbol,)
    return database.fetch_as_dict(company_query, query_params)


def get_company_by_creator(creator):
    database = db.get_database()
    company_query = """
        SELECT * from companies WHERE creator = ?
    """
    query_params = (creator,)
    return database.fetch_as_dict(company_query, query_params)


def get_company_by_full_name(full_name):
    database = db.get_database()
    company_query = """
        SELECT * from companies WHERE full_name = ?
    """
    query_params = (full_name,)
    return database.fetch_as_dict(company_query, query_params)


def get_exact_company(creator, company_symbol, full_name):
    database = db.get_database()
    company_query = """
        SELECT *
        FROM companies
        WHERE creator = ?
        AND symbol = ?
        AND full_name = ?
    """
    query_params = (creator, company_symbol, full_name)
    return database.fetch_as_dict(company_query, query_params)
