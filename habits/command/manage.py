import sys
from habits.console_definition import ConsoleDefinition
from datetime import datetime
from habits.command.command import Command


class Manage(Command):

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

    def execute(self):
        if self.args[0] == 'list':
            self.list_habits()
            return

        if self.args[0] == 'create':
            self.create_habit()
            return

        if self.args[0] == 'delete':
            self.delete_habit()
            return

        sys.stdout.write("Invalid command parameters\n")

        self.config.get('commands').get('help').display_help(Manage.definition(self.config))

    def list_habits(self):
        self.display_habit_list()

    def create_habit(self):
        sys.stdout.write('Title: ')
        title = str(input()).strip()
        sys.stdout.write('\n')
        if len(title) < 1:
            sys.stdout.write("Title can't be empty\n")
            return

        output = '{}) {}\n'
        periods = list(self.config.get('periods').keys())
        for i, name in enumerate(periods, start=1):
            sys.stdout.write(output.format(i, name))

        sys.stdout.write('Period: ')
        period_selection = int(input()) - 1
        if period_selection < 0 or period_selection >= len(periods):
            sys.stdout.write("Selected period does not exist.\n")
            return

        habit = self.habit_repository.create_new_habit(title, periods[period_selection])
        sys.stdout.write('Habit {} with id {} successfully saved.\n'.format(habit.title, habit.id))

    def delete_habit(self):
        self.display_habit_list()
        sys.stdout.write('Habit: ')
        requested_habit_id = int(input())
        sys.stdout.write('\n')
        habit = self.habit_repository.fetch_by_id(requested_habit_id)
        self.habit_repository.remove(habit.id)
        self.tracking_repository.delete_by_habit_id(habit.id)
        sys.stdout.write('Habit #{} {} deleted.\n'.format(habit.id, habit.title))
