from tkinter import *
from tkinter.ttk import *
from time import strftime
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk


class SmallOverlayWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry('300x150')
        self.title('SmallOverlay')

        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)

class CompletedTasksWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry('540x1080')
        self.title('Completed Tasks')

        ttk.Button(self, text = 'Close', command = self.destroy).pack(expand = True)

class AddTasksWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry('560x280')
        self.title('Add Task')

        ttk.Button(self, text = 'Close', command = self.destroy).pack(expand = True)

class CompleteTaskWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry('560x280')
        self.title('Complete Task')

        ttk.Button(self, text = 'Close', command = self.destroy).pack(expand = True)

class EditTasksWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry('560x280')
        self.title('Edit Task')

        ttk.Button(self, text = 'Close', command = self.destroy).pack(expand = True)

class CommitHistoryWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry('560x280')
        self.title('Commit History')

        ttk.Button(self, text = 'Close', command = self.destroy).pack(expand = True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('540x1080')
        self.title('Main Window')

        # place a button on the root window
        ttk.Button(self, text='Small Overlay', command=self.open_smalloverlaywindow).pack(expand=True)
        ttk.Button(self, text= 'Completed Tasks', command = self.open_completedtaskswindow).pack(expand = True)
        ttk.Button(self, text= 'Edit Task', command = self.open_edittaskswindow).pack(expand = True)
        ttk.Button(self, text= 'Add Task', command = self.open_addtaskswindow).pack(expand = True)
        ttk.Button(self, text= 'Commit History', command = self.open_commithistorywindow).pack(expand = True)
        ttk.Button(self, text= 'Complete Task', command = self.open_completetaskwindow).pack(expand = True)

    def open_smalloverlaywindow(self):
        window = SmallOverlayWindow(self)
        window.grab_set()
    def open_completedtaskswindow(self):
        window = CompletedTasksWindow(self)
        window.grab_set()
    def open_edittaskswindow(self):
        window = EditTasksWindow(self)
        window.grab_set()
    def open_addtaskswindow(self):
        window = AddTasksWindow(self)
        window.grab_set()
    def open_commithistorywindow(self):
        window = CommitHistoryWindow(self)
        window.grab_set()
    def open_completetaskwindow(self):
        window = CompleteTaskWindow(self)
        window.grab_set()

if __name__ == "__main__":
    app = App()
    app.mainloop()