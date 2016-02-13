from crank.parser import LOGGER


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
    LOGGER.debug("Tags: %s", tags)
    return tags, lines[len(tags):]


def parse_tag(line):
    try:
        return line.lstrip('- ').split(':')
    except:
        return ParseCallback('Tag: {}'.format(line), parse_tag)

