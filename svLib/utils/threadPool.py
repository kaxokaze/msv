import threading
import time

"""Flexible thread pool class.  Creates a pool of threads, then
accepts tasks that will be dispatched to the next available
thread."""


class ThreadPool:
    """Initialize the thread pool with numThreads workers."""

    def __init__(self, numThreads):
        self.__threads = []
        self.__resizeLock = threading.Condition(threading.Lock())
        self.__taskLock = threading.Condition(threading.Lock())
        self.__tasks = []
        self.__isJoining = False
        self.setThreadCount(numThreads)

    """ External method to set the current pool size.  Acquires
    the resizing lock, then calls the internal version to do real
    work."""

    def setThreadCount(self, newNumThreads):
        # Can't change the thread count if we're shutting down the pool!
        if self.__isJoining:
            return False

        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(newNumThreads)
        finally:
            self.__resizeLock.release()
        return True

    """Set the current pool size, spawning or terminating threads
    if necessary.  Internal use only; assumes the resizing lock is
    held."""

    def __setThreadCountNolock(self, newNumThreads):
        # If we need to grow the pool, do so
        while newNumThreads > len(self.__threads):
            newThread = ThreadPoolThread(self)
            self.__threads.append(newThread)
            newThread.start()
        # If we need to shrink the pool, do so
        while newNumThreads < len(self.__threads):
            self.__threads[0].goAway()
            del self.__threads[0]

    """Return the number of threads in the pool."""

    def getThreadCount(self):
        self.__resizeLock.acquire()
        try:
            return len(self.__threads)
        finally:
            self.__resizeLock.release()

    """Insert a task into the queue.  task must be callable;
        args and taskCallback can be None."""

    def queueTask(self, task, args=None, taskCallback=None):
        if self.__isJoining == True:
            return False
        if not callable(task):
            return False

        self.__taskLock.acquire()
        try:
            self.__tasks.append((task, args, taskCallback))
            return True
        finally:
            self.__taskLock.release()

    """ Retrieve the next task from the task queue.  For use
    only by ThreadPoolThread objects contained in the pool."""

    def getNextTask(self):
        self.__taskLock.acquire()
        try:
            if self.__tasks == []:
                return (None, None, None)
            else:
                return self.__tasks.pop(0)
        finally:
            self.__taskLock.release()

    """ Clear the task queue and terminate all pooled threads,
    optionally allowing the tasks and threads to finish."""

    def joinAll(self, waitForTasks=True, waitForThreads=True):
        # Mark the pool as joining to prevent any more task queueing
        self.__isJoining = True

        # Wait for tasks to finish
        if waitForTasks:
            while self.__tasks != []:
                time.sleep(.1)

        # Tell all the threads to quit
        self.__resizeLock.acquire()
        try:
            # Wait until all threads have exited
            if waitForThreads:
                for t in self.__threads:
                    t.goAway()
                    t.join()
                    del t

            self.__setThreadCountNolock(0)

            # Reset the pool for potential reuse
            self.__isJoining = False
        finally:
            self.__resizeLock.release()


""" Pooled thread class. """


class ThreadPoolThread(threading.Thread):
    threadSleepTime = 0.1

    """ Initialize the thread and remember the pool. """

    def __init__(self, pool):

        threading.Thread.__init__(self)
        self.__pool = pool
        self.__isDying = False

    """ Until told to quit, retrieve the next task and execute
    it, calling the callback if any.  """

    def run(self):

        while not self.__isDying:
            cmd, args, callback = self.__pool.getNextTask()

            try:
                # If there's nothing to do, just sleep a bit
                if cmd is None:
                    time.sleep(ThreadPoolThread.threadSleepTime)
                elif callback is None:
                    cmd(args) if args is not None else cmd()
                else:
                    callback(cmd(args)) if args is not None else callback(cmd())
            except Exception as e:
                pass  # couldn't care lees why the task has crashed

    """ Exit the run loop next time through."""

    def goAway(self):
        self.__isDying = True
