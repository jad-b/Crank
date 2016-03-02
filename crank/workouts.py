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

    def save(self):
        with open(self.filename, 'w') as wf:
            json.dump(self, wf, cls=WorkoutsJSONEncoder, indent='\t')

    def upgrade(self):
        """Upgrade workouts to a new syntax."""
        for i, w in enumerate(self.workouts):
            if not isinstance(self.workouts[i], Workout):
                self.workouts[i] = Workout.parse(w)
            self.workouts[i].upgrade()

    @classmethod
    def from_dict(cls, json_object):
        """Create Workouts from a dict."""
        LOGGER.debug("Parsing %s", str(json_object.keys()))
        if 'filename' in json_object:
            # import pdb; pdb.set_trace()
            return cls(json_object['filename'], json_object['workouts'])
        if 'timestamp' in json_object:
            return Workout.from_dict(json_object)

    @classmethod
    def load(cls, filename=default_file):
        """Load Workouts from file."""
        with open(filename) as wf:
            wkts = json.load(wf, object_hook=Workouts.from_dict)
        assert isinstance(wkts.workouts, Iterable)
        return wkts

    @classmethod
    def parse_wkt(cls, filename):
        """Parse a .wkt file."""
        return cls.parse(parser.stream_file(filename))

    @classmethod
    def parse(cls, wkts):
        """Parse Workouts from a string or list of strings."""
        if isinstance(wkts, str):
            wkts = wkts.split('\n')
        assert isinstance(wkts, Iterable)
        if not wkts:
            raise ValueError("Empty value provided")
        ws = cls()
        for wkt_block in parser.buffer_data(wkts):
            ws.workouts.append(Workout.parse(wkt_block))
        return ws


class WorkoutsJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Workout):
            return o.to_dict()
        elif isinstance(o, Workouts):
            return {
                'filename': o.filename,
                # Convert blist to a list for json encoding
                'workouts': [w.to_dict() for w in o.workouts]
                # 'workouts': list(o.workouts)
            }
        else:
            return super().default(o)
