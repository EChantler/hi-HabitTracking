
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
    Base.metadata.create_all(db)
    session = db_session#Session()
    # Act
    usersService = UsersService(session)
    user = await usersService.add_user(user_dto)
    # Assert
    db_user = session.query(User).first()
    
    assert db_user.name == user_dto.name
    assert db_user.email == user_dto.email
    
    
   