from datetime import datetime
from pprint import pformat
import logging

import ipdb
from ipdb import launch_ipdb_on_exception

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
log_fmt = logging.Formatter(
    "%(levelname)s %(filename)s.%(funcName)s:%(lineno)d\t%(message)s"
)
sh.setFormatter(log_fmt)
logger.addHandler(sh)


class ParseError(Exception):
    def __init__(self, message, callback):
        super().__init__(message)
        self.callback = callback


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
        ex, sets, tags, lines = parse_exercise(lines)
        exs.append({'name': ex, 'sets': sets, 'tags': tags})
    return wkt


def parse_timestamp(line):
    logger.debug(line)
    ts_format = '%Y %b %d @ %H%M'
    try:
        ts = datetime.strptime(line, ts_format)
    except:
        return ParseError('Timestamp: {}'.format(line), parse_timestamp)
    logger.info(ts)
    return ts


def parse_exercise(lines):
    logger.debug("Exercise: %s", lines)
    logger.debug("Before: %s", lines[0])
    # Exercise name & sets
    name, sets = parse_exercise_name(lines[0])
    logger.info('Name: %s, Sets: %s', name, sets)
    # Tags
    if len(lines) > 1:
        tags, lines = parse_tags(lines[1:])
    else:
        return name, sets, {}, []
    logger.debug("Remaining: %s", lines)
    return name, sets, tags, lines


def parse_exercise_name(line):
    try:
        return lines[0].split(':')
    except:
        return ParseError('Exercise: {}'.format(lines[0]), parse_exercise), ''


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


def parse_tag(line)
    try:
        return line.lstrip('- ').split(':')
    except:
        return ParseError('Tag: {}'.format(line), parse_tag)


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
        if isinstance(i, list) or isinstance(i, dict):
            dfs(i, fn)
        # not a list or dict; evaluate for error
        else:
            if isinstance(nest[i], ParseError):
                nest[i] = resolve_error(nest[i])


def resolve_error(err):
    print(err.args[0])
    redo = input('Please enter the corrected value: ').strip()
    done = 'no'
    while done not in ('y', 'yes'):
        done = input('Does this look right? {}'.format(redo))
    return redo
