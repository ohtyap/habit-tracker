import sys
from habits.database.habit_repository import HabitRepository
from habits.database.tracking_repository import TrackingRepository
from habits.console_definition import ConsoleDefinition
from datetime import datetime


class Track:
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'Checkoff a habit.',
            'track',
            '',
            {}
        )

    @staticmethod
    def execute(args, database, config):
        habit_repository = HabitRepository(database, config)

        output = '#{} {}\n'
        for habit in habit_repository.fetch_all():
            sys.stdout.write(output.format(habit.id, habit.title))

        sys.stdout.write('Habit: ')
        requested_habit_id = int(input())
        sys.stdout.write('\n')
        habit = habit_repository.fetch_by_id(requested_habit_id)

        tracking_repository = TrackingRepository(database, config)
        tracking_repository.create({
            'habit_id': habit.id,
            'created_at': datetime.now(),
        })





