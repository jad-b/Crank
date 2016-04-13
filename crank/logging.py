import logging
import sys

_logger = logging.getLogger('crank')
_logger.setLevel(logging.DEBUG)
_stdout_handler = logging.StreamHandler(sys.stdout)
_stdout_handler.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(levelname)s: %(message)s')
_stdout_handler.setFormatter(_formatter)
_logger.addHandler(_stdout_handler)

# Why am I aliasing this?
logger = _logger


def set_stdout_level(log_level):
    _stdout_handler.setLevel(log_level)
