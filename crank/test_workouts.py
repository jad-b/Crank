import json
import os

from blist import sortedset

from crank.workouts import Workouts, WorkoutsJSONEncoder


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


def test_workouts_encoding():
    wkts = Workouts.from_file('crank/squat.txt')
    wkts_json = json.dumps(wkts, cls=WorkoutsJSONEncoder)
    wkts2 = json.loads(wkts_json, object_hook=Workouts.from_dict)
    assert wkts.filename == wkts2.filename
    assert wkts.workouts == wkts2.workouts
