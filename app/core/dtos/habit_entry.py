from datetime import datetime
from pydantic import BaseModel


class HabitEntryRequest(BaseModel):
    habit_id: int


class HabitEntryResponse(BaseModel):
    user_id: int
    habit_id: int
    created_on_utc: datetime
    modified_on_utc: datetime|None



    