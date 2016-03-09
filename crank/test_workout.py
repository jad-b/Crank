import unittest
from datetime import datetime

from crank.workout import Workout


TEST_WORKOUT_LINES = [
    '2015 Oct 19 @ 1800',
    '- This workout will suck.',
    'Swing, KB: 28 x 35',
    'Squat: 20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4',
    '- unit: kg',
    '- coming off drill weekend, tired and small',
    'Curl, ring: 10/5',
    'Plate pinch: 15 x 35/30'
]


TEST_WORKOUT_RAW = Workout(timestamp=TEST_WORKOUT_LINES[0],
                           tags={'comment': TEST_WORKOUT_LINES[1][2:]},
                           raw=TEST_WORKOUT_LINES[2:])


class TestWorkout(unittest.TestCase):

    def test_parsing(self):
        wkt = Workout.parse_wkt(TEST_WORKOUT_LINES)
        assert isinstance(wkt.timestamp, datetime)
        assert 'comment' in wkt.tags
        assert wkt.exercises == []
        assert wkt.raw == TEST_WORKOUT_LINES[2:]

    def test_to_json(self):
        d = TEST_WORKOUT_RAW.to_json()
        assert 'timestamp' in d
        assert 'tags' in d
        assert 'exercises' in d
        assert 'raw' in d

    def test_from_json(self):
        TEST_WORKOUT_JSON = {
            'timestamp': TEST_WORKOUT_RAW.timestamp.isoformat(),
            'exercises': [],
            'tags': {
                'comment': TEST_WORKOUT_LINES[1][2:]  # Drop '- '
            },
            'raw': TEST_WORKOUT_RAW.raw
        }
        w = Workout.from_json(TEST_WORKOUT_JSON)
        assert w.timestamp == TEST_WORKOUT_RAW.timestamp
        assert w.tags == TEST_WORKOUT_RAW.tags
        assert w.exercises == TEST_WORKOUT_RAW.exercises
        assert w.raw == TEST_WORKOUT_RAW.raw

    def test_encoding(self):
        wkt = Workout.parse_wkt(TEST_WORKOUT_LINES)
        exp = {
            'timestamp': wkt.timestamp.isoformat(),
            'exercises': [],
            'tags': {
                'comment': TEST_WORKOUT_LINES[1][2:]  # Drop '- '
            },
            'raw': TEST_WORKOUT_LINES[2:]
        }
        assert wkt.to_json() == exp
