# -*- coding: utf-8 -*-
"""
crank.py
===
Calculates progressing reps and sets of an exercise.

Progresses in a pyramid-style scheme, where reps and sets are initially added,
and then consolidated once an arbitrary critical number of total reps have been
reached.
"""


class Cranky(object):

    def __init__(self, day, set_max, apex, name):
        """Create a Crank workout for a given day.

        :arg int day: Day inside workout to begin. Valid values are from
            1 to 2 * `apex`.
        :arg int set_max: Number of reps allowed per set.
        :arg int apex: Total number of reps allowed within workout.
        :kwarg str name: Name of the exercise.
        :kwarg int step: Increment to add to sets.
        :kwarg int stall: Number of sesions to wait before incrementing. Think
            of it as acting like a buffer.
        """
        self.day = day
        self.set_max = set_max
        self.apex = apex
        self.name = name
        self.sets = self.crank()

    def calc_base(self, day, set_max):
        """Create the base number of complete sets."""
        return (set_max,) * (day // set_max)

    def crankable(self):
        """Predicate by which we declare ourselves "not done"."""
        return True

    def crank(self):
        raise NotImplemented

    def __iter__(self):
        while self.crankable():
            yield self.crank()


class Accumulator(Cranky):
    """Manages the accumulating phase of Crank.

    Reps are appended to the last set
    When the last set is at SET_MAX, a new set is created.
    When the sum of all reps is at APEX, an :class:`Aggregator` is returned.
    """

    def crank(self):
        """Generate a series of workouts."""
        if self.day > self.apex:
            return Aggregator(self)

        # Caclulate our *base* set of reps
        base = self.calc_base(self.day, self.set_max)
        self.sets = self.add_last_set(base, self.day, self.set_max)
        self.day += 1
        return self.sets

    def add_last_set(self, sets, day, set_max):
        """Add tailing set."""
        mod = day % set_max
        if mod != 0:
            sets += (mod,)
        return sets


class Aggregator(Cranky):
    """Manages the aggregation phase of Crank."""

    def __init__(self, day, set_max=10, apex=100, name='', acc=None):
        if day < apex:
            return Accumulator(day, set_max, apex, name)

        if acc is not None:
            self.build_from_accumulator(acc)
        else:
            self.day = day
            self.set_max = set_max
            self.apex = apex
            self.name = name

        assert self.day <= 2 * self.apex - self.set_max

        self.sets = list(self.calc_base(self.apex, self.set_max))

        self.index = 0  # Always start by pointing to the first set
        self.catch_up(apex, day)

    def build_from_accumulator(self, acc):
            self.day = acc.day
            self.set_max = acc.set_max
            self.apex = acc.apex
            self.name = acc.name
            self.sets = acc.sets

    def catch_up(self, curr, final):
        """Crank down to the current day's reps."""
        while curr < final:
            self.crank()
            curr += 1

    def crank(self):
        if self.day == self.sets[0]:
            return self.sets

        # Subtract one off the end
        self.sets[-1] -= 1
        # If end is zero, remove from list
        if self.sets[-1] == 0:
            self.sets.pop()

        # Add one to set at index
        self.sets[self.index] += 1

        # Update index
        self.index = (self.index + 1) % len(self.sets[:-1])

        print(self.sets, self.index)
        return self.sets
