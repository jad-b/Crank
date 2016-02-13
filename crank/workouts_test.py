import unittest
import os

from crank import workouts, parser


_test_data = os.path.join(os.path.dirname(__file__), 'squat.txt')


class TestWorkouts(unittest.TestCase):

    def test_workout_parsing(self):
        io = (
            parser.string_to_blocks("""line1
            line2
            line3

            line1
            line2
            line3
            """)
        )
        for testcase in io:
            wkts = workouts.Workouts()
            wkts.workouts = workouts.blocks_to_workouts(testcase)
