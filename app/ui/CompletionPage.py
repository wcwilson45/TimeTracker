from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

class CompletedTasksWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("540x320")
        self.title("Completed Tasks")

        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)

def open_completedtaskswindow(parent):
    window = CompletedTasksWindow(parent)
    window.grab.set()
