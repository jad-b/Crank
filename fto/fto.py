# -*- coding: utf-8 -*-
"""
fto.py
===
Calculator for weights on the 5/3/1 plan by Jim Wendler.
"""
from math import ceil as fine_ceil
from .util import (ceiling as coarse_ceil,
                   map_weeks, zip_sets, lbs2kg)


weeks = map_weeks()


def _get_ceiling(unit='lbs'):
    """Return correct ceiling function by units.

    Python's `ceil` function rounds to the nearest integer, while 5/3/1 calls
    for rounding to the nearest multiple of five. We use the finer-grained
    :func:`ceil` when in kilograms, since jumps of 1 kg are possible.
    """
    return coarse_ceil if unit == 'lbs' else fine_ceil


def _get_max_from_previous(prev_weight, curr_week):
    """Calculate this mesocycle's top weight by using last week's weight."""
    # Get our maximum weight for this mesocycle (~month)
    # Do so by dividing last week's weight by last week's percentage
    last_week = curr_week - 1
    # Feeling dumb, so I can't get this modulo to work out right.
    # 3 => 2
    # 2 => 1
    # 1 => 3 (Skips zero)
    prev_week = last_week if last_week != 0 else len(weeks) - 1
    return prev_weight / weeks[prev_week].percent


def calc_warmup_sets(max_weight, unit='lbs'):
    """Return warm-up sets, based on top weight of the day."""
    percents = (0.4, 0.5, 0.6)
    ceiling_func = _get_ceiling(unit)
    calc_warmups = lambda percent: ceiling_func(max_weight * percent)
    return list(map(calc_warmups, percents))


def build_sets(prev_weight, curr_week, unit='lbs'):
    """Create sets based off last week's top weight.

    :param int max_weight: Training max weight.
    :param float top_percent: Percentage of our one rep max the top working
        set will be calculated at.
    :param str unit: Whether to calculate in lbs or kgs
    """
    ceiling_func = _get_ceiling(unit)
    max_weight = _get_max_from_previous(prev_weight, curr_week)
    # Create warm-up sets
    sets = calc_warmup_sets()

    for i in (2, 1, 0):
        # Subtract 10% to only use a 90% training max
        # We work our way up to the top percent
        training_percent = weeks[curr_week].percent - 0.1 * i
        weight = ceiling_func(training_percent * max_weight)
        sets.append(weight)
    if unit is "kg":
        sets = lbs2kg(sets)
    return sets


def print_exercise(prev_weight, week):
    """Build sets for a given exercise.

    :param prev_weight: Top working-set weight used last week.
    :param int week: Which week you're currently on; the week you want the
        weights calculated for. Accepts 1-3.
    """
    # Don't forget to add weight if you're calculating off week 3 weight!
    weights = build_sets(max_weight=127/0.85, new_percent=0.90)
    # Output w/ reps
    print('\n<=== Sets (Week {d}) ===>'.format(week))
    print(zip_sets(weights, week))
    print('- In kgs, (-20): {}\n'
          .format(zip_sets(lbs2kg(weights, sub=20), week)))


if __name__ == "__main__":
    last_weeks_weight = 185
    current_training_week = 1
    print_exercise(last_weeks_weight, current_training_week)
