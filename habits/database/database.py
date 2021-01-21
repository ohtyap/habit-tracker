import sqlite3
import os


class Database:
    def __init__(self, database_file):
        self._connection = sqlite3.connect(database_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._connection.row_factory = sqlite3.Row
        self.migration()

    def shutdown(self):
        self._connection.commit()
        self._connection.close()

    def load_one(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()

    def load_all(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def insert(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.lastrowid

    def delete(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)

    def migration(self):
        result = self.load_one('SELECT name FROM sqlite_master WHERE type=? AND name=?', ['table', 'habits'])
        if result is not None:
            return
        sql_file = os.path.abspath(os.path.dirname(__file__) + '/../../setup') + '/setup.sql'
        cursor = self._connection.cursor()
        cursor.executescript(open(sql_file).read())
