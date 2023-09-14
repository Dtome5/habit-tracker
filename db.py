import sqlite3
from datetime import *


def make_db(name="database.db"):
    db = sqlite3.connect(
        name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    return db


def make_tables(db):
    """"""
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
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Week_Timeline (name text, date_checked date, start_date date, stop_date date, ischecked bool)"
    )
    db.commit()


def store_habit(db, name: str, periodicity: str, date_created: date):
    """"""
    """Stores habit's name, task, periodicity into a database"""
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
    """"""
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Timeline VALUES(:name, :date_checked, :ischecked)",
        (name, date_checked, status),
    )


def delete_habit(db, habit: str):
    """"""
    cur = db.cursor()
    cur.execute("DELETE FROM Habits WHERE name = ?", (habit,))


def delete_progress(db, name: str):
    """"""
    cur = db.cursor()
    cur.execute("DELETE FROM Timeline WHERE name = ? ", (name,))
    cur.execute("DELETE FROM Streak WHERE name = ?", (name,))


def get_db_element(db, element: str):
    # db = make_db(":memory:")
    cur = db.cursor()
    result = cur.execute(f"SELECT {element} FROM timeline ")
    return result.fetchall()


def habit_exists(db, name: str):
    cur = db.cursor()
    res = cur.execute("SELECT name FROM Habits WHERE name = ?", (name,)).fetchall()
    if res == None:
        return False
    else:
        return True

def get_last_check(db,name: str):
    last_check =
cur.execute(
            "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
            (self.name,),
        ).fetchone()


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
