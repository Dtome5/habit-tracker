from habit import *


def get_habit(name):
    """"""
    res = cur.execute(
        "SELECT name, periodicity FROM Habits WHERE name = ?", (name,)
    ).fetchone()
    if res != None:
        habit = Habit(res[0], res[1])
        if habit.get() is True:
            return habit
        else:
            return f"{name} does not exist"


def get_all_habits():
    """"""
    res = cur.execute("SELECT name FROM Habits").fetchall()
    habit_list = [x[0] for x in res]
    return habit_list


def get_timeline(name: str):
    """"""
    res = cur.execute(
        "SELECT name, date_checked, ischecked FROM Timeline WHERE name = ? LIMIT 10",
        (name,),
    ).fetchall()
    names = [res[i][0] for i in range(len(res))]
    dates_raw = [res[i][1] for i in range(len(res))]
    dates_str = [date.strftime("%Y-%m-%d") for date in dates_raw]
    completed = [res[i][2] for i in range(len(res))]
    completed_str = list(map(lambda x: "yes" if x == 1 else "No", completed))
    timeline = [res[i] for i in range(len(res))]
    lists = [(names[i], dates_str[i], completed_str[i]) for i in range(len(res))]
    return lists


def timeline():
    """"""
    res = cur.execute(
        "SELECT name, date_checked, ischecked FROM Timeline ORDER BY date_checked desc LIMIT 10"
    ).fetchall()
    names = [res[i][0] for i in range(len(res))]
    dates_raw = [date.strftime(res[i][1], "%Y-%m-%d") for i in range(len(res))]
    dates = list(
        map(
            lambda x: date.strftime(x, "%Y-%m-%d"), [res[i][1] for i in range(len(res))]
        )
    )
    completed = [res[i][2] for i in range(len(res))]
    completed_str = list(map(lambda x: "yes" if x == 1 else "No", completed))
    timeline = [res[i] for i in range(len(res))]
    lists = [(names[i], dates_raw[i], completed_str[i]) for i in range(len(res))]
    return lists


def get_with_period(periodicity):
    """"""
    res = cur.execute(
        "SELECT name, periodicity FROM Habits WHERE periodicity = ? ",
        (periodicity,),
    ).fetchall()
    habit_list = [x[0] for x in res]
    print(habit_list)
    return habit_list


def history(name: str):
    """"""
    res = cur.execute(
        "SELECT name, date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked desc LIMIT 10",
        (name,),
    ).fetchall()
    names = [res[i][0] for i in range(len(res))]
    dates_raw = [date.strftime(res[i][1], "%Y-%m-%d") for i in range(len(res))]
    dates = list(
        map(
            lambda x: date.strftime(x, "%Y-%m-%d"), [res[i][1] for i in range(len(res))]
        )
    )
    completed = [res[i][2] for i in range(len(res))]
    completed_str = list(map(lambda x: "yes" if x == 1 else "No", completed))
    timeline = [res[i] for i in range(len(res))]
    lists = [(names[i], dates_raw[i], completed_str[i]) for i in range(len(res))]
    return lists


def get_lstreak(name):
    """"""
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


def get_lstreak_all():
    """"""
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


def missed_ratio(name: str):
    """"""
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
