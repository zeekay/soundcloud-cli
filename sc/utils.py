def copy_to_clipboard(text):
    try:
        from Tkinter import Tk
    except ImportError:
        return

    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.destroy()

def open_browser(url):
    import webbrowser

    webbrowser.open_new_tab(url)
