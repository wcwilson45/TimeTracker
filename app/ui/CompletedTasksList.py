from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
import csv
from tkinter import messagebox

background_color = "#A9A9A9"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "#E0E0E0"

main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"

class CompletedTasksList(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller  # Reference to main app
        self.current_sort_reverse = False  # Track sorting direction

        self.configure(background="#A9A9A9")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#d3d3d3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#d3d3d3")

        style.map("Treeview", background=[('selected', "347083")])

        # Tree view setup
        completedlist_frame = tk.Frame(self, bg="#A9A9A9")
        completedlist_frame.pack(pady=5, padx=10)

        completedlist_scroll = ttk.Scrollbar(completedlist_frame)
        completedlist_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.completed_list = ttk.Treeview(completedlist_frame,
                                           yscrollcommand=completedlist_scroll.set,
                                           selectmode="extended",
                                           height=13)
        self.completed_list.pack()

        completedlist_scroll.config(command=self.completed_list.yview)

        # Column configuration
        self.completed_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID", "Completion Date",
                                          "Total Duration")

        self.completed_list.column("#0", width=0, stretch=tk.NO)
        self.completed_list.column('Task Name', anchor=tk.W, width=135)
        self.completed_list.column('Task Time', anchor=tk.CENTER, width=75)
        self.completed_list.column('Task Weight', anchor=tk.CENTER, width=50)
        self.completed_list.column('Task ID', anchor=tk.CENTER, width=50)
        self.completed_list.column('Completion Date', anchor=tk.CENTER, width=135)
        self.completed_list.column('Total Duration', anchor=tk.CENTER, width=100)

        self.completed_list.heading("#0", text="", anchor=tk.W)
        self.completed_list.heading("Task Name", text="Task Name", anchor=tk.W,
                                    command=lambda: self.sort_completed_tasks("Task Name"))
        self.completed_list.heading("Task Time", text="Time", anchor=tk.CENTER,
                                    command=lambda: self.sort_completed_tasks("Task Time"))
        self.completed_list.heading("Task Weight", text="Weight", anchor=tk.CENTER,
                                    command=lambda: self.sort_completed_tasks("Task Weight"))
        self.completed_list.heading("Task ID", text="ID", anchor=tk.CENTER,
                                    command=lambda: self.sort_completed_tasks("Task ID"))
        self.completed_list.heading("Completion Date", text="Completed On", anchor=tk.CENTER,
                                    command=lambda: self.sort_completed_tasks("Completion Date"))
        self.completed_list.heading("Total Duration", text="Total Time", anchor=tk.CENTER,
                                    command=lambda: self.sort_completed_tasks("Total Duration"))

        self.completed_list.tag_configure('oddrow', background="white")
        self.completed_list.tag_configure('evenrow', background="#d3d3d3")

        # Button frame
        bottom_frame = tk.Frame(self, bg=background_color)
        bottom_frame.pack(fill='x', side='bottom', pady=5, padx=10)

        delete_all_button = tk.Button(bottom_frame, text="Delete All", bg=del_btn_color)
        delete_all_button.pack(side='right')

        delete_button = tk.Button(bottom_frame, text="Delete", bg=del_btn_color)
        delete_button.pack(side='right', padx=(0, 5))

        export_button = tk.Button(bottom_frame, text="Export", bg = main_btn_color)
        export_button.pack(side = "left")

        rld_button = tk.Button(bottom_frame, text = "Reload List",bg = main_btn_color, command = self.load_completed_tasks)
        rld_button.pack(side = "left", padx = 6)

        self.load_completed_tasks()

    def load_completed_tasks(self):
        """Loads completed tasks from SQLite database into Treeview."""
        for item in self.completed_list.get_children():
            self.completed_list.delete(item)

        conn = sqlite3.connect('task_list.db')
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM CompletedTasks ORDER BY completion_date DESC")
            tasks = c.fetchall()

            for i, task in enumerate(tasks):
                tag = ('evenrow' if i % 2 == 0 else 'oddrow')
                self.completed_list.insert('', 'end', values=task, tags=tag)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading completed tasks: {str(e)}")
        finally:
            conn.close()

    def sort_completed_tasks(self, col):
        """Sort completed tasks by column."""
        try:
            # Retrieve all items from Treeview
            items = [(self.completed_list.set(k, col), k) for k in self.completed_list.get_children("")]

            # Convert to appropriate type (for numeric columns)
            if col in ["Task Time", "Task Weight", "Task ID", "Total Duration"]:
                items.sort(key=lambda x: float(x[0]) if x[0] else 0, reverse=self.current_sort_reverse)
            elif col in ["Completion Date"]:
                items.sort(key=lambda x: x[0] if x[0] else "", reverse=self.current_sort_reverse)
            else:
                items.sort(reverse=self.current_sort_reverse)

            # Rearrange items in sorted order
            for index, (_, k) in enumerate(items):
                self.completed_list.move(k, "", index)

                # Reapply row colors
                self.completed_list.item(k, tags=('evenrow' if index % 2 == 0 else 'oddrow'))

            # Toggle sort direction for next click
            self.current_sort_reverse = not self.current_sort_reverse

        except Exception as e:
            messagebox.showerror("Sorting Error", f"An error occurred while sorting: {str(e)}")
