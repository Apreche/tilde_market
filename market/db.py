import os
import sqlite3

from market import settings


class Database:

    def __init__(self, path=None):
        db_path = path or getattr(settings, 'DB_PATH', ':memory:')
        self._connection = sqlite3.connect(db_path)

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._connection.cursor()

    def create_schema(self):
        sql_filename = os.path.join(
            os.path.dirname(__file__),
            "sql/createdb.sql"
        )
        with open(sql_filename) as sql_file:
            create_sql = sql_file.read()
            self.cursor.executescript(create_sql)
            self.commit()

    def query(self, query, params=(), commit=False):
        result = self.cursor.execute(query, params)
        if commit:
            self._connection.commit()
        return result

    def commit(self):
        self._connection.commit()

    def fetch_as_dict(self, query, params=()):
        result = self.query(query, params)
        keys = [key[0] for key in result.description]
        row = result.fetchone()
        if row is None:
            return None
        return dict(zip(keys, row))

    def fetchall_as_dict(self, query, params=()):
        results = self.query(query, params)
        keys = [key[0] for key in results.description]
        dict_results = []
        for row in results.fetchall():
            dict_results.append(dict(zip(keys, row)))
        return dict_results


database = None


def get_database(db_path=None):
    global database
    if database is None:
        database = Database(db_path)
    return database


def destroy_database():
    global database
    database.connection.close()
    database = None
