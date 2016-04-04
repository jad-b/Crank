import logging

_logger = logging.getLogger('crank')
_logger.setLevel(logging.DEBUG)
_stderr_handler = logging.StreamHandler()
_stderr_handler.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(levelname)s: %(message)s')
_stderr_handler.setFormatter(_formatter)
_logger.addHandler(_stderr_handler)

# Why am I aliasing this?
logger = _logger


def set_stderr_level(log_level):
    _stderr_handler.setLevel(log_level)
