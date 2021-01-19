from dataclasses import dataclass
from datetime import datetime

@dataclass
class Habit:
    id: int
    title: str
    period: str
    created_at: datetime
