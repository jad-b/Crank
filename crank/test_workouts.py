import os

from blist import sortedset

from crank.workouts import Workouts


def test_workouts_storage():
    """Parse, save, and load workouts from file(s)."""
    wkts = Workouts.from_file('crank/squat.txt')
    assert len(wkts.workouts) == 43

    wkts_filename = 'workouts.json.test'
    wkts.filename = wkts_filename
    wkts.save()
    assert os.path.exists(wkts_filename)
    del wkts

    wkts2 = Workouts(wkts_filename)
    wkts2.load()
    assert len(wkts2.workouts) == 43, wkts2.workouts
    assert isinstance(wkts2.workouts, sortedset)
