from datetime import datetime

import dateutil.parser

from crank.util.logging import logger


DATETIME_FORMAT = '%Y %b %d @ %H%M'


def get_timestamp_header():
    return datetime.now().strftime(DATETIME_FORMAT)


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
