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

### Adding habits
```
python cli.py add habitname periodicity
```

### Deleting habits
```
python cli.py delete habitname
```

### Checking-in
```
python cli.py check habitname
```

### Viewing history
```
python cli.py history habitname
```

### List habit's periodicities
```
python cli.py list periodicity
```

### List all habits
```
python cli.py list
```

### List the last entries into timeline
```
python cli.py history [habitname]
```

### Show longest streak
```
python cli.py longest-streak [habitname]
```

### Show current streak
```
python cli.py current-streak [habitname]
```

### Show consistency
```
python cli.py consistency [habitname]
```
- NOTE: Values in square brackets [] are optional

## Testing
- tests are conducted with pytest by navigating into the folder and using the command 
```
  pytest tests.py
```
To view the four weeks of habit testing data use the command
```python cli.py testdata```