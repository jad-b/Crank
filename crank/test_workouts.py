import json
import os

from blist import sortedset

from crank.workouts import Workouts, WorkoutsJSONEncoder


TEST_WKT_FILE = 'crank/squat.wkt'


def test_workouts_storage():
    """Parse, save, and load workouts from file(s)."""
    wkts = Workouts.parse_wkt(TEST_WKT_FILE)
    assert len(wkts.workouts) == 43

    wkts_filename = 'workouts.json.test'
    wkts.filename = wkts_filename
    wkts.save()
    assert os.path.exists(wkts_filename)
    del wkts

    wkts2 = Workouts.load(wkts_filename)
    assert len(wkts2.workouts) == 43, wkts2.workouts
    assert isinstance(wkts2.workouts, sortedset)


def test_workouts_encoding():
    wkts = Workouts.parse_wkt(TEST_WKT_FILE)
    wkts_json = json.dumps(wkts, cls=WorkoutsJSONEncoder)
    wkts2 = json.loads(wkts_json, object_hook=Workouts.from_dict)
    assert wkts.filename == wkts2.filename
    assert wkts.workouts == wkts2.workouts
