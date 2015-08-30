# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto.logic`.
"""
import string

from .logic import print_exercise, MassUnit, get_max_from_previous


def read_until_valid(prompt, valid_inputs=None, lmbda=None):
    """Loop until a valid input has been received.

    It is up to the caller to handle exceptions that occur outside the realm of
    calling their lambda, such as KeyboardInterrupts (^c, a.k.a C-c).

    :arg str prompt: Prompt to display.
    :kwarg ``Iterable`` valid_inputs: Acceptable inputs. If none are provided,
        then the first non-exceptional value entered will be returned.
    :arg ``func`` lmbda: Function to call on received inputs. Any errors will
        result in a re-prompting.
    """
    while True:
        user_input = input(prompt).strip(string.whitespace)
        # Apply a given function
        if lmbda is not None:
            try:
                user_input = lmbda(user_input)
            except:         # Any errors are assumed to be bad input
                continue    # So keep trying
        if valid_inputs is not None:
            if user_input in valid_inputs:
                return user_input
        else:
            return user_input



def process_input(units='lbs'):
    """Guide user through weight calculations via CLI prompts."""
    name = read_until_valid("Please enter the exercise name: ",
            lmbda=lambda x: x.capitalize())
    kgs = read_until_valid("Kilograms? y/n: ", ('y', 'n'))
    week = read_until_valid("Enter current training week: ", lmbda=int)
    weight = read_until_valid("Enter max weight: ", lmbda=int)

    units = MassUnit.kgs if kgs == 'y' else MassUnit.lbs
    if week == 1:
        increment = read_until_valid("How much are we adding? ", lmbda=int)
        weight += increment
    else:
        increment = 0

    print_exercise(name, weight, week, units)

if __name__ == '__main__':
        process_input()
