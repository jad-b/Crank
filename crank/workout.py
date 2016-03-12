from collections.abc import Iterable, Mapping
from datetime import datetime

from crank.exercise import parse_exercises, Exercise
from crank.tags import parse_tags
from crank.parser import parse_timestamp
from crank.fto.cli import read_until_valid


class Workout:

    def __init__(self,
                 timestamp,
                 tags=None,
                 exercises=None) -> None:
        """Initialize the Workout with given values."""
        if isinstance(timestamp, str):
            try:
                timestamp = parse_timestamp(timestamp)
            except:
                pass
        self.timestamp = timestamp

        self.tags = tags or {}
        assert isinstance(self.tags, Mapping)
        self.exercises = exercises or []
        assert isinstance(self.exercises, Iterable)

    @classmethod
    def parse_wkt(cls, wkt_data):
        """Create a Workout instance from a .wkt format string or iterable."""
        if isinstance(wkt_data, str):
            wkt_data = wkt_data.split('\n')
        assert isinstance(wkt_data, Iterable)
        if not wkt_data:
            raise ValueError("Empty value provided")
        # Timestamp
        try:
            timestamp = parse_timestamp(wkt_data[0])
        except:  # Store the string for later re-parsing
            timestamp = wkt_data[0]
        # Tags
        tags, wkt_data = parse_tags(wkt_data[1:])
        # Exercises
        exercises = parse_exercises(wkt_data)
        return Workout(timestamp, tags=tags, exercises=exercises)

    def upgrade(self):
        """Upgrade bootstraps the Exercise to a new schema.

        Schema versions aren't explicitly tracked, as everything's still in
        development.
        """
        if not isinstance(self.timestamp, datetime):
            prompt = '{}: '.format(self.timestamp)
            self.timestamp = read_until_valid(prompt, lmbda=parse_timestamp)

    def to_json(self):
        d = {
            'exercises': [ex.to_json() for ex in self.exercises],
            'tags': self.tags
        }
        if isinstance(self.timestamp, datetime):
            d['timestamp'] = self.timestamp.isoformat()
        else:  # Better be a string; what kind of timestamps are you storing?
            d['timestamp'] = self.timestamp
        return d

    @classmethod
    def from_json(cls, d):
        exs = []
        for ex in d.get('exercises', []):
            exs.append(Exercise.from_json(ex))
        d_wkt = dict(d)
        d_wkt['exercises'] = exs
        return cls(**d_wkt)

    def __lt__(self, other):
        if not isinstance(other, Workout):
            return NotImplemented
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        if not isinstance(other, Workout):
            return NotImplemented
        return self.timestamp == other.timestamp
