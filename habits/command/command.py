from habits.database.habit_repository import HabitRepository
from habits.database.database import Database
from habits.database.tracking_repository import TrackingRepository
import sys


class Command:
    _args: list
    _config: 'config'
    _database: Database
    _habit_repository: HabitRepository = None
    _tracking_repository: TrackingRepository = None

    def __init__(self, args: list, database: Database, config: 'config'):
        self._args = args
        self._config = config
        self._database = database

    @property
    def args(self) -> list:
        return self._args

    @property
    def config(self) -> 'config':
        return self._config

    @property
    def database(self) -> Database:
        return self._database

    @property
    def habit_repository(self) -> HabitRepository:
        if self._habit_repository is None:
            self._habit_repository = HabitRepository(self.database, self.config)

        return self._habit_repository

    @property
    def tracking_repository(self) -> TrackingRepository:
        if self._tracking_repository is None:
            self._tracking_repository = TrackingRepository(self.database, self.config)

        return self._tracking_repository

    def display_habit_list(self, period: str = None):
        output = '#{} {}\n'
        for habit in self.habit_repository.fetch_all():
            sys.stdout.write(output.format(habit.id, habit.title))