import collections
from datetime import datetime


class Workout:

    def __init__(self, timestamp, tags=(), exercises=()):
        assert isinstance(timestamp, datetime)
        self.timestamp = timestamp
        assert isinstance(tags, collections.Iterable)
        self.tags = tags
        assert isinstance(exercises, collections.Iterable)
        self.exercises = exercises

    @classmethod
    def parse(cls, wkt_data):
        """Create a Workout instance from a string, or iterable."""
        if isinstance(wkt_data, str):
            wkt_data = wkt_data.split('\n')
        assert isinstance(wkt_data, collections.Iterable)
        cls._parse_by_item(wkt_data)

    def parse_timestamp(self, line):
        ts_formats = (
            '%Y %b %d @ %H%M',
            '%d %b %Y @ %H%M',
            '%d %B %Y @ %H%M',
        )

        exc = None
        for fmt in ts_formats:
            try:
                return datetime.strptime(line, fmt)
            except Exception as e:
                exc = e
        else:
            raise exc
