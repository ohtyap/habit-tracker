from habits.command.help import Help
from habits.command.manage import Manage
from habits.command.track import Track
from habits.command.analyze import Analyze
from habits.database.habit import Habit
from habits.database.tracking import Tracking
from habits.analyze.daily import create_stream as daily_create_stream
from habits.analyze.weekly import create_stream as weekly_create_stream

config = {
    # A list of all available console command as key -> value
    # key: a string - how the command can be invoked by the CLI
    # value: the corresponding command
    'commands': {
        'help': Help,
        'manage': Manage,
        'track': Track,
        'analyze': Analyze,
    },

    # A list of all available entities, needed by the repository
    'entities': [
        Habit,
        Tracking
    ],

    # A list of all available periods as key -> value
    # key: string representation of the period, used for sqlite
    # value: corresponding stream creation
    'periods': {
        'daily': daily_create_stream,
        'weekly': weekly_create_stream,
    }
}
