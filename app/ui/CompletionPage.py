from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from tkinter import messagebox
import sqlite3
import pathlib

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("CompletionPage.py", '') + '\\Databases' + '\\task_list.db'

class TaskHistoryDB:
    def __init__(self):
        self.path = pathlib.Path(__file__).parent
        self.path = str(self.path).replace("CompletionPage.py", '') + '\\Databases' + '\\task_list.db'
        
        # Create the history table
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        
        c.execute("""CREATE TABLE IF NOT EXISTS task_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            change_date TEXT,
            field_changed TEXT,
            old_value TEXT,
            new_value TEXT,
            FOREIGN KEY (task_id) REFERENCES TaskList(task_id)
        )""")
        
        conn.commit()
        conn.close()

    def record_change(self, task_id, field_changed, old_value, new_value, existing_conn=None):
        """Record a change in the task history
        
        Args:
            task_id: The ID of the task
            field_changed: Name of the field that changed
            old_value: Previous value
            new_value: New value
            existing_conn: Optional existing database connection to use
        """
        should_close_conn = False
        if existing_conn:
            conn = existing_conn
        else:
            conn = sqlite3.connect(self.path)
            should_close_conn = True
            
        c = conn.cursor()
        
        change_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("""
            INSERT INTO task_history 
            (task_id, change_date, field_changed, old_value, new_value)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, change_date, field_changed, old_value, new_value))
        
        if should_close_conn:
            conn.commit()
            conn.close()
        # No commit if using existing connection - let the caller handle it

    def get_task_history(self, task_id):
        """Get all history records for a task"""
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        
        c.execute("""
            SELECT change_date, field_changed, old_value, new_value
            FROM task_history
            WHERE task_id = ?
            ORDER BY change_date DESC
        """, (task_id,))
        
        history = c.fetchall()
        conn.close()
        
        return history

class CommitHistoryWindow(tk.Toplevel):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id
        self.history_db = TaskHistoryDB()
        
        # Window setup
        self.title("Task History")
        self.geometry("800x600")
        self.configure(bg="#A9A9A9")
        
        # Fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=16, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=12)
        }
        
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Timeline frame on the left
        timeline_frame = ttk.Frame(self)
        timeline_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ttk.Label(timeline_frame, text="Change History", font=self.fonts['header']).pack(pady=(0, 10))

        # Configure Treeview style
        style = ttk.Style()
        style.configure(
            "Treeview", 
            background="#d3d3d3",
            foreground="black",  # Text color - black for readability
            rowheight=25,
            fieldbackground="#d3d3d3"  # Field background color
        )
        
        # Create timeline list
        self.timeline = ttk.Treeview(timeline_frame, columns=("date",), show="headings", height=20, style = "Treeview")
        self.timeline.heading("date", text="Date & Time")
        self.timeline.column("date", width=150)
        self.timeline.pack(fill="y", expand=True)
        
        # Add a scrollbar for the timeline
        timeline_scroll = ttk.Scrollbar(timeline_frame, orient="vertical", command=self.timeline.yview)
        timeline_scroll.pack(side="right", fill="y")
        self.timeline.configure(yscrollcommand=timeline_scroll.set)
        
        # Details frame on the right
        details_frame = ttk.Frame(self)
        details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Previous state
        prev_frame = ttk.LabelFrame(details_frame, text="Previous State")
        prev_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        self.prev_text = tk.Text(prev_frame, height=10, wrap="word")
        self.prev_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # New state
        new_frame = ttk.LabelFrame(details_frame, text="Changed State")
        new_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        self.new_text = tk.Text(new_frame, height=10, wrap="word")
        self.new_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bind selection event
        self.timeline.bind("<<TreeviewSelect>>", self.on_select_change)

    def load_history(self):
        history = self.history_db.get_task_history(self.task_id)
        
        # Clear existing items
        for item in self.timeline.get_children():
            self.timeline.delete(item)
        
        # Insert history records
        for i, (date, field, old_val, new_val) in enumerate(history):
            self.timeline.insert("", "end", values=(date,), tags=(date, field, old_val, new_val))
        
        # Select the first item if it exists
        if self.timeline.get_children():
            first_item = self.timeline.get_children()[0]
            self.timeline.selection_set(first_item)
            self.timeline.focus(first_item)
            self.on_select_change(None)  # Trigger the selection event

    def on_select_change(self, event):
        selection = self.timeline.selection()
        if not selection:
            return
            
        item = self.timeline.item(selection[0])
        date, field, old_val, new_val = item["tags"]
        
        # Update text widgets
        self.prev_text.delete(1.0, tk.END)
        self.new_text.delete(1.0, tk.END)
        
        self.prev_text.insert(tk.END, f"Date: {date}\nField: {field}\nValue: {old_val}")
        self.new_text.insert(tk.END, f"Date: {date}\nField: {field}\nValue: {new_val}")


class CompletedTasksWindow(tk.Tk):
    def __init__(self, task_name=None, task_weight=None, task_time=None, task_id=None, task_description=None, refresh_callback=None, start_date = None):
        super().__init__()
        self.history_db = TaskHistoryDB()
        self.task_name = task_name
        self.task_weight = task_weight
        self.task_time = task_time
        self.task_id = task_id
        self.task_description = task_description
        self.start_date = start_date
        self.refresh_callback = refresh_callback
        self.commit_history_window = None

        # Font Tuples for Use on pages
        self.fonts = {
            "Title_Tuple": tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            "Body_Tuple": tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            "Description_Tuple": tkfont.Font(family="Sf Pro Text", size=12)
        }

        self.setup_ui()

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

    def cancel_task(self):
        self.destroy(CompletedTasksWindow)

    def load_history_data(self):
        """Load the task history data into the Treeview"""
        # Get history from the database
        history = self.history_db.get_task_history(self.task_id)
        
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items to the Treeview
        for i, (date, field, old_val, new_val) in enumerate(history):
            # Create a summary of the change
            change_summary = f"{old_val} → {new_val}"
            
            # Add to Treeview with alternating row colors
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.history_tree.insert(
                "", "end", 
                values=(date, field, change_summary),
                tags=(tag, date, field, old_val, new_val)  # Store full data in tags for reference
            )
        
        # If there are items, select the first one
        if self.history_tree.get_children():
            first_item = self.history_tree.get_children()[0]
            self.history_tree.selection_set(first_item)
    
    def open_commit_history_page(self):
        """Open a new CommitHistoryWindow with the task's history"""
        if self.task_id:
            # Get the selected item for focused history
            selected = self.history_tree.selection()
            
            if self.commit_history_window is None or not tk.Toplevel.winfo_exists(self.commit_history_window):
                self.commit_history_window = CommitHistoryWindow(self.task_id)
                self.commit_history_window.grab_set()  # Make window modal
                
                # Position the history window relative to this window
                if self.winfo_exists():
                    x = self.winfo_x() + 50
                    y = self.winfo_y() + 50
                    self.commit_history_window.geometry(f"+{x}+{y}")
                
                # If a specific history item is selected, focus on it
                if selected:
                    # Find the corresponding item in the history window
                    selected_date = self.history_tree.item(selected[0])['values'][0]
                    
                    # Find and select the matching item in the new window's timeline
                    for item in self.commit_history_window.timeline.get_children():
                        if self.commit_history_window.timeline.item(item)['values'][0] == selected_date:
                            self.commit_history_window.timeline.selection_set(item)
                            self.commit_history_window.timeline.focus(item)
                            self.commit_history_window.on_select_change(None)  # Trigger update
                            break
            else:
                self.commit_history_window.lift()
                self.commit_history_window.focus_force()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to view its history.")
    
    def search_commit(self, event=None):
        """Search through commit history by date or field changed"""
        history = self.history_db.get_task_history(self.task_id)
        lookup = self.search_entry.get().lower()

        # Clear the existing treeview items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # If search field is empty, show all items
        if lookup == "":
            # Add all history items to the Treeview
            for i, (date, field, old_val, new_val) in enumerate(history):
                # Create a summary of the change
                change_summary = f"{old_val} → {new_val}"
                
                # Add to Treeview with alternating row colors
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.history_tree.insert(
                    "", "end", 
                    values=(date, field, change_summary),
                    tags=(tag, date, field, old_val, new_val)  # Store full data in tags for reference
                )
        else:
            # Search for matching date or field
            matches = []
            for i, (date, field, old_val, new_val) in enumerate(history):
                # Check if the search term is in the date or field (case-insensitive)
                if lookup in date.lower() or lookup in field.lower():
                    matches.append((i, date, field, old_val, new_val))
            
            # Insert matching items
            for i, (index, date, field, old_val, new_val) in enumerate(matches):
                change_summary = f"{old_val} → {new_val}"
                
                # Add to Treeview with alternating row colors
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.history_tree.insert(
                    "", "end", 
                    values=(date, field, change_summary),
                    tags=(tag, date, field, old_val, new_val)
                )

    def setup_ui(self):
        self.geometry("900x500")
        self.title("Task Details")
        self.configure(bg="#A9A9A9")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("Info.TLabel", font=("Arial", 10), background='#A9A9A9')
        self.style.configure("Tag.TLabel", font=("Arial", 8), background='#A9A9A9', padding=2, foreground='black')

        # Task Name Frame
        name_frame = tk.LabelFrame(self, text="Task Name", bg="#dcdcdc")
        name_frame.grid(row=0, column=0, padx=10, pady=10, sticky = "new")
        
        self.name_label = tk.Label(name_frame, text=self.task_name or "No Task Selected", 
                                   font=self.fonts['Body_Tuple'], bg="#dcdcdc")
        self.name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Task ID hidden in name frame for reference
        self.id_hidden = tk.Label(name_frame, text=self.task_id, bg="#dcdcdc")
        self.id_hidden.grid_forget()  # Hide this, just keep as a reference

        # Description Frame
        description_frame = tk.LabelFrame(self, text="Description", bg="#dcdcdc")
        description_frame.grid(row=0, column=0, padx=10, pady=80, sticky = "new")
        
        self.description_scroll = Scrollbar(description_frame)
        self.description_scroll.grid(row=1, column=1, sticky="ns")
        
        self.description_box = Text(description_frame, yscrollcommand=self.description_scroll.set,
                                   height=5, width=40, border=1, font=self.fonts['Description_Tuple'],
                                   background="#dcdcdc")
        self.description_box.grid(row=1, column=0, padx=5, pady=5)
        self.description_box.insert("1.0", self.task_description)
        self.description_scroll.config(command=self.description_box.yview)
        
        # Make description box read-only
        self.description_box.config(state=DISABLED)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Information Frame
        info_frame = tk.LabelFrame(self, text="Information", bg="#dcdcdc")
        info_frame.grid(row=0, column=1, padx=10, pady=10, sticky = "new")
        
        # Information Fields
        time_label = tk.Label(info_frame, text="Task Time:", font=self.fonts['Body_Tuple'], bg="#dcdcdc")
        time_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        time_value = tk.Label(info_frame, text=self.task_time or "00:00:00", 
                              font=self.fonts['Description_Tuple'], bg="#dcdcdc")
        time_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        weight_label = tk.Label(info_frame, text="Task Weight:", font=self.fonts['Body_Tuple'], bg="#dcdcdc")
        weight_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        weight_value = tk.Label(info_frame, text=self.task_weight or "N/A", 
                                font=self.fonts['Description_Tuple'], bg="#dcdcdc")
        weight_value.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        start_date_label = tk.Label(info_frame, text = "Start Date:", font = self.fonts['Body_Tuple'], bg="#dcdcdc")
        start_date_label.grid(row = 2, column = 0)

        start_date_value = tk.Label(info_frame, text = self.start_date or "N/A",
                                    font=self.fonts['Description_Tuple'], bg="#dcdcdc")
        start_date_value.grid(row = 2, column = 1, sticky = "w", padx = 5, pady = 5)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        date_label = tk.Label(info_frame, text="Completion Date:", font=self.fonts['Body_Tuple'], bg="#dcdcdc")
        date_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        date_value = tk.Label(info_frame, text=current_time, 
                              font=self.fonts['Description_Tuple'], bg="#dcdcdc")
        date_value.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        task_id_label = tk.Label(info_frame, text="Task ID:", font=self.fonts['Body_Tuple'], bg="#dcdcdc")
        task_id_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
        task_id_value = tk.Label(info_frame, text=self.task_id or "N/A", 
                                font=self.fonts['Description_Tuple'], bg="#dcdcdc")
        task_id_value.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Commit History Frame

        search_frame = tk.LabelFrame(self, text = "Search bar", bg = "#dcdcdc")
        search_frame.grid(row = 0, column = 0, padx = 10, pady = 235, sticky = "new")

        commit_frame = tk.LabelFrame(self, text="Commit History", bg="#dcdcdc")
        commit_frame.grid(row=0, column=0, padx=10, pady=290, sticky="new")

        btn_frame = tk.LabelFrame(self, text = "Buttons", bg = "#dcdcdc")
        btn_frame.grid(row = 0, column = 1, padx = 10, pady = 290, sticky = "sew")

        complete_btn = tk.Button(btn_frame, text = "Complete", command = self.complete_task,
                                bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                                activebackground="#A8F0A8", activeforeground="#000000")
        complete_btn.grid(row = 0, column = 0, padx = 5, pady= 5, sticky = "e")

        cancel_btn = tk.Button(btn_frame, text = "Cancel", command = self.after_cancel, bg="#F08080", fg="#000000", font=("SF Pro Text", 10),
                               activebackground="#F49797", activeforeground="#000000")
        cancel_btn.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "e")
        #Search bar
        Label(search_frame, text = "Search: ", background= "#dcdcdc").grid(row= 0, column = 0, padx = 5, pady = 5)
        self.search_entry = tk.Entry(search_frame, bg = "#dcdcdc", width = 15)
        self.search_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.search_entry.bind("<KeyRelease>", self.search_commit)
        
        #History Treeview
        history_frame = tk.Frame(commit_frame, bg="#dcdcdc")
        history_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add a scrollbar
        history_scroll = Scrollbar(history_frame)
        history_scroll.pack(side=RIGHT, fill=Y)
        
        # Configure the Treeview
        self.history_tree = ttk.Treeview(
            history_frame,
            yscrollcommand=history_scroll.set,
            selectmode="browse",
            height=6
        )
        self.history_tree.pack(side=LEFT, fill="both", expand=True)
        
        # Configure the Treeview columns
        self.history_tree['columns'] = ("Date", "Field", "Change")
        self.history_tree.column("#0", width=0, stretch=NO)  # Hide the first column
        self.history_tree.column("Date", anchor=W, width=150)
        self.history_tree.column("Field", anchor=W, width=100)
        self.history_tree.column("Change", anchor=W, width=200)
        
        # Configure the headings
        self.history_tree.heading("#0", text="", anchor=W)
        self.history_tree.heading("Date", text="Date & Time", anchor=W)
        self.history_tree.heading("Field", text="Field Changed", anchor=W)
        self.history_tree.heading("Change", text="Change Summary", anchor=W)
        
        # Configure the scrollbar
        history_scroll.config(command=self.history_tree.yview)
        
        # Configure row appearance
        self.history_tree.tag_configure('oddrow', background="#A9A9A9")
        self.history_tree.tag_configure('evenrow', background="#dcdcdc")
        
        # Bind double-click event to open detailed history view
        self.history_tree.bind("<Double-1>", lambda e: self.open_commit_history_page())
        
        # Load history data if we have a task ID
        if self.task_id:
            self.load_history_data()
