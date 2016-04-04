from collections.abc import Iterable, Mapping
from pprint import pformat

from crank.logging import logger
from crank.tags import parse_tags
from crank.set import Set


def parse_exercises(lines):
    exs = []
    while len(lines) > 0:
        ex, lines = parse_exercise(lines)
        exs.append(ex)
        logger.debug("Parsed Exercise:\n%s", ex)
        # logger.debug("Remaining lines:\n%s", pformat(lines))
    return exs


def parse_exercise(lines):
    # logger.debug("Parsing Exercise from:\n%s", lines)
    # Exercise name & sets
    ex = {}
    ex['name'], ex['raw_sets'] = parse_exercise_name(lines[0])
    ex['raw_sets'] = ex['raw_sets'].strip()
    ex['name'] = ex['name'].strip()
    lines = lines[1:]
    # Tags
    if lines:
        ex['tags'], lines = parse_tags(lines)
    # Sets
    try:
        ex['sets'] = Set.parse_sets(ex['raw_sets'])
        ex.pop('raw_sets')  # Remove raw string after successful parse
    except SyntaxError:
        logger.warning("Failed to parse %s", ex['raw_sets'])
    return Exercise(**ex), lines


def parse_exercise_name(line):
    try:
        name_sets = line.split(':')
        if len(name_sets) != 2:
            return line
        return name_sets[0], name_sets[1]
    except Exception:
        logger.exception('Error while parsing exercise name from %s', line)
        return line


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
    def parse_exercise(cls, lines):
        ex, lines = parse_exercise(lines)
        # No lines should be leftover
        assert not lines, "Content remaining after parsing: {}".format(lines)
        return ex

    def upgrade(self):
        if self.raw_sets:
            try:
                self.sets = Set.parse_sets(self.raw_sets)
                self.raw_sets = ''
            except SyntaxError:
                logger.warning("Failed to parse %s", self.raw_sets)

    def to_json(self):
        return {
            'name': self.name,
            'tags': self.tags,
            'sets': [s.to_json() for s in self.sets],
            'raw_sets': self.raw_sets
        }

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
