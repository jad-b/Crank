from datetime import datetime
import re

import dateutil.parser

from crank.logging import logger
from crank.fto.cli import read_until_valid
from crank.set import fix_set_string


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


def fix_workouts(wkts):
    """Iterate through Workouts and fix problems.

    Problem of the Day: Unparseable Set strings!
    """
    try:
        for w, ex, raw in raw_sets(wkts):
            guided_mediation(w, ex, raw)
    finally:
        wkts.save()


def raw_sets(wkts):
    """Find all the Exercises with unparsed Set strings."""
    for w in wkts.workouts:
        for ex in w.exercises:
            if ex.raw_sets:
                yield (w, ex, ex.raw_sets)


def guided_mediation(w, ex, raw):
    """CLI prompts to fix Set strings well-enough for reading."""
    print("Original: ", raw)
    choice = read_until_valid("Attempt, Rewrite, Step-through, Skip, or Drop?",
                              ['a', 'r', 's', 'k', 'd'])
    if choice == 'a':
        # Attempt to partition sets into reasonable partitions
        parts = partition_set_string(raw)
        print("Estimated Set partitions:\n\t" + '\n\t'.join(parts))
        good = read_until_valid("Does this look good?", ['y', 'n'])
        if good == 'y':
            process_set_partitions(parts)
    elif choice == 'r':
        fix_set_string(raw)
    elif choice == 's':
        sets = step_through_set_string(raw)
        ex.sets = sets
        ex.raw_sets = ''
    elif choice == 'd':
        yep = read_until_valid('Are you sure? [y/n]) ', ['y', 'n'])
        if yep == 'y':
            w.remove(ex)
        else:
            guided_mediation(w, ex, raw)


def partition_set_string(s):
    """Divide a raw Set string into collections of work and repetitions.

    This process is guided by basic syntax rules (and heuristics where those
    fail), and represents a "best-guess" partitioning. If the partitioning is
    correct, the output can be unambiguously converted into Sets.
    """
    return [(), ()]


def process_set_partitions(parts):
    """Convert a pre-partitioned list of (work, rep) tuples into Set objects.

    This function can handle shorthand expansion, e.g. a tuple like
    ``((150,), (8, 6, 3))`` knows to apply the Work, 150, across all three Rep
    values, creating three Sets.
    """
    sets = []
    return sets


def step_through_set_string(s):
    """Guided partitioning of a Set string into work and repetitions.

    Returns a list of [(work, reps)] tuples. Each tuple should be an
    unambiguous representation of one or more Sets.
    """
    parts = []
    chunk_re = r'(x|[^x,\s]+)'
    last = ''  # Last value was Work or Rep(s)
    workbuf, repbuf = list(), list()

    print("Original: ", s)
    for m in re.finditer(chunk_re, s):
        val = m.group().strip()
        wr = read_until_valid(val + "\n\tWork or Reps?", ['w', 'r'])
        if wr == 'w':
            if last == 'r':
                # Save the split we arrived at
                parts.append((tuple(workbuf), tuple(repbuf)))
            workbuf.append(int(val))
        elif wr == 'r':
            repbuf.append(int(val))
        last = wr
    return parts


def parse_timestamp(line):
    ts_formats = (
        '%Y %b %d @ %H%M',
        '%d %b %Y @ %H%M',
        '%d %B %Y @ %H%M',
        '%d%b%Y@%H%M',
        '%d%b%Y @ %H%M',
    )

    # Try ISO8601
    try:
        return dateutil.parser.parse(line)
    except:
        pass
    exc = None
    for fmt in ts_formats:
        try:
            return datetime.strptime(line, fmt)
        except Exception as e:
            exc = e
    else:
        logger.warning("Failed to parse: %s", line)
        raise exc


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
