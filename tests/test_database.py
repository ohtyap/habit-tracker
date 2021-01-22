import unittest
from habits.database.database import Database
from sqlite3 import Row
from datetime import datetime


class DatabaseTestCase(unittest.TestCase):
    def test_migration(self):
        database = Database(':memory:')
        result = database.load_one('SELECT rowid FROM habits WHERE rowid=?', [1])

        self.assertIsInstance(result, Row)

    def test_delete(self):
        database = Database(':memory:')
        database.delete('DELETE FROM habits WHERE rowid=?', [1])

        result = database.load_one('SELECT rowid FROM habits WHERE rowid=?', [1])
        self.assertIsNone(result)

    def test_insert(self):
        database = Database(':memory:')
        rowid = database.insert(''
                                'INSERT INTO habits (title, period, created_at) VALUES (?, ?, ?)',
                                ["Test", "daily", datetime.now()]
                                )
        result = database.load_one('SELECT title FROM habits WHERE rowid=?', [rowid])
        self.assertEqual(dict(result)['title'], 'Test')

    def test_load_all(self):
        database = Database(':memory:')
        result = database.load_all('SELECT * FROM habits', [])
        self.assertEqual(5, len(result))

    def test_load_one(self):
        database = Database(':memory:')
        result = database.load_one('SELECT rowid FROM habits WHERE rowid=?', [1])
        self.assertEqual(dict(result)['rowid'], 1)
