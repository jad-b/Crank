from unittest import TestCase, skip
from crank import Exercise, Workout


class WorkoutTest(TestCase):
    def setUp(self):
        self.exs = [Exercise('Push-ups', 47, 10, 100),
                    Exercise('Squats', 47, 10, 100),
                    Exercise('Dead Bugs', 27, 10, 100)]
        self.wkt = Workout(self.exs)

    def test_init(self):
        w = Workout([])
        assert w.exercises == []
        assert w.workout is None

        assert self.wkt.exercises == self.exs
        assert self.wkt.workout is None

    @skip
    def test_generate(self):
        """Tests workout generation"""
        pass


class ExerciseTest(TestCase):

    def setUp(self):
        self.ex = Exercise('Push-ups', 33, 6, 66)
        self.weird_ex = Exercise('Weird', 38, 7)

    def test_init(self):
        assert self.ex.name == 'Push-ups'
        assert self.ex.reps == 33
        assert self.ex.set_limit == 6
        assert self.ex.rep_limit == 66
        assert self.ex.sets == [6, 6, 6, 6, 6, 3]

    def test_divvy_reps(self):
        self.ex.divvy_reps()
        assert self.ex.sets == [6, 6, 6, 6, 6, 3]

        self.weird_ex.divvy_reps()
        assert self.weird_ex.sets == [7, 7, 7, 7, 7, 3]

        self.ex.reps = 1
        self.ex.divvy_reps()
        assert self.ex.sets == [1]

        self.ex.reps = self.ex.rep_limit
        self.ex.divvy_reps()
        answer = [self.ex.set_limit for x in range(self.ex.reps //
                  self.ex.set_limit)]
        assert self.ex.sets == answer

    def test_drop_index(self):
        """Tests the first decremented index in a list is returned"""
        l = [2, 1]
        assert self.ex._drop_index(l) == 1

        l = [2, 2, 1]
        assert self.ex._drop_index(l) == 2

        l = [11, 11, 11, 11, 10, 6]
        assert self.ex._drop_index(l) == 4

        l = [11, 11, 11, 11, 1]
        assert self.ex._drop_index(l) == 0

    def test_crank_up(self):
        """Tests "building" phase"""
        sets = [1]
        assert self.ex._crank(sets, 1) == [1, 1]
        sets = [1]
        assert self.ex._crank(sets, 2) == [2]

        sets = [3, 3]
        assert self.ex._crank(sets, 3) == [3, 3, 1]
        sets = [3, 3]
        assert self.ex._crank(sets, 4) == [3, 4]

        sets = [8, 8, 8, 8, 5]
        assert self.ex._crank(sets, 8) == [8, 8, 8, 8, 6]

    def test_crank_down(self):
        """Tests "aggregatation" phase"""
        sets = [1, 1]
        assert self.ex._crank(sets) == [2]

        sets = [3, 3, 3, 3]
        sets = self.ex._crank(sets)
        assert sets == [4, 3, 3, 2]
        sets = self.ex._crank(sets)
        assert sets == [4, 4, 3, 1]
        sets = self.ex._crank(sets)
        assert sets == [4, 4, 4]

    def test_crank(self):
        """Tests crank's edge cases"""
        sets = [6, 6, 6, 6, 6, 4]
        ret = self.ex.crank()
        assert ret.sets == sets

        ex = Exercise('ex', 24, 5, 25)
        ret = ex.crank()
        assert ret.sets == [5, 5, 5, 5, 5]

        ret = ex.crank()
        assert ret.sets == [6, 5, 5, 5, 4]

        ex.sets, ex.reps = [24, 1], 49
        ret = ex.crank()
        assert ret.sets == [25]
