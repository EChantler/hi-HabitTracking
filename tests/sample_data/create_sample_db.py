
# Create all tables
from datetime import datetime
from app.core.data.db import Base, Habit, HabitEntry, Session, User, db
from app.core.data.enums import Periodicity

# Run with SQLALCHEMY_DATABASE_URL=sqlite:///sample_db.db python -m tests.sample_data.create_sample_db

def db_session():
    """Creates a new database session for a test."""
    # Create all tables
    Base.metadata.create_all(db)
    session = Session()
    # Check if sampledb is empty
    if session.query(User).count() == 0:
        create_users(session)
        create_habits(session)
        create_habit_entries(session)
        print("Sample data created at sample_db.db")
    print("Sample database was already created. Run again after deleting sample_db.db to create a new one.")
    
    return session

def create_users(session):
    session.add(User(name = "test", email = "test@test.com", apiKey = "testApiKey"))
    session.add(User(name = "test2", email = "test2@test2.com", apiKey = "testApiKey2"))

    # write to db
    session.commit()

def create_habits(session):
    # habits for user 1
    session.add(Habit( user_id = 1,created_on_utc = datetime(2024,3,31), name = "read", completion_criteria = "read for 30 min a day", periodicity = Periodicity.DAILY))
    session.add(Habit( user_id = 1,created_on_utc = datetime(2024,3,30), name = "yoga", completion_criteria = "15min yoga session in your lunch break", periodicity = Periodicity.DAILY))
    session.add(Habit( user_id = 1,created_on_utc = datetime(2024,4,1), name = "gratitude drawing", completion_criteria = "draw something you're grateful for today", periodicity = Periodicity.DAILY))
    session.add(Habit( user_id = 1,created_on_utc = datetime(2024,3,31), name = "parkrun", completion_criteria = "run 5km in a 30min session", periodicity = Periodicity.WEEKLY))
    session.add(Habit( user_id = 1,created_on_utc = datetime(2024,3,31), name = "monthly planning", completion_criteria = "last sunday of the month, reflect on the past month and plan for the next", periodicity = Periodicity.MONTHLY))
    
    # habits for user 2
    session.add(Habit(user_id = 2,created_on_utc = datetime(2024,3,31), name = "meditation", completion_criteria = "meditate for 10 minutes", periodicity = Periodicity.DAILY))
    session.add(Habit(user_id = 2,created_on_utc = datetime(2024,3,31), name = "exercise", completion_criteria = "exercise for 30 minutes", periodicity = Periodicity.DAILY))
    session.add(Habit(user_id = 2,created_on_utc = datetime(2024,3,31), name = "journal", completion_criteria = "write in your journal for 15 minutes", periodicity = Periodicity.DAILY))
    session.add(Habit(user_id = 2,created_on_utc = datetime(2024,3,31), name = "meal prep", completion_criteria = "prepare meals for the week", periodicity = Periodicity.WEEKLY))
    session.add(Habit(user_id = 2,created_on_utc = datetime(2024,3,31), name = "financial review", completion_criteria = "review your finances and budget for the upcoming month", periodicity = Periodicity.MONTHLY))
    
    # write to db
    session.commit()

def create_habit_entries(session):
     # Create realistic Habit Entries from 2024-3-31 to 2024-4-30 for user 1
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,1)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,2)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,3)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,4)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,5)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,9)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,10)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,11)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,15)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,23)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,25)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,26)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,27)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,28)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,29)))
    session.add(HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime(2024,4,30)))

    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,1)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,5)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,8)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,9)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,11)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,15)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,16)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,17)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,18)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,19)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,20)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,21)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,23)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,24)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,25)))
    session.add(HabitEntry(user_id = 1, habit_id = 2, created_on_utc = datetime(2024,4,26)))

    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,1)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,2)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,3)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,4)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,5)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,8)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,9)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,10)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,11)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,12)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,13)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,14)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,15)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,16)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,17)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,18)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,19)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,20)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,21)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,23)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,24)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,25)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,26)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,27)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,28)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,29)))
    session.add(HabitEntry(user_id = 1, habit_id = 3, created_on_utc = datetime(2024,4,30)))

    session.add(HabitEntry(user_id = 1, habit_id = 4, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 1, habit_id = 4, created_on_utc = datetime(2024,4,12)))
    session.add(HabitEntry(user_id = 1, habit_id = 4, created_on_utc = datetime(2024,4,13)))
    session.add(HabitEntry(user_id = 1, habit_id = 4, created_on_utc = datetime(2024,4,17)))
    session.add(HabitEntry(user_id = 1, habit_id = 4, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 1, habit_id = 4, created_on_utc = datetime(2024,4,29)))

    session.add(HabitEntry(user_id = 1, habit_id = 5, created_on_utc = datetime(2024,4,28)))

    

    # Create realistic Habit Entries from 2024-4-1 to 2024-6-1 for user 2
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,4)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,5)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,8)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,9)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,10)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,11)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,12)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,13)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,14)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,15)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,16)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,17)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,18)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,19)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,20)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,21)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,23))) # break habit with streak 20
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,25)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,26)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,27)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,28)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,29)))
    session.add(HabitEntry(user_id = 2, habit_id = 6, created_on_utc = datetime(2024,4,30)))

    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,1)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,2)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,3)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,4)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,8)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,9)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,10)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,12)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,13)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,14)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,15)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,16)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,18)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,19)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,20)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,21)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,24)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,25)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,26)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,27)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,29)))
    session.add(HabitEntry(user_id = 2, habit_id = 7, created_on_utc = datetime(2024,4,30)))

    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,1)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,2)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,3)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,4)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,6)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,8)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,9)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,10)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,12)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,13)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,14)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,15)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,16)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,18)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,19)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,20)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,21)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,22)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,24)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,25)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,26)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,27)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,29)))
    session.add(HabitEntry(user_id = 2, habit_id = 8, created_on_utc = datetime(2024,4,30)))

    session.add(HabitEntry(user_id = 2, habit_id = 9, created_on_utc = datetime(2024,4,7)))
    session.add(HabitEntry(user_id = 2, habit_id = 9, created_on_utc = datetime(2024,4,14)))
    session.add(HabitEntry(user_id = 2, habit_id = 9, created_on_utc = datetime(2024,4,20)))

    session.add(HabitEntry(user_id = 2, habit_id = 10, created_on_utc = datetime(2024,4,30)))

    # write to db
    session.commit()
    

if __name__ == "__main__":
    session = db_session()
    
    



