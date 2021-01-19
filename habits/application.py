import sys
from habits.runtime_config import config
from habits.database.database import Database


def run(database_file):
    database = Database(database_file)

    command_name_arr = sys.argv[1:2]
    command_name = "help"
    if len(command_name_arr) != 0:
        command_name = command_name_arr[0]
    commands = config.get('commands')

    command = commands.get(command_name)
    if command is None:
        sys.stdout.write('Command not found. See help for more information\n')
        command = commands.get('help')

    command.execute(sys.argv[2:], database, config)
    database.shutdown()
