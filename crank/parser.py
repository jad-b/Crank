from datetime import datetime
import logging
import re

LOGGER = logging.getLogger(__name__)
LOGGER.propagate = False
LOGGER.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
log_fmt = logging.Formatter(
    "%(levelname)s %(filename)s.%(funcName)s:%(lineno)d\t%(message)s"
)
sh.setFormatter(log_fmt)
LOGGER.addHandler(sh)


class ParseCallback:

    def __init__(self, field, value, callback):
        self.field = field
        self.value = value
        self.callback = callback

    def resolve(self):
        # Display incorrect field
        print("{}: {}".format(self.field, self.value))
        done = 'no'
        while done not in ('y', 'yes'):
            # Request user correction
            redo = input('Please enter the corrected value: ').strip()
            # Verify input
            done = input('Does this look right? "{}" '.format(redo))
        # Apply callback
        return self.callback(redo)

    def __str__(self):
        return "{}: {}".format(self.field, self.value)


def parse_timestamp(line):
    ts_formats = (
        '%Y %b %d @ %H%M',
        '%d %b %Y @ %H%M',
        '%d %B %Y @ %H%M',
    )

    exc = None
    for fmt in ts_formats:
        try:
            return datetime.strptime(line, fmt)
        except Exception as e:
            exc = e
    else:
        LOGGER.warning("Failed to parse: %s", line)
        raise exc


def stream_str_blocks(s):
    """Group a string into a stream of lists by newline."""
    return buffer_data(line for line in s.split('\n'))


def stream_file(filename):
    LOGGER.debug('opening %s', filename)
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


def split_iter(string, delim_pattern=r"[^\n]"):
    return (x.group(0) for x in re.finditer(delim_pattern, string))


def dfs(nest, fn):
    for i in nest:
        # Keep recurring
        if isinstance(nest, list):
            dfs(i, fn)
        if isinstance(nest, dict):
            dfs(nest[i], fn)
        # not a list or dict; evaluate for error
        else:
            fn(nest, i)


def resolve_errors(struct, idx):
    if isinstance(struct[idx], ParseCallback):
        struct[idx] = struct[idx].callback()
