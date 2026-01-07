import tkinter

from svLib import globalConstants
from svLib.gui.userScriptsTab import UserScriptsTab
from svLib.viewModel.settingsViewModel import SettingsViewModel


class UserScriptsTabViewModel(SettingsViewModel):
    def __init__(self, user_scripts_tab: UserScriptsTab, link_types: list,
                 on_save_options, on_options_discard, on_options_reset_default, on_ui_changed):
        super().__init__(user_scripts_tab, on_save_options, on_options_discard, on_options_reset_default, on_ui_changed)

        self.user_scripts_tab = user_scripts_tab

        # user scripts tab
        self.usr_scripts = []
        self.user_scripts_tab.bindNewUsrScriptBtn(self.on_new_user_script)

        # auto-random clicks
        self.autorandom_clicks_enabled = tkinter.IntVar()
        self.autorandom_clicks_enabled.set(0)
        self.user_scripts_tab.bind_autorandom_clicks_enabled_checkbox(self.autorandom_clicks_enabled)

        self.click_link_types: list = link_types
        self.current_click_link_type = tkinter.StringVar()
        self.set_click_link_types(link_types)

        self.total_autorandom_clicks = tkinter.IntVar()
        self.total_autorandom_clicks.set(0)
        self.user_scripts_tab.bind_total_autorandom_clicks_spinbox(self.total_autorandom_clicks)

        # auto-random scroll
        self.autorandom_scroll_enabled = tkinter.IntVar()
        self.autorandom_scroll_enabled.set(0)
        self.user_scripts_tab.bind_autorandom_scroll_enabled_checkbox(self.autorandom_scroll_enabled)

        self.auto_scroll_percent = tkinter.DoubleVar()
        self.auto_scroll_percent.set(0)
        self.user_scripts_tab.bind_auto_scroll_percent_spinbox(self.auto_scroll_percent)

        self.after_scroll_time_min = tkinter.DoubleVar()
        self.after_scroll_time_min.set(0)
        self.user_scripts_tab.bind_after_scroll_time_min_spinbox(self.after_scroll_time_min)
        self.after_scroll_time_max = tkinter.DoubleVar()
        self.after_scroll_time_max.set(0)
        self.user_scripts_tab.bind_after_scroll_time_max_spinbox(self.after_scroll_time_max)

        self.over_scroll_time_min = tkinter.DoubleVar()
        self.over_scroll_time_min.set(0)
        self.user_scripts_tab.bind_over_scroll_time_min_spinbox(self.over_scroll_time_min)
        self.over_scroll_time_max = tkinter.DoubleVar()
        self.over_scroll_time_max.set(0)
        self.user_scripts_tab.bind_over_scroll_time_max_spinbox(self.over_scroll_time_max)

    ###
    # API
    ###

    def is_autorandom_clicks_enabled(self):
        return self.autorandom_clicks_enabled.get() == 1

    def set_autorandom_clicks_enabled(self, value: bool):
        self.autorandom_clicks_enabled.set(1 if value is True else 0)

    def get_total_autorandom_clicks(self):
        return self.total_autorandom_clicks.get()

    def set_total_autorandom_clicks(self, value: int):
        self.total_autorandom_clicks.set(value)

    def set_click_link_types(self, click_link_types: list):
        self.click_link_types = click_link_types
        self.current_click_link_type.set(self.click_link_types[1])
        self.user_scripts_tab.bind_click_link_types_cmbbx(self.click_link_types,
                                                          self.current_click_link_type)
        self.current_click_link_type.set(self.click_link_types[1])

    def set_click_link_type(self, click_link_type: str):
        self.current_click_link_type.set(click_link_type)

    def get_click_link_type(self):
        return self.current_click_link_type.get()

    def is_autorandom_scroll_enabled(self):
        return self.autorandom_scroll_enabled.get() == 1

    def set_autorandom_scroll_enabled(self, value: bool):
        self.autorandom_scroll_enabled.set(1 if value is True else 0)

    def get_auto_scroll_percent(self):
        return self.auto_scroll_percent.get()

    def set_auto_scroll_percent(self, value: float):
        self.auto_scroll_percent.set(value)

    def get_after_scroll_time_min(self):
        return self.after_scroll_time_min.get()

    def set_after_scroll_time_min(self, value: float):
        self.after_scroll_time_min.set(value)

    def get_after_scroll_time_max(self):
        return self.after_scroll_time_max.get()

    def set_after_scroll_time_max(self, value: float):
        self.after_scroll_time_max.set(value)

    def get_over_scroll_time_min(self):
        return self.over_scroll_time_min.get()

    def set_over_scroll_time_min(self, value: float):
        self.over_scroll_time_min.set(value)

    def get_over_scroll_time_max(self):
        return self.over_scroll_time_max.get()

    def set_over_scroll_time_max(self, value: float):
        self.over_scroll_time_max.set(value)

    def get_user_scripts_for_agent(self):
        u_scrs = []

        for tkScript in self.usr_scripts:
            u_script = (
                tkScript[0].get() == 1,  # on
                tkScript[1].get(),  # website
                tkScript[2].get(),  # el name
                tkScript[4].get(),  # attr name
                tkScript[6].get(),  # search_type
                tkScript[8].get(),  # search val
                tkScript[9].get(),  # percent
                tkScript[10].get(),  # iframe_type
                tkScript[11].get(),  # iframe_val
            )

            u_scrs.append(u_script)

        return u_scrs

    def set_user_scripts_from_agent(self, agent_user_scripts):
        if len(agent_user_scripts) != len(self.usr_scripts):
            return False

        for i in range(0, len(agent_user_scripts)):
            tkScript = self.usr_scripts[i]
            u_script = agent_user_scripts[i]

            tkScript[0].set(1 if u_script[0] is True else 0),  # on
            tkScript[1].set(u_script[1]),  # website
            tkScript[2].set(u_script[2]),  # el name
            tkScript[4].set(u_script[3]),  # attr name
            tkScript[6].set(u_script[4]),  # search_type
            tkScript[8].set(u_script[5]),  # search val
            tkScript[9].set(u_script[6]),  # percent
            tkScript[10].set(u_script[7]),  # iframe_type
            tkScript[11].set(u_script[8]),  # iframe_val

        return True

    def add_user_script_from_settings(self, user_script):
        self.on_new_user_script(True)

        # after onuserscript, there's one new empty script at the end of the list
        usr_script_model = self.usr_scripts[len(self.usr_scripts) - 1]

        usr_script_model[0].set(int(user_script[0] == 'True'))  # on
        usr_script_model[1].set(user_script[1])  # website
        usr_script_model[2].set(user_script[2])  # el name
        usr_script_model[4].set(user_script[3])  # attr name
        usr_script_model[6].set(user_script[4])  # srch_type
        usr_script_model[8].set(user_script[5])  # srch val
        usr_script_model[9].set(user_script[6])  # percent

        try:
            usr_script_model[10].set(user_script[7])  # iframe_type
            usr_script_model[11].set(user_script[8])  # iframe_val
        except Exception as e:
            usr_script_model[10].set(globalConstants.NO_IFRAME)
            print("exception during script adding, no extra fields", e)
        finally:
            for s_var in usr_script_model:
                self.add_change_tracking_to_var(s_var)

    def remove_userscripts(self):
        for script_ind in range(len(self.usr_scripts)):
            removed_script = self.usr_scripts[script_ind]
            for s_var in removed_script:
                self.remove_change_tracking_from_var(s_var)

            self.user_scripts_tab.del_script_row(script_ind)

        while len(self.usr_scripts) > 0:
            self.usr_scripts.pop()

    ###
    # Callbacks
    ###

    def on_new_user_script(self, from_settings=False):
        last_row = len(self.usr_scripts)
        usr_script_data = (
            tkinter.IntVar(),  # is on?
            tkinter.StringVar(),  # website
            tkinter.StringVar(),  # element name
            ['a', 'div', 'input', 'span', 'button'],  # element choices
            tkinter.StringVar(),  # attribute name
            ['class', 'id', 'name', 'href', 'type', globalConstants.TXT_SEARCH_BY_TEXT],  # attribute choices
            tkinter.StringVar(),  # search type
            [globalConstants.TXT_CONTAINS, globalConstants.TXT_EQUALS],  # search choices
            tkinter.StringVar(),  # value
            tkinter.StringVar(),  # chance_percent
            tkinter.StringVar(),  # iframe_type
            tkinter.StringVar(),  # iframe_val
            [globalConstants.NO_IFRAME, 'id', 'name', 'class', 'type', 'src'],  # iframe type choices
        )

        if not from_settings:
            self.ui_data_changed()
            for s_var in usr_script_data:
                self.add_change_tracking_to_var(s_var)

        self.user_scripts_tab.addUserScriptGui(last_row, usr_script_data, self.on_scripts_row_removal)

        self.usr_scripts.append(usr_script_data)

    def on_scripts_row_removal(self, script_ind):
        self.ui_data_changed()

        removed_script = self.usr_scripts.pop(script_ind)
        for s_var in removed_script:
            self.remove_change_tracking_from_var(s_var)

        self.user_scripts_tab.del_script_row(script_ind)

        for i in range(script_ind + 1, len(self.usr_scripts) + 1):
            self.user_scripts_tab.move_script_row(i, i - 1, self.on_scripts_row_removal)
