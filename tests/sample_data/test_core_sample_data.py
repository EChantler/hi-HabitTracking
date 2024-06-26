

from datetime import datetime
import os
from app.core.data.db import Base, Session, User, db, db_path
import pytest
from app.core.dtos.user import UserRequest, UserResponse
from app.core.services.analytics import HabitAnalyticsService
from app.core.services.users import UsersService
from tests.sample_data.create_sample_db import create_habit_entries, create_habits, create_users
import os
# Run with Run with SQLALCHEMY_DATABASE_URL=sqlite:///:memory: python -m tests.sample_data.create_sample_db
# SQLALCHEMY_DATABASE_URL=sqlite:///tests/sample_data/sample_db.db python -m pytest tests/sample_data
@pytest.fixture(scope='class')
def db_session():
    """Creates a new database session for a test."""
    # Create all tables
    Base.metadata.create_all(db)
    session = Session()
    if session.query(User).count() == 0:
        create_users(session)
        create_habits(session)
        create_habit_entries(session)

    yield session
    
    # Teardown: Rollback any changes and drop all tables
    session.rollback()
    session.close()
    Base.metadata.drop_all(db)


@pytest.mark.asyncio
async def test_get_habit_summary_user_1_habit_1(db_session):
    # Arrange
      
    # Act
    habitAnalyticsService = HabitAnalyticsService(db_session)
    habit_summary = await habitAnalyticsService.get_habit_summary(1, 1, datetime(2024,4,30))

    # Assert
    assert habit_summary.created_on_utc == datetime(2024,3,31)
    assert habit_summary.last_completed_on_utc == datetime(2024,4,30)
    assert habit_summary.longest_streak == 7
    assert habit_summary.current_streak == 6
    assert habit_summary.total_completed == 19
    assert habit_summary.total_incomplete == 12
    assert habit_summary.total_planned == 31
    assert habit_summary.success_rate == round(19/31.0,2)

@pytest.mark.asyncio
async def test_get_habits_summary_user_1(db_session):
    # Arrange
      
    # Act
    habitAnalyticsService = HabitAnalyticsService(db_session)
    habits_summary = await habitAnalyticsService.get_habits_summary(1, datetime(2024,4,30))

    # Assert
    assert habits_summary.total_habits == 5
    assert habits_summary.oldest_habit == "yoga"
    assert habits_summary.newest_habit == "gratitude drawing"
    assert habits_summary.newest_habit_created == datetime(2024,4,1)
    assert habits_summary.least_completed_habit == "monthly planning" # change this to worst performing habit
    assert habits_summary.most_completed_habit == "gratitude drawing"
    assert habits_summary.most_completed_habit_count == 30
    assert habits_summary.longest_current_streak == "gratitude drawing"
    assert habits_summary.longest_current_streak_count == 30
    assert habits_summary.most_successful_habit == "gratitude drawing"
    assert habits_summary.oldest_habit_created == datetime(2024,3,30)
    assert habits_summary.most_successful_habit_success_rate == 1
    

    


