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
path = str(path).replace("CompletedTaskDetailsPage.py", '') + '\\Databases' + '\\task_list.db'


bad_btn = "#e99e56"
good_btn = "#77DD77"
bg_color = "#A9A9A9"
frame_color = "#dcdcdc"

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
        
    def get_specific_history_entry(self, task_id, date, field):
        """Get a specific history entry based on task_id, date, and field"""
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        
        c.execute("""
            SELECT change_date, field_changed, old_value, new_value
            FROM task_history
            WHERE task_id = ? AND change_date = ? AND field_changed = ?
        """, (task_id, date, field))
        
        entry = c.fetchone()
        conn.close()
        
        return entry
class CommitHistoryWindow(tk.Toplevel):
    def __init__(self, task_id, compFlag, selected_date=None, selected_field=None):
        super().__init__()
        self.task_id = task_id
        self.selected_date = selected_date
        self.selected_field = selected_field
        self.history_db = TaskHistoryDB()
        self.compFlag = compFlag
        
        # Window setup
        self.title("Task History")
        self.geometry("800x480")
        self.configure(bg="#A9A9A9")
        self.resizable(width=0, height=0)
        
        # Fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=16, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=12)
        }
        
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self, bg="#A9A9A9")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top section for timeline
        top_frame = tk.Frame(main_container, bg="#A9A9A9")
        top_frame.pack(fill="x", padx=5, pady=5)
        
        # Timeline list with scrollbar
        timeline_frame = tk.Frame(top_frame, bg="#A9A9A9")
        timeline_frame.pack(fill="x", expand=True)
        
        timeline_scroll = ttk.Scrollbar(timeline_frame, orient="horizontal")
        timeline_scroll.pack(side="bottom", fill="x")
        
        self.timeline = ttk.Treeview(
            timeline_frame, 
            columns=("date", "field"), 
            show="headings", 
            height=6, 
            xscrollcommand=timeline_scroll.set
        )
        self.timeline.heading("date", text="Date & Time")
        self.timeline.heading("field", text="Field Changed")
        self.timeline.column("date", width=150)
        self.timeline.column("field", width=150)
        self.timeline.pack(fill="x", expand=True)
        
        timeline_scroll.config(command=self.timeline.xview)
        
        # Bottom frame to hold the comparison panels
        bottom_frame = tk.Frame(main_container, bg="#A9A9A9")
        bottom_frame.pack(fill="both", expand=True, pady=1)
        
        # Configure the grid for even spacing
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        
        # Two main panels for comparison
        # Previous state panel
        self.previous_panel = tk.LabelFrame(bottom_frame, text="Previous State", 
                                       font=self.fonts['subheader'],
                                       bg="#d3d3d3", fg="#000000")
        self.previous_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # New state panel
        self.new_panel = tk.LabelFrame(bottom_frame, text="Changed State", 
                                   font=self.fonts['subheader'],
                                   bg="#d3d3d3", fg="#000000")
        self.new_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Create sub-frames for each panel
        self.setup_panel_content(self.previous_panel, "previous")
        self.setup_panel_content(self.new_panel, "new")
        
        # Close button at bottom
        close_btn = tk.Button(main_container, text="Close", 
                           command=self.destroy,
                           bg=bad_btn, fg="#000000", 
                           font=self.fonts['body'])
        close_btn.pack(side = RIGHT, pady=1)
        
        # Bind timeline selection event
        self.timeline.bind("<<TreeviewSelect>>", self.on_select_change)

        self.timeline.pack_forget()
        timeline_scroll.pack_forget()
    
    def setup_panel_content(self, parent_frame, panel_type):
        """Create the sub-frames within each panel"""
        # Date sub-frame
        date_frame = tk.LabelFrame(parent_frame, text="Date", 
                                bg="#d3d3d3", fg="#000000",
                                font=self.fonts['subheader'])
        date_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Date value label
        if panel_type == "previous":
            self.prev_date_value = tk.Label(date_frame, text="", 
                                       font=self.fonts['body'], 
                                       bg="#d3d3d3", wraplength=300)
            self.prev_date_value.pack(fill="x", padx=10, pady=5)
        else:
            self.new_date_value = tk.Label(date_frame, text="", 
                                      font=self.fonts['body'], 
                                      bg="#d3d3d3", wraplength=300)
            self.new_date_value.pack(fill="x", padx=10, pady=5)
        
        # Field sub-frame
        field_frame = tk.LabelFrame(parent_frame, text="Field Changed", 
                                 bg="#d3d3d3", fg="#000000",
                                 font=self.fonts['subheader'])
        field_frame.pack(fill="x", padx=10, pady=5)
        
        # Field value label
        if panel_type == "previous":
            self.prev_field_value = tk.Label(field_frame, text="", 
                                        font=self.fonts['body'], 
                                        bg="#d3d3d3", wraplength=300)
            self.prev_field_value.pack(fill="x", padx=10, pady=5)
        else:
            self.new_field_value = tk.Label(field_frame, text="", 
                                       font=self.fonts['body'], 
                                       bg="#d3d3d3", wraplength=300)
            self.new_field_value.pack(fill="x", padx=10, pady=5)
        
        # Value sub-frame (using text widget for scrollable content)
        value_frame = tk.LabelFrame(parent_frame, text="Value", 
                                 bg="#d3d3d3", fg="#000000",
                                 font=self.fonts['subheader'])
        value_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add scrollbars
        scroll_y = ttk.Scrollbar(value_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        # Value text widget
        if panel_type == "previous":
            self.prev_value_text = tk.Text(value_frame, height=10, width=30,
                                      wrap="none", bg="#e0e0e0",
                                      font=self.fonts['body'],
                                      yscrollcommand=scroll_y.set)
            self.prev_value_text.pack(fill="both", expand=True, padx=5, pady=5)
            scroll_y.config(command=self.prev_value_text.yview)
            self.prev_value_text.config(state="disabled")
        else:
            self.new_value_text = tk.Text(value_frame, height=10, width=30,
                                     wrap="none", bg="#e0e0e0",
                                     font=self.fonts['body'],
                                     yscrollcommand=scroll_y.set)
            self.new_value_text.pack(fill="both", expand=True, padx=5, pady=5)
            scroll_y.config(command=self.new_value_text.yview)
            self.new_value_text.config(state="disabled")

    def load_history(self):
        history = self.history_db.get_task_history(self.task_id)
        
        # Clear existing items
        for item in self.timeline.get_children():
            self.timeline.delete(item)
        
        # Insert history records
        for i, (date, field, old_val, new_val) in enumerate(history):
            item_id = self.timeline.insert("", "end", values=(date, field), tags=(date, field, old_val, new_val))
            
            # If this is the selected date and field, store the item_id
            if (self.selected_date and date == self.selected_date and 
                self.selected_field and field == self.selected_field):
                self.selected_item_id = item_id
            # If only date is specified, still select it
            elif self.selected_date and date == self.selected_date and not self.selected_field:
                self.selected_item_id = item_id
        
        # Select the appropriate item
        if hasattr(self, 'selected_item_id'):
            # Select the item that matches the selected date and field
            self.timeline.selection_set(self.selected_item_id)
            self.timeline.focus(self.selected_item_id)
            self.timeline.see(self.selected_item_id)  # Ensure it's visible
            self.on_select_change(None)  # Trigger the selection event
        elif self.timeline.get_children():
            # Otherwise select the first item if it exists
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
        
        # Update date values
        self.prev_date_value.config(text=date)
        self.new_date_value.config(text=date)
        
        # Update field values
        self.prev_field_value.config(text=field)
        self.new_field_value.config(text=field)
        
        # Update value text widgets (must enable first, then disable after)
        self.prev_value_text.config(state="normal")
        self.prev_value_text.delete(1.0, tk.END)
        self.prev_value_text.insert(tk.END, old_val)
        self.prev_value_text.config(state="disabled")
        
        self.new_value_text.config(state="normal")
        self.new_value_text.delete(1.0, tk.END)
        self.new_value_text.insert(tk.END, new_val)
        self.new_value_text.config(state="disabled")

class CompletedTaskDetailsWindow(tk.Toplevel):
    def __init__(self, compFlag, task_id=None, parent=None):
        super().__init__(parent)
        self.compFlag = compFlag
        self.task_id = task_id
        self.parent = parent
        self.commit_history_window = None
        
        # Font Tuples for Use on pages
        self.fonts = {
            "Title_Tuple": tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            "Body_Tuple": tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            "Description_Tuple": tkfont.Font(family="Sf Pro Text", size=12)
        }

        # Load task data
        self.load_task_data()
        
        # Setup UI
        self.setup_ui()

        self.resizable(width=0, height=0)
        
        # Protocol handler for closing window
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_task_data(self):
        """Load task data from database"""
        if not self.task_id:
            return
            
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            if self.compFlag == 0:  # 0 for MainPage, 1 for completed tasks page, 2 for current task page
                c.execute("SELECT * FROM CompletedTasks WHERE task_id = ?", (self.task_id,))
                task = c.fetchone()
                print(task)
                if task:
                    self.task_name = task[0]
                    self.task_time = task[1]
                    self.task_weight = task[2]
                    self.completion_date = task[4]
                    self.total_duration = task[5]
                    self.start_date = task[6] if len(task) > 6 else None
                    self.task_tags = task[7] if len(task) > 7 else None
                    self.task_weight_type = task[8] if len(task) > 8 else None
                    self.task_description = task[9] if len(task) > 9 else ""
                else:
                    self.task_name = "Task Not Found"
                    self.task_time = "00:00:00"
                    self.task_weight = "N/A"
                    self.completion_date = "N/A"
                    self.total_duration = "00:00:00"
                    self.start_date = "N/A"
                    self.task_tags = ""
                    self.task_weight_type = "N/A"
                    self.task_description = "Task details could not be loaded."
            elif self.compFlag == 1:
                c.execute("SELECT * FROM TaskList WHERE task_id = ?", (self.task_id,))
                task = c.fetchone()
                print(task)
                if task:
                    self.task_name = task[0]
                    self.task_time = task[1]
                    self.task_weight = task[2]
                    self.completion_date = "Not applicable"
                    self.total_duration = task[5]
                    # self.start_date = task[6] if len(task) > 6 else None
                    self.start_date = task[4]
                    self.task_tags = task[8] if len(task) > 8 else None
                    self.task_weight_type = task[7] if len(task) > 7 else None
                    self.task_description = task[6] if len(task) > 6 else ""
                else:
                    self.task_name = "Task Not Found"
                    self.task_time = "00:00:00"
                    self.task_weight = "N/A"
                    self.completion_date = "N/A"
                    self.total_duration = "00:00:00"
                    self.start_date = "N/A"
                    self.task_tags = ""
                    self.task_weight_type = "N/A"
                    self.task_description = "Task details could not be loaded."
            elif self.compFlag == 2:
                c.execute("SELECT * FROM CurrentTask WHERE task_id = ?", (self.task_id,))
                task = c.fetchone()
                print(task)
                if task:
                    self.task_name = task[0]
                    self.task_time = task[1]
                    self.task_weight = task[2]
                    self.completion_date = "Not applicable"
                    self.total_duration = task[5]
                    # self.start_date = task[6] if len(task) > 6 else None
                    self.start_date = task[4]
                    self.task_tags = task[8] if len(task) > 8 else None
                    self.task_weight_type = task[7] if len(task) > 7 else None
                    self.task_description = task[6] if len(task) > 6 else ""
                else:
                    self.task_name = "Task Not Found"
                    self.task_time = "00:00:00"
                    self.task_weight = "N/A"
                    self.completion_date = "N/A"
                    self.total_duration = "00:00:00"
                    self.start_date = "N/A"
                    self.task_tags = ""
                    self.task_weight_type = "N/A"
                    self.task_description = "Task details could not be loaded."
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.task_name = "Error Loading Task"
            self.task_time = "00:00:00"
            self.task_weight = "N/A"
            self.completion_date = "N/A"
            self.total_duration = "00:00:00"
            self.start_date = "N/A"
            self.task_tags = ""
            self.task_weight_type = "N/A"
            self.task_description = f"Error loading task details: {str(e)}"
        finally:
            conn.close()

    def on_close(self):
        """Handle window close event"""
        self.destroy()

    def open_commit_history_page(self):
        """Open a new CommitHistoryWindow with the task's history"""
        if self.task_id:
            # Get the selected item for focused history
            selected = self.history_tree.selection()
            selected_date = None
            selected_field = None
            
            if selected:
                # Get the date and field from the selected item
                selected_values = self.history_tree.item(selected[0])['values']
                if len(selected_values) >= 2:
                    selected_date = selected_values[0]  # Date is at index 0
                    selected_field = selected_values[1]  # Field is at index 1
            
            if self.commit_history_window is None or not tk.Toplevel.winfo_exists(self.commit_history_window):
                # Pass the selected date AND field to the CommitHistoryWindow
                self.commit_history_window = CommitHistoryWindow(
                    self.task_id, 
                    selected_date, 
                    selected_field
                )
                self.commit_history_window.grab_set()  # Make window modal
                
                # Position the history window relative to this window
                if self.winfo_exists():
                    x = self.winfo_x() + 50
                    y = self.winfo_y() + 50
                    self.commit_history_window.geometry(f"+{x}+{y}")
            else:
                # If window already exists, bring it to front and update selected item if needed
                self.commit_history_window.lift()
                self.commit_history_window.focus_force()
                
                # If a different item is selected, update the CommitHistoryWindow
                if selected and selected_date:
                    # Update the selected properties
                    self.commit_history_window.selected_date = selected_date
                    self.commit_history_window.selected_field = selected_field
                    # Reload history with the new selection
                    self.commit_history_window.load_history()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to view its history.")

    def load_history_data(self):
        """Load the task history data into the Treeview"""
        from .TaskHistory import TaskHistoryDB
        
        history_db = TaskHistoryDB()
        history = history_db.get_task_history(self.task_id)
        
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
                tags=(tag, date, field, old_val, new_val)
            )
        
        # If there are items, select the first one
        if self.history_tree.get_children():
            first_item = self.history_tree.get_children()[0]
            self.history_tree.selection_set(first_item)

    def on_history_select(self, event):
        """Handle selection in the history tree"""
        selected = self.history_tree.selection()
        if selected:
            # Get the date, field, and values from the selected item
            item = self.history_tree.item(selected[0])
            date, field, old_val, new_val = item["tags"][1:5]  # Skip the 'oddrow'/'evenrow' tag
            
            # Highlight the selected row
            self.history_tree.focus(selected[0])

    def search_commit(self, event=None):
        """Search through commit history by date or field changed"""
        from .TaskHistory import TaskHistoryDB
        
        history_db = TaskHistoryDB()
        history = history_db.get_task_history(self.task_id)
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
                    tags=(tag, date, field, old_val, new_val)
                )
        else:
            # Search for matching date or field or values
            matches = []
            for i, (date, field, old_val, new_val) in enumerate(history):
                # Check if the search term is in the date, field, or values (case-insensitive)
                if (lookup in date.lower() or 
                    lookup in field.lower() or 
                    lookup in old_val.lower() or 
                    lookup in new_val.lower()):
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
        self.geometry("900x520")
        self.title("Task Details")
        self.configure(bg="#A9A9A9")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("Info.TLabel", font=("Arial", 10), background='#A9A9A9')
        self.style.configure("Tag.TLabel", font=("Arial", 8), background='#A9A9A9', padding=2, foreground='black')
        
        # Configure the Treeview style to match the gray background
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                            background="#e0e0e0",
                            fieldbackground="#e0e0e0")
        self.style.map('Treeview',
                    background=[('selected', '#4a6984')],
                    foreground=[('selected', 'white')])

        # Configure main layout - 2 columns, 2 rows
        self.grid_columnconfigure(0, weight=1)  # Left side
        self.grid_columnconfigure(1, weight=1)  # Right side
        self.grid_rowconfigure(0, weight=10)    # Main content area
        self.grid_rowconfigure(1, weight=1)     # Button area at bottom

        # ===== LEFT SIDE =====
        left_frame = tk.Frame(self, bg="#A9A9A9")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure left frame grid
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)  # Task name
        left_frame.grid_rowconfigure(1, weight=2)  # Info section
        left_frame.grid_rowconfigure(2, weight=6)  # Description section

        # Task Name Frame
        name_frame = tk.LabelFrame(left_frame, text="Task Name", bg="#e0e0e0")
        name_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")
        
        self.name_label = tk.Label(name_frame, text=self.task_name or "No Task Selected", 
                                  font=self.fonts['Body_Tuple'], bg="#e0e0e0")
        self.name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Task ID hidden in name frame for reference
        self.id_hidden = tk.Label(name_frame, text=self.task_id, bg="#e0e0e0")
        self.id_hidden.grid_forget()  # Hide this, just keep as a reference

        # Information Frame
        info_frame = tk.LabelFrame(left_frame, text="Information", bg="#e0e0e0")
        info_frame.grid(row=1, column=0, padx=5, pady=5, sticky="new")
        
        # Information Fields
        time_label = tk.Label(info_frame, text="Task Time:", font=self.fonts['Body_Tuple'], bg="#e0e0e0")
        time_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        time_value = tk.Label(info_frame, text=self.task_time or "00:00:00", 
                             font=self.fonts['Description_Tuple'], bg="#e0e0e0")
        time_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        weight_label = tk.Label(info_frame, text="Task Weight:", font=self.fonts['Body_Tuple'], bg="#e0e0e0")
        weight_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        weight_value = tk.Label(info_frame, text=self.task_weight or "N/A", 
                               font=self.fonts['Description_Tuple'], bg="#e0e0e0")
        weight_value.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        start_date_label = tk.Label(info_frame, text="Start Date:", font=self.fonts['Body_Tuple'], bg="#e0e0e0")
        start_date_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        start_date_value = tk.Label(info_frame, text=self.start_date or "N/A",
                                   font=self.fonts['Description_Tuple'], bg="#e0e0e0")
        start_date_value.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        date_label = tk.Label(info_frame, text="Completion Date:", font=self.fonts['Body_Tuple'], bg="#e0e0e0")
        date_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        date_value = tk.Label(info_frame, text=self.completion_date, 
                             font=self.fonts['Description_Tuple'], bg="#e0e0e0")
        date_value.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        task_id_label = tk.Label(info_frame, text="Task ID:", font=self.fonts['Body_Tuple'], bg="#e0e0e0")
        task_id_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
        task_id_value = tk.Label(info_frame, text=self.task_id or "N/A", 
                                font=self.fonts['Description_Tuple'], bg="#e0e0e0")
        task_id_value.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Description Frame
        description_frame = tk.LabelFrame(left_frame, text="Description", bg="#e0e0e0")
        description_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        # Make the description frame expandable
        description_frame.grid_columnconfigure(0, weight=1)
        description_frame.grid_rowconfigure(1, weight=1)
        
        self.description_scroll = Scrollbar(description_frame)
        self.description_scroll.grid(row=1, column=1, sticky="ns")
        
        self.description_box = Text(description_frame, yscrollcommand=self.description_scroll.set,
                                  height=5, width=40, border=1, font=self.fonts['Description_Tuple'],
                                  background="#e0e0e0")
        self.description_box.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.description_box.insert("1.0", self.task_description)
        self.description_scroll.config(command=self.description_box.yview)
        
        # Make description box read-only
        self.description_box.config(state=DISABLED)

        # ===== RIGHT SIDE =====
        right_frame = tk.Frame(self, bg="#A9A9A9")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configure right frame grid
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)  # Search bar
        right_frame.grid_rowconfigure(1, weight=9)  # Commit history

        # Search Frame
        search_frame = tk.LabelFrame(right_frame, text="Search bar", bg="#e0e0e0")
        search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")
        
        Label(search_frame, text="Search:", background="#e0e0e0").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(search_frame, bg="#e0e0e0", width=25)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.search_commit)

        # Commit History Frame
        commit_frame = tk.LabelFrame(right_frame, text="Commit History", bg="#e0e0e0")
        commit_frame.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")
        
        # Make the commit frame expandable
        commit_frame.grid_columnconfigure(0, weight=1)
        commit_frame.grid_rowconfigure(0, weight=1)
        
        # History Treeview
        history_frame = tk.Frame(commit_frame, bg="#e0e0e0")
        history_frame.pack(fill="both", expand = True, padx=5, pady=5)
        
        # Add a scrollbar
        history_scroll = Scrollbar(history_frame)
        history_scroll.pack(side=RIGHT, fill=Y)
        
        # Configure the Treeview
        self.history_tree = ttk.Treeview(
            history_frame,
            yscrollcommand=history_scroll.set,
            selectmode="browse",
            height=15
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
        self.history_tree.tag_configure('oddrow', background="#d0d0d0")  # Darker gray for odd rows
        self.history_tree.tag_configure('evenrow', background="#e0e0e0")  # Light gray for even rows
        
        # Bind double-click event to open detailed history view
        self.history_tree.bind("<Double-1>", lambda e: self.open_commit_history_page())
        
        # ===== BUTTON AREA =====
        btn_frame = tk.Frame(self, bg="#A9A9A9")
        btn_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky="sew")
        
        # Configure for right-aligned buttons
        btn_frame.grid_columnconfigure(0, weight=1)  # Spacer that pushes buttons right
        btn_frame.grid_columnconfigure(1, weight=0)  # Complete button
        btn_frame.grid_columnconfigure(2, weight=0)  # Cancel button

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.destroy,
                             bg=bad_btn, fg="#000000", font=("SF Pro Text", 10),
                             activebackground="#F49797", activeforeground="#000000",
                             width=10)
        cancel_btn.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="e")
        
        # Load history data if we have a task ID
        if self.task_id:
            self.load_history_data()
