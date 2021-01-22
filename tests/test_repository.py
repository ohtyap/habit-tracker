import unittest
from habits.database.database import Database
from habits.database.habit_repository import HabitRepository
from habits.database.habit import Habit
from habits.runtime_config import config
from datetime import datetime


class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database = Database(':memory:')
        self.repository = HabitRepository(self.database, config)

    def test_fetch_by_id(self):
        habit = self.repository.fetch_by_id(1)
        self.assertIsInstance(habit, Habit)

    def test_fetch_all(self):
        habits = self.repository.fetch_all()
        self.assertEqual(5, len(habits))
        for habit in habits:
            self.assertIsInstance(habit, Habit)

    def test_delete(self):
        self.repository.remove(1)
        self.assertRaises(RuntimeError, lambda: self.repository.fetch_by_id(1))

    def test_create(self):
        habit = self.repository.create({
            'title': 'Test',
            'period': 'daily',
            'created_at': datetime.now()
        })
        self.assertIsInstance(habit, Habit)
        self.assertEqual(habit.title, 'Test')

    def test_cache(self):
        self.repository.fetch_by_id(1)
        self.database.delete('DELETE FROM habits WHERE rowid=?', [1])
        habit = self.repository.fetch_by_id(1)
        self.assertIsInstance(habit, Habit)
        self.assertEqual(habit.id, 1)

