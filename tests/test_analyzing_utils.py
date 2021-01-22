import unittest
from habits.analyze.utils import *
from datetime import datetime


class AnalyzingUtilsTestCase(unittest.TestCase):
    def test_analyze_stream(self):
        result = analyze_stream(
            [
                (True, 2, '2020-12-01', '2020-12-02'),
                (False, 3, '2020-12-03', '2020-12-05'),
                (True, 2, '2020-12-06', '2020-12-07'),
                (False, 1, '2020-12-08', '2020-12-08'),
                (True, 1, '2020-12-09', '2020-12-09'),
            ]
        )

        self.assertEqual(result['sum_complete_units'], 9)
        self.assertEqual(result['sum_streak_units'], 5)
        self.assertEqual(result['number_of_streaks'], 3)
        self.assertEqual(result['number_of_breaks'], 2)
        self.assertEqual(result['highest_streak'], (True, 2, '2020-12-01', '2020-12-02'))

        result = analyze_stream([])
        self.assertEqual({}, result)


    def test_create_stream(self):
        result = create_stream([
            ('2020-12-01', True),
            ('2020-12-02', True),
            ('2020-12-03', False),
            ('2020-12-04', False),
            ('2020-12-05', False),
            ('2020-12-06', True),
            ('2020-12-07', True),
            ('2020-12-08', False),
            ('2020-12-09', True),
        ])
        self.assertEqual(
            list(result),
            [
                (True, 2, '2020-12-01', '2020-12-02'),
                (False, 3, '2020-12-03', '2020-12-05'),
                (True, 2, '2020-12-06', '2020-12-07'),
                (False, 1, '2020-12-08', '2020-12-08'),
                (True, 1, '2020-12-09', '2020-12-09'),
            ]
        )

        # Testing empty list
        result = create_stream([])
        self.assertEqual(list(result), [])

        # One row list
        result = create_stream([
            ('2020-12-01', True),
        ])
        self.assertEqual(
            list(result),
            [
                (True, 1, '2020-12-01', '2020-12-01'),
            ]
        )

    def test_generate_streak_ids(self):
        result = generate_streak_ids([
            ('2020-12-01', True),
            ('2020-12-02', True),
            ('2020-12-03', False),
            ('2020-12-04', False),
            ('2020-12-05', False),
            ('2020-12-06', True),
            ('2020-12-07', True),
            ('2020-12-08', False),
            ('2020-12-09', True),
        ])

        self.assertEqual(
            list(result),
            [
                ('2020-12-01', True, 0),
                ('2020-12-02', True, 0),
                ('2020-12-03', False, 1),
                ('2020-12-04', False, 1),
                ('2020-12-05', False, 1),
                ('2020-12-06', True, 2),
                ('2020-12-07', True, 2),
                ('2020-12-08', False, 3),
                ('2020-12-09', True, 4),
            ]
        )

        # Testing empty list
        result = generate_streak_ids([])
        self.assertEqual(list(result), [])

        # One row list
        result = generate_streak_ids([
            ('2020-12-01', True),
        ])
        self.assertEqual(
            list(result),
            [
                ('2020-12-01', True, 0),
            ]
        )

    def test_group_tracking(self):
        result = group_tracking(
            [
                ('2020-12-01', True, 0),
                ('2020-12-02', True, 0),
                ('2020-12-03', False, 1),
                ('2020-12-04', False, 1),
                ('2020-12-05', False, 1),
                ('2020-12-06', True, 2),
                ('2020-12-07', True, 2),
                ('2020-12-08', False, 3),
                ('2020-12-09', True, 4),
            ]
        )

        expected = [
            [
                ('2020-12-01', True, 0), ('2020-12-02', True, 0),
            ],
            [
                ('2020-12-03', False, 1), ('2020-12-04', False, 1), ('2020-12-05', False, 1),
            ],
            [
                ('2020-12-06', True, 2), ('2020-12-07', True, 2),
            ],
            [
                ('2020-12-08', False, 3),
            ],
            [
                ('2020-12-09', True, 4),
            ]
        ]

        index = 0
        for item in result:
            self.assertEqual(list(item), expected[index])
            index = index + 1

    def test_filter_streak(self):
        result = filter_streaks(
            [
                (True, 2, '2020-12-01', '2020-12-02'),
                (False, 3, '2020-12-03', '2020-12-05'),
                (True, 2, '2020-12-06', '2020-12-07'),
                (False, 1, '2020-12-08', '2020-12-08'),
                (True, 1, '2020-12-09', '2020-12-09'),
            ]
        )

        self.assertEqual(
            list(result),
            [
                (True, 2, '2020-12-01', '2020-12-02'),
                (True, 2, '2020-12-06', '2020-12-07'),
                (True, 1, '2020-12-09', '2020-12-09'),
            ]
        )

    def test_sum_units(self):
        result = sum_units(
            [
                (True, 2, '2020-12-01', '2020-12-02'),
                (False, 3, '2020-12-03', '2020-12-05'),
                (True, 2, '2020-12-06', '2020-12-07'),
                (False, 1, '2020-12-08', '2020-12-08'),
                (True, 1, '2020-12-09', '2020-12-09'),
            ]
        )

        self.assertEqual(result, 9)

    def test_highest_item(self):
        result = highest_item(
            [
                (True, 2, '2020-12-01', '2020-12-02'),
                (False, 3, '2020-12-03', '2020-12-05'),
                (True, 2, '2020-12-06', '2020-12-07'),
                (False, 1, '2020-12-08', '2020-12-08'),
                (True, 1, '2020-12-09', '2020-12-09'),
            ]
        )
        self.assertEqual(result, (False, 3, '2020-12-03', '2020-12-05'))

    def test_filter_and_sort_raw_data(self):
        input_data = [
            {"habit_id": 1, "created_at": datetime.strptime("2021-01-15 14:00:00", "%Y-%m-%d %H:%M:%S")},
            {"habit_id": 1, "created_at": datetime.strptime("2021-01-15 14:01:00", "%Y-%m-%d %H:%M:%S")},
            {"habit_id": 2, "created_at": datetime.strptime("2021-01-12 14:00:00", "%Y-%m-%d %H:%M:%S")},
            {"habit_id": 2, "created_at": datetime.strptime("2021-01-12 14:01:00", "%Y-%m-%d %H:%M:%S")},
            {"habit_id": 1, "created_at": datetime.strptime("2021-01-13 15:00:00", "%Y-%m-%d %H:%M:%S")},
            {"habit_id": 1, "created_at": datetime.strptime("2021-01-13 15:01:00", "%Y-%m-%d %H:%M:%S")},
        ]

        result = filter_and_sort_raw_data(1, input_data)
        self.assertEqual(
            result,
            [
                datetime.strptime("2021-01-13 15:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2021-01-13 15:01:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2021-01-15 14:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2021-01-15 14:01:00", "%Y-%m-%d %H:%M:%S")
            ]
        )