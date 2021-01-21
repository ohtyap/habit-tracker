from habits.database.repository import Repository
from habits.database.habit import Habit
from datetime import datetime


class HabitRepository(Repository):
    _table = 'habits'
    _entity = Habit

    def create_new_habit(self, title: str, period: str) -> Habit:
        return self.create({
            'title': title,
            'period': period,
            'created_at': datetime.now(),
        })
