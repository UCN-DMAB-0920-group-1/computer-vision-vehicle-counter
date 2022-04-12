import logging
import datetime
from configuration import Configuration


class Logger:

    _currentdate = datetime.date.today().strftime('%Y-%m-%d')
    LOG_PATH = Configuration.get("LOG_PATH")
    logging.basicConfig(filename='{0}/{1}_API_SYSTEM.log'.format(LOG_PATH, _currentdate),
                        format='%(asctime)s %(message)s',
                        filemode='a')

    def logEntry(msg):
        _logger = logging.getLogger()
        _logger.setLevel(logging.DEBUG)
        _logger.debug(msg)
        print(msg)
