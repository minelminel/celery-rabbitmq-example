from __future__ import absolute_import
from test_celery.celery import app as celery_app
import time

consumer_queue = 'celery'
consumer = 'Michaels-MBP.home'


def pause():
    print('[PAUSE] Starting')
    celery_app.control.cancel_consumer(consumer_queue)
    print('[PAUSE] Finished')


def resume():
    print('[RESUME] Starting')
    response = celery_app.control.add_consumer(
                            consumer_queue,
                            routing_key=consumer_queue,
                            destination=['celery@{}'.format(consumer)],
                            reply=True,
    )
    print(response)
    print('[RESUME] Finished')


def nap(n):
    print(f'[NAP] sleeping for {n} seconds')
    time.sleep(5)


if __name__ == '__main__':
    nap(5)
    pause()
    # time.sleep(5)
    # resume()
