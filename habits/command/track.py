import sys
from habits.console_definition import ConsoleDefinition
from habits.command.command import Command


class Track(Command):
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'Checkoff a habit.',
            'track',
            '',
            {}
        )

    def execute(self):
        self.display_habit_list()
        sys.stdout.write('\nHabit: ')

        requested_habit_id = int(input())
        sys.stdout.write('\n\n')

        try:
            habit = self.habit_repository.fetch_by_id(requested_habit_id)
            self.tracking_repository.create_new_tracking_entry(habit.id)
        except RuntimeError:
            sys.stdout.write('Invalid habit selection')





