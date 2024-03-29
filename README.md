# Habit Tracker
The habit tracker is a small python based command line application which helps you how 
well you are sticking with your daily or weekly habits.

## Installation
```commandline
$ git clone https://github.com/ohtyap/habit-tracker
$ cd habit-tracker
$ python -m habits
```

## CLI Manual

### Create a new habit
With the following command a wizard for habit creation will start. You will be asked for a title
of your habit (like "10 glasses of water") and in what period this habit should be measured (daily 
or weekly)
```commandline
$ python -m habits manage create
```

### List your habits
To retrieve a list of available habits just enter:
```commandline
$ python -m habits manage list
```
To limit the list of habits to a selected period you can add the `--period` parameter.
```commandline
$ python -m habits manage list --period daily
```

### Delete a habit
You can delete habits by executing the following command. You will be asked which habit you 
want to delete. All tracking data will be deleted too.
```commandline
$ python -m habits manage delete
```

### Checkoff a habit
One of the most common commands might be the track command. It tracks a checkoff of an task. After 
execution of the command you will asked for which habit you want to add the track.
```commandline
$ python -m habits track
```

### Analyze your success
You can analyse a single habit or analyze your overall success. Along with your success rate, your longest
streak and  the number of your streaks and breaks will be evaluated.
```commandline
$ python -m habits analyze
```

### In case you need help
To receive a list of all available commands:
```commandline
$ python -m habits help
```
If you want help for a specific command:
```commandline
$ python -m habits help manage
```

## Database
A sqlite database is used as storage backend. It is located at `sqlite/habit-tracker.db`.

## Provide your own period
In case you want to add your own period extension to provide more periods (like monthly). To do so 
a function is needed which excepts a datetime list of all tracking and returns a (identifier, is_done)
tuple.
```python
# input of all tracking - every checkoff of the user
[datetime, datetime, datetime]
# expected output
[('Nov. 2020', True), ('Dec. 2020', False)]
```
The identifier can be anything and will be used only for display purposes. It is recommended to use an
user friendly string. The boolean value indicates if the user checked off the habit in this period.

This function must be registered in `runtime_config.py`. 
```python
from habits.analyze.daily import create_stream as daily_create_stream
from habits.analyze.weekly import create_stream as weekly_create_stream
from habits.analyze.monthly import create_stream as monthly_create_stream


config = {
    #...
    "periods": {
        'daily': daily_create_stream,
        'weekly': weekly_create_stream,
        'monthly': monthly_create_stream,
    }
}
```

## Add your own console command
To add your own console command, you need to create a class which inherits from `Commmand` and 
is implementing two methods. As example a boilerplate code:

```python
from habits.console_definition import ConsoleDefinition
from habits.command.command import Command


class YourCommand(Command):
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'A little description',
            'Usage',
            'title of your parameters',
            {
                '--try': 'Explanation of --try'
            }
        )

    def execute(self):
        # Access to args
        self.args
        # Access to the database
        self.database
        # Access to the runtime config
        self.config
        # Access to the HabitRepository
        self.habit_repository
        # Access to the TrackingRepository
        self.tracking_repository
```

Like periods a command is register inside the `runtime_config`:
```python
from habits.command.help import Help
from habits.command.manage import Manage
from habits.command.track import Track
from habits.command.analyze import Analyze
from habits.command.your_command import YourCommand
config ={ 
    'commands': {
        'help': Help,
        'manage': Manage,
        'track': Track,
        'analyze': Analyze,
        'yourcommand': YourCommand
    },
}
```

## Run unit tests
```commandline
$ python -m unittest discover -s tests
```