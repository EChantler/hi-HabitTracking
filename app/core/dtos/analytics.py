from datetime import datetime
from pydantic import BaseModel

from app.core.data.enums import Periodicity
from app.core.dtos.habit import HabitResponse
class HabitSummary(BaseModel):
    habit_id: int = 0
    habit_name: str = ""
    completion_criteria: str = ""
    periodicity: Periodicity = Periodicity.DAILY
    created_on_utc: datetime = datetime.now()
    last_completed_on_utc: datetime = datetime.now()
    longest_streak: int = -1
    current_streak: int  = -1
    total_completed: int = -1
    total_incomplete: int = -1
    total_planned: int = -1


    
