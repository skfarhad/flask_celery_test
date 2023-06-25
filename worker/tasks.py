import os
import time
from celery import Celery

RMQ_HOST = os.getenv('RMQ_HOST', 'localhost')
MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
CELERY_BROKER_URL = f'pyamqp://guest:guest@{RMQ_HOST}:5672//'
CELERY_RESULT_BACKEND = f'mongodb://{MONGODB_HOST}:27017/'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'async_jobs',
    'taskmeta_collection': 'my_taskmeta_collection',
}

print("Starting celery api........")

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
app.conf.update(
    mongodb_backend_settings=CELERY_MONGODB_BACKEND_SETTINGS
)

app.conf.update(worker_pool_restarts=True, task_acks_late=True, result_expires=1800)


@app.task(name='sum-of-two-numbers')
def execute_add_async(a, b):
    print('Preparing adder.....')
    time.sleep(5)
    print('Adder ready..')
    return a + b
