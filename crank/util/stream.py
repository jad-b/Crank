import re

from crank.util.logging import logger


def stream_str_blocks(s):
    """Group a string into a stream of lists by newline."""
    return buffer_data(line for line in s.split('\n'))


def stream_file(filename):
    logger.debug('opening %s', filename)
    with open(filename) as fp:
        for line in fp:
            yield line


def buffer_data(source, delim='\n'):
    """Group data into a stream of lists."""
    bfr = []
    for line in source:
        if line == delim or not line:  # newline or empty string
            if bfr:  # if there's something there
                yield list(bfr)  # Return copy of buffer
                bfr.clear()
        else:
            bfr.append(line.strip())
    if bfr:
        yield bfr


def split_iter(string, delim_pattern=r"[^\n]+"):
    return (x.group(0) for x in re.finditer(delim_pattern, string))
