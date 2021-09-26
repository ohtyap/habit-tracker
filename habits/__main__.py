#!/usr/bin/env python
# The main entry point. Invoke as `python -m habit-tracker'.
import os
from pathlib import Path


def main():
    from habits.application import run

    # Default sqlite database location
    database_file = (
        Path().home() / ".local" / "share" / "habit-tracker" / "habit-tracker.db"
    )
    run(database_file)


if __name__ == "__main__":
    main()
