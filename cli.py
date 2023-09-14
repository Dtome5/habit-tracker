import typer
from rich.console import Console
from rich.table import Table
from analytics import *

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


@app.command("listall")
def show_timeline():
    """Shows a table of the last 10 entries into the timeline."""
    table = Table(title="Timeline")
    table.add_column("name", justify="right", style="blue", no_wrap=True)
    table.add_column("date", style="green")
    table.add_column("status", style="yellow")
    for i in timeline():
        table.add_row(*i)
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
def longest_streak(name):
    """Shows the longest streak of all habits it's starting data and it's end date."""
    if name == "all":
        print(get_lstreak_all())
    else:
        print(get_lstreak(name))


@app.command()
def consistency():
    """Shows a table of all habits and their consistency."""
    habits = get_all_habits()
    consistency = list(map(lambda x: str(missed_ratio(x)), habits))
    table = Table(title="Consistency")
    table.add_column("habit", justify="left")
    table.add_column("%complete", justify="center")
    for i in range(len(habits)):
        table.add_row(habits[i], consistency[i])
    console.print(table)


@app.command()
def main():
    """"""
    err_console.print("Here is something written to standard error")


if __name__ == "__main__":
    app()
