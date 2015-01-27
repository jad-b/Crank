# -*- coding: utf-8 -*-
"""
test_logic.py
===========
Tests for the :module:`fto.logic`.
"""
from unittest import TestCase

from fto import logic


class TestGetMaxFromPrevious(TestCase):
    max_weight = 00

    def test_returns(self):
        """Test reverse-engineering our max weight.

        Should consistently return the same max weight."""
        for week in len(1, logic.weeks + 1):
            for w in (85, 90, 95):
                self.assertEqual(self.max_weight,
                                 logic._get_max_from_previous(w, week))


class TestCalcWarmupSets(TestCase):
    max_weight = 100

    def test_simple_case(self):
        """Test we return warm-up sets at correct percent of max weight."""
        expected = (40, 50, 60)
        actual = logic.calc_warmup_sets(self.max_weight)
        self.assertEqual(actual, expected)

    def test_units_are_kgs(self):
        """Test we use the correct ceiling when in kilograms."""
        max_weight = 77

        kgs_actual = logic.calc_warmup_sets(max_weight, unit='kgs')
        lbs_actual = logic.calc_warmup_sets(max_weight, unit='lbs')

        # Assert we produced a different output, as rough stand-in for
        # testing it was more-granular
        self.assertNotEqual(kgs_actual, lbs_actual)


class TestBuildSets(TestCase):
    max_weight = 100
    warm_up = [40, 50, 60]
    working_sets = [
        [65, 75, 85],
        [70, 80, 90],
        [75, 85, 95]
    ]

    def test_build_sets(self):
        """Test basic I/O"""
        prev_weight, curr_week = 85, 2
        expected = [self.warm_up + l for l in self.working_sets]

        actual = logic.build_sets(prev_weight, curr_week)

        self.assertEqual(actual, expected)

    def test_build_sets_with_increment(self):
        """Test we add an increment when calculating week 1.

        Scenario:
        - Week 3 we did 90, implying our max weight was 90 / .95 ~= 95
        - This is the start of a new mesocycle (~1 month)
        - We're using a five lb. increment for this exercise
        """
        prev_weight, curr_week, increment = 95, 1, 5
        expected = self.warm_up + self.working_sets[0]

        actual = logic.build_sets(prev_weight, curr_week, increment=increment)

        self.assertEqual(actual, expected)
