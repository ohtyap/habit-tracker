from datetime import datetime
from datetime import timedelta


# creates a unified tracking stream [('date', <bool>)] on a daily base.
def create_stream(start: datetime, tracking: iter):
    end = datetime.now() - timedelta(days=1)

    date_range = create_date_range(start, end)

    for created_at in tracking:
        date_range[created_at.strftime('%Y-%m-%d')] = True

    return [(k, v) for k, v in date_range.items()]


# creates an initial range of days
def create_date_range(start: datetime, end: datetime) -> dict:
    return dict([((start + timedelta(days=x)).strftime('%Y-%m-%d'), False) for x in range(0, (end - start).days)])
