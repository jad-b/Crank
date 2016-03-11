from crank.exercise import Exercise


TEST_EXERCISE_LINES = [
    'Swing, KB: 28 x 35',
    'Squat: 20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4',
    '- unit: kg',
    '- coming off drill weekend, tired and small',
    'Curl, ring: 10/5',
    'Plate pinch: 15 x 35/30'
]

TEST_SQUAT_LINES = TEST_EXERCISE_LINES[1:4]


TEST_SQUAT_JSON = {
    'name': 'Squat',
    'tags': {
        'unit': 'kg',
        'comment': 'coming off drill weekend, tired and small',
    },
    'sets': '20, 60 x 5, 80, 90 x 3, 91, 105 x 5, 119 x 4'
}

TEST_EXERCISE_INSTANCE = Exercise(**TEST_SQUAT_JSON)


def test_exercise_parsing():
    ex = Exercise.parse_wkt(TEST_SQUAT_LINES)
    assert ex == TEST_EXERCISE_INSTANCE, str(ex)


def test_to_json():
    d = TEST_EXERCISE_INSTANCE.to_json()
    assert 'name' in d
    assert 'tags' in d
    assert 'sets' in d


def test_from_json():
    ex = Exercise.from_json(TEST_SQUAT_JSON)
    assert ex.name == TEST_EXERCISE_INSTANCE.name
    assert ex.tags == TEST_EXERCISE_INSTANCE.tags
    assert ex.sets == TEST_EXERCISE_INSTANCE.sets


def test_encoding():
    ex = Exercise.parse_wkt(TEST_SQUAT_LINES)
    assert ex.to_json() == TEST_SQUAT_JSON
