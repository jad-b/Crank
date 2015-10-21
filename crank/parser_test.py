import unittest

import parser


def load_squat_data():
    with open('squat.txt') as fp:
        return fp.read()


class TestParsing(unittest.TestCase):

    def test_workout_splitting(self):
        squats = load_squat_data()
        gen = parser.read_until_blankline(squats)
        wkts = list(gen)
        self.assertEqual(len(wkts), 44)


if __name__ == '__main__':
    unittest.main()
