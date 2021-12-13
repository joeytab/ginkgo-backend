import os

from redislite import Redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']


conn = Redis('/tmp/redis.db')

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()