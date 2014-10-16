"""progression.py

Calculates progressing reps and sets of an exercise. Progresses in a pyramid-
style scheme, where reps and sets are initially added, and then consolidated
once an arbitrary critical number of total reps have been reached.
"""
from itertools import tee


class Exercise(object):

    def __init__(self, name='', reps=1, set_limit=10, rep_limit=100):
        self.name = name
        self.reps = reps
        self.set_limit = set_limit
        self.rep_limit = rep_limit
        self.sets = None
        # Initialize our starting set
        self.divvy_reps()

    def _drop_index(self, l):
        """Returns index of the first index in the list less than its
        predecessor"""

        def pairwise(iterable):
            """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)

        # Build
        try:
            # Find the index of the first decrement in the list
            idx = next((i + 1 for i, (a, b) in
                        enumerate(pairwise(l)) if b < a))
        except StopIteration:
            return 0
        # [6, 6, 6, 2] is always going to return 3, so we need to reset to
        # the first element
        # if we're at the end of the list, return the start
        if idx == len(l) - 1:
            return 0
        else:
            return idx

    def _crank(self, sets, s_limit=0):
        if s_limit:     # building
            if (sets[-1] + 1) > s_limit:
                sets.append(1)
            else:
                sets[-1] += 1
        else:           # aggregation
            sets[self._drop_index(sets)] += 1    # add to needy set
            if sets[-1] == 1:   # if last value is 1
                sets.pop()      # remove from list
            else:
                sets[-1] -= 1

        return sets

    def crank(self):
        if self.reps >= self.rep_limit:     # Aggregation phase
            if len(self.sets) == 1:         # Terminal growth
                return self
            s_limit = 0
        else:                               # Building phase
            s_limit = self.set_limit

        self.sets = self._crank(self.sets, s_limit)
        self.reps += 1
        return self

    def divvy_reps(self):
        # Fill AMAP sets up to our set limit
        sets = [self.set_limit for n in range(self.reps // self.set_limit)]
        # Handle any remaining reps
        spillover = self.reps % self.set_limit
        if spillover:
            sets.append(spillover)

        self.sets = sets
        return self.sets

    def lifetime(self):
        x = Exercise(self.name, 1, self.set_limit, self.rep_limit)
        while x.sets[0] != 2 * x.rep_limit:
            print(x)
            x.crank()

    def __str__(self):
        return "{}: {}".format(self.name, self.sets)


class Workout(object):
    def __init__(self, exercises=[]):
        """Instantiates a Workout and it's child Exercises

        :params exercises: List of Exercise objects to be managed by the
            Workout.
        """
        self.exercises = exercises
        self.workout = None

    def generate(self):
        """Update reps & sets for our tracked exercises"""
        self.workout = [ex.crank() for ex in self.exercises]
        return self.workout

    def __str__(self):
        """Returns a handy string representation of the current workout"""
        s = ""
        for ex in self.exercises:
            s += '{}\n'.format(ex)
        return s


def crank(apex=100, set_max=10, start=1):
    """Generator for set/rep schemes

    :param int apex: Top number of reps to perform *in toto*
    :param int set_max: Top number of reps to perform per set
    :param int start: Reps to start at. Numbers greater than
        `apex` indicate we're in the aggregative phase, and are
        consolidating reps into fewer sets.
    """
    def divvy():
        # Divvy up our reps into sets
        sets = [set_max] * (start // set_max)
        mod = start % set_max
        if mod:
            sets.append(mod)
        return sets

    sets = divvy()
    curr = start
    # Continue to crank until it's only one set
    while sets[0] apex:
        # Yield a sequence of reps
        yield sets

        # Crank
        if sum(sets) < apex:
            # Accumulate


        curr += 1

    assert len(sets) == 1, "Should terminate with one set left"




if __name__ == '__main__':
    exs = [Exercise('Push-ups', 10, 10, 30),
           Exercise('Squats', 10, 10, 30),
           Exercise('Dead Bugs', 1, 10, 30)]
    wkt = Workout(exs)
    print(wkt)
    for x in range(49):
        print(wkt.generate())
