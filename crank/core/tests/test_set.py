from collections import namedtuple

from crank.core.set import (Set, parse_ordering, parse_set_body,
                            group_sets_by_order)


def test_parsing_set_lines():
    SetTestCase = namedtuple('SetTestCase', ['lines', 'output'])
    cases = [
        # Many-to-One order-to-set notation
        SetTestCase(['  1) 8'], [Set(reps=8, order=1)]),
        SetTestCase(['  1) 114 x 8'], [Set(work=114, reps=8, order=1)]),
        SetTestCase(['1) [30] 114 x 8'],
                    [Set(work=114, reps=8, rest=30, order=1)]),
        SetTestCase(['1,2) [30] 114 x 8'],
                    [Set(work=114, reps=8, rest=30, order=1),
                     Set(work=114, reps=8, rest=30, order=2)]),
        SetTestCase(['  4-6) [30] 114 x 8'], [
                Set(work=114, reps=8, rest=30, order=4),
                Set(work=114, reps=8, rest=30, order=5),
                Set(work=114, reps=8, rest=30, order=6)
            ]),
        # One-to-one order-to-set notation
        SetTestCase(['2,3) 100 x 8, [60] 110 x 7'], [
                Set(work=100, reps=8, order=2),
                Set(work=110, reps=7, rest=60, order=3),
            ]),
        SetTestCase(['1-3, 5-7) 100 x 8, [60] 110 x 7'], [
                Set(work=100, reps=8, order=1),
                Set(work=100, reps=8, order=2),
                Set(work=100, reps=8, order=3),
                Set(work=110, reps=7, rest=60, order=5),
                Set(work=110, reps=7, rest=60, order=6),
                Set(work=110, reps=7, rest=60, order=7),
            ]),
    ]
    for c in cases:
        ret, rem = Set.parse_sets(c.lines)
        assert not rem, "No lines should be left unparsed"
        for s in enumerate(ret):
            assert ret == c.output


def test_parsing_set_string():
    SetTestCase = namedtuple('SetTestCase', ['string', 'output'])
    cases = [
        # Many-to-One order-to-set notation
        SetTestCase('  1) 8', [Set(reps=8, order=1)]),
        SetTestCase('  1) 114 x 8', [Set(work=114, reps=8, order=1)]),
        SetTestCase('1) [30] 114 x 8',
                    [Set(work=114, reps=8, rest=30, order=1)]),
        SetTestCase('1,2) [30] 114 x 8',
                    [Set(work=114, reps=8, rest=30, order=1),
                     Set(work=114, reps=8, rest=30, order=2)]),
        SetTestCase('  4-6) [30] 114 x 8', [
                Set(work=114, reps=8, rest=30, order=4),
                Set(work=114, reps=8, rest=30, order=5),
                Set(work=114, reps=8, rest=30, order=6)
            ]),
        # One-to-one order-to-set notation
        SetTestCase('2,3) 100 x 8, [60] 110 x 7', [
                Set(work=100, reps=8, order=2),
                Set(work=110, reps=7, rest=60, order=3),
            ]),
        SetTestCase('1-3, 5-7) 100 x 8, [60] 110 x 7', [
                Set(work=100, reps=8, order=1),
                Set(work=100, reps=8, order=2),
                Set(work=100, reps=8, order=3),
                Set(work=110, reps=7, rest=60, order=5),
                Set(work=110, reps=7, rest=60, order=6),
                Set(work=110, reps=7, rest=60, order=7),
            ]),
    ]
    for c in cases:
        ret = Set.parse(c.string)
        for i, s in enumerate(ret):
            assert ret[i] == c.output[i]


def test_order_parsing():
    SetTestCase = namedtuple('SetTestCase', ['string', 'output'])
    cases = [
        SetTestCase('1) 8', ([(1,)], '8')),
        SetTestCase('1,3) 8', ([(1,), (3,)], '8')),
        SetTestCase('1 , 3) 8', ([(1,), (3,)], '8')),
        SetTestCase('1-4)    8', ([(1, 2, 3, 4)], '8')),
        SetTestCase('1,3-5, 7)8', ([(1,), (3, 4, 5), (7,)], '8'))
    ]
    for tc in cases:
        assert parse_ordering(tc.string) == tc.output


def test_set_body_parsing():
    SetTestCase = namedtuple('SetTestCase', ['string', 'output'])
    cases = [
        SetTestCase('8', [Set(reps=8)]),
        SetTestCase('100 x 8', [Set(work=100, reps=8)]),
        SetTestCase('[30] 100 x 8', [Set(work=100, reps=8, rest=30)]),
    ]
    for tc in cases:
        assert list(parse_set_body(tc.string)) == tc.output


def test_group_by_order():
    SetTestCase = namedtuple('SetTestCase', ['sets', 'output'])
    cases = [
        SetTestCase([
                Set(work=100, reps=8, order=1),
                Set(work=100, reps=8, order=2),
                Set(work=100, reps=8, order=3),
                Set(work=110, reps=7, rest=60, order=5),
                Set(work=110, reps=7, rest=60, order=6),
                Set(work=110, reps=7, rest=60, order=7),
            ],
            [
                ('1-3', (Set(work=100, reps=8, order=1),
                         Set(work=100, reps=8, order=2),
                         Set(work=100, reps=8, order=3))),
                ('5-7', (Set(work=110, reps=7, rest=60, order=5),
                         Set(work=110, reps=7, rest=60, order=6),
                         Set(work=110, reps=7, rest=60, order=7))),
            ]
        )
    ]
    for c in cases:
        assert group_sets_by_order(c.sets) == c.output
