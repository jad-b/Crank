from collections.abc import Iterable
import json

from crank import parser
# from crank.workout import Workout

from blist import sortedset


class Workouts:
    """Collection of workouts.

    Handles storage and search for individual workouts.
    """

    def __init__(self, filename='workouts.json'):
        """Initialize with configuration."""
        self.filename = filename
        self.workouts = sortedset()

    def load(self):
        with open(self.filename) as wf:
            wkts = json.load(wf)
            self.workouts = sortedset(wkts)
        assert isinstance(self.workouts, Iterable)

    def save(self):
        with open(self.filename, 'w') as wf:
            # Convert sortedset to a list for json encoding
            json.dump(list(self.workouts), wf)

    @classmethod
    def from_file(cls, filename):
        return cls.parse(parser.stream_file(filename))

    @classmethod
    def parse(cls, wkts):
        if isinstance(wkts, str):
            wkts = wkts.split('\n')
        assert isinstance(wkts, Iterable)
        if not wkts:
            raise ValueError("Empty value provided")
        ws = cls()
        for wkt_block in parser.buffer_data(wkts):
            # ws.workouts.add(Workout.parse(wkt_block))
            ws.workouts.add(wkt_block)
        return ws
