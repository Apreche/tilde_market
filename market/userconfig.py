import json
import os
import re

from market import companies
from market import mail
from market import players
from market import stocks


def validate_config_data(user, config_data):
    pattern_tuples = [
        ('symbol', r'^[A-Z]{1,5}$'),
        ('full_name', r'^[a-zA-Z ]+$'),
    ]

    error_messages = []
    for key, pattern in pattern_tuples:
        value = config_data.get(key, None)
        if value is None:
            error_messages.append(
                f"{key} is not present"
            )
            continue
        if type(value) != str:
            error_messages.append(
                f"{key}: {value} is not a string"
            )
            continue
        if not re.match(pattern, value):
            error_messages.append(
                f"{key}: {value} doesn't match {pattern}"
            )
            continue

    if error_messages:
        error_message = "\n".join(error_messages)
        error_message = f"config.json invalid:\n\n{error_message}"
        mail.send_template_email(
            user,
            'user_config_json_error',
            error_message=error_message
        )
        return False
    return True


def process_config_data(user, config_data):
    if not validate_config_data(user, config_data):
        return None
    symbol = config_data.get('symbol')
    full_name = config_data.get('full_name')

    exact_company = companies.get_exact_company(user, symbol, full_name)
    if exact_company:
        # no changes to config
        return True

    unique_properties = [
        ('User', user, companies.get_company_by_creator),
        ('Symbol', symbol, companies.get_company_by_symbol),
        ('Name', full_name, companies.get_company_by_full_name),
    ]

    error_messages = []
    for varname, value, method in unique_properties:
        found_row = method(value)
        if found_row is not None:
            error_messages.append(
                f"{varname} {value} in use. Must choose a different one"
            )

    if error_messages:
        error_message = '\n'.join(error_messages)
        mail.send_template_email(
            user,
            'user_config_json_error',
            error_message=error_message
        )
        return False

    player = players.get_player(user)
    if not player:
        players.create_player(user)
    companies.create_company(symbol, full_name, user)
    stocks.new_company_shares(user)


def process_all_config_files(homedir):
    userdirs = os.listdir(homedir)
    userdirs.sort()
    for userdir in userdirs:
        config_filename = os.path.join(homedir, userdir, '.market/config.json')
        if os.path.isfile(config_filename):
            with open(config_filename) as config_file:
                try:
                    config_data = json.load(config_file)
                except json.JSONDecodeError as e:
                    error_message = f"company.json JSONDecodeError: {e}"
                    mail.send_template_email(
                        userdir,
                        'user_config_json_error',
                        error_message=error_message
                    )
                    continue
                process_config_data(userdir, config_data)
