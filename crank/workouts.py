import json
from collections.abc import Iterable
from datetime import datetime

from crank import parser
from crank.fto.cli import read_until_valid

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
            json.dump(list(self.workouts), wf, indent='\t')

    def upgrade(self):
        """Upgrade workouts to a new syntax."""
        for w in self.workouts:
            if not isinstance(w[0], datetime):
                prompt = '{}: '.format(w[0])
                w[0] = read_until_valid(prompt, lmbda=parser.parse_timestamp)

    @classmethod
    def from_file(cls, filename):
        return cls.parse(parser.stream_file(filename))

    @classmethod
    def from_dict(cls, json_object):
        wkts = cls()
        if 'filename' in json_object:
            wkts.filename = json_object['filename']
        wkts.workouts = sortedset(json_object.get('workouts'))
        return wkts

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


class WorkoutsJSONEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            'filename': o.filename,
            'workouts': list(o.workouts)
        }
