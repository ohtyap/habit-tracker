from habits.command.help import Help
from habits.command.manage import Manage
from habits.command.track import Track
from habits.command.analyze import Analyze
from habits.database.habit import Habit
from habits.database.tracking import Tracking

config = {
    'commands': {
        'help': Help,
        'manage': Manage,
        'track': Track,
        'analyze': Analyze,
    },
    'entities': [
        Habit,
        Tracking
    ],
    'periods': {
        'daily': '',
        'weekly': '',
    }
}
