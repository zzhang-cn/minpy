#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Logging utilities."""
import logging

class _Formatter(logging.Formatter):
    """Customized log formatter."""

    def __init__(self):
        datefmt = '%m%d %H:%M:%S'
        #super().__init__(datefmt=datefmt, style='{')
        super(_Formatter, self).__init__(datefmt=datefmt)

    def _get_color(self, level):
        if logging.WARNING <= level:
            return '\x1b[31m'
        elif logging.INFO <= level:
            return '\x1b[32m'
        else:
            return '\x1b[34m'

    def _get_label(self, level):
        if level == logging.CRITICAL:
            return 'C'
        elif level == logging.ERROR:
            return 'E'
        elif level == logging.WARNING:
            return 'W'
        elif level == logging.INFO:
            return 'I'
        elif level == logging.DEBUG:
            return 'D'
        else:
            return 'U'

    def format(self, record):
        fmt = self._get_color(record.levelno)
        fmt += self._get_label(record.levelno)
        fmt += '[%(asctime)s %(process)d %(filename)s:%(lineno)d:%(funcName)s]\x1b[0m'
        fmt += ' %(message)s'
        self._fmt = fmt
        #self._style._fmt = fmt
        return super(_Formatter, self).format(record)

_handler = logging.StreamHandler()
_handler.setFormatter(_Formatter())

def get_logger(name=None, level=logging.INFO):
    """Get customized logger.

    Args:
        name: Name of the logger.
        level: Level to log.

    Returns:
        A logger.
    """
    logger = logging.getLogger(name)
    if name and not getattr(logger, '_init_done', None):
        logger._init_done = True
        logger.addHandler(_handler)
        logger.setLevel(level)
    return logger
