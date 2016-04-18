import copy
import re


SET_REGEX = re.compile(
    r'''
    \s*
    (?P<work>\d+)
    \s* x \s*
    (?P<reps>\d+)
    \s*''', re.X)


class Set:

    def __init__(self,
                 work=0,
                 reps=0,
                 rest=0,
                 order=0) -> None:
        self.work = work or 0
        assert isinstance(self.work, int)
        self.reps = reps or 0
        assert isinstance(self.reps, int)
        self.rest = rest or 0
        assert isinstance(self.rest, int)
        self.order = order or 0
        assert isinstance(self.order, int)

    @classmethod
    def parse(cls, string):
        SET_V2_RE = r'''
            \s*
            (?P<order>[\d,-]+)\)
            \s*
            (\[(?P<rest>\d+)\])?
            \s*
            ((?P<work>\d+) \s* x \s*)?
            \s*
            (?P<reps>\d+)
            '''
        ptn = re.compile(SET_V2_RE, flags=re.X)
        m = ptn.match(string)
        if not m:
            return []
        # Pass it through the Set Constructor to filter out values
        gd = m.groupdict()
        vals = {}
        for attr in ['work', 'reps', 'rest']:
            v = gd.get(attr)
            if v:
                vals[attr] = int(v)
        base = Set(**vals)

        sets = []
        for o in parse_ordering(gd['order']):
            s = copy.copy(base)
            s.order = o
            sets.append(s)
        return sets

    @classmethod
    def parse_sets(cls, lines):
        """Parse a .wkt-formatted string containing one or more Sets."""
        sets = []
        for l in lines:
            ret = cls.parse(l)
            if not ret:
                break
            sets.extend(ret)
        if not sets:
            raise ValueError("No sets parsed")
        return sets, lines[len(sets):]

    def to_json(self):
        d = {}
        for attr in ['work', 'reps', 'rest', 'order']:
            v = getattr(self, attr)
            if v:
                d[attr] = v
        return d

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
                "order={set.order})").format(set=self)


def parse_ordering(string):
    parts = string.strip(', ')
    for s in parts.split(','):
        val = s.strip()
        try:
            yield int(val)
        except:
            m = re.match(r'(\d+)-(\d+)', val)
            if not m:
                raise
            for n in range(int(m.groups()[0]), int(m.groups()[1])+1):
                yield n
