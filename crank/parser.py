from datetime import datetime
import re

from colorama import Fore, Style
import dateutil.parser

from crank.logging import logger
from crank.fto.cli import read_until_valid, confirm_input
from crank.set import fix_set_string, Set, string_tokenizer, process_rep


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
    print("{}| Original Set string: {}".format(ex.name, raw))
    choice = read_until_valid("Attempt, Rewrite, Step-through, Skip, or Drop?",
                              ['a', 'r', 's', 'k', 'd'])
    if choice == 'a':
        # Attempt to parse sets into reasonable partitions
        parts = partition_set_string(raw)
        print("Estimated Set partitions:\n\t" + '\n\t'.join(parts))
        good = read_until_valid("Does this look good?", ['y', 'n'])
        if good == 'y':
            ex.sets = process_set_partitions(parts)
            ex.raw_sets = ''
    elif choice == 'r':
        guided_mediation(w, ex, fix_set_string(raw))
    elif choice == 's':
        sets = step_through_set_string(raw)
        ex.sets = process_set_partitions(sets)
        ex.raw_sets = ''
    elif choice == 'd':
        yep = read_until_valid('Delete; are you sure? ', ['y', 'n'])
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
    buf, workbuf = [], []
    parser = string_tokenizer(s)
    prev = ''
    for val in parser:
        if val == 'x':
            pass
        elif prev == 'x':  # This value is a rep
            vals = process_rep(val)
            buf.append((tuple(workbuf), tuple(vals)))
            workbuf = []
        else:
            workbuf.append(int(val))
        prev = val
    return buf


def process_set_partitions(parts):
    """Convert a pre-partitioned list of (work, rep) tuples into Set objects.

    This function can handle shorthand expansion, e.g. a tuple like
    ``((150,), (8, 6, 3))`` knows to apply the Work, 150, across all three Rep
    values, creating three Sets.
    """
    sets = []
    for piece in parts:
        if len(piece[0]) == 1 and len(piece[1]) == 1:
            sets.append(Set(piece[0][0], piece[1][0]))
        elif len(piece[0]) > 1 and len(piece[1]) == 1:
            rep = piece[1][0]
            for w in piece[0]:
                sets.append(Set(w, rep))
        elif len(piece[0]) == 1 and len(piece[1]) > 1:
            w = piece[0][0]
            for rep in piece[1]:
                sets.append(Set(w, rep))
        else:
            raise ValueError("Invalid (work, rep) tuple:\n{}"
                             .format(str(parts)))
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
        if val == 'x':
            print("Saw 'x'")
            continue
        prompt = "({}) Work or Reps?".format(Fore.GREEN + val + Style.RESET_ALL)
        wr = read_until_valid(prompt, ['w', 'r'])
        if wr == 'w':
            if last == 'r':
                # Save the split we arrived at
                parts.append((tuple(workbuf), tuple(repbuf)))
                workbuf, repbuf = list(), list()
            workbuf.append(int(val))
        elif wr == 'r':
            try:
                repbuf.append(int(val))
            except ValueError:  # Not an int
                rewrite = input('Please space-separate the reps: ')
                while not confirm_input(rewrite):
                    rewrite = input('Please space-separate the reps: ')
                repbuf.extend(map(int, rewrite.split(' ')))
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
