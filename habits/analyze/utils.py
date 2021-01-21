from itertools import groupby


def analyze_stream(stream: iter) -> dict:
    stream = list(stream)
    streaks = list(extract_streaks(stream))

    number_of_streaks = len(streaks)

    return {
        'sum_streak_units': sum_units(streaks),
        'sum_complete_units': sum_units(stream),
        'highest_streak': highest_item(streaks),
        'number_of_streaks': number_of_streaks,
        'number_of_breaks': len(stream) - number_of_streaks,
    }


def create_stream(tracking: iter) -> iter:
    def create(item) -> iter:
        item = list(item)

        length = len(item)
        is_streak = item[0][1]
        start = item[0][0]
        end = item[length - 1][0]

        return is_streak, length, start, end

    return map(create, group_tracking(tracking))


def group_tracking(tracking: iter) -> iter:
    for index, group in groupby(generate_streak_ids(tracking), lambda item: item[2]):
        yield group


def generate_streak_ids(tracking: iter) -> iter:
    streak_id = 0
    for index, item in enumerate(tracking):
        if index != 0 and tracking[index - 1][1] != tracking[index][1]:
            streak_id = streak_id + 1

        yield item[0], item[1], streak_id


def highest_item(stream: iter) -> tuple:
    def highest_period(item):
        return item[1]

    return max(stream, key=highest_period)


def sum_units(stream: iter) -> int:
    return sum([item[1] for item in stream])


def extract_streaks(stream: iter) -> iter:
    def is_streak(item) -> bool:
        return item[0]
    return filter(is_streak, stream)


def filter_and_sort_raw_data(habit_id: int, tracking: iter) -> iter:
    filtered_tracking = [(item['created_at']) for item in filter(lambda item: item['habit_id'] == habit_id, tracking)]
    filtered_tracking.sort()
    return filtered_tracking
