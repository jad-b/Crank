# -*- coding: utf-8 -*-
"""
util.py
===
Utility functions for :module:`fto`.
"""
from collections import namedtuple
from enum import Enum

Week = namedtuple('Week', ['percent', 'reps'])


class MassUnit(str, Enum):
    """Enum for standardizing unit of mass abbreviations."""
    pounds = lbs = 'lbs'
    kilograms = kgs = 'kgs'


def map_weeks():
    """Map training week to prescribed percent and repetitions."""
    reps_by_week = (
        (5, 5, 10),
        (3, 3, 8),
        (5, 3, 5)
    )
    percents_by_week = (0.85, 0.90, 0.95)

    return [None] + list(map(Week, percents_by_week, reps_by_week))

# First index is empty to allow for direct indexing by week number
_weeks = map_weeks()


def mround(x, units=MassUnit.lbs):
    """Find ceiling of number, a la 5/3/1 method.

    Name is taken from the equivalent Google Spreadsheet formula.

    :param int x: Number to round.
    :para int base: Integer multiple to round to.
    """
    base = 1 if units == MassUnit.kgs else 5
    # Round to 5 lbs if in pounds, else go by 1 kg increments
    return int(base * round(float(x) / base))


def lbs2kg(sets, sub=0):
    """Convert a set of weights in pounds to kilograms.

    :param list sets: Iterable of prescribed weights.
    :param int sub: Amount to subtract from each converted weight. Useful
    for when taking into account bar weight.
    """
    lb_kg = lambda w: int(round(w / 2.20462) - sub)
    return (lb_kg(x) for x in sets)


def kgs2lbs(sets, sub=0):
    """Convert a set of weights in kilograms to pounds.

    :param list sets: Iterable of prescribed weights.
    :param int sub: Amount to subtract from each converted weight. Useful
    for when taking into account bar weight.
    """
    kg_lb = lambda w: int(round(w * 2.20462) - sub)
    return (kg_lb(x) for x in sets)


def one_rep(weight, week=1, inc=5):
    """Calculate one rep max from week's percentage."""
    percents = (0.85, 0.9, 0.95)
    percent = percents[week-1]
    return weight / percent + inc if week == 3 else 0


def zip_sets(weights, week=1):
    """Attach repeptitions to given weights."""
    warm_up_reps = (5, 5, 3)
    reps = warm_up_reps + _weeks[week].reps
    sets = zip(weights, reps)
    output = ''
    for s in sets:
        output += ' {} x {},'.format(s[0], s[1])
    return output.rstrip(', ')
