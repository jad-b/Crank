from unittest import TestCase
from itertools import repeat

from crank.program.ssp.crank import Accumulator, Aggregator


class TestAccumulatorCases(TestCase):
    outputs = (
        (1,),               # 1
        (10, 1),            # 11
        (10, 10, 2),        # 22
        (10,) * 6 + (8,),   # 68
        (10,) * 8 + (7,),  # 87
        (10,) * 9 + (9,),  # 99
        (10,) * 10          # 100
    )
    # Corresponding days
    day_inputs = map(sum, outputs)
    set_max = 10
    apex = 100
    inputs = zip(day_inputs, repeat(set_max), repeat(apex))
    # print('Examining the following inputs: {}'.format(inputs))

    def test_all_cases(self):
        for input_, output in zip(self.inputs, self.outputs):
            self.compare_sets(input_, output)

    def compare_sets(self, inputs, output):
        acc = Accumulator(*inputs, name='Exercise')
        self.assertTupleEqual(acc.sets, output,
                              '{} vs. {}'.format(acc.sets, output))


class TestAggregatorCases(TestCase):
    outputs = (
        [11, 10, 10, 10, 10, 10, 10, 10, 10, 9],
    )

    # Corresponding days
    day_inputs = (101, 111, 123, 136, 150, 165, 181, 198, 200)
    set_max = 10
    apex = 100
    inputs = zip(day_inputs, repeat(set_max), repeat(apex))

    def test_all_cases(self):
        for input_, output in zip(self.inputs, self.outputs):
            self.compare_sets(input_, output)

    def compare_sets(self, inputs, output):
        agg = Aggregator(*inputs)
        self.assertListEqual(agg.sets, output,
                             '{} vs. {}'.format(agg.sets, output))


class TestIterAggregateCrank(TestCase):
    aggregates = (
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],   # 100
        [11, 10, 10, 10, 10, 10, 10, 10, 10, 9],    # 101
        [11, 11, 10, 10, 10, 10, 10, 10, 10, 8],    # 102
        [11, 11, 11, 10, 10, 10, 10, 10, 10, 7],    # 103
        [11, 11, 11, 11, 10, 10, 10, 10, 10, 6],    # 104
        [11, 11, 11, 11, 11, 10, 10, 10, 10, 5],    # 105
        [11, 11, 11, 11, 11, 11, 10, 10, 10, 4],    # 106
        [11, 11, 11, 11, 11, 11, 11, 10, 10, 3],    # 107
        [11, 11, 11, 11, 11, 11, 11, 11, 10, 2],    # 108
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 1],    # 109
        [12, 11, 11, 11, 11, 11, 11, 11, 11],      # 110
        [12, 12, 11, 11, 11, 11, 11, 11, 10],       # 111
    )
    day = 100
    set_max = 10
    apex = 100

    def test_cases(self):
        days = range(self.day, (self.day + len(self.aggregates) + 1))
        for day, output in zip(days, self.aggregates):
            agg = Aggregator(day, self.set_max, self.apex)
            self.assertListEqual(agg.sets, output)
