from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('540x1080')
        self.title('Full Page')

        menubar = Menu(self)
        self.config(menu=menubar)

        dropdown = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="...", menu=dropdown)
        dropdown.add_command(label="Small Overlay", command=lambda: open_smalloverlaywindow(self))
        dropdown.add_command(label="Full Page", command = lambda: open_fullpagewindow(self))
        dropdown.add_command(label="Completed Tasks", command = lambda: open_completedtaskswindow(self))
        dropdown.add_command(label="Import", command=ImportCommand)
        dropdown.add_command(label="Export", command=ExportCommand)


class SmallOverlayWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("540x320")
        self.title("Small Overlay")

        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)


def open_smalloverlaywindow(parent):
    window = SmallOverlayWindow(parent)
    window.grab_set()


class FullPageWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("540x1080")
        self.title("Full Page")

        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)

def open_fullpagewindow(parent):
    window = FullPageWindow(parent)
    window.grab_set()



class CompletedTasksWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("540x320")
        self.title("Completed Tasks")

        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)

def open_completedtaskswindow(parent):
    window = CompletedTasksWindow(parent)
    window.grab.set()


def ImportCommand():
    filename = filedialog.askopenfilename(
        initialdir="~",
        title="Select a File (.csv)",
        filetypes=[("CSV files", "*.csv")]
    )
    if filename:
        print(f"Selected file: {filename}")


def ExportCommand():
    print("Export")


if __name__ == "__main__":
    app = App()
    app.mainloop()
