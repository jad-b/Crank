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

    def test_split_iter(self):
        ex1 = """This is a string.
            For which I don't really care.
            But here it is.
            So what you gonna do?"""
        io = ((ex1, ex1.split('\n')),)
        for test_in, test_out in io:
            self.assertEqual(test_out, list(parser.split_iter(test_in)))


if __name__ == '__main__':
    unittest.main()
