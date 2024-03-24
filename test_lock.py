"module"
import time

from utils import NamedLock

with NamedLock("lock1", blocking_timeout=5):
    print("Got the lock. Doing some work ...")
    for i in range(20):
        time.sleep(1)
        print(f"Working ... {i}")
