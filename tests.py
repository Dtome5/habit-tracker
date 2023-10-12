import pytest
from analytics import *
from freezegun import freeze_time


db = make_db(":memory:")
make_tables(db)


@freeze_time(date(2023, 9, 1))
def do():
    laundry = Habit("laundry", "weekly", db)
    study = Habit("study", "daily", db)
    chores = Habit("chores", "daily", db)
    meditation = Habit("meditation", "daily", db)
    gym = Habit("gym", "weekly", db)
    laundry.store()
    study.store()
    chores.store()
    meditation.store()
    gym.store()
    # print(study.date_created)
    # print(date.today())
    study.checkin(date(2023, 9, 1))
    study.checkin(date(2023, 9, 2))
    study.checkin(date(2023, 9, 3))
    study.checkin(date(2023, 9, 4))
    study.checkin(date(2023, 9, 6))
    study.checkin(date(2023, 9, 8))
    study.checkin(date(2023, 9, 9))
    study.checkin(date(2023, 9, 10))
    study.checkin(date(2023, 9, 11))
    study.checkin(date(2023, 9, 12))
    study.checkin(date(2023, 9, 13))
    study.checkin(date(2023, 9, 14))
    study.checkin(date(2023, 9, 15))
    study.checkin(date(2023, 9, 16))
    study.checkin(date(2023, 9, 17))
    study.checkin(date(2023, 9, 20))
    study.checkin(date(2023, 9, 21))
    study.checkin(date(2023, 9, 22))
    study.checkin(date(2023, 9, 24))
    study.checkin(date(2023, 9, 25))
    study.checkin(date(2023, 9, 27))
    study.checkin(date(2023, 9, 28))
    chores.checkin(date(2023, 9, 1))
    chores.checkin(date(2023, 9, 2))
    chores.checkin(date(2023, 9, 3))
    chores.checkin(date(2023, 9, 4))
    chores.checkin(date(2023, 9, 5))
    chores.checkin(date(2023, 9, 6))
    chores.checkin(date(2023, 9, 8))
    chores.checkin(date(2023, 9, 10))
    chores.checkin(date(2023, 9, 12))
    chores.checkin(date(2023, 9, 14))
    chores.checkin(date(2023, 9, 15))
    chores.checkin(date(2023, 9, 16))
    chores.checkin(date(2023, 9, 17))
    chores.checkin(date(2023, 9, 18))
    chores.checkin(date(2023, 9, 20))
    chores.checkin(date(2023, 9, 23))
    chores.checkin(date(2023, 9, 24))
    chores.checkin(date(2023, 9, 25))
    chores.checkin(date(2023, 9, 26))
    chores.checkin(date(2023, 9, 27))
    meditation.checkin(date(2023, 9, 1))
    meditation.checkin(date(2023, 9, 3))
    meditation.checkin(date(2023, 9, 4))
    meditation.checkin(date(2023, 9, 5))
    meditation.checkin(date(2023, 9, 6))
    meditation.checkin(date(2023, 9, 8))
    meditation.checkin(date(2023, 9, 11))
    meditation.checkin(date(2023, 9, 14))
    meditation.checkin(date(2023, 9, 15))
    meditation.checkin(date(2023, 9, 16))
    meditation.checkin(date(2023, 9, 17))
    meditation.checkin(date(2023, 9, 18))
    meditation.checkin(date(2023, 9, 19))
    meditation.checkin(date(2023, 9, 20))
    meditation.checkin(date(2023, 9, 21))
    meditation.checkin(date(2023, 9, 22))
    meditation.checkin(date(2023, 9, 23))
    meditation.checkin(date(2023, 9, 26))
    meditation.checkin(date(2023, 9, 28))
    laundry.checkin(date(2023, 9, 4))
    laundry.checkin(date(2023, 9, 16))
    laundry.checkin(date(2023, 9, 24))
    gym.checkin(date(2023, 9, 1))
    gym.checkin(date(2023, 9, 8))
    gym.checkin(date(2023, 9, 15))
    gym.checkin(date(2023, 9, 22))
    cur = db.cursor()
    res = cur.execute("select * from timeline where name = ? ", ("gym",)).fetchall()
    print(res)


do()


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


def test_weekly_check():
    habit = Habit("laundry", "weekly", db)
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
