import re
import textwrap

import numpy as np

from crank.core.set import Set
from crank.util.logging import logger
from crank.util.cli import confirm_input


def parse_v1_sets(value):
    sets = parse_simple_sets(value)
    try:
        return validate_sets(value, sets), ''
    except SyntaxError:
        return [], value


def set_parsing_pipeline(s):
    """Parse sets through a series of steps.

        1. string => Tokenize => [int]
        2. Partition => [(work,), (reps,)]
        3. Process => [Set]

    If an error occurs during any step, the original value is returned.
    """
    # Tokenize set string
    tokens = None
    try:
        tokens = string_tokenizer(s)
    except:
        return s
    # Partition tokens into collections of work and rep pairings
    parts = None
    try:
        parts = partition_set_tokens(tokens)
    except:
        return list(tokens)
    # Process partitions into a list of Sets
    sets = None
    try:
        sets = process_set_partitions(parts)
    except:
        return parts
    return sets


def partition_set_tokens(tokens):
    """Divide a raw Set string into collections of work and repetitions.

    This process is guided by basic syntax rules (and heuristics where those
    fail), and represents a "best-guess" partitioning. If the partitioning is
    correct, the output can be unambiguously converted into Sets.
    """
    buf, workbuf = [], []
    prev = ''
    for token in tokens:
        if token == 'x':
            pass
        elif prev == 'x':  # This value is a rep
            vals = process_rep(token)
            buf.append((tuple(workbuf), tuple(vals)))
            workbuf = []
        else:
            workbuf.append(int(token))
        prev = token
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


def validate_sets(string, sets):
    """Validate our parsed Sets."""
    # Simple sets follow 'Work x Reps'; 1 Set per 2 Numbers
    estd_sets = len(re.findall(r'(\d+)', string)) / 2.
    if len(sets) != estd_sets or len(sets) != string.count('x'):
        logger.warning('%d sets anticipated, found %d', estd_sets, len(sets))
        raise SyntaxError('Failed to parse {}'.format(string))
    return sets


def parse_simple_sets(string):
    """Parse the most basic Set string: Work x Reps"""
    simple_re = r'(\d+)\s*x\s*(\d+)'
    sets = []
    for m in re.finditer(simple_re, string):
        sets.append(Set(work=int(m.groups()[0]),
                        reps=int(m.groups()[1])))
    return sets


def fix_set_string(string):
    """Guide the user through fixing their broken, broken Set string syntax."""
    print('We were unable to parse this string for Sets:\n{}'.format(string))
    s = input('Please re-type the string:\n')
    while not confirm_input(s):
        s = input('Please re-type corrections:\n')
    return s


def string_tokenizer(string):
    """Yield parsed components of a set string."""
    # An 'x', or everything not an x, comma, or whitespace
    chunk_re = r'(x|[^x,\s]+)'
    for m in re.finditer(chunk_re, string):
        yield m.group().strip()


def parse_complex_sets(string):
    """Iteratively parse a Set string."""
    logger.debug("Parsing Sets from: {}".format(string))
    parser = string_tokenizer(string)

    # All numbers up to the first X are work sets
    work = []
    while True:
        val = next(parser)
        if val == 'x':
            break
        work.append(val)
        logger.debug("Parsed: {:s}".format(val))
    # Assumption: All values up to the first 'x' have been parsed.
    logger.debug("Pre-loaded work: {:s}".format(str(work)))

    sets = []
    reps = []
    for m in parser:
        val = m.group().strip()
        if val == 'x':
            work, reps, sets = process_sets(work, reps, sets)
        else:
            reps.append(val)
            logger.debug("Reps: {:s}".format(str(reps)))
    else:  # Final processing
        work, reps, sets = process_sets(work, reps, sets, eof=True)
    # Nothing should be left in the work or reps buffers
    assert not work
    assert not reps
    return sets


