# -*- coding: utf-8 -*-
"""
test_crank.py
===
Unit tests for Crank (tm)
"""
from unittest import TestCase

from crank.program.ssp.crank import Accumulator


class TestAccumulator(TestCase):

    def setUp(self):
        self.day = 73
        self.set_max = 10
        self.apex = 100
        self.name = 'Exercise'

        self.starting_set = (10,) * 7 + (3,)

        self.acc = Accumulator(self.day, self.set_max, self.apex, self.name)

    def test_init(self):
        # After building sets, day will have incremented
        self.assertEqual(self.day + 1, self.acc.day)
        self.assertEqual(self.set_max, self.acc.set_max)
        self.assertEqual(self.apex, self.acc.apex)
        self.assertEqual(self.name, self.acc.name)
        self.assertTupleEqual(self.starting_set, self.acc.sets)

    def test_crank(self):
        ret = self.acc.crank()
        new_sets = tuple(self.starting_set[:-1] +
                         (self.starting_set[-1] + 1,))

        # Assert we incremented our day
        self.assertEqual(self.day + 2, self.acc.day)
        # Assert we added one to the end
        self.assertTupleEqual(new_sets, ret)
