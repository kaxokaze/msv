import threading
import datetime

from svLib.viewModel.eventsTabViewModel import EventsTabViewModel

lgr_log_queue_sem = threading.Semaphore(1)
lgr_log_queue = []

MSG_TYPE_EVENT = 1
MSG_TYPE_ERROR = 2


def step(events_viewmodel: EventsTabViewModel):
    if len(lgr_log_queue) > 0:
        lgr_log_queue_sem.acquire()

        message = lgr_log_queue.pop(0)
        if message[0] == MSG_TYPE_EVENT:
            events_viewmodel.logEvent(message[1])
        elif message[0] == MSG_TYPE_ERROR:
            events_viewmodel.logError(message[1])

        lgr_log_queue_sem.release()


def log_event(*args):
    _do_log(MSG_TYPE_EVENT, args)


def log_error(*args):
    _do_log(MSG_TYPE_ERROR, args)


def _do_log(e_type, *args):
    lgr_log_queue_sem.acquire()

    timestamp = str(datetime.datetime.now().replace(microsecond=0).time())
    thread_name = threading.current_thread().name

    message_text = "[" + timestamp + " " + thread_name + "] " + " ".join(map(str, args))

    lgr_log_queue.append((e_type, message_text))

    lgr_log_queue_sem.release()
