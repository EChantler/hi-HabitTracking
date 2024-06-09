import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
import typing
db_path = "db.db"
db = sa.create_engine(f"sqlite:///{db_path}")
# db = sa.create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=db)
Base = declarative_base()
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

from sqlalchemy import event
event.listen(db, 'connect', _fk_pragma_on_connect)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    apiKey: Mapped[str]
    created_on_utc: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_on_utc: Mapped[datetime]= mapped_column(default=None, nullable=True)
    habits: Mapped[typing.List["Habit"]] = relationship(
        "Habit", back_populates="user"
    )
    habit_entries: Mapped[typing.List["HabitEntry"]] = relationship(
        "HabitEntry", back_populates="user"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, apiKey={self.apiKey!r}, created_on_utc={self.created_on_utc!r}, modified_on_utc={self.modified_on_utc!r})"

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = sa.Column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped[str] = relationship("User", back_populates="habits", foreign_keys=[user_id])
    name: Mapped[str]
    completion_criteria: Mapped[str]
    periodicity: Mapped[int]#enum int
    created_on_utc: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_on_utc: Mapped[datetime]= mapped_column(default=None, nullable=True)
    habit_entries: Mapped[typing.List["HabitEntry"]] = relationship(
        "HabitEntry", back_populates="habit"
    )
    def __repr__(self) -> str:
        return f"Habit(id={self.id!r}, user_id={self.user_id!r}, name={self.name!r}, completion_criteria={self.completion_criteria!r}, periodicity={self.periodicity!r}, created_on_utc={self.created_on_utc!r}, modified_on_utc={self.modified_on_utc!r})"

class HabitEntry(Base):
    __tablename__ = "habit_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = sa.Column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped[User] = relationship("User", back_populates="habit_entries")
    habit_id: Mapped[int] = sa.Column(
        sa.Integer, sa.ForeignKey("habits.id"), nullable=False, index=True
    )
    habit: Mapped[Habit] = relationship("Habit", back_populates="habit_entries")
    created_on_utc: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_on_utc: Mapped[datetime]= mapped_column(default=None, nullable=True)

    def __repr__(self) -> str:
        return f"HabitEntry(id={self.id!r}, user_id={self.user_id!r}, habit_id={self.habit_id!r}, created_on_utc={self.created_on_utc!r}, modified_on_utc={self.modified_on_utc!r})"

def main() -> None:
    Base.metadata.create_all(db)
    user = User(name = "test", email = "test@test.com", apiKey = "testApiKey")
    habit = Habit( user_id = 1 ,name = "test", completion_criteria = "test", periodicity = 1)
    habit_entry = HabitEntry(user_id = 1, habit_id = 1, created_on_utc = datetime.now())
    with Session() as session:
        session.add(user)
        session.add(habit)
        session.add(habit_entry)
        session.commit()
        print(session.query(User).all())
        print(session.query(Habit).all())
        print(session.query(HabitEntry).all())


if __name__ == "__main__":
    main()