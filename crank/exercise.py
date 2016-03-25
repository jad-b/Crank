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
        logger.debug("Remaining lines:\n%s", pformat(lines))
    return exs


def parse_exercise(lines):
    logger.debug("Parsing Exercise from:\n%s", lines)
    # Exercise name & sets
    ex = {}
    ex['name'], ex['sets'] = parse_exercise_name(lines[0])
    ex['name'] = ex['name'].strip()
    lines = lines[1:]
    # Tags
    if lines:
        ex['tags'], lines = parse_tags(lines)
    # Sets
    ex['sets'] = Set.parse_sets(ex['sets'].strip())
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
                 tags=None):
        self.name = name
        assert isinstance(self.name, str)
        self.sets = sets or []
        assert isinstance(self.sets, Iterable)
        self.tags = tags or {}
        assert isinstance(self.tags, Mapping)

    @classmethod
    def parse_wkt(cls, lines):
        ex, lines = parse_exercise(lines)
        # No lines should be leftover
        assert not lines, "Content remaining after parsing: {}".format(lines)
        return ex

    def to_json(self):
        return {
            'name': self.name,
            'tags': self.tags,
            'sets': self.sets
        }

    @classmethod
    def from_json(cls, d):
        return cls(**d)

    def __eq__(self, o):
        if not isinstance(o, Exercise):
            return NotImplemented
        return (self.name == o.name and
                self.tags == o.tags and
                self.sets == o.sets)

    def __str__(self):
        return pformat(self.to_json())

    def __repr__(self):
        return 'Exercise<{}>'.format(self.name)
