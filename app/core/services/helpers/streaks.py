
from datetime import datetime, timedelta
from calendar import monthrange
from app.core.data.enums import Periodicity
import math
def calculate_total_planned(start_date: datetime, end_date: datetime, periodicity: Periodicity) -> int:
    '''Calculates the total planned entries for a given date range, where a planned entry is defined as a day or week or month after the start_date up to the end_date depending on the periodicity'''
    if periodicity == Periodicity.DAILY:
        return (end_date - start_date).days +1
    if periodicity == Periodicity.WEEKLY:
        return int(math.ceil((end_date - start_date).days / 7))
    if periodicity == Periodicity.MONTHLY:
        years_difference = end_date.year - start_date.year
        months_difference = end_date.month - start_date.month
        return int(math.ceil(years_difference * 12 + months_difference))
    return 0

def calculate_streak(entry_dates: list[datetime],start_date: datetime, end_date: datetime, periodicity: Periodicity) -> int:
    '''Calculates the the current and longest streak based on step-through logic for the date range and returns a json object in this format: {"longest_streak": longest_streak, "current_streak": current_streak}'''
    entry_dates = [dt.replace(hour=0, minute=0, second=0) for dt in entry_dates]
    longest_streak = 0
    current_streak = 0
    if periodicity == Periodicity.DAILY:
        dates = [(start_date + timedelta(days=i)) for i in range((end_date - start_date).days + 1)]
        for date in dates:
            # print(f"{date.strftime('%d-%m-%Y')}: {date in entry_dates}, current streak: {current_streak+1}, longest streak: {longest_streak}")
            if date in entry_dates:
                current_streak += 1
            else:
                current_streak = 0
            if current_streak > longest_streak:
                longest_streak = current_streak

    if periodicity == Periodicity.WEEKLY:

        # Get the start of the week
        start_date_iso = datetime.isocalendar(start_date)
        cursor_date = datetime.fromisocalendar(start_date_iso[0], start_date_iso[1], 1)
        
        # Step through with our cusrsor until we go past the end_date
        while cursor_date <= end_date:

            # Calculate the end of the week
            next_cursor_date = cursor_date + timedelta(days=6)

            # Check if the entry is in the current week
            entry = any(cursor_date<= date<= next_cursor_date for date in entry_dates)
            # print(f"Week({cursor_date.strftime('%d-%m-%Y')}-> {next_cursor_date.strftime('%d-%m-%Y')}): {entry}, current streak: {current_streak+1}, longest streak: {longest_streak}")
            
            if(entry):
                current_streak += 1
            else:
                if current_streak > longest_streak:
                    longest_streak = current_streak
                current_streak = 0

            # Update our cursor to start of the next week
            cursor_date = next_cursor_date +timedelta(days=1)

    if periodicity == Periodicity.MONTHLY:
        # Get the start of the month
        month_start_cursor_date = start_date - timedelta(days=start_date.day - 1, hours=start_date.hour, minutes=start_date.minute, seconds=start_date.second)
        
        # Get the end of the month for the end date
        end_date_month_end = end_date - timedelta(days=end_date.day - 1, hours=end_date.hour, minutes=end_date.minute, seconds=end_date.second) + timedelta(days= monthrange(month_start_cursor_date.year, month_start_cursor_date.month)[1])
        
        # Step through with our cusrsor until we go past the end_date
        while month_start_cursor_date < end_date_month_end:

            # Calculate the end of the current month we are looking at
            next_cursor_date = month_start_cursor_date + timedelta(days= monthrange(month_start_cursor_date.year, month_start_cursor_date.month)[1]-1)
            
            # Check if the entry is in the current month
            entry = any(month_start_cursor_date<= date<= next_cursor_date for date in entry_dates)
            # print(f"Month({month_start_cursor_date.strftime('%d-%m-%Y')}-> {next_cursor_date.strftime('%d-%m-%Y')}): {entry}, current streak: {current_streak+1}, longest streak: {longest_streak}")
            
            if(entry):
                current_streak += 1
            else:
                if current_streak > longest_streak:
                    longest_streak = current_streak
                current_streak = 0

            # Update our cursor to start of the next month
            month_start_cursor_date = next_cursor_date+ timedelta(days=1)
    return {"longest_streak": longest_streak, "current_streak": current_streak}

def count_unique_completion_within_periods(entry_dates: list[datetime],start_date: datetime, end_date: datetime, periodicity: Periodicity) -> int:
    '''Calculate the number of unique completions within a date range'''
    count = 0
    entry_dates = [dt.replace(hour=0, minute=0, second=0, microsecond=0) for dt in entry_dates]
    if periodicity == Periodicity.DAILY:
        dates = [(start_date + timedelta(days=i)) for i in range((end_date - start_date).days + 1)]
        for date in dates:
            if date in entry_dates:
                count += 1
    if periodicity == Periodicity.WEEKLY:
        start_date_iso = datetime.isocalendar(start_date)
        cursor_date = datetime.fromisocalendar(start_date_iso[0], start_date_iso[1], 1)
        while cursor_date <= end_date:

            next_cursor_date = cursor_date + timedelta(days=6)
            entry = any(cursor_date<= date<= next_cursor_date for date in entry_dates)
            if(entry):
                count += 1
            cursor_date = next_cursor_date +timedelta(days=1)
    if periodicity == Periodicity.MONTHLY:
        month_start_cursor_date = start_date - timedelta(days=start_date.day - 1, hours=start_date.hour, minutes=start_date.minute, seconds=start_date.second)
        end_date_month_end = end_date - timedelta(days=end_date.day - 1, hours=end_date.hour, minutes=end_date.minute, seconds=end_date.second) + timedelta(days= monthrange(month_start_cursor_date.year, month_start_cursor_date.month)[1])
        while month_start_cursor_date < end_date_month_end:
            next_cursor_date = month_start_cursor_date + timedelta(days= monthrange(month_start_cursor_date.year, month_start_cursor_date.month)[1]-1)
            entry = any(month_start_cursor_date<= date<= next_cursor_date for date in entry_dates)
            if(entry):
                count += 1
            month_start_cursor_date = next_cursor_date+ timedelta(days=1)
    return count

   

 