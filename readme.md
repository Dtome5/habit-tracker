# Habit Tracker
This is an app used for tracking habits created for learning purposes.
It allows users to create delete and track the progress of habits using
the command line.
## Installation
Dependencies:
- Typer
- Rich

For tests:
- Pytest
- Freezegun

### How to install:

To install the app download the files and store them in one folder. Install Python on your device. Open the terminal 
and cd to the folder where the package is then use pip install requirements.txt to install all the 
required packages.

## Usage
The app's commands are accessed through the cli.py module.

The commands follow the syntax python cli.py command objects
The app has the following functions
```
python cli.py add [habitname] periodicity
python cli.py delete habitname
python cli.py check habitname
python cli.py history habitname
python cli.py list periodicity
python cli.py listall
python cli.py timeline
python cli.py longest-streak
python cli.py list-streak
python cli.py consistency habitname
python cli.py consistency-all
```
tests are conducted with pytest using the command 
```
  pytest tests.py
```
To view the four weeks of habit testing data use the command
```python cli.py testdata```