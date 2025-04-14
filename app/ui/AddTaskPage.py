from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import pathlib
import sqlite3
from datetime import date
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH, DB_DIR

background_color = "#A9A9A9"
green_btn_color = "#b2fba5"
org_btn_color = "#e99e56"

class AddTaskWindow(tk.Toplevel):
    def __init__(self, main_app):
        # Initialize Toplevel first, then do other operations
        tk.Toplevel.__init__(self, main_app.root)
        
        # Store references
        self.main_app = main_app
        self.main_app.addtask_window = self
        
        # Set the main window properties
        self.title("Add Task")
        self.geometry("500x500")
        self.configure(bg=background_color)
        self.transient(main_app.root)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Define path for main database
        self.path = DB_PATH
        self.tags_path = DB_PATH
        
        # Create global values list for tags
        global values
        values = []
        
        # Create or Connect to the database
        try:
            conn = sqlite3.connect(self.tags_path)
            c = conn.cursor()
            
            # Check if tags table exists
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tags'")
            if not c.fetchone():
                # Create the tags table if it doesn't exist
                c.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    tag_id INTEGER PRIMARY KEY,
                    tag_name TEXT
                )
                """)
                conn.commit()
            
            c.execute("SELECT tag_name FROM tags")  # Fetch tag_names from tag database
            tags = c.fetchall()
            
            # Add data to the list
            for tag in tags:
                values.append(tag[0])

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to tags database: {e}")
        finally:
            # Close connection to the database
            if 'conn' in locals():
                conn.close()

        # Create fonts with fallbacks - MUST use simple tuples for Linux compatibility
        self.fonts = {
            'header': ('Arial', 18, 'bold'),
            'subheader': ('Arial', 12, 'bold'),
            'body': ('Arial', 12)
        }

        # Create the main content frame
        main_frame = tk.Frame(self, bg=background_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Task Name label and entry
        task_name_frame = tk.Frame(main_frame, bg=background_color)
        task_name_frame.pack(fill="x", pady=5)
        
        tk.Label(task_name_frame, text="Task Name:", font=self.fonts['subheader'], 
                bg=background_color).pack(side="left")
                
        self.task_name_entry = tk.Entry(task_name_frame, bg="#d3d3d3", width=40)
        self.task_name_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Create a frame for main content with two columns
        content_frame = tk.Frame(main_frame, bg=background_color)
        content_frame.pack(fill="both", expand=True, pady=5)
        
        # Left column
        left_frame = tk.Frame(content_frame, bg=background_color)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Description label and text area
        tk.Label(left_frame, text="Description:", font=self.fonts['subheader'], 
               bg=background_color).pack(anchor="w")
               
        desc_frame = tk.Frame(left_frame, bg=background_color)
        desc_frame.pack(fill="both", expand=True, pady=5)
        
        desc_scroll = tk.Scrollbar(desc_frame)
        desc_scroll.pack(side="right", fill="y")
        
        self.desc_text = tk.Text(desc_frame, height=7, width=30, bg="#d3d3d3", 
                               relief="solid", bd=1, yscrollcommand=desc_scroll.set)
        self.desc_text.pack(side="left", fill="both", expand=True)
        desc_scroll.config(command=self.desc_text.yview)
        
        # Time Complexity
        tk.Label(left_frame, text="Time Complexity:", font=self.fonts['subheader'], 
               bg=background_color).pack(anchor="w", pady=(10, 0))
               
        complexity_frame = tk.Frame(left_frame, bg=background_color)
        complexity_frame.pack(fill="x", pady=5)
        
        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]
        
        self.type_combo = ttk.Combobox(complexity_frame, values=self.complexity_types, state='readonly')
        self.type_combo.pack(fill="x", pady=(0, 3))
        self.type_combo.set("Select Type")
        
        self.value_combo = ttk.Combobox(complexity_frame, state='readonly')
        self.value_combo.pack(fill="x")
        self.value_combo.set("Select Value")
        
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)
        
        # Date field
        tk.Label(left_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], 
               bg=background_color).pack(anchor="w", pady=(10, 0))
               
        self.date_entry = tk.Entry(left_frame, bg="#d3d3d3")
        self.date_entry.pack(fill="x", pady=5)
        
        # Right column for tags
        right_frame = tk.Frame(content_frame, bg=background_color)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Tags section
        tk.Label(right_frame, text="Task Tags:", font=self.fonts['subheader'], 
               bg=background_color).pack(anchor="w")
               
        tag_frame = tk.Frame(right_frame, bg=background_color)
        tag_frame.pack(fill="x", pady=5)
        
        tag_scroll = tk.Scrollbar(tag_frame)
        tag_scroll.pack(side="right", fill="y")
        
        self.tag_text = tk.Text(tag_frame, height=7, width=20, bg="#d3d3d3", 
                              relief="solid", bd=1, yscrollcommand=tag_scroll.set)
        self.tag_text.pack(side="left", fill="both", expand=True)
        tag_scroll.config(command=self.tag_text.yview)
        
        # Choose tags section
        tk.Label(right_frame, text="Choose Tags:", font=self.fonts['subheader'], 
               bg=background_color).pack(anchor="w", pady=(10, 0))
               
        listbox_frame = tk.Frame(right_frame, bg=background_color)
        listbox_frame.pack(fill="x", pady=5)
        
        list_scroll = tk.Scrollbar(listbox_frame)
        list_scroll.pack(side="right", fill="y")
        
        self.tag_listbox = tk.Listbox(listbox_frame, selectmode="multiple", bg="#d3d3d3",
                                    relief="solid", yscrollcommand=list_scroll.set, 
                                    exportselection=0, height=8)
        self.tag_listbox.pack(side="left", fill="both", expand=True)
        list_scroll.config(command=self.tag_listbox.yview)
        
        # Bind tag selection to update tag text
        self.tag_listbox.bind("<<ListboxSelect>>", lambda _: self.update_tag_entry())
        
        # Add tags to listbox
        for value in values:
            self.tag_listbox.insert(tk.END, value)
        
        # Buttons frame at the bottom
        button_frame = tk.Frame(main_frame, bg=background_color)
        button_frame.pack(fill="x", pady=10)
        
        # Buttons with consistent width
        button_width = 10
        
        confirm_btn = tk.Button(button_frame, text="Confirm", width=button_width, 
                              bg=green_btn_color, command=self.confirm_action)
        confirm_btn.pack(side="left", padx=(0, 5))
        
        cancel_btn = tk.Button(button_frame, text="Cancel", width=button_width, 
                             bg=org_btn_color, command=self.cancel_action)
        cancel_btn.pack(side="left", padx=5)
        
        autofill_date_btn = tk.Button(button_frame, text="Autofill date", width=button_width, 
                                    bg="#E39ff6", command=self.autofill_date)
        autofill_date_btn.pack(side="left", padx=5)
        
        # Set initial focus
        self.task_name_entry.focus_set()

    def update_values(self, event=None):
        selected_type = self.type_combo.get()
        if selected_type == "T-Shirt Size":
            self.value_combo['values'] = self.tshirt_sizes
        elif selected_type == "Fibonacci":
            self.value_combo['values'] = self.fibonacci
        else:
            self.value_combo['values'] = []
        self.value_combo.set("Select Value")

    def cancel_action(self):
        self.on_close()

    def update_tag_entry(self):
        # Get selected values from the Listbox widget
        selected_values = [self.tag_listbox.get(idx) for idx in self.tag_listbox.curselection()]

        # Update with the selected values
        self.tag_text.delete(1.0, "end")  # Clear the Text widget
        self.tag_text.insert("1.0", "\n".join(selected_values))  # Insert the selected tags

    def confirm_action(self):
        task_name = self.task_name_entry.get()

        # Check task name length
        if len(task_name) > 45:
            messagebox.showwarning("Warning", "Task name cannot exceed 45 characters.")
            self.task_name_entry.delete(0, tk.END)  # Clear task name field
            self.lift()
            self.focus_force()
            return  # Stop further execution
        
        description = self.desc_text.get("1.0", tk.END).strip()
        tags = self.tag_text.get("1.0", tk.END).strip()
        complexity_type = self.type_combo.get()
        complexity_value = self.value_combo.get()
        start_date = self.date_entry.get()
        task_time = "00:00:00" 
        end_date = "01-02-2025"

        # Store required fields in a dictionary or list
        check_field = {
            "TaskName": task_name,
            "Start Date": start_date,
            "Complexity Type": complexity_type,
            "Complexity Value": complexity_value
        }

        # Check if any required field is empty and show a warning if so
        missing_fields = [field for field, value in check_field.items() if not value or value == "Select Value" or value == "Select Type"]
        
        if missing_fields:
            missing_fields_str = ", ".join(missing_fields)
            messagebox.showwarning("Warning", f"Please fill in the following required fields: {missing_fields_str}")
            self.lift()
            self.focus_force()
            
            # Stop further action if any field is missing
            return
            
        # Pattern for Date
        pattern = r"^(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])-(19|20)\d{2}$"
        if not re.match(pattern, start_date):
            messagebox.showwarning("Warning", f"The Start Date you have is invalid")
            self.lift()
            self.focus_force()
            return
        
        # Check tags if there are any
        if tags:
            res = tags.split('\n')  # Splits the string to check tags
            
            # Make sure values is defined and includes empty string
            global values
            if not hasattr(globals(), 'values') or values is None:
                values = [""]
            elif "" not in values:
                values.append("")
                
            if not all(tag in values for tag in res):  # Checks to see if tags are in the accepted tags
                messagebox.showwarning("Warning", f"The Tags you have selected are invalid")
                self.lift()
                self.focus_force()
                return
                
        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Add", "Are you sure you want to add this task?")
            
        # Adds task
        if confirm:
            try:
                # Connect to the database
                conn = sqlite3.connect(self.path)
                c = conn.cursor()

                # Get the highest task ID from all tables
                c.execute("SELECT MAX(task_id) FROM TaskList")
                max_tasklist_id = c.fetchone()[0]
                max_tasklist_id = max_tasklist_id if max_tasklist_id is not None else 0

                c.execute("SELECT MAX(task_id) FROM CompletedTasks")
                max_completed_id = c.fetchone()[0]
                max_completed_id = max_completed_id if max_completed_id is not None else 0

                c.execute("SELECT MAX(task_id) FROM CurrentTask")
                current_task_id = c.fetchone()[0]
                current_task_id = current_task_id if current_task_id is not None else 0

                # Find the next task_id (1 + max of all task lists)
                task_id = max(max_tasklist_id, max_completed_id, current_task_id) + 1

                # Then for list_place, explicitly check if this is a new task or a restored task
                # If it's a new task, use the highest list_place + 1
                c.execute("SELECT COALESCE(MAX(list_place), 0) FROM TaskList")
                max_list_place = c.fetchone()[0] or 0
                list_place = max(task_id, max_list_place + 1)

                # Insert data
                c.execute(
                    "INSERT INTO TaskList VALUES(:task_name, :task_time, :task_weight, :task_id, :task_start_date, :task_end_date, :task_description, :task_weight_type, :task_tags, :list_place)",
                    {
                        "task_name": task_name,
                        "task_time": task_time,
                        "task_weight": complexity_value,
                        "task_id": task_id,
                        "task_start_date": start_date,
                        "task_end_date": end_date,
                        "task_description": description,
                        "task_weight_type": complexity_type,
                        "task_tags": tags,
                        "list_place": list_place
                    }
                )

                conn.commit()
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error adding task: {e}")
                return
            finally:
                conn.close()
            
            # Refresh the main app's task list
            if hasattr(self.main_app, 'query_database'):
                self.main_app.query_database()

            self.destroy()
            
        else:
            return

    def autofill_date(self):
        CurrentDate = date.today()
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, CurrentDate.strftime("%m-%d-%Y"))

    def on_close(self):
        self.main_app.addtask_window = None  # Reset reference to allow reopening
        self.main_app.add_button.config(state=tk.NORMAL)
        self.destroy()

# Don't run as standalone module
# if __name__ == "__main__":
#     app = AddTaskWindow(None)
#     app.mainloop()