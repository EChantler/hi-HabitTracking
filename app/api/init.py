
# from fastapi import FastAPI, Header
# from . import habits, users, habit_entries, analytics

# app = FastAPI()
# app.include_router(users.router, tags=["Users"], prefix="/users")
# app.include_router(habits.router, tags=["Habits"], prefix="/habits")
# app.include_router(habit_entries.router, tags=["Habit Entries"], prefix="/habit-entries")
# app.include_router(analytics.router, tags=["Habit Analytics"], prefix="/habit-analytics")







# @app.get("/users/header-sample")
# def header_sample(apiKey: Annotated[str | None, Header()] = None):
#     return {"ApiKey": apiKey}

# @app.get("/users/register")
# def register():
#     return{success: True}

# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None






# @app.post("/habits", response_model=None)
# async def create_habit(session: Session, habit: Habit) -> Any:
#     habits_service = HabitsService(session)
#     return await habits_service.add_habit(habit)