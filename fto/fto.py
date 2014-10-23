# -*- coding: utf-8 -*-
"""
fto.py
===
Calculator for weights on the 5/3/1 plan by Jim Wendler.
"""
from enum import Enum
from math import ceil as fine_ceil
from .util import (ceiling as coarse_ceil,
                   map_weeks, zip_sets, lbs2kg)


class MassUnit(str, Enum):
    """Enum for standardizing unit of mass abbreviations."""
    pounds = 'lbs'
    lbs = pounds
    kilograms = 'kgs'
    kgs = kilograms

weeks = map_weeks()


def _get_ceiling(unit=MassUnit.lbs):
    """Return correct ceiling function by units.

    Python's `ceil` function rounds to the nearest integer, while 5/3/1 calls
    for rounding to the nearest multiple of five. We use the finer-grained
    :func:`ceil` when in kilograms, since jumps of 1 kg are possible.
    """
    return coarse_ceil if unit == MassUnit.lbs else fine_ceil


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
    max_weight = prev_weight / weeks[prev_week].percent
    return max_weight


def calc_warmup_sets(max_weight, unit=MassUnit.lbs):
    """Return warm-up sets, based on top weight of the day."""
    percents = (0.4, 0.5, 0.6)
    ceiling_func = _get_ceiling(unit)
    calc_warmups = lambda percent: ceiling_func(max_weight * percent)
    return list(map(calc_warmups, percents))


def build_sets(prev_weight, curr_week, unit=MassUnit.lbs, increment=0):
    """Create sets based off last week's top weight.

    :param int max_weight: Training max weight.
    :param float top_percent: Percentage of our one rep max the top working
        set will be calculated at.
    :param str unit: Whether to calculate in lbs or kgs
    """
    ceiling_func = _get_ceiling(unit)
    max_weight = _get_max_from_previous(prev_weight, curr_week)
    # Bump weight if this is the start of a new cycle
    max_weight += increment if curr_week == 1 else 0
    # Create warm-up sets
    sets = calc_warmup_sets(max_weight, unit)

    for i in (2, 1, 0):
        # Ramp up our percents
        training_percent = weeks[curr_week].percent - 0.1 * i
        weight = ceiling_func(max_weight * training_percent)
        sets.append(weight)
    if unit is MassUnit.kilograms:
        sets = lbs2kg(sets)
    return sets


def print_exercise(prev_weight, week, unit, increment=5):
    """Build sets for a given exercise.

    :param prev_weight: Top working-set weight used last week.
    :param int week: Which week you're currently on; the week you want the
        weights calculated for. Accepts 1-3.
    """
    # Don't forget to add weight if you're calculating off week 3 weight!
    weights = build_sets(prev_weight, week, unit, increment)
    # Output w/ reps
    print('\n<=== Sets (Week {}) ===>'.format(week))
    print(zip_sets(weights, week))

    if unit == MassUnit.lbs:
        print('- In kgs, (-20): {}\n'
              .format(zip_sets(lbs2kg(weights, sub=20), week)))


if __name__ == "__main__":
    last_weeks_weight = 207
    current_training_week = 3
    # units = MassUnit.kgs
    units = MassUnit.lbs
    print_exercise(last_weeks_weight, current_training_week, units)
