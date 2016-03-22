from crank.set import Set


class SetCase:

    def __init__(self, string, exp):
        self.string = string
        self.exp = exp


TEST_SET_STRINGS = {
    'single': SetCase(
        '20 x 5',
        [Set(work=20, reps=5)]
    ),
    'simple_list': SetCase(
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
    'same_reps': SetCase(
        '20, 60, 80 x 5',
        [
            Set(work=20, reps=5),
            Set(work=60, reps=5),
            Set(work=80, reps=5)
        ]
    ),
    'same_weight': SetCase(
        '60 x 8, 6, 4',
        [
            Set(work=60, reps=8),
            Set(work=60, reps=6),
            Set(work=60, reps=4)
        ]
    ),
    'same_reps_then_weights': SetCase(
        '20, 60, 80 x 5, 60 x 8, 6, 4',
        [
            Set(work=20, reps=5),
            Set(work=60, reps=5),
            Set(work=80, reps=5),
            Set(work=60, reps=8),
            Set(work=60, reps=6),
            Set(work=60, reps=4)
        ]
    ),
    'shorthand_list': SetCase(
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
    'rest-pause': SetCase(
        '134 x 10/5',
        [
            Set(work=134, reps=10),
            Set(work=134, reps=5)
        ]
    ),
    'unilateral': SetCase(
        '15 x 35|30',
        [
            Set(work=15, reps=35),
            Set(work=35, reps=30)
        ]
    ),
    'master': SetCase(
        '100 x 5, 7, 70, 80,90 x 6, 110 x 6,5, 4, 120 x 3 (2), 2, 100 x 5/4/3',
        []
    )
}


def test_master_parsing():
    """If it can parse this, it's probably good."""
    test_str = \
        '100 x 5, 7, 70, 80,900 x 6, 110 x 6,5, 4, 120 x 3 (2), 2, 100 x 5/4/3'
    assert test_str


def test_parsing():
    case_name = 'same_reps'
    case = TEST_SET_STRINGS[case_name]
    sets = Set.parse_sets(case.string)
    assert len(sets) == len(case.exp)


def test_set_parsing_regression():
    """Regression test that we don't break existing set-parsing abilities."""
    vetted = (
        'single',
        'simple_list',
    )
    for name in vetted:
        case = TEST_SET_STRINGS[name]
        sets = Set.parse_sets(case.string)
        assert len(sets) == len(case.exp)
