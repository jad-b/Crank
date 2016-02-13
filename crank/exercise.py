from crank.parser import ParseCallback, LOGGER
from crank.tags import parse_tags


class Exercise:

    @classmethod
    def parse(cls, lines):
        while len(lines) > 0:
            cls(lines)

    def __init__(self, lines):
        self.lines = lines


def parse_exercise(lines):
    LOGGER.debug("Exercise: %s", lines)
    LOGGER.debug("Before: %s", lines[0])
    # Exercise name & sets
    ex = {}
    ex['name'], ex['sets'] = parse_exercise_name(lines[0])
    lines = lines[1:]
    LOGGER.info('Name: %s, Sets: %s', ex['name'], ex['sets'])
    # Tags
    if len(lines) > 1:
        ex['tags'], lines = parse_tags(lines)
    LOGGER.debug("Remaining: %s", lines)
    return ex, lines


def parse_exercise_name(line):
    try:
        name_sets = line.split(':')
        if len(name_sets) != 2:
            return ParseCallback('exercise name', line, parse_exercise), ''
        return name_sets[0], name_sets[1]
    except Exception:
        LOGGER.exception('Error while parsing exercise')
        return ParseCallback('exercise name', line, parse_exercise), ''
