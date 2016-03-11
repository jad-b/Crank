from datetime import datetime

from crank.workout import Workout
from crank.exercise import Exercise


TEST_WORKOUT_LINES = [
    '2015 Oct 19 @ 1800',
    '- This workout will suck.',
    'Swing, KB: 28 x 35',
    'Squat: 20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4',
    '- unit: kg',
    '- coming off drill weekend, tired and small',
    'Curl, ring: 10/5',
    'Plate pinch: 15 x 35/30'
]


TEST_WORKOUT = Workout(timestamp=TEST_WORKOUT_LINES[0],
                       tags={'comment': TEST_WORKOUT_LINES[1][2:]},
                       exercises=[
                           Exercise.parse_wkt([TEST_WORKOUT_LINES[2]]),
                           Exercise.parse_wkt(TEST_WORKOUT_LINES[3:6]),
                           Exercise.parse_wkt([TEST_WORKOUT_LINES[6]]),
                           Exercise.parse_wkt([TEST_WORKOUT_LINES[7]])
                            ])


TEST_WORKOUT_JSON = {
    'timestamp': TEST_WORKOUT.timestamp.isoformat(),
    'exercises': [ex.to_json() for ex in TEST_WORKOUT.exercises],
    'tags': {
        'comment': TEST_WORKOUT_LINES[1][2:]  # Drop '- '
    },
}


def test_parsing():
    wkt = Workout.parse_wkt(TEST_WORKOUT_LINES)
    assert isinstance(wkt.timestamp, datetime)
    assert 'comment' in wkt.tags
    assert len(wkt.exercises) == 4


def test_to_json():
    d = TEST_WORKOUT.to_json()
    assert 'timestamp' in d
    assert 'tags' in d
    assert 'exercises' in d


def test_from_json():
    w = Workout.from_json(TEST_WORKOUT_JSON)
    assert w.timestamp == TEST_WORKOUT.timestamp
    assert w.tags == TEST_WORKOUT.tags
    assert w.exercises == TEST_WORKOUT.exercises


def test_encoding():
    assert TEST_WORKOUT.to_json() == TEST_WORKOUT_JSON
