from db import *

# db = make_db("dsposable1.db")
# cur = db.cursor()
# make_tables(db)


class Habit:
    """The habit class"""

    def __init__(self, name: str, periodicity: str, db=make_db("habits.db")):
        """The intialisation function initialized the habit with the parametres:
        name: the habit's name
        periodicity: the habit's periodicity
        db: the database to store the habit's data
        date_created: the date the habit is created set to "today" """
        self.name = name
        self.periodicity = periodicity
        self.date_created = date.today()
        self.db = db
        make_tables(db)

    def store(self):
        """Stores Habit name and periodicity in the database"""
        db = self.db
        cur = db.cursor()
        if habit_exists(db, self.name):
            return f"the habit {self.name} already exists"
        else:
            store_habit(db, self.name, self.periodicity, self.date_created)
            db.commit()

    def drop(self):
        """Deletes Habit from database"""
        delete_habit(self.db, self.name)
        delete_progress(self.db, self.name)

    def due_week(self, date: date):
        """Finds the date that a weekly habit is due given the date created
        Arguments:
            date: the date evaluated
        Returns:
            deadline: the deadline date of a weekly habit"""
        weeks_between = (date - self.date_created).days // 7
        deadline = self.date_created + (timedelta(weeks=weeks_between + 1))
        return deadline

    def update_streak(self, current_end):
        """Updates the habits streak by incrementing it by one, if the current streak is longer than the
        longest streak the current streak becomes the longest streak"""
        db = self.db
        cur = db.cursor()
        res = cur.execute(
            "SELECT current_streak, longest_streak, longest_end From STREAK WHERE name =?",
            (self.name,),
        ).fetchone()
        current_streak, longest_streak, longest_end = (
            res if res is not None else (0, 0, date.today())
        )
        current_streak += 1
        if current_streak > longest_streak:
            longest_streak = current_streak
            longest_end = current_end
        cur.execute(
            "UPDATE Streak SET current_streak = ?, longest_streak = ?,current_end =?, longest_end = ? WHERE name = ?",
            (current_streak, longest_streak, current_end, longest_end, self.name),
        )
        db.commit()
        newres = cur.execute("select * from Streak").fetchall()
        return f"{self.name} new streak is {current_streak}{newres}"

    def reset_streak(self, new_start):
        """resets the current streak to 1 and updates the streaks starting date
        Arguments:
            new_start: the new starting date for the streak"""
        db = self.db
        cur = db.cursor()
        cur.execute(
            "UPDATE Streak SET current_streak = ?,current_start = ? WHERE name = ?",
            (1, new_start, self.name),
        )
        db.commit()
        return f"{self.name}'s streak has been reset"

    def get_last_log(self):
        """Retreives the date_checked and is_checked values for a habit
        Returns:
            last_log: A tuple of the habit's last log date and is_checked value"""
        db = self.db
        cur = db.cursor()
        res = cur.execute(
            "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
            (self.name,),
        ).fetchone()
        if res == None:
            last_check = (None,)
        else:
            last_check = res
        return last_check

    def missed_days(self, datenow):
        """Calculates all the dates the user has missed and fills them with the value false"""
        db = self.db
        cur = db.cursor()
        last_check = self.get_last_log()
        last_date = self.date_created if last_check == None else last_check[0]
        datelist = []
        if self.periodicity == "daily":
            while last_date < datenow - timedelta(days=1):
                last_date += timedelta(days=1)
                datelist.append((self.name, last_date, False))
            cur.executemany(
                "INSERT INTO Timeline VALUES(:name, :date_checked, :ischecked)",
                datelist,
            )
            db.commit()
        elif self.periodicity == "weekly":
            deadline = self.due_week(datenow)
            last_due = self.due_week(last_date)
            while last_due < deadline - timedelta(weeks=1):
                last_due += timedelta(weeks=1)
                datelist.append((self.name, last_due, False))
            cur.executemany(
                "INSERT INTO Timeline VALUES(:name, :date_checked, :ischecked)",
                datelist,
            )

    def checkin(self, date_checked: date):
        """Checks in habit for date_checked, fills in missed dates and updates or resets streak"""
        db = self.db
        cur = db.cursor()
        last_check = self.get_last_log()
        last_date = last_check[0]
        if self.periodicity == "daily":
            if last_date == date_checked:
                return f"{self.name} has already been checked for today"
            elif last_date == None:
                self.update_streak(date_checked)
            elif date_checked - last_date == timedelta(days=1):
                self.update_streak(date_checked)
            elif date_checked - last_date > timedelta(days=1):
                self.missed_days(date_checked)
                self.reset_streak(date_checked)
            else:
                pass
            check(db, self.name, date_checked, True)
            db.commit()
            return f"Checked {self.name} for the day"
        elif self.periodicity == "weekly":
            if last_date == None:
                # print(last_check)
                self.update_streak(date_checked)
            elif self.due_week(last_date) < self.due_week(date_checked):
                deadline = self.due_week(date_checked)
                prev_due = self.due_week(last_date)
                # print(prev_due, deadline)
                if deadline - prev_due <= timedelta(weeks=2):
                    self.update_streak(date_checked)
                else:
                    self.missed_days(date_checked)
                    self.reset_streak(date_checked)
            else:
                return f"already checked {self.name} for the week"
            check(db, self.name, date_checked, True)
            db.commit()
            return f"Checked {self.name} for the week"

    def cstreak(self):
        db = self.db
        cur = db.cursor()
        res = cur.execute(
            "SELECT current_streak FROM Streak WHERE name = ?", (self.name,)
        ).fetchone()
        return res[0]

    def lstreak(self):
        db = self.db
        cur = db.cursor()
        res = cur.execute(
            "SELECT longest_streak FROM Streak WHERE name = ?", (self.name,)
        ).fetchone()
        return res[0]


# def get(self):
#     """"""
#     habit = cur.execute(
#         "SELECT name FROM Habits WHERE name = ?", (self.name,)
#     ).fetchone()
#     exists = habit is not None
#     return exists

# def get_last_check(self):
#     """"""
#     db = self.db
#     cur = db.cursor()
#     res = cur.execute(
#         "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
#         (self.name,),
#     ).fetchone()
#     if res is not None:
#         return res
#     else:
#         return (None, None)
