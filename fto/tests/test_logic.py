# -*- coding: utf-8 -*-
"""
test_logic.py
===========
Tests for the :module:`fto.logic`.
"""
from unittest import TestCase

from fto import logic, util


class TestGetMaxFromPrevious(TestCase):
    max_weight = 100

    def test_previous_max_calculations(self):
        """Test reverse-engineering our max weight.

        Should consistently return the same max weight."""
        for week, w in zip(range(1, len(logic.weeks)), (95, 85, 90)):
                self.assertEqual(self.max_weight,
                                 logic.get_max_from_previous(w, week,
                                     increment=0),
                                 "week = {}, weight = {}".format(week, w))


class TestCalcWarmupSets(TestCase):
    max_weight = 100

    def test_simple_case(self):
        """Test we return warm-up sets at correct percent of max weight."""
        expected = [40, 50, 60]
        actual = logic.calc_warmup_sets(self.max_weight)
        self.assertEqual(actual, expected)

    def test_units_are_kgs(self):
        """Test we use the correct ceiling when in kilograms."""
        max_weight = 77

        kgs_actual = logic.calc_warmup_sets(max_weight, units='kgs')
        lbs_actual = logic.calc_warmup_sets(max_weight, units='lbs')

        # Assert we produced a different output, as rough stand-in for
        # testing it was more-granular
        self.assertNotEqual(kgs_actual, lbs_actual)


class TestBuildSets(TestCase):

    def test_build_sets(self):
        """Test basic I/O"""
        max_weight = 100
        steps = (0.2, 0.1, 0)

        res = logic.build_sets(max_weight, logic.weeks[1].percent)[-3:]
        self.assertEqual(res, [65, 75, 85])
        res = logic.build_sets(max_weight, logic.weeks[2].percent)[-3:]
        self.assertEqual(res, [70, 80, 90])
        res = logic.build_sets(max_weight, logic.weeks[3].percent)[-3:]
        self.assertEqual(res, [75, 85, 95])
