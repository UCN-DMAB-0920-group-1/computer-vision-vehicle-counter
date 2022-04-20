from cgitb import handler
import logging
import datetime
import sys

from flask import Config
from configuration import Configuration


class Logger:

    _currentdate = datetime.date.today().strftime('%Y-%m-%d')
    LOG_PATH = Configuration.get("APP_SETTINGS.LOG_PATH")
    PRINT_LOG = Configuration.get("APP_SETTINGS.PRINT_LOG_ENTRY")

    _handlers = []
    _handlers.append(logging.FileHandler(
        '{0}/{1}_API_SYSTEM.log'.format(LOG_PATH, _currentdate), "a"))
    if PRINT_LOG:
        _handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        handlers=_handlers)

    def logEntry(msg):
        _logger = logging.getLogger()
        _logger.debug(msg)
