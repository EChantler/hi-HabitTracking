from datetime import datetime
from pydantic import BaseModel

from app.core.data.enums import Periodicity
class HabitSummary(BaseModel):
    habit_id: int
    habit_name: str
    completion_criteria: str
    periodicity: Periodicity
    created_on_utc: datetime
    last_completed_on_utc: datetime
    longest_streak: int
    current_streak: int
    total_completed: int
    total_incomplete: int
    total_planned: int
    
