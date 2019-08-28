import logging
import redis
from flask import current_app

from .. import redis_client

log = logging.getLogger(__name__)

def increment_redis_hits():
    key = current_app.config['REDIS_HIT_COUNTER']
    try:
        redis_client.incr(key)
    except redis.exceptions.ConnectionError as e:
        log.error(f'[INCREMENT HITS] {str(e)}')
        pass

def get_redis_hits():
    key = current_app.config['REDIS_HIT_COUNTER']
    try:
        hits = int(redis_client.get(key))
    except redis.exceptions.ConnectionError as e:
        log.error(f'[BEFORE FIRST REQUEST] {str(e)}')
        hits = None
    return hits

def reset_redis_hits():
    key = current_app.config['REDIS_HIT_COUNTER']
    try:
        redis_client.set(key, 0)
    except redis.exceptions.ConnectionError as e:
        log.error(f'[RESET REDIS HITS] {str(e)}')
        pass
