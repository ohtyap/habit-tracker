from itertools import groupby


# analyzes a stream (created by create_stream)
# and returns a dictionary of
# sum_streak_units: The complete amount of streak period units since habit creation until now(e.g. for daily: days)
# sum_complete_units: The complete amount of period units since habit creation until now(e.g. for daily: days)
# highest_streak: A tuple of the longest streak
# number_of_streaks: The number of streaks
# number_of_breaks: The number of breaks
def analyze_stream(stream: list) -> dict:
    stream = list(stream)
    if len(stream) == 0:
        return {}
    
    streaks = list(filter_streaks(stream))

    number_of_streaks = len(streaks)

    return {
        'sum_streak_units': sum_units(streaks),
        'sum_complete_units': sum_units(stream),
        'highest_streak': highest_item(streaks),
        'number_of_streaks': number_of_streaks,
        'number_of_breaks': len(stream) - number_of_streaks,
    }


# Takes a unified tracking stream in form of a list of tuples
# [('period data', <bool>), ('period data', <bool>)]
# The first entry is a string representation of the period unit (e.g. the date in form of Y-m-d in case of a
# daily habit). The second on is a bool value which indicates if the user checked off the task for this period unit
# a list of tuples are return, whereas a tuple consist of:
# - is it a positive streak (the user fulfilled the task) or a negative one
# - the length of the streak
# - the start and end of the streak as string representation of the corresponding period unit
def create_stream(tracking: iter) -> iter:
    def create(item) -> iter:
        item = list(item)

        length = len(item)
        is_streak = item[0][1]
        start = item[0][0]
        end = item[length - 1][0]

        return is_streak, length, start, end

    return map(create, group_tracking(tracking))


# Every streak (consecutively events in a row) will receive an unique id.
# period unit | fulfilled | unique_id
# 2020-12-01  | True      | 1
# 2020-12-02  | True      | 1
# 2020-12-03  | False     | 2
# 2020-12-04  | False     | 2
# 2020-12-05  | True      | 3
# 2020-12-06  | False     | 4
# Returning a generator
def generate_streak_ids(tracking: iter) -> iter:
    streak_id = 0
    for index, item in enumerate(tracking):
        if index != 0 and tracking[index - 1][1] != tracking[index][1]:
            streak_id = streak_id + 1

        yield item[0], item[1], streak_id


# Grouping based on the generated unique_id; returning a generator
def group_tracking(tracking: iter) -> iter:
    for index, group in groupby(generate_streak_ids(tracking), lambda item: item[2]):
        yield group


# Returns the streak tuple with the highest length from a streak stream
def highest_item(stream: iter) -> tuple:
    def highest_period(item):
        return item[1]

    return max(stream, key=highest_period)


# Summarize the period units from a streak stream
def sum_units(stream: iter) -> int:
    return sum([item[1] for item in stream])


# filter negative streaks; return a streak stream with only positive streaks
def filter_streaks(stream: iter) -> iter:
    def is_streak(item) -> bool:
        return item[0]
    return filter(is_streak, stream)


# Takes the raw database response from the tracking table,
# filters by a given habit_id,
# creates a list of of created_at datetime
# sort based on the datetime
def filter_and_sort_raw_data(habit_id: int, tracking: iter) -> iter:
    filtered_tracking = [(item['created_at']) for item in filter(lambda item: item['habit_id'] == habit_id, tracking)]
    filtered_tracking.sort()
    return filtered_tracking
