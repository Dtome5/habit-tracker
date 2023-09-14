from db import *

db = make_db(":memory:")
cur = db.cursor()
make_tables(db)


class Habit:
    """"""

    def __init__(self, name: str, periodicity: str):
        """"""
        self.name = name
        self.periodicity = periodicity
        self.date_created = date.today()

    def get(self):
        """"""
        habit = cur.execute(
            "SELECT name FROM Habits WHERE name = ?", (self.name,)
        ).fetchone()
        exists = habit is not None
        return exists

    def get_last_check(self):
        """"""
        res = cur.execute(
            "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
            (self.name,),
        ).fetchone()
        if res is not None:
            return res
        else:
            return (None, None)

    def due_week(self, date: date):
        """"""
        weeks_between = (date - self.date_created).days // 7
        due_date = self.date_created + (timedelta(weeks=weeks_between + 1))
        return due_date

    def update_streak(self, current_end):
        """"""
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
        """"""
        cur.execute(
            "UPDATE Streak SET current_streak = ?,current_start = ? WHERE name = ?",
            (1, new_start, self.name),
        )
        db.commit()
        return f"{self.name}'s streak has been reset"

    def store(self):
        """Stores Habit name and periodicity in the database"""
        if self.get() == False:
            store_habit(db, self.name, self.periodicity, self.date_created)
            return f"Added {self.name} to database"
        else:
            return f"{self.name} already exists"
        db.commit()

    def drop(self):
        """Deletes Habit from database"""
        delete_habit(db, self.name)
        delete_progress(db, self.name)

    def missed_days(self, datenow):
        """Calculates all the dates the user has missed and fills them with the value false"""
        last_check = cur.execute(
            "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
            (self.name,),
        ).fetchone()
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
            due_date = self.due_week(datenow)
            last_due = self.due_week(last_date)
            while last_due < due_date - timedelta(weeks=1):
                last_due += timedelta(weeks=1)
                datelist.append((self.name, last_due, False))
            cur.executemany(
                "INSERT INTO Timeline VALUES(:name, :date_checked, :ischecked)",
                datelist,
            )

    def checkin(self, date_checked: date):
        """Checks in habit for date_checked"""
        last_check = cur.execute(
            "SELECT date_checked, ischecked FROM Timeline WHERE name = ? ORDER BY date_checked DESC",
            (self.name,),
        ).fetchone()
        if self.periodicity == "daily":
            last_date = (
                last_check[0]
                if last_check is not None
                else self.date_created - timedelta(days=1)
            )
            print(last_date)
            if last_date >= date_checked:
                return f"{self.name} has already been checked for today"
            else:
                if date_checked - last_date == timedelta(days=1):
                    self.update_streak(date_checked)
                else:
                    self.missed_days(date_checked)
                    self.reset_streak(date_checked)
                check(db, self.name, date_checked, True)
                db.commit()
                return f"Checked {self.name} for the day"
        elif self.periodicity == "weekly":
            last_date = last_check[0] if last_check is not None else self.date_created
            if self.due_week(last_date) < self.due_week(date_checked):
                due_date = self.due_week(date_checked)
                prev_due = self.due_week(last_date)
                if due_date - prev_due <= timedelta(weeks=2):
                    self.update_streak(date_checked)
                else:
                    self.missed_days(date_checked)
                    self.reset_streak(date_checked)
                check(db, self.name, date_checked, True)
                return f"Checked {self.name} for the week"
            else:
                return f"already checked {self.name} for the week"
        db.commit()


habit1 = Habit("yoga", "daily")
