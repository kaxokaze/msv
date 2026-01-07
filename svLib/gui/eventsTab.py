from tkinter import ttk, LabelFrame, Label, W, E, S, N, END
import svLib.gui.helpers as gui_helpers
from svLib import globalConstants


class EventsTab:
    def __init__(self, note_book):
        parent_frame = self.tab_events = ttk.Frame(note_book)
        note_book.add(self.tab_events, text=globalConstants.EVENTS_TAB_NAME)

        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        self.events_stat_lfr = LabelFrame(parent_frame, text=globalConstants.EVENTS_TAB_STATS)
        self.events_stat_lfr.grid(row=0, column=0, padx=3, pady=3, ipadx=3, sticky=W + E)

        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_VIS_STATUS).grid(row=0, column=0, padx=3)
        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_COMPL_VISITS).grid(row=1, column=0, padx=3)

        self.vis_status_lbl = Label(self.events_stat_lfr)
        self.vis_status_lbl.grid(row=0, column=1, padx=3)
        self.compl_vis_lbl = Label(self.events_stat_lfr)
        self.compl_vis_lbl.grid(row=1, column=1, padx=3)

        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_TIMEOUTS).grid(row=0, column=2, padx=3)
        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_W_THREADS).grid(row=1, column=2, padx=3)

        self.timed_out_lbl = Label(self.events_stat_lfr)
        self.timed_out_lbl.grid(row=0, column=3, padx=3)
        self.act_thrds_stst_lbl = Label(self.events_stat_lfr)
        self.act_thrds_stst_lbl.grid(row=1, column=3, padx=3)

        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_SCH_VISITS).grid(row=0, column=4, padx=3)
        self.sch_vis_lbl = Label(self.events_stat_lfr)
        self.sch_vis_lbl.grid(row=0, column=5, padx=3)
        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_ERRS).grid(row=1, column=4, padx=3)
        self.error_cnt_lbl = Label(self.events_stat_lfr)
        self.error_cnt_lbl.grid(row=1, column=5, padx=3)

        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_SUCC_VISITS).grid(row=0, column=6, padx=3)
        self.succ_vis_lbl = Label(self.events_stat_lfr)
        self.succ_vis_lbl.grid(row=0, column=7, padx=3)

        Label(self.events_stat_lfr, text=globalConstants.EVENTS_TAB_ALL_THREADS).grid(row=1, column=6, padx=3)
        self.all_threads_lbl = Label(self.events_stat_lfr)
        self.all_threads_lbl.grid(row=1, column=7, padx=3)

        # Event log zone
        self.events_log_lfr = LabelFrame(parent_frame, text=globalConstants.EVENTS_TAB_LOG)
        self.events_log_lfr.grid(row=1, column=0, padx=3, pady=3, ipadx=3, sticky=W + E + S + N)
        self.events_log_lfr.grid_rowconfigure(0, weight=1)
        self.events_log_lfr.grid_columnconfigure(0, weight=1)

        self.event_listbox, lb_frame = gui_helpers.makeScrollableListBox(self.events_log_lfr, 0)
        lb_frame.grid_rowconfigure(0, weight=1)
        lb_frame.grid_columnconfigure(0, weight=1)
        lb_frame.grid(sticky=W + E + S + N)
        self.event_listbox.grid(sticky=W + E + S + N)

    ###
    # API
    ###

    def insertInEventListbox(self, string, item_color=None):
        self.event_listbox.insert(END, string)
        if item_color is not None:
            self.event_listbox.itemconfig(END, foreground=item_color, selectbackground=item_color)

    def clearEventListbox(self):
        self.event_listbox.delete(0, END)

    def getEventsListboxContents(self):
        return self.event_listbox.get(0, self.event_listbox.size())

    ###
    # VieModel bindings
    ###

    def bind_vis_status_lbl(self, var):
        self.vis_status_lbl.config(textvariable=var)

    def bind_compl_vis_lbl(self, var):
        self.compl_vis_lbl.config(textvariable=var)

    def bind_succ_vis_lbl(self, var):
        self.succ_vis_lbl.config(textvariable=var)

    def bind_all_threads_lbl(self, var):
        self.all_threads_lbl.config(textvariable=var)

    def bind_sch_vis_lbl(self, var):
        self.sch_vis_lbl.config(textvariable=var)

    def bind_timed_out_lbl(self, var):
        self.timed_out_lbl.config(textvariable=var)

    def bind_act_thrds_stst_lbl(self, var):
        self.act_thrds_stst_lbl.config(textvariable=var)

    def bind_error_cnt_lbl(self, var):
        self.error_cnt_lbl.config(textvariable=var)
