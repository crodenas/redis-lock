"module"
from datetime import datetime, timezone
from typing import Any, Optional

from redis import StrictRedis

CFG = {
    "RED_DB_HOST": "localhost",
    "RED_DB_PORT": 6379,
    "RED_DB": 0,
}


class Redis:
    "Class for Redis connection"

    def __init__(
        self,
        host: str = CFG["RED_DB_HOST"],
        port: int = CFG["RED_DB_PORT"],
        database: int = CFG["RED_DB"],
    ) -> None:
        "function"
        self.host = host
        self.port = port
        self.database = database
        self.conn = StrictRedis(
            host=self.host,
            port=self.port,
            db=self.database,
        )


class NamedLock:
    "Context manager for named user locks"

    class NamedLockException(Exception):
        "Custom exception for NamedLocks"

    def __init__(
        self,
        lock_name: str,
        blocking: bool = True,
        blocking_timeout: int = 30,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        "function"
        self.lock_name = lock_name
        self.blocking = blocking
        self.blocking_timeout = blocking_timeout
        self.timeout = timeout
        self.redis = Redis(**kwargs)
        self.lock = None

    def __enter__(self):
        "function"
        try:
            self.lock = self.redis.conn.lock(self.lock_name)
            if self.lock.acquire(
                blocking=self.blocking,
                blocking_timeout=self.blocking_timeout,
            ):
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
