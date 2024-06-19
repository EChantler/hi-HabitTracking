

from sqlalchemy import and_
from app.core.data.db import Habit, HabitEntry
from app.core.dtos.analytics import HabitSummary
from app.core.services.helpers.streaks import calculate_total_planned

class HabitAnalyticsService:
    def __init__(self, session):
        self.session = session
    def get_entries_for_habit(self, user_id, habit_id):
        habit = self.session.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == user_id)).first()
        entries = habit.entries
        return entries
    def get_habit_summary(self, user_id, habit_id):
        # return object with summary data such as start date, total habit entries, longest streak, max possible entries
        habit_summary = HabitSummary()
        habit = self.session.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == user_id)).first()
        entries = sorted(habit.entries, key=lambda entry: entry.created_on_utc)
        habit_summary.total_completed = len(entries)
        habit_summary.habit_name = habit.name
        habit_summary.habit_id = habit.id
        habit_summary.completion_criteria = habit.completion_criteria
        habit_summary.periodicity = habit.periodicity
        habit_summary.created_on_utc = habit.created_on_utc
        habit_summary.last_completed_on_utc = entries[-1].created_on_utc

        # Determine longest streak based on start date and periodicity
        habit_summary.longest_streak = 0
    
        # Determine current streak based on last falter and periodicity
        habit_summary.current_streak = 0

        # Determine total planned based on start date and periodicity
        habit_summary.total_planned = calculate_total_planned(habit.created_on_utc, habit.periodicity)

        habit_summary.total_incomplete = habit_summary.total_planned - habit_summary.total_completed


        return habit_summary
        