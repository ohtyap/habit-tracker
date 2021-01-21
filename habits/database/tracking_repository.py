from habits.database.repository import Repository
from habits.database.tracking import Tracking
from datetime import datetime


class TrackingRepository(Repository):
    _table = 'tracking'
    _entity = Tracking

    def delete_by_habit_id(self, habit_id: int):
        self._database.delete(
            'DELETE FROM ' + self.table + ' WHERE habit_id=?',
            [habit_id]
        )

        self.clear()

    def create_new_tracking_entry(self, habit_id: int):
        return self.create({
            'habit_id': habit_id,
            'created_at': datetime.now(),
        })
