from datetime import datetime
from datetime import timedelta
from math import ceil


def create_stream(start: datetime, tracking: iter):
    end = datetime.now() - timedelta(days=7)

    date_range = create_date_range(start, end)

    for created_at in tracking:
        date_range[created_at.strftime('%Y-KW%W')] = True

    return [(k, v) for k, v in date_range.items()]


def create_date_range(start: datetime, end: datetime) -> dict:
    return dict([((start + timedelta(days=x*7)).strftime('%Y-KW%W'), False) for x in range(0, ceil((end - start).days/7))])
