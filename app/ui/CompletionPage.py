from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from tkinter import messagebox
import sqlite3
from .TaskHistory import CommitHistoryWindow, TaskHistoryDB
import pathlib

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("CompletionPage.py", '') + '\\Databases' + '\\task_list.db'


class CompletedTasksWindow(tk.Tk):
    def __init__(self, task_name=None, task_weight=None, task_time=None, task_id=None, task_description=None, refresh_callback=None):
        super().__init__()
        self.history_db = TaskHistoryDB()
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
        self.style.configure("Info.TLabel", font=("Arial", 10), background='#A9A9A9')
        self.style.configure("Tag.TLabel", font=("Arial", 8), background='#A9A9A9', padding=2, foreground='black')

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
            font=("Arial", 16, "bold"),
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
        tk.Label(self.tags_frame, text="Tags:", font=("Arial", 10), bg='#A9A9A9').pack(anchor=tk.W)

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
                # Begin transaction
                c.execute("BEGIN")
                
                # Get current task state before completion
                c.execute("SELECT * FROM TaskList WHERE task_id = ?", (self.task_id,))
                old_task = c.fetchone()

                # Add any missing columns to the CompletedTasks table
                # Check for required columns and add them if missing
                required_columns = {
                    "task_name": "TEXT", 
                    "task_time": "TEXT", 
                    "task_weight": "TEXT", 
                    "task_id": "INTEGER", 
                    "completion_date": "TEXT", 
                    "total_duration": "TEXT", 
                    "start_date": "TEXT", 
                    "task_tags": "TEXT", 
                    "task_weight_type": "TEXT", 
                    "task_description": "TEXT"
                }
                
                # Check existing columns
                c.execute("PRAGMA table_info(CompletedTasks)")
                existing_columns = {col[1]: col[2] for col in c.fetchall()}
                
                # Add any missing columns
                for col_name, col_type in required_columns.items():
                    if col_name not in existing_columns:
                        try:
                            c.execute(f"ALTER TABLE CompletedTasks ADD COLUMN {col_name} {col_type}")
                        except sqlite3.Error as e:
                            print(f"Error adding column {col_name}: {e}")
                
                # Record completion as a history event
                self.history_db.record_change(
                    self.task_id,
                    "status",
                    "in_progress",
                    "completed",
                    existing_conn=conn
                )

                # Insert into CompletedTasks with all fields
                completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("""INSERT INTO CompletedTasks 
                        (task_name, task_time, task_weight, task_id, completion_date, 
                        total_duration, start_date, task_tags, task_weight_type, task_description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (self.task_name, self.task_time, self.task_weight,
                        self.task_id, completion_time, self.task_time,
                        old_task[4] if old_task and len(old_task) > 4 else None,  # start_date
                        old_task[8] if old_task and len(old_task) > 8 else None,  # task_tags
                        old_task[7] if old_task and len(old_task) > 7 else None,  # task_weight_type
                        self.task_description))  # task_description

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

        tk.Label(header_frame, text=title, font=("Arial", 10), bg='#A9A9A9').pack(side=tk.LEFT, padx=5, pady=2)

        if title == "Commit History:":
                container_frame = tk.Frame(frame, bg='#A9A9A9', bd=1, relief='solid')
                container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 2))

                # Get task history
                history = self.history_db.get_task_history(self.task_id) if self.task_id else []

                tree = ttk.Treeview(container_frame, columns=("Date", "Change"), show="headings", height=7)
                tree.heading("Date", text="Date", anchor="center")
                tree.heading("Change", text="Change", anchor="center")
                tree.column("Date", anchor="center", width=120)
                tree.column("Change", anchor="center", width=180)

                scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                # Populate history
                for change_date, field, old_val, new_val in history:
                    tree.insert("", "end", values=(change_date, f"Changed {field}"), 
                            tags=(change_date, field, old_val, new_val))

                def on_history_select(event):
                    selected = tree.selection()
                    if selected:
                        item = tree.item(selected[0])
                        date, field, old_val, new_val = item["tags"]
                        self.open_commit_history_page()

                tree.bind("<Double-1>", on_history_select)
                tree.tag_configure('oddrow', background="#A9A9A9")
                tree.tag_configure('evenrow', background="#d3d3d3")
                tree.tag_configure('selected', background='#b3b3b3')

    def create_tag(self, text):
        tag_label = tk.Label(
            self.tags_frame,
            text=text,
            font=("Arial", 8),
            bg='#d3d3d3',
            fg='black',
            padx=5,
            pady=2
        )
        tag_label.pack(side=tk.LEFT, padx=(0, 5))

    def create_info_field(self, label_text, value_text):
        frame = tk.Frame(self.right_panel, bg='#A9A9A9', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text=label_text, font=("Arial", 10), bg='#A9A9A9').pack(anchor=tk.W)
        tk.Label(frame, text=value_text, font=("Arial", 10), bg='#A9A9A9').pack(anchor=tk.W)

    def open_commit_history_page(self):
        """Modified to use new CommitHistoryWindow"""
        if hasattr(self, 'task_id') and self.task_id:
            history_window = CommitHistoryWindow(self.task_id)
            history_window.grab_set()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to view its history.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompletedTasksWindow("Sample Task", "12/4/24", "03:23:56")
    root.mainloop()
