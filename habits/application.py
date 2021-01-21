import sys
from habits.runtime_config import config
from habits.database.database import Database


def run(database_file: str):

    # Initializing the sqlite database wrapper
    database = Database(database_file)

    # Commands must be on the second place in the argv list (argv[1])
    command_name_arr = sys.argv[1:2]

    # The default command is set to 'help'. Will be used when argv[1] is empty
    command_name = "help"
    if len(command_name_arr) != 0:
        command_name = command_name_arr[0]

    commands = config.get('commands')

    command = commands.get(command_name)
    # When selected command does not exist in the runtime_config, fallback to `help`
    if command is None:
        sys.stdout.write('Command not found. See help for more information\n')
        command = commands.get('help')

    try:
        # Forward the remaining argv arguments, the database and the runtime config to the command
        command.execute(sys.argv[2:], database, config)
    except KeyboardInterrupt:
        # In case the user interrupts the input (ctrl + c)
        pass

    database.shutdown()
