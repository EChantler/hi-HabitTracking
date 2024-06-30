from datetime import datetime
from pydantic import BaseModel
from app.core.data.enums import Periodicity

class HabitResponse(BaseModel):
    id: int
    name: str
    completion_criteria: str
    periodicity: Periodicity
    created_on_utc: datetime
    
class HabitRequest(BaseModel):
    name: str
    completion_criteria: str
    periodicity: Periodicity
