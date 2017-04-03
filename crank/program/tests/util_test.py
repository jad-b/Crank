import contextlib
import sys
from collections import namedtuple
from io import StringIO

from crank.program import util


@contextlib.contextmanager
def capture():
    """Capture stdout as a context manager."""
    _stdout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out
        yield out
    finally:
        sys.stdout = _stdout
        out = out.getvalue()


def test_generate_percents():
    testcases = (
        (.05, .25, .05, [.05, .1, .15, .2, .25]),
    )
    for tc in testcases:
        assert list(util.generate_percents(*tc[:3])) == tc[-1]


def test_calculate_weights():
    TC = namedtuple.TestCase('weight', 'low', 'high', 'step', 'exp')
    testcases = (
        TC(100, .5, 1., .1, [50, 60, 70, 80, 90, 100]),
    )
    for tc in testcases:
        percents = util.generate_percents(tc.low, tc.high, tc.step)
        assert list(util.calculate_weights(tc.weight, percents)) == tc.exp


def print_sets():
    TC = namedtuple.TestCase('weights', 'reps', 'exp')
    testcases = (
        TC([50, 60, 70], [10, 10, 8], "50 x 10, 60 x 10, 70 x 8"),
    )
    for tc in testcases:
        with capture as out:
            util.print_sets(tc.weights, tc.reps)
        assert tc.exp == out
