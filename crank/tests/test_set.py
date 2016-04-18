from collections import namedtuple

from crank.set import Set, parse_ordering


def test_parsing_set_lines():
    SetTestCase = namedtuple('SetTestCase', ['lines', 'output'])
    cases = [
        SetTestCase([
                '  1) 8',
                '  2) 114 x 8',
                '  3) [30] 114 x 8',
                '  4-6) [30] 114 x 8'
            ],
            [
                Set(reps=8, order=1),
                Set(work=114, reps=8, order=2),
                Set(work=114, reps=8, rest=30, order=3),
                Set(work=114, reps=8, rest=30, order=4),
                Set(work=114, reps=8, rest=30, order=5),
                Set(work=114, reps=8, rest=30, order=6)
            ])
    ]
    for c in cases:
        ret, rem = Set.parse_sets(c.lines)
        assert not rem, "No lines should be left unparsed"
        for s in enumerate(ret):
            assert ret == c.output


def test_parsing_set_string():
    SetTestCase = namedtuple('SetTestCase', ['string', 'output'])
    cases = [
        SetTestCase('  1) 8', [Set(reps=8, order=1)]),
        SetTestCase('  2) 114 x 8', [Set(work=114, reps=8, order=2)]),
        SetTestCase('  3) [30] 114 x 8',
                    [Set(work=114, reps=8, rest=30, order=3)]),
        SetTestCase('  4-6) [30] 114 x 8',
                    [Set(work=114, reps=8, rest=30, order=4),
                     Set(work=114, reps=8, rest=30, order=5),
                     Set(work=114, reps=8, rest=30, order=6)]),
    ]
    for c in cases:
        ret = Set.parse(c.string)
        for i, s in enumerate(ret):
            assert ret[i] == c.output[i]


def test_order_parsing():
    SetTestCase = namedtuple('SetTestCase', ['string', 'output'])
    cases = [
        SetTestCase('1', [1]),
        SetTestCase('1,3', [1, 3]),
        SetTestCase('1 , 3', [1, 3]),
        SetTestCase('1-4', [1, 2, 3, 4]),
        SetTestCase('1,3-5, 7', [1, 3, 4, 5, 7])
    ]
    for tc in cases:
        assert list(parse_ordering(tc.string)) == tc.output
