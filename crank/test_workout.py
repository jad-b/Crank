import unittest
from datetime import datetime

from crank.workouts import Workout
from crank import test_data


class TestWorkout(unittest.TestCase):

    def test_parsing(self):
        exp = Workout(timestamp=datetime(2015, 10, 19, 18, 00))
        test_in = (
            test_data.squat_wkt_str,
            test_data.squat_wkt_str.split('\n')
        )
        for t_in in test_in:
            wkt = Workout.parse(t_in)
            self.assertEqual(wkt, exp)
