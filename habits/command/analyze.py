import sys
from habits.console_definition import ConsoleDefinition


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
        pass





