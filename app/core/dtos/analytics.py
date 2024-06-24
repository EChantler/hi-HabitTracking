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
    success_rate: float = -1.0
class HabitsSummary(BaseModel):
    total_habits: int = -1
    longest_streak: str = ""
    longest_streak_count: int = -1
    longest_current_streak: str = ""
    longest_current_streak_count: int = -1
    oldest_habit: str = ""
    oldest_habit_created: datetime = datetime.now()
    newest_habit: str = ""
    newest_habit_created: datetime = datetime.now()
    most_completed_habit: str = ""
    most_completed_habit_count: int = -1
    least_completed_habit: str = ""
    most_successful_habit: str = ""
    most_successful_habit_success_rate: float = -1.0





    
