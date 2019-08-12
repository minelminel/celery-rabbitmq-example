import time

from .tasks import holding_tank


if __name__ == '__main__':
    raise NotImplementedError('Use this method for calling items directly, otherwise use the API.')
    # url = 'http://www.google.com'
    # result = holding_tank.delay(url)
    # # at this time, our task is not finished, so it will return False
    # print(f'[BEFORE] Task finished? {result.ready()}')
    # print(f'[BEFORE] Task result: {result.result}')
    # # sleep for 10 seconds to ensure that our task has been finished
    # time.sleep(5)
    # # now the task should be finished and ready method will return True
    # print(f'[AFTER] Task finished? {result.ready()}')
    # print(f'[AFTER] Task result: {result.result}')
