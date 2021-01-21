import sys
from habits.console_definition import ConsoleDefinition
from habits.command.command import Command


class Help(Command):
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        command_list = config.get('commands')

        commands = {}
        for item in command_list.keys():
            # Necessary to avoid circular method call for the help command
            if item == 'help':
                commands[item] = 'Get help on a command.'
            else:
                commands[item] = command_list.get(item).definition(config).description

        return ConsoleDefinition(
            'Get help on a command.',
            'help [COMMAND]',
            'Available commands:',
            commands
        )

    @staticmethod
    def display_help(console_definition: ConsoleDefinition):
        sys.stdout.write('Usage:\n  ' + console_definition.usage + '\n\n')
        if len(console_definition.parameters) == 0:
            return

        sys.stdout.write(console_definition.parameter_title + '\n')
        output = '  {}{}{}\n'
        for item in console_definition.parameters.keys():
            sys.stdout.write(output.format(item, " " * (15 - len(item)), console_definition.parameters.get(item)))
        sys.stdout.write('\n')

    def execute(self):
        commands = self.config.get('commands')

        if len(self.args) == 0:
            Help.display_help(Help.definition(self.config))
            return

        if self.args[0] not in commands:
            sys.stdout.write('Command {} does not exist.\n'.format(self.args[0]))
            Help.display_help(Help.definition(self.config))
            return

        command = commands.get(self.args[0])
        Help.display_help(command.definition(self.config))
