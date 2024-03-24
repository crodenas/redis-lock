import unittest
from unittest.mock import MagicMock

from utils import NamedLock


class TestNamedLock(unittest.TestCase):
    def test_lock_acquired(self):
        # Mock Redis connection and lock
        redis_mock = MagicMock()
        lock_mock = MagicMock()
        redis_mock.conn.lock.return_value = lock_mock

        # Create NamedLock instance
        lock = NamedLock("lock1", blocking_timeout=5)
        lock.redis = redis_mock

        # Acquire lock
        with lock:
            # Assert that lock was acquired
            lock_mock.acquire.assert_called_once_with(blocking=True, blocking_timeout=5)

    def test_lock_not_acquired(self):
        # Mock Redis connection and lock
        redis_mock = MagicMock()
        lock_mock = MagicMock()
        lock_mock.acquire.return_value = False
        redis_mock.conn.lock.return_value = lock_mock

        # Create NamedLock instance
        lock = NamedLock("lock1", blocking_timeout=5)
        lock.redis = redis_mock

        # Try to acquire lock
        with self.assertRaises(lock.NamedLockException):
            with lock:
                pass

    def test_lock_released(self):
        # Mock Redis connection and lock
        redis_mock = MagicMock()
        lock_mock = MagicMock()
        redis_mock.conn.lock.return_value = lock_mock

        # Create NamedLock instance
        lock = NamedLock("lock1", blocking_timeout=5)
        lock.redis = redis_mock

        # Acquire and release lock
        with lock:
            pass

        # Assert that lock was released
        lock_mock.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()
