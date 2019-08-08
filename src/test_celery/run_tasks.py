from .tasks import longtime_add
import time

if __name__ == '__main__':
    num = 50
    for i in range(num):
        longtime_add.delay(1,2)
    print(f'[run_tasks.__main__]{num} tasks added to queue')
    # at this time, our task is not finished, so it will return False
    # print(f'[BEFORE] Task finished? {result.ready()}')
    # print(f'[BEFORE] Task result: {result.result}')
    # # sleep for 10 seconds to ensure that our task has been finished
    # time.sleep(10)
    # # now the task should be finished and ready method will return True
    # print(f'[AFTER] Task finished? {result.ready()}')
    # print(f'[AFTER] Task result: {result.result}')
