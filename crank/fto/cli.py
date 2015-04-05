# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto.logic`.
"""
import string

from .logic import print_exercise, MassUnit, get_max_from_previous


def process_input(units='lbs'):
    """Guide user through weight calculations via CLI prompts."""
    name = input("Please enter the exercise name: ")\
        .strip(string.whitespace)
    kgs = input("Kilograms? y/n: ").strip(string.whitespace)
    units = MassUnit.kgs if kgs == 'y' else MassUnit.lbs
    week = int(input("Enter current training week: "))

    weight = int(input("Enter max weight: "))
    if week == 1:
        increment = int(input("How much are we adding? "))
        weight += increment
    else:
        increment = 0

    print_exercise(name, weight, week, units)

if __name__ == '__main__':
        process_input()
