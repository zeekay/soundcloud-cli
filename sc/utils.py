import os
import sys

def copy_to_clipboard(text):
    # reliable on mac
    if sys.platform == 'darwin':
        os.system('echo "{0}" | pbcopy'.format(text))
        return

    # okay we'll try cross-platform way
    try:
        from Tkinter import Tk
    except ImportError:
        return

    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text.encode('ascii'))
    r.destroy()

def open_browser(url):
    import webbrowser

    webbrowser.open_new_tab(url)
