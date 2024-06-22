from datetime import datetime, timedelta
from app.core.data.enums import Periodicity
from app.core.services.helpers.streaks import calculate_streak

def test_daily_streak():
    # entry dates with daily streak 3, one falter, current streak 2
    entry_dates: list[datetime] = [ datetime.fromisocalendar(2024,1,1), datetime.fromisocalendar(2024,1,2), datetime.fromisocalendar(2024,1,3), datetime.fromisocalendar(2024,1,5), datetime.fromisocalendar(2024,1,6)]
    streaks = calculate_streak(entry_dates, datetime.fromisocalendar(2024,1,1), datetime.fromisocalendar(2024,1,6), Periodicity.DAILY)
    print(streaks)
    
    assert streaks["longest_streak"] == 3
    assert streaks["current_streak"] == 2

def test_weekly_streak():
    # entry dates with weekly streak 2, one falter, current streak 2
    entry_dates: list[datetime] = [ datetime.fromisocalendar(2024,1,1), datetime.fromisocalendar(2024,1,2), datetime.fromisocalendar(2024,2,1), datetime.fromisocalendar(2024,2,3), datetime.fromisocalendar(2024,4,4),datetime.fromisocalendar(2024,5,4)]
    streaks = calculate_streak(entry_dates, datetime.fromisocalendar(2024,1,1),datetime.fromisocalendar(2024,5,5) , Periodicity.WEEKLY)
    print(streaks)
    assert streaks["longest_streak"] == 2
    assert streaks["current_streak"] == 2

def test_monthly_streak():
    # entry dates with monthly streak 2, one falter and current streak 3
    entry_dates = [datetime(2024, 1, 1), datetime(2024, 2, 1), datetime(2024, 4, 1), datetime(2024, 5, 1), datetime(2024, 6, 1)]
    streaks = calculate_streak(entry_dates, datetime(2024, 1, 1), datetime(2024, 6, 2), Periodicity.MONTHLY)
    print(streaks)
if __name__ == "__main__":
    test_daily_streak()
    test_weekly_streak()
    test_monthly_streak()
