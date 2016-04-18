import re

from colorama import Fore, Style

from crank.util.cli import read_until_valid, confirm_input
from crank.core.set import (fix_set_string, partition_set_tokens,
                            process_set_partitions)


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
