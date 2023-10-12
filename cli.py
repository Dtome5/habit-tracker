import typer
from rich.console import Console
from rich.table import Table
from analytics import *
from typing import Optional

app = typer.Typer()
console = Console()

err_console = Console(stderr=True)


@app.command()
def add(name: str, periodicity: str):
    """Command for adding habit with name and periodicity."""
    habit = Habit(name, periodicity)
    print(habit.store())


@app.command()
def delete(name):
    """Command for delete habit using name."""
    habit = get_habit(name)
    habit.drop()


@app.command()
def check(name: str):
    """Command for checking habit."""
    habit = get_habit(name)
    print(habit.checkin(date.today()))


@app.command("history")
def show_history(habit: Optional[str] = typer.Argument(default=None)):
    """Shows a table of the last 10 entries into the timeline."""
    table = Table(title="Timeline")
    table.add_column("name", justify="right", style="blue", no_wrap=True)
    table.add_column("date", style="green")
    table.add_column("status", style="yellow")
    timeline = get_timeline(habit) if habit is not None else history()
    for i in timeline:
        table.add_row(*i)
    console.print(table)


@app.command("list")
def list_all(periodicity: Optional[str] = typer.Argument(default=None)):
    """Shows a table of all habits."""
    table = Table(title="Weekly Habits")
    table.add_column("name", justify="center", style="cyan")
    if periodicity == None or "all":
        for i in get_all_habits():
            table.add_row(i)
    elif periodicity == "weekly" or "daily":
        for i in get_with_period(periodicity):
            table.add_row(i)
    else:
        console.print("please specify periodicity")
    console.print(table)


@app.command()
def list_weekly():
    """Shows a table of all weekly habits."""
    table = Table(title="Weekly Habits")
    table.add_column("name", justify="center", style="cyan")
    for i in get_with_period("weekly"):
        print(i)
        table.add_row(i)
    console.print(table)


@app.command()
def list_daily():
    """Shows a table of all daily habits."""
    table = Table(title="Daily Habits")
    table.add_column("name", justify="center", style="cyan")
    for i in get_with_period("daily"):
        table.add_row(i)
    console.print(table)


@app.command()
def longest_streak(name: Optional[str] = typer.Argument(default=None)):
    """Shows the longest streak of all habits it's starting data and it's end date."""
    if name == None:
        print(get_lstreak_all())
    else:
        print(get_lstreak(name))


@app.command()
def current_streak(name: str):
    """Shows the current streak of all habits it's starting data and it's end date."""
    print(get_cstreak(name))


@app.command()
def show_consistency(habit: Optional[str] = typer.Argument(default=None)):
    """Shows a table of all habits and their consistency."""
    habits = get_all_habits()
    consistencies = (
        list(map(lambda x: str(consistency(x)), habits))
        if habit == None
        else consistency(habit)
    )
    table = Table(title="Consistency")
    table.add_column("habit", justify="left")
    table.add_column("%complete", justify="center")
    if habit == None:
        for i in range(len(habits)):
            table.add_row(habits[i], consistencies[i])
    else:
        table.add_row(habit, str(consistencies))
    console.print(table)


@app.command("testdata")
def show_test_data():
    table = Table(title="Timeline")
    table.add_column("name", justify="right", style="blue", no_wrap=True)
    table.add_column("date", style="green")
    table.add_column("status", style="yellow")
    for i in history(make_db("tests.db")):
        table.add_row(*i)
    console.print(table)


@app.command()
def main():
    """"""
    err_console.print("Here is something written to standard error")


if __name__ == "__main__":
    app()
