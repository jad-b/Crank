# -*- coding: utf-8 -*-
"""
cli.py
===
User-facing command-line functions for :module:`fto.logic`.
"""
from argparse import ArgumentParser

from crank.fto.logic import print_exercise, MassUnit
from crank.util.cli import read_until_valid


def process_input():
    """Guide user through weight calculations via CLI prompts."""
    name = read_until_valid("Please enter the exercise name: ",
                            lmbda=lambda x: x.capitalize())
    kgs = read_until_valid("Kilograms?", ('y', 'n'))
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
