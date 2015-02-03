# -*- coding: utf-8 -*-
"""
fto.py
===
Calculator for weights on the 5/3/1 plan by Jim Wendler.
"""
from crank.common import get_timestamp_header
from .util import mround, map_weeks, zip_sets, lbs2kg, MassUnit


weeks = map_weeks()


def get_max_from_previous(prev_weight, curr_week, increment=5,
                          units=MassUnit.lbs, smooth=False):
    """Calculate this mesocycle's top weight by using last week's weight.

    :param int prev_weight: Top planned weight from previous workout.
    :param int curr_week: Current week.
    :param int increment: Amount to auto-increase the max by, if this is the
    start of a new cycle.
    :param bool smooth: Whether or not to round the max to the nearest unit
    multiple (1 for kilograms, 5 if in pounds).
    :param units: Pounds or kilograms.
    :type units: :class:`MassUnit`.
    """
    last_week = curr_week - 1
    # Feeling dumb, so I can't get this modulo to work out right.
    # 3 => 2
    # 2 => 1
    # 1 => 3 (Skips zero)
    prev_week = last_week if last_week != 0 else len(weeks) - 1
    # Lookup last week's percentage
    max_weight = prev_weight / weeks[prev_week].percent
    # Increment if this is the start of a new cycle
    max_weight += increment if curr_week == 1 else 0
    if smooth:
        max_weight = mround(max_weight, units)
    return max_weight


def calc_warmup_sets(max_weight, units=MassUnit.lbs):
    """Return warm-up sets, based on top weight of the day."""
    percents = (0.4, 0.5, 0.6)
    calc_warmups = lambda percent: mround(max_weight * percent, units)
    return list(map(calc_warmups, percents))


def build_sets(max_weight, percent, units=MassUnit.lbs):
    """Create sets based off last week's top weight.

    :param int max_weight: 1RM for the exercise.
    :param float percent: Percentage of our one rep max the top working
        set will be calculated at.
    :param str units: Whether to calculate in lbs or kgs.
    """
    warm_ups = calc_warmup_sets(max_weight, units)
    steps = (0.2, 0.1, 0)
    sets = list(map(lambda x: mround(max_weight * (percent - x)), steps))
    return warm_ups + sets


def plan_cycle(max_weight):
    """Calculate one complete cycle.

    :param int prev_weight: Peak *planned* weight used during last cycle.
    """
    return [build_sets(max_weight, weeks[w].percent)
            for w in range(1, len(weeks))]


def print_exercise(name, max_weight, week, units=MassUnit.lbs):
    """Build sets for a given exercise.

    :param prev_weight: Top working-set weight used last week.
    :param int week: Which week you're currently on; the week you want the
        weights calculated for. Accepts 1-3.
    """
    # Don't forget to add weight if you're calculating off week 3 weight!
    weights = build_sets(max_weight, weeks[week].percent, units)
    # Output w/ reps
    print('\n<=== Sets (Week {}) ===>'.format(week))
    print(get_timestamp_header())
    print('- Training max: {}'.format(max_weight))
    print('{}:'.format(name), zip_sets(weights, week))

    if units == MassUnit.lbs:
        print('- In kgs, (-20): {}\n'
              .format(zip_sets(lbs2kg(weights, sub=20), week)))


if __name__ == "__main__":
    name = ''
    last_weeks_weight = 207
    current_training_week = 3
    # units = MassUnit.kgs
    units = MassUnit.lbs
    print_exercise(name, last_weeks_weight, current_training_week, units)
