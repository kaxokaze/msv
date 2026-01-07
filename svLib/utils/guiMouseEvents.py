_scrollable_items = []


def add_mouse_scroll_to(scrollframe):
    scrollframe.bind('<Enter>', _bound_to_mousewheel)
    scrollframe.bind('<Leave>', _unbound_to_mousewheel)


def _bound_to_mousewheel(event):
    scrollframe = event.widget

    scrollframe.bind_all("<MouseWheel>", _on_mousewheel)
    _scrollable_items.append(scrollframe)


def _unbound_to_mousewheel(event):
    scrollframe = event.widget

    scrollframe.unbind_all("<MouseWheel>")
    _scrollable_items.remove(scrollframe)


def _on_mousewheel(event):
    for scrollable_widget in _scrollable_items:
        scrollable_widget.yview_scroll(int(-1*(event.delta/120)), "units")
