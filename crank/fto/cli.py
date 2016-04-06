# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto.logic`.
"""
from argparse import ArgumentParser
import string

from crank.fto.logic import print_exercise, MassUnit


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
    if valid_inputs:
        prompt += ' ' + str(valid_inputs) + ') '
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


def confirm_input(string):
    """Confirm the input looks good."""
    x = read_until_valid("Does this look good? [y/n] =>\n{}\n".format(string),
                         ['y', 'n'])
    return x == 'y'


def process_input():
    """Guide user through weight calculations via CLI prompts."""
    name = read_until_valid("Please enter the exercise name: ",
                            lmbda=lambda x: x.capitalize())
    kgs = read_until_valid("Kilograms? y/n: ", ('y', 'n'))
    week = read_until_valid("Enter current training week: ", lmbda=int)
    weight = read_until_valid("Enter max weight: ", lmbda=int)
    units = MassUnit.kilograms if kgs == 'y' else MassUnit.lbs
    if week == 1:
        increment = read_until_valid("How much are we adding? ", lmbda=int)
        weight += increment

    print_exercise(name, weight, week, units)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-n', '--name')
    parser.add_argument('-u', '--units', default='kg')
    parser.add_argument('--weight', type=int)
    parser.add_argument('--week', type=int)
    parser.add_argument('--increment', type=int)
    parser.add_argument('-m', '--max', type=int)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.name:
        if args.increment:
            args.weights += args.increment
        print_exercise(args.name, args.weight, args.week, MassUnit.kilograms)
    else:
        process_input()
