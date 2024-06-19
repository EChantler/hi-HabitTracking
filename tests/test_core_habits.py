from datetime import datetime
import os
from app.core.data.db import Base, Habit, Session, User, db
import pytest
from app.core.data.enums import Periodicity
from app.core.dtos.habit import HabitRequest
from app.core.dtos.user import UserRequest
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
async def test_add_habit(db_session):
    # Arrange
    await init(db_session)
    
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.add(1, HabitRequest(name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY))
    
    # Assert
    habit = db_session.query(Habit).filter(Habit.id == habit_response.id).first()
    
    assert habit.name == "testHabit"
    assert habit.completion_criteria == "testCompletionCriteria"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.id == 1

@pytest.mark.asyncio
async def test_add_habit_user_does_not_exist(db_session):
    # Arrange

    # Act
    habitsService = HabitsService(db_session)
    with pytest.raises(Exception):
        habit_response = await habitsService.add(1, HabitRequest(name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY))
    
    

@pytest.mark.asyncio
async def test_get_habit(db_session):
    # Arrange
    await init(db_session)
    db_session.add(Habit(user_id = 1, name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY, created_on_utc = datetime.now()))
    db_session.commit()
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.get(1, 1)

    # Assert
    habit = db_session.query(Habit).filter(Habit.id == habit_response.id).first()
    
    assert habit.name == "testHabit"
    assert habit.completion_criteria == "testCompletionCriteria"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.id == 1

@pytest.mark.asyncio
async def test_get_habit_not_found(db_session):
    # Arrange
    await init(db_session)
    
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.get(1, 1)

    # Assert
    assert habit_response == None    
    

@pytest.mark.asyncio
async def test_update_habit_not_found(db_session):
    # Arrange
    await init(db_session)
    
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.update(1, 1, HabitRequest(name = "testHabit2", completion_criteria = "testCompletionCriteria2", periodicity = Periodicity.WEEKLY))

    # Assert
    habit = db_session.query(Habit).filter(Habit.id == 1).first()
    
    assert habit_response == False
   

@pytest.mark.asyncio
async def test_delete_habit(db_session):
    # Arrange
    await init(db_session)
    db_session.add(Habit(user_id = 1, name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.WEEKLY, created_on_utc = datetime.now()))
    db_session.commit()
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.delete(1, 1)

    # Assert
    habit = db_session.query(Habit).filter(Habit.id == 1).first()
    
    assert habit_response == True
    assert habit == None

@pytest.mark.asyncio
async def test_delete_habit_not_found(db_session):
    # Arrange
    await init(db_session)
    
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.delete(1, 1)

    # Assert
    assert habit_response == False

@pytest.mark.asyncio
async def test_get_all_habit(db_session):
    # Arrange
    await init(db_session)
    db_session.add(Habit(user_id = 1, name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.WEEKLY, created_on_utc = datetime.now()))
    db_session.add(Habit(user_id = 1, name = "testHabit2", completion_criteria = "testCompletionCriteria2", periodicity = Periodicity.DAILY, created_on_utc = datetime.now()))
    db_session.commit()
    
    # Act
    habitsService = HabitsService(db_session)
    habit_response = await habitsService.get_all(1)

    # Assert
    habits = db_session.query(Habit).filter(Habit.user_id == 1)
    
    assert habits.count() == 2