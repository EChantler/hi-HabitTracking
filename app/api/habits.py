from fastapi import APIRouter, Depends
from app.api.auth import api_key_auth
from app.core.data.enums import Periodicity
from app.core.dtos.habit import HabitRequest, HabitResponse
from app.core.data.db import Session
from app.core.services.habits import HabitsService

router = APIRouter()

@router.get("", description="Get all habits for signed in user")
async def get_habits(user_id: int = Depends(api_key_auth)) -> list[HabitResponse]:
    with Session() as session:
        habits_service = HabitsService(session)
        return await habits_service.get_all(user_id)
    
@router.get("/periodicity/{periodicity}", description="Get all habits for signed in user by periodicity")
async def get_habits_by_periodicity(periodicity: Periodicity, user_id: int = Depends(api_key_auth)) -> list[HabitResponse]:
    with Session() as session:
        habits_service = HabitsService(session)
        return await habits_service.get_all_by_periodicity(user_id, periodicity)
    
@router.get("/{habit_id}", description="Get a specific habit for signed in user")
async def get_habit(habit_id: int, user_id: int = Depends(api_key_auth)) -> HabitResponse:
    with Session() as session:
        habits_service = HabitsService(session)
        return await habits_service.get(user_id, habit_id)

@router.post("", description="Add a new habit for signed in user")
async def add_habit(request: HabitRequest, user_id: int = Depends(api_key_auth)) -> HabitResponse:
    with Session() as session:
        habits_service = HabitsService(session)
        return await habits_service.add(user_id, request)

@router.put("/{habit_id}", description="Update a specific habit for signed in user")
async def update_habit(habit_id: int, habit_dto: HabitRequest, user_id: int = Depends(api_key_auth)) -> bool:
    with Session() as session:
        habits_service = HabitsService(session)
        return await habits_service.update(user_id, habit_id, habit_dto)

@router.delete("/{habit_id}", description="Delete a specific habit for signed in user")
async def delete_habit(habit_id: int, user_id: int = Depends(api_key_auth)) -> bool:
    with Session() as session:
        habits_service = HabitsService(session)
        return await habits_service.delete(user_id, habit_id)