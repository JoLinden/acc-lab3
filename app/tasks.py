from celery import Celery

app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@rabbitmq:5672/')


@app.task
def add(x, y):
    return x + y
