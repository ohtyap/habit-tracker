#!/usr/bin/env python
# The main entry point. Invoke as `python -m habit-tracker'.
import os


def main():
    from habits.application import run
    # Default sqlite database location
    database_file = os.path.abspath(os.path.dirname(__file__) + '/../sqlite') + '/habit-tracker.db'
    run(database_file)


if __name__ == '__main__':
    main()
