from habit import *

db = make_db("habits.db")
cur = db.cursor()
make_tables(db)


def get_habit(name, db=make_db("habits.db")):
    """Retreives a habit from the databaase if it exists and returns a class"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT name, periodicity FROM Habits WHERE name = ?", (name,)
    ).fetchone()
    if res != None:
        habit = Habit(res[0], res[1])
        return habit
    else:
        return f"{name} does not exist"


def get_all_habits(db=make_db("habits.db")):
    """Returns a list of all habits"""
    cur = db.cursor()
    res = cur.execute("SELECT name FROM Habits").fetchall()
    habit_list = [x[0] for x in res]
    return habit_list


def get_with_period(periodicity, db=make_db("habits.db")):
    """Returns a list of all habits with the specified periodicity"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT name, periodicity FROM Habits WHERE periodicity = ? ",
        (periodicity,),
    ).fetchall()
    habit_list = [x[0] for x in res]
    return habit_list


def get_timeline(name: str, db=make_db("habits.db")):
    """Returns a list of the last ten entries into the timeline of the habit"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT name, date_checked, ischecked FROM Timeline WHERE name = ? LIMIT 10",
        (name,),
    ).fetchall()
    names = [res[i][0] for i in range(len(res))]
    dates = [date.strftime(res[i][1], "%Y-%m-%d") for i in range(len(res))]
    completed = list(
        map((lambda x: "yes" if x == 1 else "No"), [res[i][2] for i in range(len(res))])
    )
    timeline = [res[i] for i in range(len(res))]
    lists = [(names[i], dates[i], completed[i]) for i in range(len(res))]
    return lists


def history(db=make_db("habits.db")):
    """Returns a list of the last ten entries into the timeline"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT name, date_checked, ischecked FROM Timeline ORDER BY date_checked desc LIMIT 10"
    ).fetchall()
    names = [res[i][0] for i in range(len(res))]
    dates = [date.strftime(res[i][1], "%Y-%m-%d") for i in range(len(res))]
    completed = list(
        map((lambda x: "yes" if x == 1 else "No"), [res[i][2] for i in range(len(res))])
    )
    timeline = [res[i] for i in range(len(res))]
    lists = [(names[i], dates[i], completed[i]) for i in range(len(res))]
    return lists


def get_lstreak(name, db=make_db("habits.db")):
    """Returns the longest streak of a habit"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT longest_streak, longest_start, longest_end FROM Streak WHERE name = ?",
        (name,),
    ).fetchone()
    habit = get_habit(name)
    if habit.periodicity == "daily":
        unit = "days"
    elif habit.periodicity == "weekly":
        unit = "weeks"
    if res[0] > 0:
        return f"the longest streak for {habit.name} is {res[0]}{unit} from {res[1]} to {res[2]}"
    else:
        return f"there is no streak for {habit.name}"


def get_cstreak(name, db=make_db("habits.db")):
    """Returns the current streak of a habit"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT current_streak, current_start, current_end FROM Streak WHERE name = ?",
        (name,),
    ).fetchone()
    habit = get_habit(name)
    if habit.periodicity == "daily":
        unit = "days"
    elif habit.periodicity == "weekly":
        unit = "weeks"
    if res[0] > 0:
        return f"the current streak for {habit.name} is {res[0]}{unit} from {res[1]} to {res[2]}"
    else:
        return f"there is no streak for {habit.name}"


def get_lstreak_all(db=make_db("habits.db")):
    """Gives a list of the longest streak on all habits"""
    cur = db.cursor()
    res = cur.execute(
        "SELECT longest_streak,name,longest_start,longest_end FROM Streak ORDER BY longest_streak DESC"
    ).fetchone()
    habit = get_habit(res[1])
    if habit.periodicity == "daily":
        unit = "days"
    elif habit.periodicity == "weekly":
        unit = "weeks"
    else:
        unit = "nothing"
    if res[0] == 0:
        return f"There are no streaks"
    return f"The longest streak is the habit {res[1]} {res[0]}{unit} from {res[2]} to {res[3]}"


def consistency(name: str, db=make_db("habits.db")):
    cur = db.cursor()
    """Gives the ratio of completed dates to missed dates"""
    habit = get_habit(name)
    missed = cur.execute(
        "SELECT date_checked FROM Timeline WHERE name = ? and ischecked = ?", (name, 0)
    ).fetchall()
    completed = cur.execute(
        "SELECT date_checked FROM Timeline WHERE name = ? and ischecked = ?", (name, 1)
    ).fetchall()
    if completed != None:
        ratio = len(completed) / (len(missed) + len(completed))
    else:
        ratio = 0
    return round(ratio, 2)
