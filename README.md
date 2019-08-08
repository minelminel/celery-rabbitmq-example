# Python Celery RabbitMQ Tutorial - Notes
[Source](https://tests4geeks.com/python-celery-rabbitmq-tutorial/)  
[Breaking Into Modules *](https://medium.com/@frassetto.stefano/flask-celery-howto-d106958a15fe)

Note: for some reason, RabbitMQ does not work within a virtualenv (tackle this at some later point..)

# Starting/Stopping RabbitMQ on Mac

```bash
export PATH=/usr/local/sbin:$PATH

brew services start rabbitmq
brew services stop rabbitmq
```


# Configure RabbitMQ for Celery

These commands must be run __after__ starting RabbitMQ service.
```bash
# add user michael with password 'michael123'
rabbitmqctl add_user michael michael123
# add virtual host 'michael_vhost'
rabbitmqctl add_vhost michael_vhost
# add user tag 'michael_tag' for user 'michael'
rabbitmqctl set_user_tags michael michael_tag
# set permission for user 'michael' on virtual host 'michael_vhost'
rabbitmqctl set_permissions -p michael_vhost michael ".*" ".*" ".*"
```
For the last command, the 3 kinds of operations in RabbitMQ are `configure`, `write`, and `read`. Here we have given our user permission to perform all 3.

---
# <span>celery.py</span>
```python
from __future__ import absolute_import
from celery import Celery

app = Celery(
            # Name of the project package.
            'test_celery',
            # 'broker' arg specifies the broker URL, which should be our RabbitMQ instance.
            # The format is as follows.
            # transport://userid:password@hostname:port/virtual_host
            broker='amqp://michael:michael123@localhost/michael_vhost',
            # 'backend' arg specifies the backend URL.
            # It is used for storing task results.
            # rpc is an acceptable format for this demo.
            backend='rpc://',
            # 'include' arg specifies a list of modules that you want to import when Celery worker starts.
            # Add tasks module here of the worker can find our task.
            include=['test_celery.tasks'],
)
```
---
# <span>tasks.py</span>
```python
from __future__ import absolute_import
from test_celery.celery import app
import time


@app.task
def longtime_add(x,y):
  print('long time task begins')
  # do something
  time.sleep(5)
  print('long time task finished')
  return x + y
```
Here we import the `app` defined in the previous `celery` module and use it as a decorator for our task method.

---
# <span>run_tasks.py</span>
```python
from .tasks import longtime_add
import time

if __name__ == '__main__':
  result = longtime_add.delay(1,2)
  # at this time, our task is not finished, so it will return False
  print(f'[BEFORE] Task finished? {result.ready()}')
  print(f'[BEFORE] Task result: {result.result}')
  # sleep for 10 seconds to ensure that our task has been finished
  time.sleep(10)
  # now the task should be finished and ready method will return True
  print(f'[AFTER] Task finished? {result.ready()}')
  print(f'[AFTER] Task result: {result.result}')
```
Here, we call the task `longtime_add` using the `delay` method, which is needed if we want to process the task asynchronously. In addition, we keep the results of the task and print some information. The `ready` method will return True if the task has been finished, otherwise False. The `result` attribute is the result of the task. If the task has not been finished, it returns None.

---
# Start Celery Worker
Note: this function must be run inside the parent dir of our project dir `test_celery`

```bash
celery -A test_celery worker --loglevel=info
```

In another console, run the following command.
```bash
python3 -m test_celery.run_tasks
```

Check the previous Celery console window to ensure that our workers received our task. Logs are displayed with the following format.
```
Received task: test_celery.tasks.longtime_add[taskid]
```

# Monitor Celery in Real Time

Flower is a real-time web-based monitor for Celery.
```bash
pip install flower
```

To start a Flower web console, run the following command inside the project parent directory.
```bash
celery -A test_celery flower
```

# Use Case - Scraper

### Workflow

- process is initially disabled
- enabled is set to True, event triggered
- on event, add element to 'all_urls'
- on event, add element from 'all_urls' to 'released_urls'
- released_urls() is called async
- response is received
  - response is moved to 'parse_urls'
    - response is parsed for info
    - resulting content is saved to database
-
