from tkinter import ttk, W, N, E, S

from svLib import globalConstants
from svLib.gui.components.toolTip import ListboxToolTip


class SettingsSaveUi:
    def __init__(self, settings_buttons_frame):
        self.save_opts_btn = ttk.Button(settings_buttons_frame, text=globalConstants.USCRIPTS_SAVE)
        self.save_opts_btn.grid(row=0, column=0, sticky=W + N + E + S, padx=4, pady=4, ipady=4)

        ListboxToolTip(self.save_opts_btn, [globalConstants.SAVING_SETTING_HINT_1,
                                            globalConstants.SAVING_SETTING_HINT_2], 39, 2)

        self.discard_opts_btn = ttk.Button(settings_buttons_frame, text=globalConstants.USCRIPTS_DISCARD)
        self.discard_opts_btn.grid(row=0, column=1, sticky=W + N + E + S, padx=4, pady=4, ipady=4)

        ListboxToolTip(self.discard_opts_btn, [globalConstants.DISCARDING_SETTING_HINT_1,
                                               globalConstants.DISCARDING_SETTING_HINT_2,
                                               globalConstants.DISCARDING_SETTING_HINT_3], 35, 3)

        self.reset_default_opts_btn = ttk.Button(settings_buttons_frame, text=globalConstants.USCRIPTS_RESET_DEFAULT)
        self.reset_default_opts_btn.grid(row=0, column=2, sticky=W + N + E + S, padx=4, pady=4, ipady=4)

        ListboxToolTip(self.reset_default_opts_btn, [globalConstants.RESETTING_SETTING_HINT_1,
                                                     globalConstants.RESETTING_SETTING_HINT_2,
                                                     globalConstants.RESETTING_SETTING_HINT_3], 32, 3)

        self.all_changes_synced()

    ###
    # API
    ###
    def new_changes_available(self):
        self.save_opts_btn.state(["!disabled"])
        self.discard_opts_btn.state(["!disabled"])

    def all_changes_synced(self):
        self.save_opts_btn.state(["disabled"])
        self.discard_opts_btn.state(["disabled"])

    ###
    # VM Bindings
    ###
    def bind_callbacks(self, on_save_options, on_options_discard, on_options_reset_default):
        self.save_opts_btn.configure(command=on_save_options)
        self.discard_opts_btn.configure(command=on_options_discard)
        self.reset_default_opts_btn.configure(command=on_options_reset_default)
