import copy
import re
import textwrap

from typing import List, TypeVar

SET_REGEX = re.compile(r'\s*(?P<work>\d+)\s*x\s*(?P<reps>\d+)\s*')


SetType = TypeVar('Set')


def process_sets(work, reps, sets):
    print(textwrap.dedent(
        """
        Before
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    if not reps:  # End-of-string parsing
        reps = work  # All our stored 'work' is actually reps
        work = []
        base = sets[-1]
        # Apply reps to last parsed set
        for r in reps:
            rest_pause = r.split('/')
            if len(rest_pause) > 1:
                for rep in rest_pause:
                    sets.append(Set(work=base.work, reps=int(rep)))
            else:
                s = copy.copy(base)  # Copy last set
                s.reps = int(rep)  # Modify reps
                sets.append(s)  # append
    if len(work) > 1:
        print("Shorthand for multiple weight/same rep detected")
        for w in work:
            sets.append(Set(work=w, reps=reps[0]))
        work = reps[1:]
    else:
        print("Shorthand for same weight/multiple reps detected")
        w = work[0]
        for r in reps[:-1]:  # Process each rep
            m = re.match(r'\((\d+)\)', r)
            if m:  # Rep multiplier; 100 x 3 (5)
                mult = int(m.groups()[0])
                base = sets[-1]
                # Make add'l copies of the previous set
                for i in range(mult-1):
                    sets.append(copy.copy(base))
            else:  # Nothing special
                sets.append(Set(work=w, reps=r))
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


def rest_pause(weight, rp_str) -> List[SetType]:
    """Parses a rest-pause set into multiple sets."""
    return []


def multiply_reps(last, multiplier) -> List[SetType]:
    """Multiplies the previous set."""
    return []


def same_work(w, reps) -> (List[SetType], List[int]):
    """Parses a run of sets at the same level of work.

    Uses an error heuristic to determine where the next rep might actually be
    the start of new work levels. For example, '20 x 12, 13, 25, 30 x 6' should
    recognize that 25 was weight performed for 6 reps, not 25 reps at 20 lbs.
    """
    return [], []


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
    import pdb; pdb.set_trace()
    for m in parser:
        val = m.group().strip()
        if val == 'x':
            work, reps, sets = process_sets(work, reps, sets)
        else:
            reps.append(val)
            print("Reps: {:s}".format(str(reps)))
    else:  # Final processing
        work, reps, sets = process_sets(work, reps, sets)
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
