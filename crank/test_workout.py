import unittest
from datetime import datetime

from crank.workouts import Workout


TEST_WORKOUT_LINES = [
    '2015 Oct 19 @ 1800',
    'Swing, KB: 28 x 35',
    'Squat: 20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4',
    '- unit: kg',
    '- coming off drill weekend, tired and small',
    'Curl, ring: 10/5',
    'Plate pinch: 15 x 35/30'
]

TEST_WORKOUT_RAW = Workout(timestamp=TEST_WORKOUT_LINES[0],
                           raw=TEST_WORKOUT_LINES[1:])


class TestWorkout(unittest.TestCase):

    def test_parsing(self):
        wkt = Workout.parse(TEST_WORKOUT_LINES)
        assert isinstance(wkt.timestamp, datetime)
        assert wkt.raw == TEST_WORKOUT_LINES[1:]

    def test_encoding(self):
        wkt = Workout.parse(TEST_WORKOUT_LINES)
        exp = {
            'timestamp': wkt.timestamp.isoformat(),
            'raw': TEST_WORKOUT_LINES[1:]
        }
        assert wkt.to_dict() == exp
