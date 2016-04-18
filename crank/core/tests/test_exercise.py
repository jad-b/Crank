from crank.core.exercise import Exercise


TEST_EXERCISE_LINES = [
    'Swing, KB: 28 x 35',
    'Squat: 20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4',
    '- unit: kg',
    '- coming off drill weekend, tired and small',
    'Curl, ring: 10/5',
    'Plate pinch: 15 x 35/30'
]

TEST_EXERCISE_V2_LINES = [
    'Swing, KB:',
    '  1) 28 x 35',
    '- units: kgs x reps',
    'Squat:',
    '- unit: kg',
    '- coming off drill weekend, tired and small',
    '  2) 20 x 5',
    '  3) [30] 60 x 5',
    '  4) 80 x 3',
    '  5) [30] 90 x 3',
    '  6) 91 x 5',
    '  7) 105 x 5',
    '  8) [300] 119 x 4',
    'Curl, ring:',
    '- units: lbs x reps',
    '  9) 10',
    '  10) [30] 5',
    'Plate pinch: ',
    '- unit: kgs x seconds',
    '  11) 15 x 35',
    '  12) [60] 15 x 30'
]

TEST_SQUAT_LINES = TEST_EXERCISE_V2_LINES[3:13]

TEST_SQUAT_V2_JSON = {
    'name': 'Squat',
    'tags': {
        'unit': 'kgs x reps',
        'comment': 'coming off drill weekend, tired and small',
    },
    'sets': [
        {'work': 20, 'reps': 5, 'order': 2},
        {'work': 60, 'reps': 5, 'order': 2, 'rest': 30},
        {'work': 80, 'reps': 3, 'order': 2},
        {'work': 90, 'reps': 3, 'order': 2, 'rest': 30},
        {'work': 91, 'reps': 5, 'order': 2},
        {'work': 105, 'reps': 5, 'order': 2},
        {'work': 119, 'reps': 4, 'order': 2, 'rest': 300},
    ],
}

TEST_EXERCISE = Exercise(**TEST_SQUAT_V2_JSON)


def test_exercise_parsing():
    ex = Exercise.parse_exercise(TEST_SQUAT_LINES)
    assert ex == TEST_EXERCISE, str(ex)


def test_to_json():
    d = TEST_EXERCISE.to_json()
    assert 'name' in d
    assert 'tags' in d
    assert 'sets' in d
    assert 'raw_sets' not in d


def test_from_json():
    ex = Exercise.from_json(TEST_SQUAT_V2_JSON)
    assert ex.name == TEST_EXERCISE.name
    assert ex.tags == TEST_EXERCISE.tags
    assert ex.raw_sets == TEST_EXERCISE.raw_sets
    assert ex.sets == TEST_EXERCISE.sets


def test_encoding():
    assert TEST_EXERCISE.to_json() == TEST_SQUAT_V2_JSON


def test_parsing_exercise_lines():
    exs = Exercise.parse_exercises(TEST_EXERCISE_LINES)
    assert len(exs) == 4
