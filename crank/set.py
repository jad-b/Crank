import copy
import re
import textwrap
from typing import List, TypeVar

import numpy as np

SET_REGEX = re.compile(r'\s*(?P<work>\d+)\s*x\s*(?P<reps>\d+)\s*')


SetType = TypeVar('Set')


def process_sets(work, reps, sets, eof=True):
    print(textwrap.dedent(
        """
        Before
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    if len(work) > 1:  # Multiple work values stored
        print("Shorthand: Multiple sets @ same weight")
        assert reps, "Multiple work sets detected with no reps listed"
        mux_work(work, reps[0])
        work = reps[1:]  # All other must values be work values for new sets
    else:  # 0-1 work value(s), 0 to n reps
        if len(work) == 0:
            raise ValueError("No work values provided")
        else:  # 0 to n reps
            assert len(work) == 1, "Expected one work value"
            w = work[0]
            for r in reps:  # Process each rep
                sets.extend(process_rep(w, r, sets[-1]))
            work = [reps[-1]]

    # Reps should *always* get reset
    reps = []

    print(textwrap.dedent(
        """
        After
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    return work, reps, sets


def max_err(w, reps):
    """Calculate the maximum error between the work value and rep values."""
    def err(r, w):
        return abs((w-r)/w)

    # Calculate error between each supposed rep and the weight
    err_arr = np.apply_along_axis(err, 0, reps, *(w,))
    # Find the differences between each error
    return max_slope(err_arr)


def max_slope(reps):
    """Find the maximum slope between two points in an array."""
    slopes = [0]
    for i in range(1, len(reps)):
        slopes.append(abs(reps[i] - reps[i-1]))
    return np.argmax(slopes), slopes


def work_rep_sim(work, reps):
    def sim(a, b):
        """Similarity between a and b. Lower is better."""
        return pow(a-b, 2)

    sims = []
    for r in reps:
        sims.append((sim(work, r), sim(reps[0], r)))
    for i, s in enumerate(sims):
        # Change when the rep becomes more similar to the work
        # than the first rep
        if s[0] < s[1]:
            return i, sims
    return i, sims


def rest_pause(base_work, rp_str) -> List[SetType]:
    """Parses a rest-pause set into multiple sets."""
    sets = []
    rest_pause = rp_str.split('/')
    if len(rest_pause) > 1:
        for rep in rest_pause:
            sets.append(Set(work=base_work, reps=int(rep.strip())))
    return sets


def multiply_reps(last_set, multiplier) -> List[SetType]:
    """Multiplies the previous set."""
    sets = []
    # Look for the multiplier notation: (\d+)
    m = re.match(r'\((\d+)\)', multiplier)
    if m:  # Rep multiplier; 100 x 3 (5)
        mult = int(m.groups()[0])
        # Make add'l copies of the previous set
        for i in range(mult-1):
            sets.append(copy.copy(last_set))

    return sets


def process_rep(w, r, last_set):
    try:  # To save it as a normal rep
        r = int(r)
        # Compare against
        return [Set(work=w, reps=r)]
    except ValueError:
        # try our special cases
        setz = rest_pause(w, r)
        if setz:
            return setz
        setz = multiply_reps(last_set, r)
        if setz:
            return setz


def mux_work(work, reps) -> (List[SetType]):
    """Parses a run of sets at the same level of work.

    Uses an error heuristic to determine where the next rep might actually be
    the start of new work levels. For example, '20 x 12, 13, 25, 30 x 6' should
    recognize that 25 was weight performed for 6 reps, not 25 reps at 20 lbs.
    """
    sets = []
    for w in work:
        sets.append(Set(work=w, reps=reps[0]))
    return sets


def parse_sets(string):
    """Iteratively parse a Set string."""
    print("Parsing {} for Sets".format(string))
    parser = iter_set_parser(string)

    # All numbers up to the first X are work sets
    work = []
    while True:
        val = next(parser).group().strip()
        if val == 'x':
            break
        work.append(val)
        print("Parsed: {:s}".format(val))
    # Assumption: All values up to the first 'x' have been parsed.
    print("Pre-loaded work: {:s}".format(str(work)))

    sets = []
    reps = []
    for m in parser:
        val = m.group().strip()
        if val == 'x':
            work, reps, sets = process_sets(work, reps, sets)
        else:
            reps.append(val)
            print("Reps: {:s}".format(str(reps)))
    else:  # Final processing
        work, reps, sets = process_sets(work, reps, sets, eof=True)
    # Nothing should be left in the work or reps buffers
    assert not work
    assert not reps
    return sets


def iter_set_parser(string):
    """Creates an iterative set parser."""
    chunk_re = r'(x|[^x,\s]+)'
    return re.finditer(chunk_re, string)


class Set:

    def __init__(self,
                 work=-1,
                 work_unit='',
                 reps=0,
                 rep_unit='',
                 rest=-1,
                 order=-1) -> None:
        if isinstance(work, str):
            work = int(work)
        self.work = work
        assert isinstance(self.work, int)
        self.work_unit = work_unit

        if isinstance(reps, str):
            reps = int(reps)
        self.reps = reps
        assert isinstance(self.reps, int)
        self.rep_unit = rep_unit

        self.order = order
        assert isinstance(self.order, int)
        self.rest = rest
        assert isinstance(self.rest, int)

    @classmethod
    def parse_set(cls, string):
        """Parse a .wkt-formatted string containing a single Set."""
        return parse_sets(string)

    def to_json(self):
        return {
            'work': self.work,
            'reps': self.reps,
            'order': self.order,
            'rest': self.rest
        }

    @classmethod
    def from_json(cls, d):
        """Build a Set from a JSON object (dict)."""
        return cls(**d)

    def __lt__(self, other):
        """Sets are sorted by their workout order.

        It is invalid to compare Sets outside of the same Workout.
        """
        if not isinstance(other, Set):
            return NotImplemented
        return self.order < other.order

    def __eq__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        return (self.order == other.order and
                self.work == other.work and
                self.reps == other.reps and
                self.rest == other.rest)

    def __str__(self):
        return "Set({:d} x {:d})".format(self.work, self.reps)

    def __repr__(self):
        return ("Set(work={set.work}, work_unit={set.work_unit}, "
                "reps={set.reps}, rep_unit={set.rep_unit}, rest={set.rest}, "
                "order={set.order}").format(set=self)
