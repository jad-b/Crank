# -*- coding: utf-8 -*-
"""
crank.py
===
Calculates progressing reps and sets of an exercise.

Progresses in a pyramid-style scheme, where reps and sets are initially added,
and then consolidated once an arbitrary critical number of total reps have been
reached.
"""
from itertools import tee


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def crank(day, set_max, apex, name='', step=1, stall=1):
    """Generate a series of workouts."""
    def calc_base(day, set_max):
        return (set_max,) * (day // set_max)

    def add_last_set(sets, day, set_max):
        mod = day % set_max
        if mod != 0:
            sets += (mod,)
        return sets

    def distribute_excess(sets, excess):
        """Distribute reps, favoring earlier sets."""
        pass

    excess = day - apex if day > apex else 0
    if excess:
        day = apex - excess

    base = calc_base(day, set_max)
    sets = add_last_set(base, day, set_max)
    if excess:
        sets = distribute_excess(sets, excess)
    return sets


if __name__ == '__main__':
    exs = [('Push-ups', 10, 10, 30),
           ('Squats', 10, 10, 30),
           ('Dead Bugs', 1, 10, 30)]
