from crank.util.logging import logger


def parse_tags(lines):
    tags = {}
    for i, line in enumerate(lines):
        if line.startswith('-'):  # Valid tag prefix
            parts = parse_tag(line)
            if len(parts) == 1:
                tags['comment'] = parts[0].strip()
            else:
                tags[parts[0]] = parts[1].strip()
        else:
            break
    if tags:
        logger.debug("Parsed tags: %s", tags)
    return tags, lines[len(tags):]


def parse_tag(line):
    try:
        return line.lstrip('- ').split(':')
    except:
        return line
