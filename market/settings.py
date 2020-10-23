import os

DB_PATH = os.environ.get('MARKET_DB_PATH', ':memory:')
SMTP_HOST = os.environ.get('SMTP_HOST', None)
