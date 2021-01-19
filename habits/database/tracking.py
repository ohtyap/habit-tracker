from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tracking:
    id: int
    habit_id: int
    created_at: datetime
