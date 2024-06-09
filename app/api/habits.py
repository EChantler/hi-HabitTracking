
from fastapi import APIRouter
from app.core.dtos.habit import HabitRequest, HabitResponse
from app.core.data.db import Session
from app.core.services.habits import HabitsService

router = APIRouter()

@router.get("")
async def get_habits() -> list[HabitResponse]:
    session = Session()
    user_id = 1

    habits_service = HabitsService(session)
    return await habits_service.get_all(user_id)

@router.get("/{habit_id}")
async def get_habit(habit_id: int) -> HabitResponse:
    session = Session()
    user_id = 1
    habits_service = HabitsService(session)
    return await habits_service.get(user_id, habit_id)

@router.post("")
async def add_habit(request: HabitRequest) -> HabitResponse:
    session = Session()
    user_id = 1
    habits_service = HabitsService(session)
    return await habits_service.add(user_id, request)

@router.put("/{habit_id}")
async def update_habit(habit_id: int, habit_dto: HabitRequest) -> bool:
    session = Session()
    user_id = 1
    habits_service = HabitsService(session)
    return await habits_service.update(user_id, habit_id, habit_dto)

@router.delete("/{habit_id}")
async def delete_habit(habit_id: int) -> bool:
    session = Session()
    user_id = 1
    habits_service = HabitsService(session)
    return await habits_service.delete(user_id, habit_id)