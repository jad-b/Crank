# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto`.
"""
import string

from .util import ceil, lbs2kg, map_weeks
from .fto import build_sets


_weeks = map_weeks()


def process_input(units='lbs'):
    """Guide user through weight calculations via CLI prompts."""
    name = input("Please enter the exercise name: ")\
        .strip(string.whitespace)
    units = input("Kilograms? y or n: ").strip(string.whitespace)
    weight = int(input("Enter last week's max weight: "))
    week = int(input("Enter current training week:"))

    if week == 1:  # weight is from last cycle's week 3
        jump = int(input("Enter weight jump: "))
        lbs = ceil(((weight / 0.95) + jump))
        sets = build_sets(lbs, 0.85)
        reps = [5, 5, 3, 5, 5, 5]
    elif week == 2:  # weight is from week 1
        lbs = ceil((weight / 0.85))
        sets = build_sets(lbs, 0.90)
        reps = [5, 5, 3, 3, 3, 3]
    elif week == 3:  # weight is from week 2
        lbs = ceil((weight / 0.90))
        sets = build_sets(lbs, 0.95)
        reps = [5, 5, 3, 5, 3, 1]
    elif week is 'deload':  # weight is from week 3
        lbs = ceil(weight / 0.95)
        sets = build_sets(lbs, 0.60)
        reps = [5, 5, 5, 5, 5, 5]

    if units is "y":
        sets = lbs2kg(sets)
    sets = list(map(lambda x, y: str(x) + "x" + str(y), sets, reps))
    print(("{}: {}".format(name, ','.join(sets))))


def ask_user():
    """Start command-line prompt for user input."""
    # Ask for user input
    while True:
        try:
            process_input()
        except EOFError:
            break
