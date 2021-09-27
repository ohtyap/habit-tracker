import importlib.resources
import os
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, database_file):
        self._connection = sqlite3.connect(database_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._connection.row_factory = sqlite3.Row
        self.migration()

    # Closes the connection and commits the transaction
    def shutdown(self):
        self._connection.commit()
        self._connection.close()

    # Fetch one row by a given SQL statement
    def load_one(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()

    # Fetches all date by a given SQL statement
    def load_all(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    # Send am insert SQL statement to the sqlite connection and return the last insert id
    def insert(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.lastrowid

    # Send a delete SQL statement to the sqlite connection
    def delete(self, sql, params):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)

    # Lookup if the table "habits" exists in the current sqlite connection
    # If not, assume the database must be initialized.
    # setup.sql (including dummy data) will be inserted
    def migration(self):
        result = self.load_one('SELECT name FROM sqlite_master WHERE type=? AND name=?', ['table', 'habits'])
        if result is not None:
            return
        cursor = self._connection.cursor()
        cursor.executescript(
            importlib.resources.read_text("habits.database", "setup.sql")
        )
