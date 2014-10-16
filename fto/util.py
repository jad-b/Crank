# -*- coding: utf-8 -*-
"""
util.py
===
Utility functions for :module:`fto`.
"""
import math
from collections import namedtuple

Week = namedtuple('Week', ['percent', 'reps'])


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


def ceiling(f):
    """Find ceiling of number, a la 5/3/1 method."""
    # Apply modulus to weight in increments of 5
    mod = math.fmod(f, 5)
    # Short heuristic to determine rounding
    if mod > 2.5:  # round up
        return math.trunc(f - mod + 5)
    else:  # round down
        return math.trunc(f - mod)


def lbs2kg(sets, sub=0):
    """Convert a set of weights in pounds to kilograms.

    :param list sets: Iterable of prescribed weights.
    :param int sub: Amount to subtract from each converted weight. Useful
    for when taking into account bar weight.
    """
    lb_kg = lambda w: int(round(w / 2.20462) - sub)
    return (lb_kg(x) for x in sets)


def one_rep(weight, week=1, inc=5):
    """Calculate one rep max from week's percentage."""
    percents = (0.85, 0.9, 0.95)
    percent = percents[week]
    return weight / percent + inc if week == 3 else 0


def zip_sets(weights, week=1):
    """Attach repeptitions to given weights."""
    warm_up_reps = (5, 5, 3)
    reps = warm_up_reps + _weeks[week-1]
    sets = zip(weights, reps)
    output = ''
    for s in sets:
        output += ' {} x {},'.format(s[0], s[1])
    return output.rstrip(', ')
