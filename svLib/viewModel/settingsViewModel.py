from tkinter import Variable

from svLib.gui.settingsSaveUi import SettingsSaveUi


class SettingsViewModel:
    def __init__(self, ui: SettingsSaveUi, on_save_options, on_options_discard, on_options_reset_default,
                 on_ui_changed):
        self.ui = ui
        self.on_save_options_callback = on_save_options
        self.on_options_discard_callback = on_options_discard
        self.on_options_reset_default_callback = on_options_reset_default
        self.on_ui_changed_callback = on_ui_changed
        self.ui.bind_callbacks(self.on_save_options, self.on_options_discard, self.on_options_reset_default)
        self.changes_tracked = True

    ###
    # API
    ###

    def ui_data_changed(self):
        self.on_ui_settings_change(None, None, None)

    def show_new_changes_to_ui(self):
        if self.changes_tracked:
            self.ui.new_changes_available()

    def remove_new_changes_from_ui(self):
        self.ui.all_changes_synced()

    def add_change_tracking_to_var(self, var_field):
        if issubclass(type(var_field), Variable):
            var_field.trace_add("write", self.on_ui_settings_change)

    def remove_change_tracking_from_var(self, var_field):
        if issubclass(type(var_field), Variable):
            info = var_field.trace_info()
            if len(info) > 0 and len(info[0]) > 1:
                var_field.trace_remove("write", info[0][1])

    ###
    # Bindings
    ###
    def bind_change_callback_to_all_vars(self):
        all_vars_dict = vars(self)
        for var_field_name in all_vars_dict:
            self.add_change_tracking_to_var(all_vars_dict[var_field_name])

    ###
    # Callbacks
    ###
    def on_save_options(self):
        self.changes_tracked = False
        self.on_save_options_callback()
        self.remove_new_changes_from_ui()
        self.changes_tracked = True

    def on_options_discard(self):
        self.changes_tracked = False
        self.on_options_discard_callback()
        self.remove_new_changes_from_ui()
        self.changes_tracked = True

    def on_options_reset_default(self):
        self.on_options_reset_default_callback()

    def on_ui_settings_change(self, target, mode, callback):
        self.on_ui_changed_callback()
        self.show_new_changes_to_ui()
