import tkinter


class EventsTabViewModel:
    def __init__(self, events_tab):
        self.events_tab = events_tab
        
        # Event log tab (main window)
        self.vis_status = tkinter.StringVar()
        self.vis_status.set('None')
        self.act_threads = tkinter.StringVar()
        self.act_threads.set('0')
        self.events_tab.bind_vis_status_lbl(self.vis_status)
        self.complete_visits = tkinter.StringVar()
        self.complete_visits.set('0')
        self.events_tab.bind_compl_vis_lbl(self.complete_visits)
        self.success_visits = tkinter.StringVar()
        self.success_visits.set('0')
        self.events_tab.bind_succ_vis_lbl(self.success_visits)
        self.sch_vis = tkinter.StringVar()
        self.sch_vis.set('0')
        self.events_tab.bind_sch_vis_lbl(self.sch_vis)
        self.timed_out_cnt = tkinter.StringVar()
        self.timed_out_cnt.set('0')
        self.events_tab.bind_timed_out_lbl(self.timed_out_cnt)
        self.events_tab.bind_act_thrds_stst_lbl(self.act_threads)
        self.error_cnt = tkinter.StringVar()
        self.error_cnt.set('0')
        self.events_tab.bind_error_cnt_lbl(self.error_cnt)
        self.all_thread_count = tkinter.StringVar()
        self.all_thread_count.set('0')
        self.events_tab.bind_all_threads_lbl(self.all_thread_count)

    ###
    # API
    ###
    
    def setThreadsActive(self, value):
        self.act_threads.set(str(value))

    def set_complete_visits(self, val):
        self.complete_visits.set(str(val))

    def set_success_visits(self, val):
        self.success_visits.set(str(val))

    def set_sch_vis(self, val):
        self.sch_vis.set(str(val))

    def set_timed_out_cnt(self, val):
        self.timed_out_cnt.set(str(val))

    def set_error_cnt(self, val):
        self.error_cnt.set(str(val))

    def set_all_thread_count(self, val):
        self.all_thread_count.set(str(val))

    def set_vis_status(self, val):
        self.vis_status.set(val)

    def logEvent(self, event_str):
        self.events_tab.insertInEventListbox(event_str)

    def logError(self, error_str):
        self.events_tab.insertInEventListbox(error_str, item_color='#B80934')

    def clrEvents(self):
        self.events_tab.clearEventListbox()

    def save_log_to_file(self, c_file):
        events = self.events_tab.getEventsListboxContents()
        for i in range(len(events)):
            c_file.write(events[i] + '\n')
