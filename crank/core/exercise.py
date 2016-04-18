from collections.abc import Iterable, Mapping
from pprint import pformat

from crank.core.set import Set
from crank.core.tags import parse_tags
from crank.util.logging import logger


class Exercise:

    def __init__(self,
                 name='',
                 sets=None,
                 raw_sets='',
                 tags=None):
        self.name = name
        assert isinstance(self.name, str)
        self.sets = sets or []
        assert isinstance(self.sets, Iterable)
        self.tags = tags or {}
        assert isinstance(self.tags, Mapping)
        self.raw_sets = raw_sets
        assert isinstance(self.raw_sets, str)

    @classmethod
    def parse(cls, lines):
        ex = {}
        ex['name'], remainder = parse_exercise_name(lines[0])
        lines = lines[1:]
        # Tags
        ex['tags'], lines = parse_tags(lines)
        # Sets
        try:
            ex['sets'], lines = Set.parse_sets(lines)
        except ValueError:
            ex['sets'], ex['raw_sets'] = Set.parse_sets(remainder)
        return Exercise(**ex), lines

    @classmethod
    def parse_exercises(cls, lines):
        exs = []
        while len(lines) > 0:
            ex, lines = Exercise.parse(lines)
            exs.append(ex)
            logger.debug("Parsed Exercise:\n%s", ex)
            # logger.debug("Remaining lines:\n%s", pformat(lines))
        assert not lines, "Unparsed lines after exercise parsing"
        return exs

    def upgrade(self):
        if self.raw_sets:
            try:
                self.sets = Set.parse_sets(self.raw_sets)
                self.raw_sets = ''
            except SyntaxError:
                logger.warning("Failed to parse %s", self.raw_sets)

    def to_json(self):
        d = {
            'name': self.name,
            'tags': self.tags,
            'sets': [s.to_json() for s in self.sets]
        }
        if self.raw_sets:
            d['raw_sets'] = self.raw_sets
        return d

    @classmethod
    def from_json(cls, d):
        return cls(**{
            'name': d.get('name'),
            'tags': d.get('tags'),
            'sets': [Set.from_json(s) for s in d.get('sets', [])],
            'raw_sets': d.get('raw_sets')
        })

    def __eq__(self, o):
        if not isinstance(o, Exercise):
            return NotImplemented
        return (self.name == o.name and
                self.tags == o.tags and
                self.sets == o.sets and
                self.raw_sets == o.raw_sets)

    def __str__(self):
        return pformat(self.to_json())

    def __repr__(self):
        return 'Exercise<{}>'.format(self.name)


def parse_exercise_name(line):
    try:
        name_sets = line.split(':')
        if len(name_sets) != 2:
            return name_sets[0]
        return name_sets[0], name_sets[1]
    except Exception:
        logger.exception('Error while parsing exercise name from %s', line)
        return line
