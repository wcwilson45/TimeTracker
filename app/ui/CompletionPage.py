
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from tkinter import messagebox
import sqlite3
from .CommitHistoryPage import CommitHistoryWindow
import pathlib

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("CompletionPage.py", '') + '\\Databases' + '\\task_list.db'


class CompletedTasksWindow(tk.Tk):
    def __init__(self, task_name=None, task_weight=None, task_time=None, task_id=None, task_description=None, refresh_callback=None):
        super().__init__()

        self.task_name = task_name
        self.task_weight = task_weight
        self.task_time = task_time
        self.task_id = task_id
        self.task_description = task_description
        self.refresh_callback = refresh_callback

        # Font Tuples for Use on pages
        self.fonts = {
            "Title_Tuple": tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            "Body_Tuple": tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            "Description_Tuple": tkfont.Font(family="Sf Pro Text", size=12)
        }

        self.geometry("500x475")
        self.title("Task Details")
        self.configure(bg="#A9A9A9")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("Info.TLabel", font=("SF Pro Text", 10), background='#A9A9A9')
        self.style.configure("Tag.TLabel", font=("SF Pro Text", 8), background='#A9A9A9', padding=2, foreground='black')

        # Main container
        self.main_container = tk.Frame(self, bg='#A9A9A9', bd=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Top frame for title
        self.top_frame = tk.Frame(self.main_container, bg='#A9A9A9', bd=0)
        self.top_frame.pack(fill=tk.X, pady=(0, 5))

        # Header
        self.header_label = tk.Label(
            self.top_frame,
            text=self.task_name if self.task_name else "No Task Selected",
            font=("SF Pro Text", 16, "bold"),
            bg='#A9A9A9',
            bd=0
        )
        self.header_label.pack(side=tk.LEFT)

        # Main content frame using grid
        self.content_frame = tk.Frame(self.main_container, bg='#A9A9A9', bd=0)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel (description and commit history)
        self.left_panel = tk.Frame(self.content_frame, bg='#A9A9A9', bd=0, width=300)
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Right panel (info and buttons)
        self.right_panel = tk.Frame(self.content_frame, bg='#A9A9A9', bd=0, width=160)
        self.right_panel.grid(row=0, column=1, sticky='n')
        self.right_panel.grid_propagate(False)

        # Configure grid weights
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Description and Commit History sections
        self.create_collapsible_section(self.left_panel, "Description:", "Enter description here...", height=12)
        self.create_collapsible_section(self.left_panel, "Commit History:", "Enter commit history...", height=12)

        # Tags
        self.tags_frame = tk.Frame(self.right_panel, bg='#A9A9A9', bd=0)
        self.tags_frame.pack(fill=tk.X, pady=(25, 5))
        tk.Label(self.tags_frame, text="Tags:", font=("SF Pro Text", 10), bg='#A9A9A9').pack(anchor=tk.W)

        # Create tag labels
        self.create_tag("Blue")
        self.create_tag("Small")
        self.create_tag("Tech")

        # Time information
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.create_info_field("Time of Completion:", self.task_time if self.task_time else "00:00:00")
        self.create_info_field("Task Weight:", self.task_weight if self.task_weight else "N/A")
        self.create_info_field("Date Completed:", current_time)

        # Buttons at the bottom
        self.button_frame = tk.Frame(self.content_frame, bg='#A9A9A9', bd=0)
        self.button_frame.place(relx=1.0, x=6.5, y=405.75, anchor="e")

        # Cancel and Complete buttons
        self.cancel_btn = tk.Button(
            self.button_frame,
            text="Cancel",
            command=self.open_commit_history_page,
            bg='#e99e56',
            fg='black',
            # relief='flat',
            padx=10,
            pady=5
        )
        self.cancel_btn.pack(side=tk.RIGHT, padx=1)

        self.complete_btn = tk.Button(
            self.button_frame,
            text="Complete",
            command=self.complete_task,
            bg='#b2fba5',
            fg='black',
            padx=10,
            pady=5
        )
        self.complete_btn.pack(side=tk.RIGHT)

    def complete_task(self):
        if self.task_id:
            conn = sqlite3.connect(path)
            c = conn.cursor()

            try:
                # Insert into CompletedTasks
                completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("""INSERT INTO CompletedTasks 
                           (task_name, task_time, task_weight, task_id, completion_date, total_duration)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                          (self.task_name, self.task_time, self.task_weight,
                           self.task_id, completion_time, self.task_time))

                # Delete from TaskList
                c.execute("DELETE FROM TaskList WHERE task_id = ?", (self.task_id,))

                conn.commit()
                messagebox.showinfo("Success", "Task completed successfully!")

                if self.refresh_callback:
                    self.refresh_callback()
                self.destroy()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error completing task: {str(e)}")
                conn.rollback()
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "No task selected to complete.")

    def create_collapsible_section(self, parent, title, placeholder, height=7):
        frame = tk.Frame(parent, bg='#A9A9A9', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))

        header_frame = tk.Frame(frame, bg='#A9A9A9')
        header_frame.pack(fill=tk.X, anchor=tk.W)

        tk.Label(header_frame, text=title, font=("SF Pro Text", 10), bg='#A9A9A9').pack(side=tk.LEFT, padx=5, pady=2)

        if title == "Commit History:":
            container_frame = tk.Frame(frame, bg='#A9A9A9', bd=1, relief='solid')
            container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 2))

            tree_frame = tk.Frame(container_frame, bg='#A9A9A9')
            tree_frame.pack(fill=tk.BOTH, expand=True)

            tree = ttk.Treeview(tree_frame, columns=("Date",), show="headings", height=7)
            tree.heading("Date", text="Date", anchor="center")
            tree.column("Date", anchor="center", width=120)

            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            dates = ["12/4/24", "12/6/24", "12/8/24", "12/10/24", "10/8/24", "11/2/24",
                     "10/8/24", "11/2/24", "10/8/24", "11/2/24", "10/8/24"]
            for i, date in enumerate(dates):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                tree.insert("", "end", values=(date,), tags=(tag,))

            tree.tag_configure("oddrow", background="#A9A9A9")
            tree.tag_configure("evenrow", background="#d3d3d3")
            tree.tag_configure('selected', background='#b3b3b3')

            def on_commit_click(event):
                try:
                    selected_item = tree.selection()[0]
                    for item in tree.get_children():
                        tree.item(item, tags=(tree.item(item)['tags'][0],))
                    tree.item(selected_item, tags=('selected',))
                    self.open_commit_history_page()
                except IndexError:
                    pass

            tree.bind("<Button-1>", on_commit_click)

        else:
            container_frame = tk.Frame(frame, bg='#A9A9A9', bd=1, relief='solid')
            container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 2))

            scrollbar = tk.Scrollbar(container_frame, orient="vertical")
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text = tk.Text(container_frame, height=height, wrap=tk.WORD, bg='#d3d3d3', bd=0,
                           yscrollcommand=scrollbar.set)
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=text.yview)
            text.insert("1.0", self.task_description if self.task_description else placeholder)

    def create_tag(self, text):
        tag_label = tk.Label(
            self.tags_frame,
            text=text,
            font=("SF Pro Text", 8),
            bg='#d3d3d3',
            fg='black',
            padx=5,
            pady=2
        )
        tag_label.pack(side=tk.LEFT, padx=(0, 5))

    def create_info_field(self, label_text, value_text):
        frame = tk.Frame(self.right_panel, bg='#A9A9A9', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text=label_text, font=("SF Pro Text", 10), bg='#A9A9A9').pack(anchor=tk.W)
        tk.Label(frame, text=value_text, font=("SF Pro Text", 10), bg='#A9A9A9').pack(anchor=tk.W)

    def open_commit_history_page(self):
        self.task_window = CommitHistoryWindow()
        self.task_window.grab_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = CompletedTasksWindow("Sample Task", "12/4/24", "03:23:56")
    root.mainloop()
