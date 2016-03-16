from collections import namedtuple

from crank.set import Set


TestCase = namedtuple('TestCase', ['string', 'exp'])
TEST_SET_STRINGS = {
    'single': TestCase(
        '20 x 5',
        Set(work=20, reps=5)
    ),
    'simple_list': TestCase(
        '20 x 5, 60 x 5, 80 x 3, 90 x 3, 91 x 5, 105 x 5, 119 x 4',
        [
            Set(work=20, reps=5),
            Set(work=60, reps=5),
            Set(work=80, reps=3),
            Set(work=90, reps=3),
            Set(work=91, reps=5),
            Set(work=105, reps=5),
            Set(work=119, reps=4)
        ]
    ),
    'same_reps': TestCase(
        '20, 60, 80 x 5',
        [
            Set(work=20, reps=5),
            Set(work=60, reps=5),
            Set(work=80, reps=5)
        ]
    ),
    'same_weight': TestCase(
        '60 x 8, 6, 4',
        [
            Set(work=60, reps=8),
            Set(work=60, reps=6),
            Set(work=60, reps=4)
        ]
    ),
    'shorthand_list': TestCase(
        '20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4',
        [
            Set(work=20, reps=5),
            Set(work=60, reps=5),
            Set(work=80, reps=3),
            Set(work=90, reps=3),
            Set(work=91, reps=5),
            Set(work=105, reps=5),
            Set(work=119, reps=4)
        ]
    ),
    'rest-pause': TestCase(
        '134 x 10/5',
        [
            Set(work=134, reps=10),
            Set(work=134, reps=5)
        ]
    ),
    'unilateral': TestCase(
        '15 x 35|30',
        [
            Set(work=15, reps=35),
            Set(work=35, reps=30)
        ]
    )
}


def test_set_splitting():
    sets = Set.parse_sets(TEST_SET_STRINGS['simple_list'].string)
    assert len(sets) == len(TEST_SET_STRINGS['simple_list'].exp)
