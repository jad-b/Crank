# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto`.
"""
import string

from .fto import print_exercise, MassUnit


def process_input(units='lbs'):
    """Guide user through weight calculations via CLI prompts."""
    name = input("Please enter the exercise name: ")\
        .strip(string.whitespace)
    kgs = input("Kilograms? y or n: ").strip(string.whitespace)
    weight = int(input("Enter last week's max weight: "))
    week = int(input("Enter current training week:"))

    units = MassUnit.kgs if kgs else MassUnit.lbs
    print_exercise(name, weight, week, units)

if __name__ == '__main__':
            process_input()
