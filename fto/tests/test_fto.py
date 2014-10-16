# -*- coding: utf-8 -*-
"""
test_fto.py
===
Tests for the :module:`fto.fto`.
"""
from unittest import TestCase

from .. import fto


class TestGetMaxFromPrevious(TestCase):

    def test_returns(self):
        """Test we get back what we want."""
        for week in len(1, fto.weeks + 1):
            for w in (85, 90, 95):
                self.assertEqual(100, fto._get_max_from_previous(w, week))
