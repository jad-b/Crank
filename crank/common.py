"""
util
===
Common utilities across the Crank system.
"""
from datetime import datetime


DATETIME_FORMAT = '%Y %b %d @ %H%M'


def get_timestamp_header():
    return datetime.now().strftime(DATETIME_FORMAT)
