from crank import tags

TEST_TAGS = [
    '- 1RM: 300',
    "- Freakin' tired. Maybe not enough kcals.",
    'Curl, Ring: 8?',  # Should terminate at the next exercise
    '- Good burn.'
]


def test_tag_parsing():
    exp = {'1RM': '300', 'comment': "Freakin' tired. Maybe not enough kcals."}
    obs, remainder = tags.parse_tags(TEST_TAGS)
    assert exp == obs
    assert remainder == TEST_TAGS[2:]
