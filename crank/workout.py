from pprint import pformat

from crank.parser import LOGGER
from crank.exercise import parse_exercise
from crank.tags import parse_tags


class Workout:

    def __init__(self, timestamp=None, *exercises):
        self.timestamp = timestamp
        self.exercises = exercises


def parse_workout(lines):
    wkt = {}
    if len(lines) == 0:
        return wkt
    LOGGER.debug('%s', pformat(lines))
    # Timestamp
    timestamp = parse_timestamp(lines[0])
    lines = lines[1:]
    # Tags
    wkt['tags'], lines = parse_tags(lines)
    # Exercises
    wkt['exercises'] = exs = []
    while len(lines) > 0:
        ex, lines = Exercise.parse(lines)
        exs.append(ex)
    return {timestamp.isoformat(): wkt}


def parse_timestamp(line):
    LOGGER.debug(line)
    ts_formats = (
        '%Y %b %d @ %H%M',
        '%d %b %Y @ %H%M',
        '%d %B %Y @ %H%M',
    )

    for fmt in ts_formats:
        try:
            return datetime.strptime(line, fmt)
        except:
            pass
    else:
        return ParseCallback('Timestamp', line, parse_timestamp)
