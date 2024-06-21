
from datetime import datetime, timedelta

from app.core.data.enums import Periodicity
import math
def calculate_total_planned(start_date: datetime, periodicity: Periodicity) -> int:
    current_date = datetime.now()
    if periodicity == Periodicity.DAILY:
        return (current_date - start_date).days
    if periodicity == Periodicity.WEEKLY:
        return int(math.ceil((current_date - start_date).days / 7))
    if periodicity == Periodicity.MONTHLY:
        years_difference = current_date.year - start_date.year
        months_difference = current_date.month - start_date.month
        return int(math.ceil(years_difference * 12 + months_difference))
    return 0

def calculate_longest_streak(entries: list[datetime],start_date: datetime, periodicity: Periodicity) -> int:
    dates = generate_date_list(start_date, datetime.now().date())
    longest_streak = 0
    current_streak = 0
    if periodicity == Periodicity.DAILY:
        for date in dates:
            if date in [entry.date() for entry in entries]:
                current_streak += 1
            else:
                if current_streak > longest_streak:
                    longest_streak = current_streak
                current_streak = 0

        return longest_streak


   

def generate_date_list(start_date, end_date):
    # Convert the start_date string to a datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Calculate the number of days between the past date and current date
    delta = end_date - start_date
    
    # Generate a list of dates using list comprehension
    date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]
    
    return date_list