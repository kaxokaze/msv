from tkinter import Toplevel, Label, font, W, LEFT

from svLib import globalConstants


class AboutWindow:
    def __init__(self, third_party_links, third_party_download_clicked):
        self.link_color = "#3027e3"

        self.about_window = Toplevel()
        self.about_window.withdraw()
        self.about_window.resizable(width=False, height=False)
        self.about_window.title(globalConstants.ABOUT_TITLE)
        self.about_window.protocol('WM_DELETE_WINDOW', self.onAboutWinClose)

        try:
            self.about_window.wm_iconbitmap(bitmap="icon.ico")
        except:
            pass

        Label(self.about_window, justify=LEFT, text=globalConstants.ABOUT_TEXT_0).grid(row=0, column=0, padx=5,
                                                                                       pady=5,
                                                                                       sticky=W)
        Label(self.about_window, justify=LEFT, text=globalConstants.ABOUT_TEXT_1).grid(row=1, column=0, padx=5,
                                                                                       pady=5,
                                                                                       sticky=W)

        last_link_row = self.addThirdPartyDownloadLinks(2, third_party_links, third_party_download_clicked)

        Label(self.about_window, justify=LEFT, text=globalConstants.ABOUT_TEXT_2).grid(row=last_link_row, column=0,
                                                                                       padx=5, pady=5, sticky=W)

    def addThirdPartyDownloadLinks(self, link_text_row, third_party_links, third_party_download_clicked):
        third_party_header_font = font.Font(weight='bold', family='Helvetica', size=8)
        Label(self.about_window, justify=LEFT, text=globalConstants.ABOUT_TEXT_THIRD_PARTY,
              font=third_party_header_font) \
            .grid(row=link_text_row, column=0, padx=5, pady=1, sticky=W)

        third_party_link_font = font.Font(family='Helvetica', size=8, underline=True)
        link_row = link_text_row + 1
        for link_url in third_party_links:
            link_widget = Label(self.about_window, justify=LEFT, text=link_url, fg=self.link_color, cursor="hand2",
                                font=third_party_link_font)
            link_widget.grid(row=link_row, column=0, padx=5, pady=1, sticky=W)
            link_widget.bind("<Button-1>", third_party_download_clicked)
            link_row += 1

        return link_row

    def onAboutWinClose(self):
        self.about_window.withdraw()
