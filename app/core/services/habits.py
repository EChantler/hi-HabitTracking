from datetime import datetime

from sqlalchemy import and_
from app.core.data.db import Habit
from app.core.dtos.habit import HabitRequest, HabitResponse
class HabitsService:
    def __init__(self, session):
        self.session = session

    async def get_all(self, user_id) -> list[HabitResponse]:
        '''Get all habits for signed in user'''
        habits = self.session.query(Habit).filter(Habit.user_id == user_id).all()
        return [HabitResponse(id=habit.id, name=habit.name, completion_criteria=habit.completion_criteria, periodicity=habit.periodicity, created_on_utc=habit.created_on_utc) for habit in habits]
    async def get_all_by_periodicity(self, user_id, periodicity) -> list[HabitResponse]:
        '''Get all habits by periodicity for signed in user'''
        habits = self.session.query(Habit).filter(and_(Habit.periodicity == periodicity, Habit.user_id == user_id)).all()
        return [HabitResponse(id=habit.id, name=habit.name, completion_criteria=habit.completion_criteria, periodicity=habit.periodicity, created_on_utc=habit.created_on_utc) for habit in habits]
    
    async def get(self, user_id, habit_id):
        '''Get a specific habit for signed in user'''
        habit = self.session.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == user_id)).first()
        return habit
    
    async def add(self, user_id, request:HabitRequest):
        '''Add a new habit for signed in user'''
        habit = Habit( 
            user_id = user_id,
            name=request.name,
            completion_criteria=request.completion_criteria,
            periodicity=request.periodicity, 
            created_on_utc = datetime.now()
        )

        # Add the Habit object to the session and commit the changes to the database
        self.session.add(habit)
        self.session.commit()
        
        return HabitResponse(name=habit.name, 
                             completion_criteria=habit.completion_criteria, 
                             periodicity=habit.periodicity, 
                             created_on_utc=habit.created_on_utc, id = habit.id)
    
    async def update(self, user_id, habit_id, habit_dto:HabitResponse):
        '''Update a specific habit for signed in user, returns True if successful, False otherwise'''
        habit = self.session.query(Habit).filter(Habit.id == habit_id and Habit.user_id == user_id).first()
        if not habit:
            return False
        habit.name = habit_dto.name
        habit.completion_criteria = habit_dto.completion_criteria
        habit.periodicity = habit_dto.periodicity
        habit.modified_on_utc = datetime.now()
        self.session.commit()
        return True
    
    async def delete(self, user_id, habit_id):
        '''Delete a specific habit for signed in user, returns True if successful, False otherwise'''
        habit = self.session.query(Habit).filter(Habit.id == habit_id and Habit.user_id == user_id).first()
        if not habit:
            return False
        self.session.delete(habit)
        self.session.commit()
        return True