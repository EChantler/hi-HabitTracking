
from fastapi import APIRouter
from app.core.data.db import Session
from app.core.dtos.habit_entry import HabitEntryRequest, HabitEntryResponse
from app.core.services.habit_entries import HabitEntriesService

router = APIRouter()

@router.get("", description = "Get all habit entries for signed in user")
async def get_habits_entries() -> list[HabitEntryResponse]:
    session = Session()
    user_id = 1

    habit_entries_service = HabitEntriesService(session)
    return await habit_entries_service.get_by_user(user_id)

@router.get("/habit/{habit_id}")
async def get_habit(habit_id: int) -> list[HabitEntryResponse]:
    session = Session()
    user_id = 1
    habit_entries_service = HabitEntriesService(session)
    return await habit_entries_service.get_by_habit(user_id, habit_id)

@router.delete("{habit_entry_id}")
async def delete_habit(habit_entry_id: int) -> bool:
    session = Session()
    user_id = 1
    habit_entries_service = HabitEntriesService(session)
    return await habit_entries_service.delete(user_id, habit_entry_id)

@router.post("")
async def add_habit(request: HabitEntryRequest) -> HabitEntryResponse:
    session = Session()
    user_id = 1
    habit_entries_service = HabitEntriesService(session)
    return await habit_entries_service.add(user_id, request)

