
from datetime import datetime
from fastapi import APIRouter, Depends
from app.api.auth import api_key_auth
from app.core.data.db import Session
from app.core.dtos.analytics import HabitSummary, HabitsSummary
from app.core.services.analytics import HabitAnalyticsService

router = APIRouter()

@router.get("/summary/{habit_id}", description="Get summary for a specific habit for signed in user")
async def get_summary(habit_id: int, user_id: int = Depends(api_key_auth)) -> HabitSummary:
    session = Session()
    analytics_service = HabitAnalyticsService(session)
    return await analytics_service.get_habit_summary(user_id, habit_id, datetime.now())

@router.get("/summary", description="Get summary of all habits for signed in user")
async def get_summary(user_id: int = Depends(api_key_auth)) -> HabitsSummary:
    session = Session()
    analytics_service = HabitAnalyticsService(session)
    return await analytics_service.get_habits_summary(user_id, datetime.now())
