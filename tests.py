import pytest
from analytics import *
from freezegun import freeze_time


db = make_db(":memory:")
make_tables(db)


def test_store():
    habit = Habit("laundry", "weekly", db)
    habit.store()
    assert habit_exists(db, habit.name) is True


def test_delete():
    habit = Habit("gym", "weekly", db)
    habit.store()
    assert habit_exists(db, habit.name) is True
    delete_habit(db, habit.name)
    assert habit_exists(db, habit.name) is False


def test_check_daily():
    habit = Habit("read", "daily", db)
    habit.store()
    habit.checkin(date.today())
    assert get_last_check(db, habit.name) is not None


def test_daily_streak():
    habit = Habit("something2", "daily", db)
    habit.store()
    habit.checkin(date.today())
    habit.checkin(date.today())
    habit.checkin(date.today() + timedelta(days=1))
    habit.checkin(date.today() + timedelta(days=2))
    habit.checkin(date.today() + timedelta(days=3))
    assert habit.cstreak() == 4


def test_weekly_streak():
    habit = Habit("gym", "weekly", db)
    habit.store()
    habit.checkin(date.today())
    habit.checkin(date.today() + timedelta(days=7))
    habit.checkin(date.today() + timedelta(days=14))
    habit.checkin(date.today() + timedelta(days=45))
    habit.checkin(date.today() + timedelta(days=53))
    assert habit.cstreak() == 2
    assert habit.lstreak() == 3


# habit = Habit("gym", "weekly", db)
# habit.store()
# habit.checkin(date.today())
# habit.checkin(date.today() + timedelta(days=7))


# print(type(date.today() + timedelta(days=1)))
# habit = Habit("ready", "daily")
# habit.store()
# print(habit.checkin(date.today()))
# streak
# streak_break
# missed_days
# missed_ratio
# longest_streak
# timeline
