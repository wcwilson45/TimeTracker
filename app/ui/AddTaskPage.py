from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('540x1080')
        self.title('Main Application')

        menubar = Menu(self)
        self.config(menu=menubar)

        dropdown = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=dropdown)
        dropdown.add_command(label="Small Overlay", command=lambda: open_smalloverlaywindow(self))
        dropdown.add_command(label="Full Page", command=lambda: open_fullpagewindow(self))
        dropdown.add_command(label="Completed Tasks", command=lambda: open_completedtaskswindow(self))
        dropdown.add_command(label="Add Task", command=lambda: open_addtaskwindow(self))
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
    window.grab_set()


class AddTaskWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("540x720")
        self.title("Add Task")

        # Task Name
        Label(self, text="Task Name:").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=40).grid(row=0, column=1, pady=10)

        # Task Description
        Label(self, text="Description:").grid(row=1, column=0, sticky="nw", padx=20, pady=10)
        Text(self, height=5, width=40).grid(row=1, column=1, pady=10)

        # Tags
        Label(self, text="Tags:").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=40).grid(row=2, column=1, pady=10)

        # Time of Completion
        Label(self, text="Time of Completion (hours):").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=20).grid(row=3, column=1, pady=10, sticky="w")

        # Time Complexity
        Label(self, text="Time Complexity:").grid(row=4, column=0, sticky="w", padx=20, pady=10)
        ttk.Combobox(self, values=["Low", "Medium", "High"], width=17).grid(row=4, column=1, pady=10, sticky="w")

        # Date Completed
        Label(self, text="Date Completed:").grid(row=5, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=20).grid(row=5, column=1, pady=10, sticky="w")

        # Buttons at Bottom-Right
        confirm_button = Button(self, text="Confirm", width=15)
        confirm_button.grid(row=6, column=1, pady=20, sticky="e")

        exit_button = Button(self, text="Exit", width=15, command=self.destroy)
        exit_button.grid(row=6, column=1, pady=20, sticky="w")


def open_addtaskwindow(parent):
    window = AddTaskWindow(parent)
    window.grab_set()


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
