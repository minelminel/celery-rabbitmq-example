import logging
from artifice.scraper.foreground.models import db, Queue, Content

log = logging.getLogger(__name__)

def my_func():
    # here should be something actually useful
    log.info('This message is coming from within the custom graph function.')
    return 3

schedule = {'weeks': 0,
             'days': 0,
             'hours': 0,
             'minutes': 0,
             'seconds': 30}
