from datetime import datetime

from crank.workout import parse_workout
from crank import parser


class Workouts:

    def __init__(self, **workouts):
        self.source = None
        self._workouts = workouts or {}

    @property
    def workouts(self):
        return self._workouts

    @workouts.setter
    def workouts(self, workouts):
        self._workout = workouts

    def get_workout(self, timestamp):
        if isinstance(timestamp, datetime):
            timestamp = timestamp.toisoformat()
        self.workouts.get(timestamp.toisoformat())

    def read_file(self, filename):
        self.source = filename
        wkt_stream = parser.stream_blocks(filename)
        for wkt_list in wkt_stream:
            wkt = parse_workout(wkt_list)
            self.workouts[wkt.timestamp] = wkt


def parse_workouts(wkt_src):
    return (parse_workout(wkt) for wkt in wkt_src)
