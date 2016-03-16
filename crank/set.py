import re


SET_REGEX = re.compile(r'\s*(?P<work>\d+)\s*x\s*(?P<reps>\d+)\s*')


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
    def parse_sets(cls, string):
        """Parse a .wkt-formatted string of multiple Sets."""
        assert isinstance(string, str)
        sets = []
        # Split string
        split = string.split(',')
        for set_string in split:
            s_dict = SET_REGEX.match(set_string).groupdict()
            sets.append(Set(**s_dict))
        return sets

    @classmethod
    def parse_set(cls, string):
        """Parse a .wkt-formatted string containing a single Set."""
        assert isinstance(string, str)
        return cls()

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
