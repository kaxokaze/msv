import random
import threading
import time

from svLib.agent.visitWorker import VisitWorker
from svLib.log import svLogger
from svLib.utils import threadPool


##########################################
# Scheduler creates a separate thread, that manages creation and running of the worker threads that perform the
# visiting of web-sites
##########################################
class AgentScheduler:
    def __init__(self, agent_settings, websites, n_visits, referrers, user_agents, proxies, max_threads, browser):
        self.agent_settings = agent_settings

        self.thread = None

        # semaphores
        self.sv_worker_kill_call = threading.Semaphore(1)  # locks the flag of whether the kill all workers command was executed
        self.sv_f_count_sem = threading.Semaphore(1)  # counts failures from worker threads
        self.sv_s_count_sem = threading.Semaphore(1)  # counts successes from worker threads
        self.sv_to_count_sem = threading.Semaphore(1)  # counts timeouts from worker threads
        self.sv_thread_list_sem = threading.Semaphore(1)  # when thread list is modified

        self.sv_stat_log_sem = threading.Semaphore(1)  # when proxy resp gets logged

        self.max_act_threads = max_threads
        self.act_workers = []

        self.visits_pending = 0
        self.visits_made = 0
        self.visits_complete = 0

        self.error_count = 0
        self.success_count = 0
        self.timeout_count = 0

        self.websites = websites
        self.n_visits = n_visits
        self.referrers = list(referrers) if referrers is not None else None
        self.user_agents = list(user_agents) if user_agents is not None else None
        self.proxies = list(proxies) if proxies is not None else None
        self.max_threads = max_threads
        self.browser = browser

        self.n_loaded_proxies = len(proxies) if proxies is not None else 0

        self.test_mode = False

        self.workers_killed = False  # whether a call to kill the workers has been made already
        self.alive = True  # main working method (scheduleNVisitors) will check this flag from time to time,
                           # and stop making new threads and call the kill_workers if False

        self.thread_pool = threadPool.ThreadPool(self.max_threads)

    def startVisits(self):
        self.thread = threading.Thread(target=self.scheduleNVisitors)
        self.thread.start()

    def startTests(self):
        self.test_mode = True
        self.thread = threading.Thread(target=self.scheduleProxyTests)
        self.thread.start()

    def __del__(self):
        self.alive = False
        self.kill_workers()

    def countError(self):
        self.sv_f_count_sem.acquire()
        self.error_count += 1
        self.sv_f_count_sem.release()

    def countSuccess(self):
        self.sv_s_count_sem.acquire()
        self.success_count += 1
        self.sv_s_count_sem.release()

    def countTimeout(self):
        self.sv_to_count_sem.acquire()
        self.timeout_count += 1
        self.sv_to_count_sem.release()

    def getErrCnt(self):
        return self.error_count

    def getSuccessCnt(self):
        return self.success_count

    def getTimeoutCnt(self):
        return self.timeout_count

    def kill(self):
        self.alive = False

    # rudely interrupts all the workers, workers_killed is used to ensure, that the method is called only once
    def kill_workers(self):
        self.sv_worker_kill_call.acquire()

        if not self.workers_killed:
            self.workers_killed = True

            # an embarrassing hack - so that we won't have to wait for the first thread termination
            # before the gui gets a 'signal' about the fact that we're stopping now
            if self.agent_settings.sv_th_stop_callback is not None:
                self.agent_settings.sv_th_stop_callback()

            # kill the workers - send close, quit commands
            for worker in self.act_workers:
                worker.kill()
            for worker in self.act_workers:
                worker.purge()

            # this joins all the threads in the pool, waiting for all the python threads to stop
            self.thread_pool.joinAll(False)

            # final touch - any visitor workers that haven't reported to the scheduler yet about their termination
            # will (be forced to) do it here
            while len(self.act_workers) > 0:
                worker = self.act_workers[len(self.act_workers) - 1]
                worker.join()

        self.sv_worker_kill_call.release()

    # doesn't wait for the workers to finish, doesn't join threads or clears the worker list
    # simply sends kill process signal to all driver instances, and tells them to stop 'living'
    def purge_workers(self):
        self.sv_worker_kill_call.acquire()

        if not self.workers_killed:
            for worker in self.act_workers:
                worker.purge()

        self.thread_pool.joinAll(False)

        self.sv_worker_kill_call.release()

    def scheduleProxyTests(self):
        web_url = self.websites[0]

        while self.alive and len(self.proxies) > 0:
            if len(self.act_workers) < self.max_act_threads and self.alive:
                to_check_proxy = self.proxies.pop(0)
                worker = VisitWorker(self.agent_settings, self, web_url, None, None, to_check_proxy)
                worker.start_test()
            elif not self.alive:
                self.kill_workers()

            time.sleep(0.75)

        # wait for everything to get done, or rudely interrupt all remaining after creation threads on '''signal'''
        # (just a bool set, actually) so check that bool periodically with intervals
        while len(self.act_workers) > 0:
            if not self.alive:
                self.kill_workers()
            else:
                time.sleep(2.0)  # sleep is used to be friendly with other processes and context switching

        # final cleanup after all is said and done
        try:
            self.thread_pool.joinAll(False)
        except:
            pass

    def scheduleNVisitors(self):
        self.visits_made = 0
        self.visits_complete = 0
        self.visits_pending = self.n_visits

        # create new threads, until we haven't hit the mark
        while (((not self.agent_settings.sva_count_success_only) and self.visits_made < self.visits_pending) or
               (self.agent_settings.sva_count_success_only and self.success_count < self.visits_pending)) and self.alive:

            # create threads, but make sure, that we don't have too many running at the same time
            # actually, we can rely on thread pool for this now, but w/e
            if len(self.act_workers) < self.max_act_threads and self.alive:

                web_url = self.websites[random.randint(0, len(self.websites) - 1)]

                referrer = self.choose_ref(self.referrers)

                user_agent = self.choose_ua(self.user_agents)

                proxy = self.choose_proxy(self.proxies)

                svLogger.log_event('\n\t***Visiting', web_url, str(self.visits_made + 1), "out of",
                                   self.visits_pending, 'times', "ref: '%s'" % referrer, 'ua: "%s"' % user_agent,
                                   'proxy: "%s"' % proxy, '\n')

                worker = VisitWorker(self.agent_settings, self, web_url, referrer, user_agent, proxy, self.browser)
                worker.start()

                self.visits_made += 1
            elif not self.alive:
                self.kill_workers()

            # sleep is used to be friendly with other processes and context switching, because this loop can run and
            # wait for quite a while (like hours)
            # and we don't want our cpu be fully occupied with just this one script
            time.sleep(0.75)

        # wait for everything to get done, or rudely interrupt all remaining after creation threads on '''signal'''
        # (just a bool set, actually)
        # so check that bool periodically with intervals
        while len(self.act_workers) > 0:
            if not self.alive:
                self.kill_workers()
            else:
                time.sleep(2.0)  # sleep is used to be friendly with other processes and context switching

        # final cleanup after all is said and done
        try:
            self.thread_pool.joinAll(False)
        except:
            pass

        print(self.agent_settings.sv_proxy_responses)

    def choose_ref(self, referrers):
        if not referrers:
            return None
        return referrers[random.randint(0, len(referrers) - 1)]

    def choose_ua(self, user_agents):
        if not user_agents:
            return None
        return user_agents[random.randint(0, len(user_agents) - 1)]

    def choose_proxy(self, proxies):
        if not proxies:
            return None
        proxy = None
        n_proxies = len(proxies)

        if n_proxies > 0:
            p_index = random.randint(0, n_proxies - 1)

            def_choice = False
            p_search_attempts = 0

            while (not def_choice) and (p_search_attempts < n_proxies):
                proxy = proxies[p_index]

                # check the stats to see the fail rate
                failures = 0
                successes = 0
                if proxy in self.agent_settings.sv_proxy_responses:
                    for result in self.agent_settings.sv_proxy_responses[proxy]:
                        if result > self.agent_settings.sva_success_page_min_size:
                            successes += 1
                            break  # might as well break here, 1 success is proof enough
                        else:
                            failures += 1

                # use this proxy or search linearly for a good one
                if successes < 1 and failures > self.agent_settings.sva_max_proxy_fails:
                    p_index = (p_index + 1) % n_proxies
                    p_search_attempts += 1
                else:
                    def_choice = True

        return proxy

    def n_workers(self):
        return len(self.act_workers)

    def add_worker(self, worker: VisitWorker):
        self.sv_thread_list_sem.acquire()

        self.act_workers.append(worker)

        # print 'worker added', len(self.act_workers), worker, self, self.alive

        if self.agent_settings.sv_th_start_callback is not None:
            self.agent_settings.sv_th_start_callback()

        self.sv_thread_list_sem.release()

    def clear_worker(self, worker: VisitWorker):
        # Always release the list lock, including when logging or callbacks fail.
        self.sv_thread_list_sem.acquire()
        try:
            if self.alive:
                self.visits_complete += 1

            try:
                worker_ind = self.act_workers.index(worker)
                self.act_workers.pop(worker_ind)
            except ValueError:
                # Repeated cleanup can happen during stop/purge races.
                return

            worker_thread = worker.get_thread()
            thread_name = worker_thread.name if worker_thread is not None else "unknown"
            svLogger.log_event("Worker", worker_ind, "(thread %s)" % thread_name, "is done.")

            if self.agent_settings.sv_th_stop_callback is not None:
                self.agent_settings.sv_th_stop_callback()
        except Exception:
            svLogger.log_error("Error while clearing a visitor worker")
        finally:
            self.sv_thread_list_sem.release()

    def get_sv_stat_log_sem(self):
        return self.sv_stat_log_sem

    def get_n_loaded_proxies(self):
        return self.n_loaded_proxies

    def get_is_test_mode(self):
        return self.test_mode

    def get_is_alive(self):
        return self.alive
