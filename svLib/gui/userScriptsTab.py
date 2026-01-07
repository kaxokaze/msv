import sys
from tkinter import ttk, Canvas, LabelFrame, Scrollbar, N, S, W, E, Checkbutton, Frame, Label, Entry, LEFT, Spinbox

from svLib import globalConstants
from svLib.gui.components.toolTip import ListboxToolTip
from svLib.gui.settingsSaveUi import SettingsSaveUi
from svLib.utils import guiMouseEvents


class UserScriptsTab(SettingsSaveUi):
    def __init__(self, note_book):
        self.tab_user_scripts = ttk.Frame(note_book)
        note_book.add(self.tab_user_scripts, text=globalConstants.USCRIPTS_TAB_NAME)

        self.tab_user_scripts.grid_columnconfigure(0, weight=1)
        self.tab_user_scripts.grid_rowconfigure(0, weight=0)
        self.tab_user_scripts.grid_rowconfigure(2, weight=1000000)

        # auto behavior section
        self.auto_behavior_canvas = Canvas(self.tab_user_scripts, bd=0, highlightthickness=0, relief='ridge')
        self.auto_behavior_canvas.grid(row=0, column=0, sticky=N + S + W + E)
        self.auto_behavior_canvas.grid_columnconfigure(0, weight=1)
        self.auto_behavior_canvas.grid_rowconfigure(0, weight=1)
        self.auto_behavior_section = LabelFrame(self.auto_behavior_canvas, text=globalConstants.USCRIPTS_AUTO_BEHAVIOR)
        self.auto_behavior_section.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)
        self.auto_behavior_section.grid_columnconfigure(0, weight=1)
        self.auto_behavior_section.grid_columnconfigure(1, weight=10)
        self.auto_behavior_section.grid_rowconfigure(0, weight=1)

        self.auto_click_canvas = Canvas(self.auto_behavior_section, bd=0, highlightthickness=0, relief='ridge')
        self.auto_click_canvas.grid(row=0, column=0, sticky=N + S + W + E)
        self.auto_click_canvas.grid_columnconfigure(0, weight=1)
        self.auto_click_canvas.grid_rowconfigure(0, weight=1)
        self.auto_click_section = LabelFrame(self.auto_click_canvas, text=globalConstants.USCRIPTS_RANDOM_CLICK)
        self.auto_click_section.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4)
        self.auto_click_section.grid_columnconfigure(0, weight=1)

        self.enable_random_clicks = Checkbutton(self.auto_click_section, text=globalConstants.USCRIPTS_ENABLE_CLICKS)
        self.enable_random_clicks.grid(row=0, column=0, sticky=W + N)
        self.random_click_types_frame = ttk.Frame(self.auto_click_section)
        self.random_click_types_frame.grid(row=1, column=0, sticky=W + N, pady=4, ipady=4)
        Label(self.random_click_types_frame, justify=LEFT, text=globalConstants.USCRIPTS_CLICK_LINKS_LABEL) \
            .grid(row=0, column=0, sticky=W + N)
        self.random_click_types = ttk.Combobox(self.random_click_types_frame, state='readonly', width=42)
        self.random_click_types.grid(row=0, column=1, sticky=W + N)
        self.random_click_number_frame = ttk.Frame(self.auto_click_section)
        self.random_click_number_frame.grid(row=2, column=0, sticky=W + N)
        Label(self.random_click_number_frame, justify=LEFT, text=globalConstants.USCRIPTS_NUM_CLICKS) \
            .grid(row=0, column=0, sticky=W + N)
        self.random_click_amount = Spinbox(self.random_click_number_frame, from_=0, to=sys.maxsize, width=9)
        self.random_click_amount.grid(row=0, column=1, sticky=W + N)
        ListboxToolTip(self.random_click_number_frame, [globalConstants.USCRIPTS_CLICK_TIME_TIP_1,
                                                        globalConstants.USCRIPTS_CLICK_TIME_TIP_2,
                                                        globalConstants.USCRIPTS_CLICK_TIME_TIP_3,
                                                        globalConstants.USCRIPTS_CLICK_TIME_TIP_4], 80, 4)

        self.auto_scroll_canvas = Canvas(self.auto_behavior_section, bd=0, highlightthickness=0, relief='ridge')
        self.auto_scroll_canvas.grid(row=0, column=1, sticky=N + S + W + E)
        self.auto_scroll_canvas.grid_columnconfigure(0, weight=1)
        self.auto_scroll_canvas.grid_rowconfigure(0, weight=1)
        self.auto_scroll_section = LabelFrame(self.auto_scroll_canvas, text=globalConstants.USCRIPTS_RANDOM_SCROLL)
        self.auto_scroll_section.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4)

        self.enable_random_scroll = Checkbutton(self.auto_scroll_section, text=globalConstants.USCRIPTS_ENABLE_SCROLL)
        self.enable_random_scroll.grid(row=0, column=0, sticky=W + N)

        self.random_scroll_number_frame = ttk.Frame(self.auto_scroll_section)
        self.random_scroll_number_frame.grid(row=1, column=0, sticky=W + N)
        ListboxToolTip(self.random_scroll_number_frame, [globalConstants.USCRIPTS_PERCENT_SCROLL_HINT_1,
                                                         globalConstants.USCRIPTS_PERCENT_SCROLL_HINT_2,
                                                         globalConstants.USCRIPTS_PERCENT_SCROLL_HINT_3,
                                                         globalConstants.USCRIPTS_PERCENT_SCROLL_HINT_4], 43, 4)
        Label(self.random_scroll_number_frame, justify=LEFT, text=globalConstants.USCRIPTS_SCROLL) \
            .grid(row=0, column=0, sticky=W + N)
        self.random_scroll_page_percent = Spinbox(self.random_scroll_number_frame, from_=0, to=100, width=8)
        self.random_scroll_page_percent.grid(row=0, column=1, sticky=W + N)
        Label(self.random_scroll_number_frame, justify=LEFT, text=globalConstants.USCRIPTS_PERCENT_OF_PAGE) \
            .grid(row=0, column=2, sticky=W + N)

        self.random_after_seconds_frame = ttk.Frame(self.auto_scroll_section)
        self.random_after_seconds_frame.grid(row=2, column=0, sticky=W + N)
        ListboxToolTip(self.random_after_seconds_frame, [globalConstants.USCRIPTS_AFTER_SCROLL_HINT_1,
                                                         globalConstants.USCRIPTS_AFTER_SCROLL_HINT_2,
                                                         globalConstants.USCRIPTS_AFTER_SCROLL_HINT_3,
                                                         globalConstants.USCRIPTS_AFTER_SCROLL_HINT_4], 43, 4)
        Label(self.random_after_seconds_frame, justify=LEFT, text=globalConstants.USCRIPTS_SCROLL_AFTER) \
            .grid(row=0, column=0, sticky=W + N)
        self.random_scroll_page_after_min = Spinbox(self.random_after_seconds_frame, from_=0, to=sys.maxsize, width=9)
        self.random_scroll_page_after_min.grid(row=0, column=1, sticky=W + N)
        Label(self.random_after_seconds_frame, justify=LEFT, text="-") \
            .grid(row=0, column=2, sticky=W + N)
        self.random_scroll_page_after_max = Spinbox(self.random_after_seconds_frame, from_=0, to=sys.maxsize, width=9)
        self.random_scroll_page_after_max.grid(row=0, column=3, sticky=W + N)
        Label(self.random_after_seconds_frame, justify=LEFT, text=globalConstants.USCRIPTS_SCROLL_SECONDS_1) \
            .grid(row=0, column=4, sticky=W + N)

        self.random_over_seconds_frame = ttk.Frame(self.auto_scroll_section)
        self.random_over_seconds_frame.grid(row=3, column=0, sticky=W + N)
        ListboxToolTip(self.random_over_seconds_frame, [globalConstants.USCRIPTS_OVER_SCROLL_HINT_1,
                                                        globalConstants.USCRIPTS_OVER_SCROLL_HINT_2,
                                                        globalConstants.USCRIPTS_OVER_SCROLL_HINT_3], 43, 3)
        Label(self.random_over_seconds_frame, justify=LEFT, text=globalConstants.USCRIPTS_SCROLL_OVER) \
            .grid(row=0, column=0, sticky=W + N)
        self.random_scroll_page_over_min = Spinbox(self.random_over_seconds_frame, from_=0, to=sys.maxsize, width=9)
        self.random_scroll_page_over_min.grid(row=0, column=1, sticky=W + N)
        Label(self.random_over_seconds_frame, justify=LEFT, text="-") \
            .grid(row=0, column=2, sticky=W + N)
        self.random_scroll_page_over_max = Spinbox(self.random_over_seconds_frame, from_=0, to=sys.maxsize, width=9)
        self.random_scroll_page_over_max.grid(row=0, column=3, sticky=W + N)
        Label(self.random_over_seconds_frame, justify=LEFT, text=globalConstants.USCRIPTS_SCROLL_SECONDS_2) \
            .grid(row=0, column=4, sticky=W + N)

        # new script btn section
        self.new_script_frame = ttk.Frame(self.tab_user_scripts)
        self.new_script_frame.grid(row=1, column=0, sticky=W, padx=4)
        self.new_user_script_btn = ttk.Button(self.new_script_frame, text=globalConstants.USCRIPTS_NEW_SCRIPT)
        self.new_user_script_btn.grid(row=0, column=0, sticky=W, padx=4, pady=2, ipady=2)
        Label(self.new_script_frame, justify=LEFT, text=globalConstants.USCRIPTS_NEW_SCRIPT_WARN) \
            .grid(row=0, column=1, sticky=W, padx=4, pady=2, ipady=2)

        self.user_script_canvas = Canvas(self.tab_user_scripts, bd=0, highlightthickness=0, relief='ridge')
        self.user_script_canvas.grid(row=2, column=0, sticky=N + S + W + E)
        self.user_script_canvas.grid_columnconfigure(0, weight=1)
        self.user_script_canvas.grid_rowconfigure(0, weight=1)

        guiMouseEvents.add_mouse_scroll_to(self.user_script_canvas)

        # All the code below is just to make it scrollable
        self.user_script_section = LabelFrame(self.user_script_canvas, text=globalConstants.USCRIPTS_USER_SCRIPTS)
        self.user_script_section.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)
        self.user_script_section.grid_columnconfigure(0, weight=1)
        self.user_script_section.grid_rowconfigure(0, weight=1)
        self.user_script_section.bind("<Configure>", self.onUserScriptsFrameConfigure)

        v_scrollbar = Scrollbar(self.tab_user_scripts)
        v_scrollbar.grid(row=2, column=1, sticky=N + S + W + E)
        v_scrollbar.config(command=self.user_script_canvas.yview)
        self.user_script_canvas.config(yscrollcommand=v_scrollbar.set, scrollregion=self.user_script_canvas.bbox("all"))
        self.user_script_canvas.create_window((0, 0), window=self.user_script_section, anchor="nw")

        # Save button
        settings_buttons_frame = ttk.Frame(self.tab_user_scripts)
        settings_buttons_frame.grid(row=3, column=0, sticky=W + N + E + S)

        super(UserScriptsTab, self).__init__(settings_buttons_frame)

    ###
    # API
    ###

    def addUserScriptGui(self, placement_row, bindings_tuple, row_removal_callback):
        on_var = bindings_tuple[0]
        website_var = bindings_tuple[1]
        element_var = bindings_tuple[2]
        element_choices = bindings_tuple[3]
        attribute_var = bindings_tuple[4]
        attribute_choices = bindings_tuple[5]
        search_type_var = bindings_tuple[6]
        search_type_choices = bindings_tuple[7]
        value_var = bindings_tuple[8]
        percent_var = bindings_tuple[9]
        iframe_type = bindings_tuple[10]
        iframe_val = bindings_tuple[11]
        iframe_type_choices = bindings_tuple[12]

        on_var.set(1)

        script_frame = Frame(self.user_script_section)
        script_frame.grid(row=placement_row, column=0, sticky=W + E)
        script_frame.grid_rowconfigure(placement_row, weight=1)
        script_frame.grid_columnconfigure(0, weight=1)

        Checkbutton(script_frame, text='', variable=on_var).grid(row=0, column=0, sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_IF_URL).grid(row=0, column=1, sticky=W + E)
        Entry(script_frame, width=18, textvariable=website_var).grid(row=0, column=2, sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_FIND_ELT).grid(row=0, column=3, sticky=W + E)
        element_var.set(element_choices[0])
        ttk.Combobox(script_frame, width=5, values=element_choices, textvariable=element_var).grid(row=0, column=4,
                                                                                                   sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_BY_ATTR).grid(row=0, column=5, sticky=W + E)
        attribute_var.set(attribute_choices[0])
        ttk.Combobox(script_frame, width=5, values=attribute_choices, textvariable=attribute_var).grid(row=0,
                                                                                                       column=6,
                                                                                                       sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_WHICH).grid(row=0, column=7, sticky=W + E)
        search_type_var.set(search_type_choices[0])
        ttk.Combobox(script_frame, width=7, values=search_type_choices,
                     state='readonly', textvariable=search_type_var).grid(row=0, column=8, sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_A_VAL).grid(row=0, column=9, sticky=W + E)
        Entry(script_frame, width=15, textvariable=value_var).grid(row=0, column=10, sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_IS_IN_FRAME).grid(row=0, column=11,
                                                                                          sticky=W + E)
        iframe_type.set(iframe_type_choices[0])
        ttk.Combobox(script_frame, width=4, values=iframe_type_choices, textvariable=iframe_type) \
            .grid(row=0, column=12, sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_IFRAME_VAL).grid(row=0, column=13, sticky=W + E)
        Entry(script_frame, width=10, textvariable=iframe_val).grid(row=0, column=14, sticky=W + E)

        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_CLICK_WITH_CHANCE).grid(row=0, column=15,
                                                                                                sticky=W + E)
        percent_var.set('100')
        Spinbox(script_frame, from_=1, to=100, increment=1, width=3, textvariable=percent_var).grid(row=0,
                                                                                                    column=16,
                                                                                                    sticky=W + E)
        Label(script_frame, justify=LEFT, text=globalConstants.USCRIPTS_PERCENT).grid(row=0, column=17, sticky=W + E)

        ttk.Button(script_frame, text='-', width=2,
                   command=lambda: row_removal_callback(placement_row)).grid(row=0, column=18, sticky=W + E)

    def del_script_row(self, row_ind):
        row_holder = self.getRowFrameHolder(self.user_script_section, row_ind)
        children = self.getAllChildrenInRow(self.user_script_section, row_ind)

        for child in children:
            child.destroy()
        row_holder.destroy()

    def move_script_row(self, old_row, new_row, row_removal_callback):
        row_frame_holder = self.getRowFrameHolder(self.user_script_section, old_row)

        # print 'Moving old row', old_row, 'children', len(children), 'to position', new_row

        # Move the child: same cell in a different row
        row_frame_holder.grid(row=new_row, column=0)

        # rebind the remove button to pass the new correct index of the row to clear
        for child in self.getAllChildrenInRow(self.user_script_section, new_row):
            if isinstance(child, ttk.Button) and child.cget('text') == '-':
                child.configure(command=lambda: row_removal_callback(new_row))

    def getRowFrameHolder(self, widget, row_ind):
        for child in widget.children.values():
            info = child.grid_info()

            if info['row'] == row_ind:
                return child

    def getAllChildrenInRow(self, widget, row_ind):
        children = []

        for sub_child in self.getRowFrameHolder(widget, row_ind).children.values():
            children.append(sub_child)

        return children

    # when the new element is added to this frame, set the view portion of the canvas
    def onUserScriptsFrameConfigure(self, event):
        self.user_script_canvas.configure(scrollregion=self.user_script_canvas.bbox("all"))

    ###
    # ViewModel bindings
    ###

    def bindNewUsrScriptBtn(self, callback):
        self.new_user_script_btn.config(command=callback)

    def bind_click_link_types_cmbbx(self, click_link_types: list, current_click_link_type):
        self.random_click_types.config(values=click_link_types, textvariable=current_click_link_type)

    def bind_autorandom_clicks_enabled_checkbox(self, autorandom_clicks_enabled, callback=None):
        self.enable_random_clicks.config(variable=autorandom_clicks_enabled, command=callback)

    def bind_total_autorandom_clicks_spinbox(self, total_autorandom_clicks):
        self.random_click_amount.config(textvariable=total_autorandom_clicks)

    def bind_autorandom_scroll_enabled_checkbox(self, autorandom_scroll_enabled, callback=None):
        self.enable_random_scroll.config(variable=autorandom_scroll_enabled, command=callback)

    def bind_auto_scroll_percent_spinbox(self, auto_scroll_percent):
        self.random_scroll_page_percent.config(textvariable=auto_scroll_percent)

    def bind_after_scroll_time_min_spinbox(self, after_scroll_time_min):
        self.random_scroll_page_after_min.config(textvariable=after_scroll_time_min)

    def bind_after_scroll_time_max_spinbox(self, after_scroll_time_max):
        self.random_scroll_page_after_max.config(textvariable=after_scroll_time_max)

    def bind_over_scroll_time_min_spinbox(self, over_scroll_time_min):
        self.random_scroll_page_over_min.config(textvariable=over_scroll_time_min)

    def bind_over_scroll_time_max_spinbox(self, over_scroll_time_max):
        self.random_scroll_page_over_max.config(textvariable=over_scroll_time_max)
