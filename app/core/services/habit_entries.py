from datetime import datetime
from sqlalchemy import and_
from app.core.data.db import Habit, HabitEntry
from app.core.dtos.habit import HabitRequest, HabitResponse
from app.core.dtos.habit_entry import HabitEntryRequest, HabitEntryResponse
class HabitEntriesService:
    def __init__(self, session):
        self.session = session

    async def get_by_habit(self, user_id, habit_id) -> list[HabitEntryResponse]:
        habit_entries = self.session.query(HabitEntry).filter(and_(HabitEntry.user_id == user_id, HabitEntry.habit_id == habit_id)).all()
        return [HabitEntryResponse(id = entry.id, user_id=entry.user_id, habit_id=entry.habit_id, created_on_utc=entry.created_on_utc, modified_on_utc=entry.modified_on_utc) for entry in habit_entries]

    async def get_by_user(self, user_id) -> list[HabitEntryResponse]:
        habit_entries = self.session.query(HabitEntry).filter(HabitEntry.user_id == user_id).all()
        return [HabitEntryResponse(id = entry.id, user_id=entry.user_id, habit_id=entry.habit_id, created_on_utc=entry.created_on_utc, modified_on_utc=entry.modified_on_utc) for entry in habit_entries]
    
    async def add(self, user_id, request:HabitEntryRequest):
        habit_entry = HabitEntry(
            user_id = user_id,
            habit_id = request.habit_id,
            created_on_utc = datetime.now()
        )

        # Add the Habit object to the session
        self.session.add(habit_entry)
        self.session.commit()
        return HabitEntryResponse(id = habit_entry.id, user_id=habit_entry.user_id, 
                         habit_id=habit_entry.habit_id, 
                         created_on_utc=habit_entry.created_on_utc, modified_on_utc=None)
    
    async def delete(self, user_id, habit_id, habit_entry_id):
        habit_entry = self.session.query(HabitEntry).filter(and_(HabitEntry.user_id == user_id, HabitEntry.habit_id == habit_id, HabitEntry.id == habit_entry_id)).first()
        if not habit_entry:
            return False
        self.session.delete(habit_entry)
        self.session.commit()
        return True
    