from collections import namedtuple

import pytest

from crank.core.set_v1 import (Set, rest_pause, max_err, max_slope,
                               work_rep_sim, process_set_partitions,
                               partition_set_tokens, string_tokenizer,
                               parse_v1_sets)


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
        sets, _ = parse_v1_sets(case.string)
        assert len(sets) == len(case.exp)


SetTestCase = namedtuple('TestCase', ['raw', 'tokens', 'work_reps', 'final'])
test_cases = (
    SetTestCase(
        '95,115,130,150x5,170x5/3/2, 185x5',
        ['95', '115', '130', '150', 'x', '5', '170', 'x',
         '5/3/2', '185', 'x', '5'],
        [
            ((95, 115, 130, 150), (5,)),
            ((170,), (5, 3, 2)),
            ((185,), (5,))
        ],
        [Set(95, 5), Set(115, 5), Set(130, 5), Set(150, 5), Set(170, 5),
         Set(170, 3), Set(170, 2), Set(185, 5)]
    ),
)


def test_string_tokenizer():
    for tc in test_cases:
        assert list(string_tokenizer(tc.raw)) == tc.tokens


def test_set_string_partitioning():
    for tc in test_cases:
        assert partition_set_tokens(tc.tokens) == tc.work_reps


def test_set_partition_processing():
    for tc in test_cases:
        assert process_set_partitions(tc.work_reps) == tc.final
