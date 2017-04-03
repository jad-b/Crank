import copy
import itertools
import re


SET_ORDERING_RE = re.compile(r'''
    \s*
    (?P<order>[\d\s,-]+)\)
    \s*
    ''', re.X)
SET_RE = re.compile(r'''
    (\[(?P<rest>\d+)\])?
    \s*
    ((?P<work>\d+) \s* x \s*)?
    \s*
    (?P<reps>\d+)
    ''', re.X)


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
        # parse ordering groups
        order_groups, set_str = parse_ordering(string)
        # parse set information
        sets = parse_set_body(set_str)

        final = []
        # Many-to-one order-to-set notation
        #   4-6) [30] 114 x 8
        if len(sets) == 1 and len(order_groups) >= 1:
            base = sets[0]
            for o in itertools.chain(*order_groups):
                s = copy.copy(base)
                s.order = o
                final.append(s)
        # One-to-one order-to-set notation
        #   1-3,5-7) 100 x 8, 110x9
        elif len(order_groups) == len(sets):
            for i, og in enumerate(order_groups):  # [(1,2,3), (5,6,7)]
                for o in og:  # (1,2,3)
                    s = copy.copy(sets[i])
                    s.order = o
                    final.append(s)
        # One-to-Many notation
        #   1-3) 100x8, 110x7, 120x 6
        elif (len(order_groups) == 1 and
              len(order_groups[0]) == len(sets)):
            for i, o in enumerate(order_groups[0]):
                sets[i].order = o
                final.append(sets[i])
        else:
            raise ValueError("Set notation mismatch")
        return final

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
        s = ''
        if self.rest:
            s += '[' + str(self.rest) + '] '
        if self.work:
            s += str(self.work) + ' x '
        return s + str(self.reps)

    def __repr__(self):
        return ("Set(work={set.work}, "
                "reps={set.reps}, rest={set.rest}, "
                "order={set.order})").format(set=self)


def parse_ordering(string):
    m = SET_ORDERING_RE.match(string)
    if not m:
        raise ValueError(string + " isn't a recognized set string")
    parts = m.groupdict()['order'].strip(', ')
    ordering = []
    for s in parts.split(','):
        val = s.strip()
        try:
            ordering.append((int(val),))
        except ValueError:
            n = re.match(r'(\d+)-(\d+)', val)
            if not n:
                raise
            # 'a-d) ...' => (a,b,c,d)
            ordering.append(tuple(range(int(n.groups()[0]),
                                        int(n.groups()[1])+1)))
    return ordering, m.string[m.end():]


def parse_set_body(string):
    sets = []
    for m in SET_RE.finditer(string):
        gd = m.groupdict()
        # Pass it through the Set Constructor to filter out values
        vals = {}
        for attr in ['work', 'reps', 'rest']:
            v = gd.get(attr)
            if v:
                vals[attr] = int(v)
        sets.append(Set(**vals))
    return sets
