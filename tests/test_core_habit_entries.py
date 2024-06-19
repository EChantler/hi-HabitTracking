from datetime import datetime
import os
from app.core.data.db import Base, Habit, HabitEntry, Session, User, db
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
    db_session.add(Habit(user_id = 1, name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY, created_on_utc = datetime.now()))
    db_session.commit()

@pytest.mark.asyncio
async def test_add_habit_entry(db_session):
    # Arrange
    await init(db_session)
    # Act
    habitsEntriesService = HabitEntriesService(db_session)
    habitEntryResponse = await habitsEntriesService.add(1, HabitEntryRequest(habit_id = 1))

    # Assert
    habitEntry = db_session.query(HabitEntry).filter(HabitEntry.id == habitEntryResponse.id).first()
    
    assert habitEntry.id == habitEntryResponse.id
    assert habitEntry.user_id == habitEntryResponse.user_id
    assert habitEntry.habit_id == habitEntryResponse.habit_id

@pytest.mark.asyncio
async def test_get_habit_entries_by_user(db_session):
    # Arrange
    await init(db_session)
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime.now()))
    # Act
    habitsEntriesService = HabitEntriesService(db_session)
    habitEntryResponse = await habitsEntriesService.get_by_user(1)

    # Assert
    assert len(habitEntryResponse) == 1

@pytest.mark.asyncio
async def test_get_habit_entries_by_habit(db_session):
    # Arrange
    await init(db_session)
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime.now()))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime.now()))
    db_session.commit()
    # Act
    habitsEntriesService = HabitEntriesService(db_session)
    habitEntryResponse = await habitsEntriesService.get_by_habit(1, 1)

    # Assert
    assert len(habitEntryResponse) == 2

@pytest.mark.asyncio
async def test_delete_habit_entry(db_session):
    # Arrange
    await init(db_session)
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime.now()))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime.now()))
    db_session.commit()
    # Act
    habitsEntriesService = HabitEntriesService(db_session)
    habitEntryResponse = await habitsEntriesService.delete(1, 1, 1)

    # Assert
    habitEntries = db_session.query(HabitEntry).filter(HabitEntry.habit_id == 1).all()

    assert habitEntryResponse == True
    assert len(habitEntries) == 1 # one left after delete

@pytest.mark.asyncio
async def test_delete_habit_habit_entry_not_found(db_session):
    # Arrange
    await init(db_session)
    # Act
    habitsEntriesService = HabitEntriesService(db_session)
    habitEntryResponse = await habitsEntriesService.delete(1, 1, 1)

    # Assert
    assert habitEntryResponse == False
    