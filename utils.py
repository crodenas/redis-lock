"module"
from datetime import datetime, timezone

from redis import StrictRedis

CFG = {
    "RED_DB_HOST": "localhost",
    "RED_DB_PORT": 6379,
    "RED_DB": 0,
}


class Redis:
    "Class for Redis connection"

    def __init__(self, **kwargs):
        "function"
        self.host = kwargs.get("host", CFG["RED_DB_HOST"])
        self.port = kwargs.get("port", CFG["RED_DB_PORT"])
        self.database = kwargs.get("database", CFG["RED_DB"])
        self.conn = StrictRedis(
            host=self.host,
            port=self.port,
            db=self.database,
        )


class NamedLock:
    "Context manager for named user locks"

    class NamedLockException(Exception):
        "Custom exception for NamedLocks"

    def __init__(self, lock_name, **kwargs):
        "function"
        self.lock_name = lock_name
        self.timeout = kwargs.get("timeout", 30)
        self.redis = Redis(**kwargs)
        self.lock = None

    def __enter__(self):
        "function"
        try:
            self.lock = self.redis.conn.lock(self.lock_name)
            if self.lock.acquire(blocking=True, blocking_timeout=self.timeout):
                print(
                    f"NamedLock '{self.lock_name}' acquired at: "
                    f"{datetime.now(timezone.utc).isoformat()}"
                )
                return
            raise self.NamedLockException("Unable to acquire DB lock")
        except Exception as e:
            raise self.NamedLockException(f"Error acquiring lock: {e}")

    def __exit__(self, *_):
        "function"
        self.lock.release()
        print(
            f"NamedLock '{self.lock_name}' released at: "
            f"{datetime.now(timezone.utc).isoformat()}"
        )
