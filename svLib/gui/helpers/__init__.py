from tkinter import Scrollbar, Listbox, Frame, Label, Checkbutton, N, S, W, E, HORIZONTAL

from svLib.utils import guiMouseEvents


def makeScrollableListBox(parent_frame, lb_column, start_row=0, start_col=0):
    hb_frame = Frame(parent_frame)
    hb_frame.grid(row=0, column=lb_column, padx=5)

    list_box = Listbox(hb_frame, width=45)
    list_box.grid(row=start_row, column=start_col, sticky=N + S + W + E)

    guiMouseEvents.add_mouse_scroll_to(list_box)

    v_scrollbar = Scrollbar(hb_frame)
    v_scrollbar.grid(row=start_row, column=start_col + 1, sticky=N + S + W + E)
    # attach listbox to scrollbar
    v_scrollbar.config(command=list_box.yview)

    h_scrollbar = Scrollbar(hb_frame, orient=HORIZONTAL)
    h_scrollbar.grid(row=start_row + 1, column=start_col, sticky=N + S + W + E)
    # attach listbox to scrollbar
    h_scrollbar.config(command=list_box.xview)

    list_box.config(yscrollcommand=v_scrollbar.set)
    list_box.config(xscrollcommand=h_scrollbar.set)

    return list_box, hb_frame


def label4CheckBoxHeader(parent_frame, label_text, check_box_on_txt, check_box_on_color, curr=False):
    header1_frame = Frame(parent_frame)
    header1_frame.grid(row=0, column=0, sticky=W)

    cb1 = Checkbutton(header1_frame, text=check_box_on_txt, fg=check_box_on_color)
    cb1.grid(row=0, column=0)

    Label(header1_frame, text=label_text, font="-weight bold").grid(row=0, column=1)

    cur_val_lab = None
    if curr:
        cur_val_lab = Label(header1_frame, text="0", fg="#13ea7f")
        cur_val_lab.grid(row=0, column=2)

    max_val_lab = Label(header1_frame, text="-1")
    max_val_lab.grid(row=0, column=3)

    return cur_val_lab, max_val_lab, cb1
