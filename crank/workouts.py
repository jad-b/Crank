import json
from collections.abc import Iterable

from blist import blist

from crank.parser import LOGGER
from crank import parser
from crank.workout import Workout


class Workouts:
    """Collection of workouts.

    Handles storage and search for individual workouts.
    """
    default_file = 'workouts.json'

    def __init__(self, filename=default_file, workouts=()):
        """Initialize with configuration."""
        self.filename = filename
        self.workouts = blist(workouts)

    def upgrade(self):
        """Upgrade workouts to a new syntax."""
        for i, w in enumerate(self.workouts):
            if not isinstance(self.workouts[i], Workout):
                self.workouts[i] = Workout.parse_wkt(w)
            self.workouts[i].upgrade()

    def to_json(self, *args):
        """Convert Workouts to a JSON-compatible dictionary."""
        wkts = []
        for w in self.workouts:
            wkts.append(w.to_json())
        return {
            'filename': self.filename,
            'workouts': wkts
        }

    @classmethod
    def from_json(cls, json_object):
        """Create Workouts from a dict.

        This is intended for use in the json.loads 'default' argument. As such,
        it will get passed _every_ parsed dict object, and needs a way to tell
        the difference between nested dictionaries, such as Workouts vs. a
        Workout.

        This is gonna break when _more_ nested dictionaries start popping up.
        Providing a custom JSONDecoder, whose 'decode()' method begins with the
        raw pre-parsed JSON string, is probably a better long-term solution.
        """
        LOGGER.debug("Parsing %s", str(json_object.keys()))
        # import pdb; pdb.set_trace()
        if 'filename' in json_object:
            # Decode each workout
            wkts = []
            for w in json_object['workouts']:
                wkts.append(Workout.from_json(w))
            return cls(json_object['filename'], wkts)

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
        return cls.parse_wkt(parser.stream_file(filename))

    @classmethod
    def parse_wkt(cls, wkts):
        """Parse Workouts from a .wkt-formatted string or list of strings."""
        if isinstance(wkts, str):
            wkts = wkts.split('\n')
        assert isinstance(wkts, Iterable)
        if not wkts:
            raise ValueError("Empty value provided")
        ws = cls()
        for wkt_block in parser.buffer_data(wkts):
            ws.workouts.append(Workout.parse_wkt(wkt_block))
        return ws


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
