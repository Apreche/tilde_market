import os
import json

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


def process_file(user, filename):
    with open(filename) as company_file:
        data = json.load(company_file)
    company = data.get('company', {})
    symbol = company.get('symbol', None)
    full_name = company.get('full_name', None)
    import ipdb
    ipdb.set_trace()
    print(f"{symbol} - {full_name}")


def process_company_files(homedir):
    for userdir in os.listdir(homedir):
        company_file = os.path.join(homedir, userdir, '.market/company.json')
        if os.path.isfile(company_file):
            process_file(userdir, company_file)
