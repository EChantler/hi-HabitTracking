
from datetime import datetime
import os
from app.core.data.db import Base, Session, User, db
import pytest
from app.core.dtos.user import UserRequest
from app.core.services.users import UsersService

os.environ["PYTEST_CURRENT_TEST"] = "pytest"

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

@pytest.mark.asyncio
async def test_add_user(db_session):
    # Arrange
    user_dto = UserRequest(name="test2", email="test2@test.com", apiKey="testApiKey2")
    
    # Act
    usersService = UsersService(db_session)
    user = await usersService.add_user(user_dto)
    # Assert
    db_user = db_session.query(User).first()
    
    assert db_user.name == user_dto.name
    assert db_user.email == user_dto.email
    
@pytest.mark.asyncio
async def test_get_user(db_session):
    # Arrange
    db_user = db_session.add(User(name = "testUser", email = "test3@test.com", apiKey = "1234", created_on_utc = datetime.now()))
    db_session.commit()

    # Act
    usersService = UsersService(db_session)
    user = await usersService.get(1)

    # Assert
    assert user.name == "testUser"
    assert user.email == "test3@test.com"
    assert user.api_key == "1234"

@pytest.mark.asyncio
async def test_get_user_id_with_api_key(db_session):
     # Arrange
    db_user = db_session.add(User(name = "testUser", email = "test3@test.com", apiKey = "1234", created_on_utc = datetime.now()))
    db_session.commit()

    # Act
    usersService = UsersService(db_session)
    user_id = await usersService.get_with_api_key("1234")

    # Assert
    assert user_id == 1

    
   