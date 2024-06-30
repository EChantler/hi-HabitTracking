from fastapi import APIRouter, Depends
from app.api.auth import api_key_auth
from app.core.data.db import Session
from app.core.dtos.habit_entry import HabitEntryRequest, HabitEntryResponse
from app.core.services.habit_entries import HabitEntriesService

router = APIRouter()

@router.get("", description = "Get all habit entries for signed in user")
async def get_habits_entries(user_id: int = Depends(api_key_auth)) -> list[HabitEntryResponse]:
    with Session() as session:
        habit_entries_service = HabitEntriesService(session)
        return await habit_entries_service.get_by_user(user_id)

@router.get("/habit/{habit_id}", description="Get habit-entries for a specific habit for signed in user")
async def get_habit(habit_id: int, user_id: int = Depends(api_key_auth)) -> list[HabitEntryResponse]:
    with Session() as session:
        habit_entries_service = HabitEntriesService(session)
        return await habit_entries_service.get_by_habit(user_id, habit_id)

@router.delete("{habit_entry_id}", description="Delete a specific habit entry for signed in user")
async def delete_habit(habit_entry_id: int, user_id: int = Depends(api_key_auth)) -> bool:
    with Session() as session:
        habit_entries_service = HabitEntriesService(session)
        return await habit_entries_service.delete(user_id, habit_entry_id)

@router.post("", description="Add a new habit entry for signed in user")
async def add_habit(request: HabitEntryRequest, user_id: int = Depends(api_key_auth)) -> HabitEntryResponse:
    with Session() as session:
        habit_entries_service = HabitEntriesService(session)
        return await habit_entries_service.add(user_id, request)

