from typing import List, TypeVar
import copy
import re
import textwrap

import numpy as np

from crank.logging import logger
from crank.fto.cli import confirm_input


SET_REGEX = re.compile(r'\s*(?P<work>\d+)\s*x\s*(?P<reps>\d+)\s*')
# Used for type annotations
SetType = TypeVar('Set')


class Set:

    def __init__(self,
                 work=-1,
                 reps=0,
                 rest=-1,
                 order=-1,
                 special='') -> None:
        if isinstance(work, str):
            work = int(work)
        assert isinstance(work, int)
        self.work = work

        if isinstance(reps, str):
            reps = int(reps)
        assert isinstance(reps, int)
        self.reps = reps

        assert isinstance(order, int)
        self.order = order

        assert isinstance(rest, int)
        self.rest = rest

        assert isinstance(special, str)
        self.special = special

    @classmethod
    def parse_sets(cls, string):
        """Parse a .wkt-formatted string containing one or more Sets."""
        assert isinstance(string, str)
        sets = parse_simple_sets(string)
        return validate_sets(string, sets)

    def to_json(self):
        return {
            'work': self.work,
            'reps': self.reps,
            'order': self.order,
            'rest': self.rest,
            'special': self.special
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
        return ("Set(work={set.work}, "
                "reps={set.reps}, rest={set.rest}, "
                "order={set.order}").format(set=self)


def validate_sets(string, sets):
    """Validate our parsed Sets."""
    # Simple sets follow 'Work x Reps'; 1 Set per 2 Numbers
    estd_sets = len(re.findall(r'(\d+)', string)) / 2.
    if len(sets) != estd_sets or len(sets) != string.count('x'):
        logger.warning('%d sets anticipated, found %d', estd_sets, len(sets))
        raise SyntaxError('Failed to parse {}'.format(string))
    return sets


def parse_simple_sets(string):
    """Parse the most basic Set string: Work x Reps"""
    simple_re = r'(\d+)\s*x\s*(\d+)'
    sets = []
    for m in re.finditer(simple_re, string):
        sets.append(Set(work=int(m.groups()[0]),
                        reps=int(m.groups()[1])))
    return sets


def fix_set_string(string):
    """Guide the user through fixing their broken, broken Set string syntax."""
    print('We were unable to parse this string for Sets:\n{}'.format(string))
    s = input('Please re-type the string:\n')
    while not confirm_input(s):
        s = input('Please re-type corrections:\n')
    return s


def parse_complex_sets(string):
    """Iteratively parse a Set string."""
    logger.debug("Parsing Sets from: {}".format(string))
    chunk_re = r'(x|[^x,\s]+)'
    parser = re.finditer(chunk_re, string)

    # All numbers up to the first X are work sets
    work = []
    while True:
        val = next(parser).group().strip()
        if val == 'x':
            break
        work.append(val)
        logger.debug("Parsed: {:s}".format(val))
    # Assumption: All values up to the first 'x' have been parsed.
    logger.debug("Pre-loaded work: {:s}".format(str(work)))

    sets = []
    reps = []
    for m in parser:
        val = m.group().strip()
        if val == 'x':
            work, reps, sets = process_sets(work, reps, sets)
        else:
            reps.append(val)
            logger.debug("Reps: {:s}".format(str(reps)))
    else:  # Final processing
        work, reps, sets = process_sets(work, reps, sets, eof=True)
    # Nothing should be left in the work or reps buffers
    assert not work
    assert not reps
    return sets


def process_sets(work, reps, sets, eof=False):
    logger.debug(textwrap.dedent(
        """
        Before
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    # import pdb
    # pdb.set_trace()
    if len(work) > 1:  # Multiple work values stored
        logger.debug("Shorthand: Multiple sets @ same weight")
        assert reps, "Multiple work sets detected with no reps listed"
        demux_work(work, reps[0])
        work = reps[1:]  # Remainder *must* be new work values
    else:  # 1 work value(s), 0 to n reps
        logger.debug("Shorthand: Multiple sets @ same weight")
        assert len(work) == 1, "Expected one work value"
        w = work[0]
        if eof:  # No more to parse; it's all reps
            logger.debug("EOF sent; parsing all reps in relation to work")
            reps, new_work = reps, []
        else:
            # Find the best split between reps for this value of work and
            # the start of a new run of work values.
            reps, new_work = split_reps(w, reps)

        for r in reps:  # Process each rep
            sets.extend(process_rep(w, r, sets[-1]))

        work = new_work

    # Reps should *always* get reset
    reps = []

    logger.debug(textwrap.dedent(
        """
        After
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    return work, reps, sets


def split_reps(w, reps):
    logger.debug("Splitting {}".format(str(reps)))
    if len(reps) < 2:
        return reps, []
    idx, _ = max_slope(reps)
    r, w = reps[:idx], reps[idx:]
    logger.debug("\t{}\n\t{}".format(str(r), str(w)))
    return r, w


def process_rep(w, r, last_set):
    logger.debug("Processing :d{} x {:d}".format(w, r))
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


def demux_work(work, reps) -> (List[SetType]):
    """Parses a run of sets at the same level of work.

    Uses an error heuristic to determine where the next rep might actually be
    the start of new work levels. For example, '20 x 12, 13, 25, 30 x 6' should
    recognize that 25 was weight performed for 6 reps, not 25 reps at 20 lbs.
    """
    logger.debug("demux_work: {} x {}".format(work, str(reps)))
    sets = []
    for w in work:
        sets.append(Set(work=w, reps=reps[0]))
    return sets


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
    return np.argmax(slopes), slopes/np.max(slopes)


def work_rep_sim(work, reps):
    def sim(a, b):
        """Similarity between a and b. Lower is better."""
        return abs(a-b)

    sims = []
    for r in reps:
        sims.append((sim(work, r), sim(reps[0], r)))
    for i, s in enumerate(sims):
        # Change when the rep becomes more similar to the work
        # than the first rep
        if s[0] < s[1]:
            return i, sims
    return i, np.array(sims)/np.max([work]+reps)


def rest_pause(base_work, rp_str) -> List[SetType]:
    """Parses a rest-pause set into multiple sets."""
    sets = []
    rest_pause = rp_str.split('/')
    if len(rest_pause) > 1:
        logger.debug("\tRest-Pause set of {:d} x {} found".format(base_work,
                                                                  rp_str))
        for rep in rest_pause:
            sets.append(Set(work=base_work,
                            reps=int(rep.strip()),
                            rest=30  # A default
                            ))
    return sets


def multiply_reps(last_set, multiplier) -> List[SetType]:
    """Multiplies the previous set."""
    sets = []
    # Look for the multiplier notation: (\d+)
    m = re.match(r'\((\d+)\)', multiplier)
    if m:  # Rep multiplier; 100 x 3 (5)
        mult = int(m.groups()[0])
        logger.debug("\tMultiplying {:d} x {:d} for {:d} sets".format(
            last_set.work, last_set.reps, mult))
        # Make add'l copies of the previous set
        for i in range(mult-1):
            sets.append(copy.copy(last_set))

    return sets
