from habits.database.repository import Repository
from habits.database.habit import Habit


class HabitRepository(Repository):
    _table = 'habits'
    _entity = Habit