def process_sets(work, reps, sets, eof=False):
    logger.debug(textwrap.dedent(
        """
        Before
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    # import pdb
    # pdb.set_trace()
    if len(work) > 1:  # Multiple work values stored
        logger.debug("Shorthand: Multiple sets @ same weight")
        assert reps, "Multiple work sets detected with no reps listed"
        demux_work(work, reps[0])
        work = reps[1:]  # Remainder *must* be new work values
    else:  # 1 work value(s), 0 to n reps
        logger.debug("Shorthand: Multiple sets @ same weight")
        assert len(work) == 1, "Expected one work value"
        w = work[0]
        if eof:  # No more to parse; it's all reps
            logger.debug("EOF sent; parsing all reps in relation to work")
            reps, new_work = reps, []
        else:
            # Find the best split between reps for this value of work and
            # the start of a new run of work values.
            reps, new_work = split_reps(w, reps)

        for r in reps:  # Process each rep
            sets.extend(process_rep(w, r, sets[-1]))

        work = new_work

    # Reps should *always* get reset
    reps = []

    logger.debug(textwrap.dedent(
        """
        After
        ======
        Work: {:s}
        Reps: {:s}
        """.format(str(work), str(reps))))

    return work, reps, sets


def split_reps(w, reps):
    logger.debug("Splitting {}".format(str(reps)))
    if len(reps) < 2:
        return reps, []
    idx, _ = max_slope(reps)
    r, w = reps[:idx], reps[idx:]
    logger.debug("\t{}\n\t{}".format(str(r), str(w)))
    return r, w


def demux_work(work, reps):
    """Parses a run of sets at the same level of work.

    Uses an error heuristic to determine where the next rep might actually be
    the start of new work levels. For example, '20 x 12, 13, 25, 30 x 6' should
    recognize that 25 was weight performed for 6 reps, not 25 reps at 20 lbs.
    """
    logger.debug("demux_work: {} x {}".format(work, str(reps)))
    sets = []
    for w in work:
        sets.append(Set(work=w, reps=reps[0]))
    return sets


def max_err(w, reps):
    """Calculate the maximum error between the work value and rep values."""
    def err(r, w):
        return abs((w-r)/w)

    # Calculate error between each supposed rep and the weight
    err_arr = np.apply_along_axis(err, 0, reps, *(w,))
    # Find the differences between each error
    return max_slope(err_arr)


def max_slope(reps):
    """Find the maximum slope between two points in an array."""
    slopes = [0]
    for i in range(1, len(reps)):
        slopes.append(abs(reps[i] - reps[i-1]))
    return np.argmax(slopes), slopes/np.max(slopes)


def work_rep_sim(work, reps):
    def sim(a, b):
        """Similarity between a and b. Lower is better."""
        return abs(a-b)

    sims = []
    for r in reps:
        sims.append((sim(work, r), sim(reps[0], r)))
    for i, s in enumerate(sims):
        # Change when the rep becomes more similar to the work
        # than the first rep
        if s[0] < s[1]:
            return i, sims
    return i, np.array(sims)/np.max([work]+reps)


def process_rep(r):
    try:  # To save it as a normal rep
        return (int(r),)
    except ValueError:
        # try our special cases
        setz = rest_pause(r)
        if setz:
            return setz
        setz = multiply_reps(r)
        if setz:
            return setz


def rest_pause(r):
    """Parses a rest-pause set into multiple sets."""
    sets = []
    rest_pause = r.split('/')
    if len(rest_pause) > 1:
        for rep in rest_pause:
            sets.append(int(rep.strip()))
    return sets


def multiply_reps(r):
    """Multiplies the previous set."""
    sets = []
    # Look for the multiplier notation: (\d+)
    m = re.match(r'(\d+)\s*\((\d+)\)', r)
    if m:  # Rep multiplier; 100 x 3 (5)
        val, mult = int(m.groups()[0]), int(m.groups()[1])
        # Make add'l copies of the previous set
        for i in range(mult):
            sets.append(val)
    return sets
