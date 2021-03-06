from datetime import datetime

from crank.core.workout import Workout
from crank.core.exercise import Exercise


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


TEST_WORKOUT_EXERCISES = [
    Exercise.parse([TEST_WORKOUT_LINES[2]])[0],
    Exercise.parse(TEST_WORKOUT_LINES[3:6])[0],
    Exercise.parse([TEST_WORKOUT_LINES[6]])[0],
    Exercise.parse([TEST_WORKOUT_LINES[7]])[0]
]
TEST_WORKOUT = Workout(timestamp=TEST_WORKOUT_LINES[0],
                       tags={'comment': TEST_WORKOUT_LINES[1][2:]},
                       exercises=TEST_WORKOUT_EXERCISES)

TEST_WORKOUT_EXERCISE_JSON = [ex.to_json() for ex in TEST_WORKOUT_EXERCISES]
TEST_WORKOUT_JSON = {
    'timestamp': TEST_WORKOUT.timestamp.isoformat(),
    'exercises': TEST_WORKOUT_EXERCISE_JSON,
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
