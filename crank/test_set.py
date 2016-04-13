import textwrap
from collections import namedtuple

import pytest

from crank.set import (Set, rest_pause, max_err, max_slope,
                       work_rep_sim)


class SetCase:

    def __init__(self, string, exp):
        self.string = string
        self.exp = exp


FUTURE_SET = {
    'object': Set(
    ),
    'raw': textwrap.dedent(
        """
        2016 Apr 04 @ 1246
        Press:
        - sets:
            - 24 x 5
            - 30 x 5
            - 37 x 3
            - 43 x 3
            - 49 x 3
            - 55 x 8
        - Training max: 61 kgs
        - week: 2
        Pull-up: 5 x 9/4/2
        Press: 42 x 10/3/2
        Handstands: 12, 8
        - unit: breaths

        """),
    'old_raw': textwrap.dedent(
        """
        2016 Apr 04 @ 1246
        Press: 24 x 5, 30 x 5, 37 x 3, 43 x 3, 49 x 3, 55 x 8
        - Training max: 61 kgs
        - week: 2
        Pull-up: 5 x 9/4/2
        Press: 42 x 10/3/2
        Handstands: 12, 8
        - unit: breaths
        """)
}


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


@pytest.mark.skip()
def test_rep_detection():
    TestCase = namedtuple('TestCase', ('work', 'reps', 'index'))
    cases = (
        TestCase(100, [5, 7, 70, 80, 90], 2),
        TestCase(20, [12, 13, 23, 22], 2)
    )
    predictions = {}
    for c in cases:
        predictions[str(c.reps)] = {
            'max_err': max_err(c.work, c.reps),
            'max_slope': max_slope(c.reps),
            'work_rep_sim': work_rep_sim(c.work, c.reps)
        }
    from pprint import pprint
    pprint(predictions)
    # No actual assertion is made, besides that no syntax errors occur.


@pytest.mark.xfail()
def test_rest_pause():
    rp_str = '5/4/3'
    test_weight = 100
    exp = [
        Set(work=test_weight, reps=5),
        Set(work=test_weight, reps=4),
        Set(work=test_weight, reps=3),
    ]
    obs = rest_pause(test_weight, rp_str)
    assert obs == exp
    # An empty list should be returned if no rest-pause notation is found
    assert rest_pause(test_weight, '543') == []


@pytest.mark.xfail()
def test_parsing_hard_string():
    """If it can parse this, it's probably good."""
    test_str = \
        '100 x 5, 7, 70, 80,90 x 6, 110 x 6,5, 4, 120 x 3 (2), 2, 100 x 5/4/3'
    try:
        sets = Set.parse_sets(test_str)
    except SyntaxError:
        pytest.fail("Told you it was hard")
    assert len(sets) == 12


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
