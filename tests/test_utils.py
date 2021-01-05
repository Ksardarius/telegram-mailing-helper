import threading
from datetime import datetime
from datetime import timedelta


class CountDownLatch(object):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notifyAll()
        self.lock.release()

    def wait(self, timeout=None):
        self.lock.acquire(timeout=timeout)
        time = datetime.now()
        while self.count > 0:
            self.lock.wait(timeout=timeout)
            if timeout and datetime.now() - time > timedelta(seconds=timeout):
                break
        self.lock.release()
