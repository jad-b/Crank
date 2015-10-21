def parse_workout(lines):
    wkt = {}
    wkt['timestamp'] = parse_timestamp(lines[0])
    if lines[1].startswith('-'):
        wkt['tags'], lines = parse_tags(lines[1:])
    wkt['exercises'] = exs = []
    while len(lines) > 0:
        ex, sets, tags, lines = parse_exercise(lines)
        exs.append({'name': ex, 'sets': sets, 'tags': tags})
    return wkt


def parse_timestamp(line):
    ts_format = '%Y %b %d @ %H%M'
    return datetime.strptime(line, ts_format)


def parse_exercises(lines):
    name, sets = line[0].split(':')
    lines = lines[1]
    if lines[0].startswith('-'):
        tags, lines = parse_tags(lines)
    return name, sets, tags, lines


def parse_tags(lines):
    tags = {}
    for i, line in enumerate(lines):
        if line.startswith('-'):
            parts = line.lstrip('- ').split(':')
            if len(parts) == 1:
                tags['comment'] = parts
            else:
                tags[parts[0]] = parts[1]
        else:
            return tags, lines[i:]


def read_until_blankline(source):
    bfr = []
    for line in source:
        if line == '\n':
            # Return copy of buffer
            yield list(bfr)
            bfr.clear()
        else:
            bfr.append(line.strip())
    yield bfr
