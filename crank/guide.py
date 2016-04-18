import re

from colorama import Fore, Style

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


def review_raw_sets(wkts):
    """Show the Sets with unparsed set strings."""
    i = 0
    for w, ex, raw in raw_sets(wkts):
        print("{}: {:s}".format(ex.name, raw))
        i += 1
    print("{:d} sets found with raw_sets attributes".format(i))


def guided_mediation(w, ex, raw):
    """CLI prompts to fix Set strings well-enough for reading."""
    print("{}| Original Set string: {}".format(ex.name, raw))
    choice = read_until_valid("Attempt, Rewrite, Step-through, Skip, or Drop?",
                              ['a', 'r', 's', 'k', 'd'])
    if choice == 'a':
        # Attempt to parse sets into reasonable partitions
        parts = partition_set_tokens(raw)
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
