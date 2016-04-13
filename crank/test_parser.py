from collections import namedtuple

import pytest

from crank import parser
from crank.set import Set, string_tokenizer


def test_split_iter():
    ex1 = """This is a string.
        For which I don't really care.
        But here it is.
        So what you gonna do?"""
    io = (
        (ex1, ex1.split('\n')),
    )
    for test_in, test_out in io:
        assert test_out == list(parser.split_iter(test_in))

SetTestCase = namedtuple('TestCase', ['raw', 'pieces', 'work_reps', 'final'])
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
        assert list(string_tokenizer(tc.raw)) == tc.pieces


@pytest.mark.xfail
def test_set_string_partitioning():
    for tc in test_cases:
        assert parser.partition_set_string(tc.raw) == tc.work_reps


def test_set_partition_processing():
    for tc in test_cases:
        assert parser.process_set_partitions(tc.work_reps) == tc.final
