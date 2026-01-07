from tkinter import ttk, Tk, Menu

from svLib import globalConstants
from svLib.gui.aboutWindow import AboutWindow
from svLib.gui.eventsTab import EventsTab
from svLib.gui.mainTab import MainTab
from svLib.gui.optionsTab import OptionsTab
from svLib.gui.scrapProxiesTab import ScrapProxiesTab
from svLib.gui.userScriptsTab import UserScriptsTab


class MainWindow:
    def __init__(self, b_start_callback, b_stop_callback, on_frame, third_party_links,
                 on_third_party_download_clicked, on_snapshots_folder_open, update_drivers_command):
        self.root = Tk()
        self.root.title(globalConstants.PROGRAM_TITLE)
        self.root.geometry("1130x650+200+20")

        self.on_frame = on_frame
        try:
            self.root.wm_iconbitmap(bitmap="icon.ico")
        except:
            pass

        # main window consists of a few tabs, notebook object holds them
        self.note_book = ttk.Notebook(self.root)

        # Populates the main tab with all the things about listing active proxies, making requests, etc.
        self.main_tab: MainTab = MainTab(self.note_book, b_start_callback, b_stop_callback, update_drivers_command)

        self.events_tab: EventsTab = EventsTab(self.note_book)

        self.options_tab: OptionsTab = OptionsTab(self.note_book, on_snapshots_folder_open)

        self.user_scripts_tab: UserScriptsTab = UserScriptsTab(self.note_book)

        self.scrap_proxies_tab: ScrapProxiesTab = ScrapProxiesTab(self.note_book, self.root)

        self.note_book.pack(expand=1, fill="both")

        self.aboutWindow: AboutWindow = AboutWindow(third_party_links, on_third_party_download_clicked)

        # main menu
        self.initTopMenu(self.root)

    # ==============
    # === This section here is all about creation and placement of the buttons and shiet
    # ==============

    def initTopMenu(self, parent_frame):
        self.menubar = Menu(parent_frame)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=globalConstants.MENU_ITEM_EXP_HEALTHY_PROXIES)
        self.filemenu.add_command(label=globalConstants.MENU_ITEM_EXP_NON_LAGGING_PROXIES)
        self.filemenu.add_command(label=globalConstants.MENU_ITEM_SAVE_LOG)
        self.menubar.add_cascade(label=globalConstants.MENU_FILE, menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label=globalConstants.MENU_ITEM_ABOUT, command=self.openAboutWin)
        self.menubar.add_cascade(label=globalConstants.MENU_HELP, menu=self.helpmenu)

        parent_frame.config(menu=self.menubar)

    # ==============
    # ==="""""API""""" of the gui
    # ==============

    def go(self):
        self.root.mainloop()

    def setTitle(self, title):
        self.root.wm_title(globalConstants.PROGRAM_TITLE + ' [' + title + ']')

    def run(self):
        self.root.after(100, self.every_frame)

    # ==============
    # Some internal callbacks
    # ==============

    def every_frame(self):
        if self.on_frame is not None:
            self.on_frame()
        self.root.after(100, self.every_frame)

    def openAboutWin(self):
        self.aboutWindow.about_window.deiconify()

    # ==============
    # === Tkinter Var binding (used from the Model class)
    # ==============

    def bindExportHealthyProxies(self, command):
        self.filemenu.entryconfig(self.filemenu.index(globalConstants.MENU_ITEM_EXP_HEALTHY_PROXIES), command=command)

    def bindExportNonLaggedProxies(self, command):
        self.filemenu.entryconfig(self.filemenu.index(globalConstants.MENU_ITEM_EXP_NON_LAGGING_PROXIES),
                                  command=command)
    def bindSaveLog(self, command):
        self.filemenu.entryconfig(self.filemenu.index(globalConstants.MENU_ITEM_SAVE_LOG), command=command)
