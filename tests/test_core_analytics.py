from datetime import datetime
import os
from app.core.data.db import Base, Habit, Session, User, db
import pytest
from app.core.data.enums import Periodicity
from app.core.dtos.habit import HabitRequest
from app.core.dtos.habit_entry import HabitEntryRequest
from app.core.dtos.user import UserRequest
from app.core.services.habit_entries import HabitEntriesService
from app.core.services.habits import HabitsService
from app.core.services.users import UsersService

@pytest.fixture(scope='function')
def db_session():
    """Creates a new database session for a test."""
    # Create all tables
    Base.metadata.create_all(db)
    session = Session()
    
    yield session
    
    # Teardown: Rollback any changes and drop all tables
    session.rollback()
    session.close()
    Base.metadata.drop_all(db)

async def init(db_session):
    db_session.add(User(name = "test", email = "test@test.com", apiKey = "1234", created_on_utc = datetime.now()))
    db_session.commit()

@pytest.mark.asyncio
async def test_get_habit_entries(db_session):
    # Arrange
    await init(db_session)
    
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.add(1, HabitRequest(name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY))
    habitEntriesService = HabitEntriesService(db_session)
    habit_entries = await habitEntriesService.add(1, HabitEntryRequest(habit_id = 1))
    habit_entries = await habitEntriesService.add(1, HabitEntryRequest(habit_id = 1))
    habit_entries = await habitEntriesService.add(1, HabitEntryRequest(habit_id = 1))
    # Assert
    habit = db_session.query(Habit).filter(Habit.id == habit_response.id).first()
    
    assert habit.name == "testHabit"
    assert habit.completion_criteria == "testCompletionCriteria"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.id == 1
    assert len(habit.habit_entries) == 3
