from crank.util import stream


def test_split_iter():
    ex1 = """This is a string.
        For which I don't really care.
        But here it is.
        So what you gonna do?"""
    io = (
        (ex1, ex1.split('\n')),
    )
    for test_in, test_out in io:
        assert test_out == list(stream.split_iter(test_in))
