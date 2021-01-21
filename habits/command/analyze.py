import sys
from habits.console_definition import ConsoleDefinition
from habits.analyze.utils import analyze_stream
from habits.analyze.utils import filter_and_sort_raw_data
from habits.analyze.utils import create_stream
from habits.database.habit_repository import HabitRepository


class Analyze:
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'Analyze your habits.',
            'analyze',
            'Available parameters:',
            {}
        )

    @staticmethod
    def execute(args, database, config):
        repository = HabitRepository(database, config)
        output = '#{} {}\n'
        sys.stdout.write(output.format(0, 'All habits'))
        for habit in repository.fetch_all():
            sys.stdout.write(output.format(habit.id, habit.title))

        sys.stdout.write('Habit: ')
        requested_habit_id = int(input())
        sys.stdout.write('\n\n')

        tracking = []
        for item in database.load_all('SELECT * FROM tracking', []):
            tracking.append(dict(item))

        periods = config.get('periods')
        stream = []

        if requested_habit_id == 0:
            sql = 'SELECT rowid as id, * FROM habits'
            params = []
        else:
            sql = 'SELECT rowid as id, * FROM habits WHERE rowid=?'
            params = [requested_habit_id]

        for item in database.load_all(sql, params):
            habit = dict(item)
            data = filter_and_sort_raw_data(habit['id'], tracking)
            data = periods.get(habit['period'])(habit['created_at'], data)
            stream = stream + list(create_stream(data))

        info = analyze_stream(stream)
        sys.stdout.write("Longest streak: {} - {}\n".format(info['highest_streak'][2], info['highest_streak'][3]))
        sys.stdout.write("Number of streaks: {}\n".format(info['number_of_breaks']))
        sys.stdout.write("Number of breaks: {}\n".format(info['number_of_streaks']))
        sys.stdout.write("Success rate: {}%\n".format(round(info['sum_streak_units']/info['sum_complete_units'] * 100)))

