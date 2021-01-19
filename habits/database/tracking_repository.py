from habits.database.repository import Repository
from habits.database.tracking import Tracking


class TrackingRepository(Repository):
    _table = 'tracking'
    _entity = Tracking
