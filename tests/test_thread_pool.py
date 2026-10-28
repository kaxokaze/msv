"""Unit tests for the small generic thread-pool helper.

These tests use local no-op tasks only and never open browsers or send network traffic.
"""
import threading
import unittest

from svLib.utils.threadPool import ThreadPool


class ThreadPoolTests(unittest.TestCase):
    def test_task_runs(self):
        done = threading.Event()
        pool = ThreadPool(1)
        try:
            self.assertTrue(pool.queueTask(lambda: done.set()))
            self.assertTrue(done.wait(timeout=2), "queued task did not execute")
        finally:
            pool.joinAll(waitForTasks=True, waitForThreads=True)

    def test_invalid_task_rejected(self):
        pool = ThreadPool(1)
        try:
            self.assertFalse(pool.queueTask("not callable"))
        finally:
            pool.joinAll(waitForTasks=True, waitForThreads=True)


if __name__ == "__main__":
    unittest.main()
