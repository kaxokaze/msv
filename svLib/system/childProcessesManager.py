import svLib.system.psutilReplacer as psutilReplacer
try:
    import psutil
except:
    psutil = psutilReplacer
import os
import signal
import threading


_purge_lock = threading.Semaphore(1)
_purging_thread = None
_ignored_pids = []


def purge_children(is_recursive=True, purge_ignored=False, pid=None, separate_thread=True):
    if separate_thread:
        global _purging_thread
        if _purging_thread is not None:
            _purging_thread.join()

        _purging_thread = threading.Thread(target=_do_purging, args=(is_recursive, purge_ignored, pid, separate_thread))
        _purging_thread.start()
    else:
        _do_purging(is_recursive, purge_ignored, pid, separate_thread)


def ignorePid(pid):
    _ignored_pids.append(pid)


def unIgnorePid(pid):
    try:
        _ignored_pids.remove(pid)
    except:
        pass


def _do_purging(is_recursive, purge_ignored, pid, separate_thread):
    _purge_lock.acquire()

    current_process = psutil.Process(pid)
    children = current_process.children(recursive=is_recursive)
    for child in children:
        child_pid = child.pid
        try:
            is_ignored = False
            try:
                _ignored_pids.index(child_pid)
            except:
                pass
            else:
                is_ignored = True

            if purge_ignored or not is_ignored:
                os.kill(int(child_pid), signal.SIGTERM)
        except:
            pass

    if separate_thread:
        global _purging_thread
        _purging_thread = None

    _purge_lock.release()
