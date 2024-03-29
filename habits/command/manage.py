import sys
from habits.console_definition import ConsoleDefinition
from habits.command.command import Command


class Manage(Command):

    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'List, create and delete habits.',
            'manage (delete|create|list) [--period xyz]',
            'Available parameters:',
            {
                'create': 'Starts wizard for creating a habit.',
                'delete': 'Starts wizard for deleting a habit.',
                'list': 'List all current habits.',
                '--period': 'Limit the output to a selected period. Only works in combination with list.'
            }
        )

    def execute(self):
        command = ''
        if len(self.args) > 0:
            command = self.args[0]

        if command == 'list':
            self.list_habits()
            return

        if command == 'create':
            self.create_habit()
            return

        if command == 'delete':
            self.delete_habit()
            return

        sys.stdout.write("Invalid command parameters\n")
        self.config.get('commands').get('help').display_help(Manage.definition(self.config))

    def list_habits(self):
        period = None
        if len(self.args) == 3 and self.args[1] == '--period':
            period = self.args[2]

        if period is not None and period not in self.config.get('periods'):
            sys.stdout.write("Invalid period\n")
            return

        self.display_habit_list(period)

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
