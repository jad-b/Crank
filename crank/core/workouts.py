import json
from collections.abc import Iterable
from datetime import datetime

from blist import sortedset

from crank.util import stream
from crank.core.workout import Workout


class Workouts:
    """Collection of workouts.

    Handles storage and search for individual workouts.
    """
    default_file = 'workouts.json'

    def __init__(self, filename=default_file, workouts=()):
        """Initialize with configuration."""
        self.filename = filename
        self.workouts = sortedset(workouts)
        self.modified = None

    @property
    def length(self):
        return len(self.workouts)

    def upgrade(self):
        """Upgrade workouts to a new syntax."""
        for i, w in enumerate(self.workouts):
            if not isinstance(self.workouts[i], Workout):
                self.workouts[i] = Workout.parse_wkt(w)
            self.workouts[i].upgrade()

    def to_json(self, *args):
        """Convert Workouts to a JSON-compatible dictionary."""
        return {
            'filename': self.filename,
            'workouts': [w.to_json() for w in self.workouts],
            'written_at': str(datetime.utcnow())
        }

    @classmethod
    def from_json(cls, json_object):
        """Create Workouts from a dict."""
        return cls(**{
            'filename': json_object.get('filename'),
            'workouts': sortedset([Workout.from_json(w) for w in
                                   json_object.get('workouts', [])])
            })

    def save(self):
        with open(self.filename, 'w') as wf:
            json.dump(self, wf, default=self.to_json, indent=2)

    @classmethod
    def load(cls, filename=default_file):
        """Load Workouts from file."""
        with open(filename) as wf:
            wkts = json.load(wf, cls=WorkoutsJSONDecoder)
        assert isinstance(wkts.workouts, Iterable)
        return wkts

    @classmethod
    def parse_wkt_file(cls, filename):
        """Parse a .wkt file."""
        return cls.parse_wkt(stream.stream_file(filename))

    @classmethod
    def parse_wkt(cls, wkts):
        """Parse Workouts from a .wkt-formatted string or list of strings."""
        if isinstance(wkts, str):
            wkts = wkts.split('\n')
        assert isinstance(wkts, Iterable)
        if not wkts:
            raise ValueError("Empty value provided")
        ws = cls()

        for wkt_block in stream.buffer_data(wkts):
            ws.workouts.add(Workout.parse_wkt(wkt_block))
        return ws

    def __repr__(self):
        json_str = json.dumps(self.to_json(), indent=2)
        return "Workouts(**{})".format(json_str)


class WorkoutsJSONEncoder(json.JSONEncoder):

    def default(self, o):
        # Delegate to the class's to_json call
        return Workouts.to_json(o)


class WorkoutsJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        # Decode strings to JSON-compatible dictionary
        json_obj = super().decode(s)
        # Feed dictionary to class methods for further decoding
        return Workouts.from_json(json_obj)
