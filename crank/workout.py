import collections
from datetime import datetime
from collections.abc import Iterable

from crank.parser import parse_timestamp
from crank.fto.cli import read_until_valid


class Workout:

    def __init__(self,
                 timestamp,
                 tags=(),
                 exercises=(),
                 raw=None) -> None:
        """Initialize the Workout with given values.

        :attr str or list raw: Unprocessed data.
        """
        self.timestamp = timestamp
        assert isinstance(tags, Iterable)
        self.tags = tags
        assert isinstance(exercises, Iterable)
        self.exercises = exercises
        self.raw = raw

    @classmethod
    def parse(cls, wkt_data):
        """Create a Workout instance from a string, or iterable."""
        if isinstance(wkt_data, str):
            wkt_data = wkt_data.split('\n')
        assert isinstance(wkt_data, collections.Iterable)
        if not wkt_data:
            raise ValueError("Empty value provided")
        # Timestamp
        try:
            timestamp = parse_timestamp(wkt_data[0])
        except:  # Store the string for later re-parsing
            timestamp = wkt_data[0]
        # lines = lines[1:]
        # Tags
        # wkt['tags'], lines = parse_tags(lines)
        # Exercises
        # wkt['exercises'] = exs = []
        # while len(lines) > 0:
        # ex, lines = Exercise.parse(lines)
        # exs.append(ex)
        return Workout(timestamp, raw=wkt_data[1:])

    def upgrade(self):
        if not isinstance(self.timestamp, datetime):
            prompt = '{}: '.format(self.timestamp)
            self.timestamp = read_until_valid(prompt, lmbda=parse_timestamp)

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'raw': self.raw
        }

    def __lt__(self, other):
        if not isinstance(other, Workout):
            return NotImplemented
        return self.timestamp < other.timestamp
