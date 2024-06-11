from datetime import datetime
from pydantic import BaseModel
class HabitResponse(BaseModel):
    id: int
    name: str
    completion_criteria: str
    periodicity: int
    created_on_utc: datetime
    
class HabitRequest(BaseModel):
    name: str
    completion_criteria: str
    periodicity: int
