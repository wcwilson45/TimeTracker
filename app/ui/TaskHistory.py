import sqlite3
from datetime import datetime
import pathlib
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class TaskHistoryDB:
    def __init__(self):
        self.path = pathlib.Path(__file__).parent
        self.path = str(self.path).replace("TaskHistory.py", '') + '\\Databases' + '\\task_list.db'
        
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
        
        # Create timeline list
        self.timeline = ttk.Treeview(timeline_frame, columns=("date",), show="headings", height=20)
        self.timeline.heading("date", text="Date")
        self.timeline.column("date", width=150)
        self.timeline.pack(fill="y", expand=True)
        
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
        for date, field, old_val, new_val in history:
            self.timeline.insert("", "end", values=(date,), tags=(date, field, old_val, new_val))

    def on_select_change(self, event):
        selection = self.timeline.selection()
        if not selection:
            return
            
        item = self.timeline.item(selection[0])
        date, field, old_val, new_val = item["tags"]
        
        # Update text widgets
        self.prev_text.delete(1.0, tk.END)
        self.new_text.delete(1.0, tk.END)
        
        self.prev_text.insert(tk.END, f"Field: {field}\nValue: {old_val}")
        self.new_text.insert(tk.END, f"Field: {field}\nValue: {new_val}")
