import sys
from habits.console_definition import ConsoleDefinition
from habits.analyze.utils import analyze_stream
from habits.analyze.utils import filter_and_sort_raw_data
from habits.analyze.utils import create_stream
from habits.command.command import Command


class Analyze(Command):
    @staticmethod
    def definition(config: dict) -> ConsoleDefinition:
        return ConsoleDefinition(
            'Analyze your habits.',
            'analyze',
            'Available parameters:',
            {}
        )

    def execute(self):
        selected_habit_id = self._request_user_input()

        periods = self.config.get('periods')
        stream = []
        for item in self._raw_habits(selected_habit_id):
            habit = dict(item)
            data = filter_and_sort_raw_data(habit['id'], self._raw_tracking())
            data = periods.get(habit['period'])(habit['created_at'], data)
            stream = stream + list(create_stream(data))

        analyzed_stream = {}
        if len(stream) > 0:
            analyzed_stream = analyze_stream(stream)

        self._output_result(analyzed_stream)

    def _request_user_input(self) -> int:
        output = '#{} {}\n'
        sys.stdout.write(output.format(0, 'All habits'))
        self.display_habit_list()
        sys.stdout.write('Habit: ')
        selected_habit_id = int(input())
        sys.stdout.write('\n\n')

        return selected_habit_id

    def _output_result(self, info: dict):
        if 'number_of_breaks' not in info.keys():
            sys.stdout.write('Not enough data to provide analyzing')
            return

        sys.stdout.write("Longest streak: {} - {}\n".format(info['highest_streak'][2], info['highest_streak'][3]))
        sys.stdout.write("Number of streaks: {}\n".format(info['number_of_breaks']))
        sys.stdout.write("Number of breaks: {}\n".format(info['number_of_streaks']))
        sys.stdout.write("Success rate: {}%\n".format(round(info['sum_streak_units'] / info['sum_complete_units'] * 100)))

    def _raw_habits(self, selected_habit_id: int) -> iter:
        if selected_habit_id == 0:
            sql = 'SELECT rowid as id, * FROM habits'
            params = []
        else:
            sql = 'SELECT rowid as id, * FROM habits WHERE rowid=?'
            params = [selected_habit_id]

        return self.database.load_all(sql, params)

    def _raw_tracking(self) -> iter:
        for item in self.database.load_all('SELECT * FROM tracking', []):
            yield dict(item)




