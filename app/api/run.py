

from app.core.data.db import Session, User

from app.core.data.db import Base, db
from app.core.dtos.user import UserRequest
from app.core.services.users import UsersService
import uvicorn
import asyncio
from fastapi import FastAPI, Header
from . import habits, users, habit_entries, analytics

# init the db
Base.metadata.create_all(db)

# Create the FastAPI app
app = FastAPI()

# Include the routers
app.include_router(users.router, tags=["Users"], prefix="/users")
app.include_router(habits.router, tags=["Habits"], prefix="/habits")
app.include_router(habit_entries.router, tags=["Habit Entries"], prefix="/habit-entries")
app.include_router(analytics.router, tags=["Habit Analytics"], prefix="/habit-analytics")

# Create a session object
session = Session()

# Seed the database
async def init():
    us = UsersService(session)
    if(session.query(User).count() == 0):
        await us.add_user(UserRequest(name="test", email="test@test.com", apiKey="testApiKey"))

# Run the FastAPI app
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    uvicorn.run(app, host="0.0.0.0", port=8000)