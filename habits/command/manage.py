import sys
from habits.database.habit_repository import HabitRepository
from habits.console_definition import ConsoleDefinition
from habits.command.help import Help
from datetime import datetime


class Manage:
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'List, create and delete habits.',
            'manage (delete|create|list)',
            'Available parameters:',
            {
                'create': 'Starts wizard for creating a habit.',
                'delete': 'Starts wizard for deleting a habit.',
                'list': 'List all current habits.',
            }
        )

    @staticmethod
    def execute(args, database, config):
        repository = HabitRepository(database, config)

        if len(args) == 0 or args[0] == 'list':
            Manage.list_habits(repository)
            return

        if args[0] == 'create':
            Manage.create_habit(repository, config)
            return

        if args[0] == 'delete':
            Manage.delete_habit(repository)
            return

        sys.stdout.write("Invalid command parameters\n")

        Help.display_help(Manage.definition(config))

    @staticmethod
    def list_habits(repository: HabitRepository):
        output = '#{} - {} ({} habit)\n'
        for habit in repository.fetch_all():
            sys.stdout.write(output.format(habit.id, habit.title, habit.period))

    @staticmethod
    def create_habit(repository: HabitRepository, config):
        sys.stdout.write('Title: ')
        title = str(input()).strip()
        sys.stdout.write('\n')
        if len(title) < 1:
            sys.stdout.write("Title can't be empty\n")
            return

        output = '{}) {}\n'
        periods = list(config.get('periods').keys())
        for i, name in enumerate(periods, start=1):
            sys.stdout.write(output.format(i, name))

        sys.stdout.write('Period: ')
        period_selection = int(input()) - 1
        if period_selection < 0 or period_selection >= len(periods):
            sys.stdout.write("Selected period does not exist.\n")
            return

        habit = repository.create({
            'title': title,
            'period': periods[period_selection],
            'created_at': datetime.now(),
        })
        sys.stdout.write('Habit {} with id {} successfully saved.\n'.format(habit.title, habit.id))

    @staticmethod
    def delete_habit(repository: HabitRepository):
        output = '#{} {}\n'
        for habit in repository.fetch_all():
            sys.stdout.write(output.format(habit.id, habit.title))

        sys.stdout.write('Habit: ')
        requested_habit_id = int(input())
        sys.stdout.write('\n')
        habit = repository.fetch_by_id(requested_habit_id)
        repository.remove(habit.id)
        sys.stdout.write('Habit #{} {} deleted.\n'.format(habit.id, habit.title))
