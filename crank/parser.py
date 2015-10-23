from datetime import datetime
from pprint import pformat
import logging

import ipdb
from ipdb import launch_ipdb_on_exception

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
log_fmt = logging.Formatter(
    "%(levelname)s %(filename)s.%(funcName)s:%(lineno)d\t%(message)s"
)
sh.setFormatter(log_fmt)
logger.addHandler(sh)


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


def parse_workouts(wkt_src):
    with launch_ipdb_on_exception():
        return (parse_workout(wkt) for wkt in wkt_src)


def parse_workout(lines):
    wkt = {}
    if len(lines) == 0:
        return wkt
    logger.debug('%s', pformat(lines))
    # Timestamp
    wkt['timestamp'] = parse_timestamp(lines[0])
    lines = lines[1:]
    # Tags
    wkt['tags'], lines = parse_tags(lines)
    # Exercises
    wkt['exercises'] = exs = []
    while len(lines) > 0:
        ex, lines = parse_exercise(lines)
        exs.append(ex)
    return wkt


def parse_timestamp(line):
    logger.debug(line)
    ts_formats = (
        '%Y %b %d @ %H%M',
        '%d %b %Y @ %H%M',
        '%d %B %Y @ %H%M',
    )

    for fmt in ts_formats:
        try:
            return datetime.strptime(line, fmt)
        except:
            pass
    else:
        return ParseCallback('Timestamp', line, parse_timestamp)


def parse_exercise(lines):
    logger.debug("Exercise: %s", lines)
    logger.debug("Before: %s", lines[0])
    # Exercise name & sets
    ex = {}
    ex['name'], ex['sets'] = parse_exercise_name(lines[0])
    lines = lines[1:]
    logger.info('Name: %s, Sets: %s', ex['name'], ex['sets'])
    # Tags
    if len(lines) > 1:
        ex['tags'], lines = parse_tags(lines)
    logger.debug("Remaining: %s", lines)
    return ex, lines


def parse_exercise_name(line):
    try:
        name_sets = line.split(':')
        if len(name_sets) != 2:
            return ParseCallback('exercise name', line, parse_exercise), ''
        return name_sets[0], name_sets[1]
    except Exception as e:
        logger.exception('Error while parsing exercise')
        return ParseCallback('exercise name', line, parse_exercise), ''


def parse_tags(lines):
    tags = {}
    for i, line in enumerate(lines):
        if line.startswith('-'):
            parts = parse_tag(line)
            if len(parts) == 1:
                tags['comment'] = parts[0]
            else:
                tags[parts[0]] = parts[1]
        else:
            break
    logger.debug("Tags: %s", tags)
    return tags, lines[len(tags):]


def parse_tag(line):
    try:
        return line.lstrip('- ').split(':')
    except:
        return ParseCallback('Tag: {}'.format(line), parse_tag)


def stream_blocks(filename):
    return buffer_blocks(stream_file(filename))


def stream_file(filename):
    logger.debug('opening %s', filename)
    with open(filename) as fp:
        for line in fp:
            yield line

def buffer_blocks(source):
    bfr = []
    for line in source:
        if line == '\n':
            # Return copy of buffer
            if bfr: # But only if there's something there
                yield list(bfr)
                bfr.clear()
        else:
            bfr.append(line.strip())
    yield bfr


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
    if isinstance(struct[i], ParseCallback):
        struct[i] = struct[i].callback()
