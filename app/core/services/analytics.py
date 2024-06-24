

from datetime import datetime
import math
from sqlalchemy import and_
from app.core.data.db import Habit, HabitEntry
from app.core.data.enums import Periodicity
from app.core.dtos.analytics import HabitSummary, HabitsSummary
from app.core.services.helpers.streaks import calculate_streak, calculate_total_planned, count_unique_completion_within_periods

class HabitAnalyticsService:
    def __init__(self, session):
        self.session = session
        
    def get_entries_for_habit(self, user_id, habit_id) -> list[HabitEntry]:
        habit = self.session.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == user_id)).first()
        entries = habit.habit_entries
        return entries
    async def get_habits_summary(self, user_id, current_date) -> HabitsSummary:
        habits: list[Habit] = self.session.query(Habit).filter(Habit.user_id == user_id).all()
        if(len(habits) == 0):
            return HabitsSummary()
        habits_summary = HabitsSummary()
        habits_summary.total_habits = len(habits)
        
        habit_summaries: list[HabitSummary] = [await self.get_habit_summary(user_id, habit.id, current_date) for habit in habits]
        
        # sort once by date created
        habits.sort(key=lambda habit: habit.created_on_utc)
        habits_summary.oldest_habit = habits[0].name 
        habits_summary.oldest_habit_created = habits[0].created_on_utc 
        habits_summary.newest_habit = habits[-1].name
        habits_summary.newest_habit_created = habits[-1].created_on_utc

        habits_summary.least_completed_habit = sorted(habit_summaries, key=lambda habit_summary: habit_summary.total_completed)[0].habit_name 
        habits_summary.most_completed_habit = sorted(habit_summaries, key=lambda habit_summary: habit_summary.total_completed, reverse=True)[0].habit_name
        # TODO make this complete success rate rather than total completed
        habits_summary.most_completed_habit_count = sorted(habit_summaries, key=lambda habit_summary: habit_summary.total_completed, reverse=True)[0].total_completed
        
        # check if all current streaks are zero
        if not all(habit_summary.current_streak == 0 for habit_summary in habit_summaries):
            habits_summary.longest_current_streak = sorted(habit_summaries, key=lambda habit_summary: habit_summary.current_streak, reverse=True)[0].habit_name
            habits_summary.longest_current_streak_count = sorted(habit_summaries, key=lambda habit_summary: habit_summary.current_streak, reverse=True)[0].current_streak
        else:
            habits_summary.longest_current_streak = "None"
            habits_summary.longest_current_streak_count = 0
            
        habits_summary.longest_streak = sorted(habit_summaries, key=lambda habit_summary: habit_summary.longest_streak, reverse=True)[0].habit_name
        habits_summary.longest_streak_count = sorted(habit_summaries, key=lambda habit_summary: habit_summary.longest_streak, reverse=True)[0].longest_streak

        habits_summary.most_successful_habit = sorted(habit_summaries, key=lambda habit_summary: habit_summary.success_rate, reverse=True)[0].habit_name
        habits_summary.most_successful_habit_success_rate = sorted(habit_summaries, key=lambda habit_summary: habit_summary.success_rate, reverse=True)[0].success_rate

        return habits_summary

    async def get_habit_summary(self, user_id, habit_id, current_date) -> HabitSummary:
        # return object with summary data such as start date, total habit entries, longest streak, max possible entries
        habit = self.session.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == user_id)).first()
        entries: list[HabitEntry] = sorted(habit.habit_entries, key=lambda entry: entry.created_on_utc)
        entry_dates: list[datetime] = [entry.created_on_utc for entry in entries]
        habit_summary = HabitSummary()
        habit_summary.total_completed = count_unique_completion_within_periods(entry_dates, habit.created_on_utc, current_date, habit.periodicity)#unique days or weeks or months depending on periodicity
        habit_summary.habit_name = habit.name
        habit_summary.habit_id = habit.id
        habit_summary.completion_criteria = habit.completion_criteria
        habit_summary.periodicity = habit.periodicity
        habit_summary.created_on_utc = habit.created_on_utc

        if(len(entries) == 0):
            return habit_summary
        # Determine last completed date
        habit_summary.last_completed_on_utc = entries[-1].created_on_utc

        # Determine longest streak based on start date and periodicity
        
        streaks = calculate_streak(entry_dates, habit.created_on_utc, current_date, habit.periodicity)
        habit_summary.longest_streak = streaks["longest_streak"]

        # Determine current streak based on last falter and periodicity
        habit_summary.current_streak = streaks["current_streak"]

        # Determine total planned based on start date and periodicity
        habit_summary.total_planned = calculate_total_planned(habit.created_on_utc, current_date ,habit.periodicity)

        habit_summary.total_incomplete = max( habit_summary.total_planned - habit_summary.total_completed, 0)

        habit_summary.success_rate = round(habit_summary.total_completed / habit_summary.total_planned, 2)



        return habit_summary
    def get_total_periods(self, start_date, end_date, periodicity):
        if(periodicity == Periodicity.DAILY):
            return (end_date - start_date).days
        if(periodicity == Periodicity.WEEKLY):
            return int(math.ceil((end_date - start_date).days / 7))
        if(periodicity == Periodicity.MONTHLY):
            years_difference = end_date.year - start_date.year
            months_difference = end_date.month - start_date.month
            return int(math.ceil(years_difference * 12 + months_difference))
        return 0
    def get_all_periods_set(self, start_date, end_date, periodicity):
        if(periodicity == Periodicity.DAILY):
            return set(range(start_date.day, end_date.day + 1))
        if(periodicity == Periodicity.WEEKLY):
            return set(range(start_date.isocalendar()[1], end_date.isocalendar()[1] + 1))
        if(periodicity == Periodicity.MONTHLY):
            return set(range(start_date.month, end_date.month + 1))
        return set()