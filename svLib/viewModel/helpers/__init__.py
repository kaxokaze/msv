from tkinter import filedialog

import svLib
from svLib.userData import svSettings
from svLib.utils import stdHelper


def fillGuiWithFileConts(t_file, add_method):
    with t_file:
        entries = stdHelper.loadFileEntries(t_file)
        for entry in entries:
            add_method(entry)


def populateGui(add_method, title=None):
    t_file = openFileDial(title)
    if t_file is None:
        return

    fillGuiWithFileConts(t_file, add_method)


def openFileDial(title=None):
    return filedialog.askopenfile(mode='r', title=title,
                                  initialdir=svLib.userData.svSettings.program_data_folder)


def saveAsFileDial(title=None):
    return filedialog.asksaveasfile(mode='w', title=title,
                                    initialdir=svLib.userData.svSettings.program_data_folder)


def saveAsFilenameDial(title=None):
    return filedialog.asksaveasfilename(title=title, initialdir=svLib.userData.svSettings.program_data_folder)


def openFilenameDial(title=None):
    result = filedialog.askopenfilename(title=title, initialdir=svLib.userData.svSettings.program_data_folder)
    return result


def openDirectoryDial(title=None):
    result = filedialog.askdirectory(title=title, initialdir=svLib.userData.svSettings.program_data_folder)
    return result
