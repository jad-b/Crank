import unittest
import os

import parser


_test_data = os.path.join(os.path.dirname(__file__), 'squat.txt')


class TestParsing(unittest.TestCase):

    def test_workout_splitting(self):
        stream = parser.stream_blocks(_test_data)
        wkts = []
        try:
            for wkt in parser.parse_workouts(stream):
                wkts.append(wkt)
        except:
            print('{:d} workouts parsed'.format(len(wkts)))
            raise
        self.assertEqual(len(wkts), 44)

    def test_workout_parsing(self):
        pass


if __name__ == '__main__':
    unittest.main()
