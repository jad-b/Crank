# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto.logic`.
"""
import string

from fto.logic import print_exercise, MassUnit, get_max_from_previous


def process_input(units='lbs'):
    """Guide user through weight calculations via CLI prompts."""
    name = input("Please enter the exercise name: ")\
        .strip(string.whitespace)
    kgs = input("Kilograms? y/n: ").strip(string.whitespace)
    units = MassUnit.kgs if kgs == 'y' else MassUnit.lbs
    week = int(input("Enter current training week: "))

    if week == 1:
        prev_weight = int(input('Enter previous weight: '))
        increment = int(input("How much are we adding? "))
        weight = get_max_from_previous(prev_weight, week, increment, units)
    else:
        weight = int(input("Enter max weight: "))
        increment = 0

    print_exercise(name, weight, week, increment, units)

if __name__ == '__main__':
        process_input()
