from pprint import pformat

from crank.parser import LOGGER
from crank.tags import parse_tags


def parse_exercises(lines):
    exs = []
    while len(lines) > 0:
        ex, lines = parse_exercise(lines)
        exs.append(ex)
        LOGGER.debug("Parsed Exercise:\n%s", ex)
        LOGGER.debug("Remaining lines:\n%s", lines)
    return exs


def parse_exercise(lines):
        # LOGGER.debug("Exercise: %s", lines)
        # Exercise name & sets
        ex = {}
        ex['name'], ex['sets'] = parse_exercise_name(lines[0])
        ex['name'] = ex['name'].strip()
        ex['sets'] = ex['sets'].strip()
        # LOGGER.info('Name: %s, Sets: %s', ex['name'], ex['sets'])
        lines = lines[1:]
        # Tags
        if lines:
            ex['tags'], lines = parse_tags(lines)
        # LOGGER.debug("Remaining: %s", lines)
        return Exercise(**ex), lines


def parse_exercise_name(line):
    try:
        name_sets = line.split(':')
        if len(name_sets) != 2:
            return line
        return name_sets[0], name_sets[1]
    except Exception:
        LOGGER.exception('Error while parsing exercise')
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
