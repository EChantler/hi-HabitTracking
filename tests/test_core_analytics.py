import asyncio
from datetime import datetime
import os
from app.core.data.db import Base, Habit, HabitEntry, Session, User, db
import pytest
from app.core.data.enums import Periodicity
from app.core.dtos.habit import HabitRequest
from app.core.dtos.habit_entry import HabitEntryRequest
from app.core.dtos.user import UserRequest
from app.core.services.analytics import HabitAnalyticsService
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
    await habitEntriesService.add(1, HabitEntryRequest(habit_id = 1))
    await habitEntriesService.add(1, HabitEntryRequest(habit_id = 1))
    await habitEntriesService.add(1, HabitEntryRequest(habit_id = 1))
    
    # Assert
    habit = db_session.query(Habit).filter(Habit.id == habit_response.id).first()
    
    assert habit.name == "testHabit"
    assert habit.completion_criteria == "testCompletionCriteria"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.id == 1
    assert len(habit.habit_entries) == 3

@pytest.mark.asyncio
async def test_get_habit_summary(db_session):
    # Arrange
    await init(db_session)
    
    db_session.add(Habit(user_id = 1, name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY, created_on_utc = datetime(2024,1,1)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,1)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,2,22)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,3)))
    # Act
    habitAnalyticsService = HabitAnalyticsService(db_session)
    habit_summary = await habitAnalyticsService.get_habit_summary(1, 1, datetime(2024,1,3))
    # Assert
    
    assert habit_summary.habit_id == 1
    assert habit_summary.habit_name == "testHabit"
    assert habit_summary.completion_criteria == "testCompletionCriteria"
    assert habit_summary.periodicity == Periodicity.DAILY
    assert habit_summary.created_on_utc == datetime(2024,1,1)
    assert habit_summary.last_completed_on_utc == datetime(2024,1,3)
    assert habit_summary.longest_streak == 3
    assert habit_summary.current_streak == 3
    assert habit_summary.total_completed == 3
    assert habit_summary.total_incomplete == 0
    assert habit_summary.total_planned == 3

@pytest.mark.asyncio
async def test_get_habits_summary(db_session):
    # Arrange
    await init(db_session)
    
    db_session.add(Habit(user_id = 1, name = "testHabit", completion_criteria = "testCompletionCriteria", periodicity = Periodicity.DAILY, created_on_utc = datetime(2024,1,1)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,1)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,2)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,3)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,1,4)))
    
    db_session.add(Habit(user_id = 1, name = "testHabit2", completion_criteria = "testCompletionCriteria2", periodicity = Periodicity.WEEKLY, created_on_utc = datetime(2023,1,9)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,1,10)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,1,11)))
    db_session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,1,13)))

    # Act
    habitAnalyticsService = HabitAnalyticsService(db_session)
    habits_summary = await habitAnalyticsService.get_habits_summary(1,datetime(2024,1,13) )
    # Assert
    
    assert habits_summary.total_habits == 2
    assert habits_summary.oldest_habit == "testHabit2"
    assert habits_summary.oldest_habit_created == datetime(2023,1,9)
    assert habits_summary.newest_habit == "testHabit"
    assert habits_summary.newest_habit_created == datetime(2024,1,1)
    assert habits_summary.least_completed_habit == "testHabit2"
    assert habits_summary.most_completed_habit == "testHabit"
    assert habits_summary.most_completed_habit_count == 4
    assert habits_summary.longest_current_streak == "testHabit2"
    assert habits_summary.longest_current_streak_count == 1
    assert habits_summary.longest_streak == "testHabit"
    assert habits_summary.longest_streak_count == 4
    
if __name__ == "__main__":
    async def main():
        Base.metadata.create_all(db)
        session = Session()
        await test_get_habit_summary(session)
    
    asyncio.run(main())
