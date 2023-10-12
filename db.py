import sqlite3
from datetime import date, timedelta


def make_db(name="database.db"):
    """Creates and returns and sqlite3 connection
    args:
        name -- the name of the file to be connected
    returns:
        db -- and sqlite3 connection"""
    db = sqlite3.connect(
        name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    return db


def make_tables(db):
    """Creates the tables for Habits, Streaks, Timeline, and week_timeline
    args:
        db: the database to put the tables"""
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Habits (name text, periodicity text, date_created date)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Streak (name text, current_start date, longest_start date, current_end date, longest_end date, current_streak integer, longest_streak integer)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Timeline (name text, date_checked date, ischecked bool)"
    )
    db.commit()


def store_habit(db, name: str, periodicity: str, date_created: date):
    """Stores habit's name, task, periodicity into a database
    Args:
        db: the database to store the habit
        name: the habit's name
        periodicity: the habit's periodicity
        date_created: the date the habit was created
    """
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Habits VALUES(:habit, :periodicity, :date_created)",
        (name, periodicity, date_created),
    )
    cur.execute(
        "INSERT INTO Streak VALUES(:name, :current_start, :longest_start, :current_end, :longest_end, :current_streak, :longest_streak)",
        (name, date_created, date_created, date_created, date_created, 0, 0),
    )
    db.commit()


def check(db, name, date_checked: date, status: bool):
    """marks habit as complete for the date_checked
    Args:
        db: the database to store the habit
        name: the habit's name
        periodicity: the habit's periodicity
        date_created: the date the habit was created
    """
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Timeline VALUES(:name, :date_checked, :ischecked)",
        (name, date_checked, status),
    )


def delete_habit(db, name: str):
    """Deletes habit from the Habit table
    Args:
    db: the database the habit is stored in
    name: the habit's name
    """
    cur = db.cursor()
    cur.execute("DELETE FROM Habits WHERE name = ?", (name,))


def delete_progress(db, name: str):
    """Deletes Habits logs from the Timeline and streak tables.
    Args:
    db: the database the habit is stored in
    name: the habit's name
    """
    cur = db.cursor()
    cur.execute("DELETE FROM Timeline WHERE name = ? ", (name,))
    cur.execute("DELETE FROM Streak WHERE name = ?", (name,))


def get_db_element(db, element: str):
    cur = db.cursor()
    result = cur.execute(f"SELECT {element} FROM timeline ")
    return result.fetchall()


def habit_exists(db, name: str):
    """Checks if habit is stored in the database
    Args:
    db: the database the habit is stored in
    name: the habit's name
    """
    cur = db.cursor()
    res = cur.execute("SELECT name FROM Habits WHERE name = ?", (name,)).fetchone()
    if res == None:
        return False
    else:
        return True


def get_last_check(db, name: str):
    cur = db.cursor()
    last_check = cur.execute(
        "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
        (name,),
    ).fetchone()
    return last_check


def update_streak(
    db,
    name: str,
    current_start: date,
    longest_start: date,
    current_end: date,
    longest_end: date,
    current_streak: int,
    longest_streak: int,
):
    """Updates the habit's streak data
    Args:
    db: the database the data is stored in
    name: the name of the habit
        current_start: the starting date of the current streak
        longest_start: the starting date of the longest streak
        current_end: the last date of the current streak
        longest_end: the last date of the longest streak
        current_streak: the value of the current streak
        longest_streak: the value of the longest streak"""
    cur = db.cursor()
    cur.execute(
        "UPDATE Streak SET current_start = ?, longest_start = ?, current_end = ?, longest_end = ?, current_streak = ?, longest_streak = ?",
        (
            current_start,
            longest_start,
            current_end,
            longest_end,
            current_streak,
            longest_streak,
        ),
    )
