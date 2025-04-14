from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
import csv
from tkinter import messagebox
from config import DB_PATH, COLORS, FONTS
import pathlib
import os
from datetime import datetime
from .TaskHistory import TaskHistoryDB
from .CommitHistoryPage import CommitHistoryWindow
from .CompletedTaskDetailsPage import CompletedTaskDetailsWindow

# Use DB_PATH directly - no need to redefine
path = DB_PATH

# Get colors from config
background_color = COLORS["background_color"]
grey_button_color = COLORS["grey_button_color"]
green_button_color = COLORS["green_button_color"]
red_button_color = COLORS["red_button_color"]
scroll_trough_color = COLORS["scroll_trough_color"]
main_btn_color = COLORS["main_btn_color"]
del_btn_color = COLORS["del_btn_color"]

class CompletedTasksList(tk.Frame):
    def __init__(self, parent, main_app, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.current_sort_reverse = False
        self.history_db = TaskHistoryDB()
        self.commithistory_window = None
        self.task_details_window = None
        self.configure(background=background_color)
        self.main_app = main_app

        # Create main container
        self.main_container = tk.Frame(self, bg=background_color)
        self.main_container.pack(fill="both", expand=True)

        # Left side - Tasks list
        self.tasks_frame = tk.Frame(self.main_container, bg=background_color)
        self.tasks_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Configure Treeview style
        style = ttk.Style()
        try:
            style.theme_use('clam')  # Better for Linux
        except:
            style.theme_use('default')  # Fallback
            
        style.configure("Treeview",
                    background=grey_button_color,
                    foreground="black",
                    rowheight=25,
                    fieldbackground=grey_button_color)
        style.map("Treeview", background=[('selected', "#347083")])

        # Create Treeview for completed tasks
        completedlist_frame = tk.Frame(self.tasks_frame, bg=background_color)
        completedlist_frame.pack(fill="both", expand=True)

        completedlist_scroll = ttk.Scrollbar(completedlist_frame)
        completedlist_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the completed tasks list
        self.completed_list = ttk.Treeview(completedlist_frame,
                                       yscrollcommand=completedlist_scroll.set,
                                       selectmode="extended",
                                       height=13)
        self.completed_list.pack(fill="both", expand=True)

        completedlist_scroll.config(command=self.completed_list.yview)

        # Configure columns
        self.completed_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID",
                                      "Completion Date", "Total Duration")

        self.completed_list.column("#0", width=0, stretch=tk.NO)
        self.completed_list.column('Task Name', anchor=tk.W, width=140)
        self.completed_list.column('Task Time', anchor=tk.CENTER, width=77)
        self.completed_list.column('Task Weight', anchor=tk.CENTER, width=77)
        self.completed_list.column('Task ID', anchor=tk.CENTER, width=0,stretch=tk.NO)
        self.completed_list.column('Completion Date', anchor=tk.CENTER, width=140)
        self.completed_list.column('Total Duration', anchor=tk.CENTER, width=110)

        # Configure headings
        for col in self.completed_list['columns']:
            self.completed_list.heading(col, text=col, anchor=tk.CENTER,
                                    command=lambda c=col: self.sort_completed_tasks(c))

        self.completed_list.tag_configure('oddrow', background="white")
        self.completed_list.tag_configure('evenrow', background=grey_button_color)

        # Bind double-click to open task details
        self.completed_list.bind("<Double-1>", self.open_task_details)

        # Right side - History view
        self.history_frame = tk.Frame(self.main_container, bg=background_color, width=400)
        self.history_frame.pack(side="right", fill="both", padx=5, pady=5)
        
        # Get available fonts
        avail_fonts = tkfont.families()
        title_font = "SF Pro Display" if "SF Pro Display" in avail_fonts else "Arial"
        
        # History title
        self.history_title = tk.Label(self.history_frame, 
                                    text="Task History", 
                                    font=(title_font, 14, "bold"),
                                    bg=background_color)
        self.history_title.pack(pady=(0, 5))

        # Previous state frame
        self.prev_frame = ttk.LabelFrame(self.history_frame, text="Previous State")
        self.prev_frame.pack(fill="both", expand=True, pady=5)
        
        self.prev_text = tk.Text(self.prev_frame, height=10, wrap="word", bg=grey_button_color)
        self.prev_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Changed state frame
        self.new_frame = ttk.LabelFrame(self.history_frame, text="Changed State")
        self.new_frame.pack(fill="both", expand=True, pady=5)
        
        self.new_text = tk.Text(self.new_frame, height=10, wrap="word", bg=grey_button_color)
        self.new_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Button frame
        button_frame = tk.Frame(self.tasks_frame, bg=background_color)
        button_frame.pack(fill='x', side='bottom', pady=5)

        # Create uniform buttons with consistent width
        button_width = 10
        
        delete_all_button = tk.Button(button_frame, text="Delete All",
                                    bg=del_btn_color, width=button_width,
                                    command=self.delete_all_tasks)
        delete_all_button.pack(side='right')

        delete_button = tk.Button(button_frame, text="Delete",
                                bg=del_btn_color, width=button_width,
                                command=self.delete_selected_task)
        delete_button.pack(side='right', padx=5)

        export_button = tk.Button(button_frame, text="Export",
                                bg=main_btn_color, width=button_width,
                                command=self.export_tasks)
        export_button.pack(side="left")

        self.commit_button = tk.Button(button_frame, text="Commit History",
                                    bg=main_btn_color, width=button_width,
                                    command=self.open_CommitHistoryWindow)
        self.commit_button.pack(side="left", padx=5)

        undo_button = tk.Button(button_frame, text="Undo Commit",
                            bg=main_btn_color, width=button_width,
                            command=self.undo_task_completion)
        undo_button.pack(side="left")

        # View details button
        details_button = tk.Button(button_frame, text="View Details",
                                bg=main_btn_color, width=button_width,
                                command=self.open_selected_task_details)
        details_button.pack(side="left", padx=5)

        # Bind selection event
        self.completed_list.bind('<<TreeviewSelect>>', self.on_task_select)

        self.load_completed_tasks()
    
    def open_task_details(self, event):
        """Open task details window on double-click"""
        # Get the selected item
        selected = self.completed_list.selection()
        if not selected:
            return
            
        # Get the task ID
        task_id = self.completed_list.item(selected[0])['values'][3]
        
        # Open the task details window
        self.open_task_details_window(task_id)
    
    def open_selected_task_details(self):
        """Open task details window for the selected task"""
        # Get the selected item
        selected = self.completed_list.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a task to view details.")
            return
            
        # Get the task ID
        task_id = self.completed_list.item(selected[0])['values'][3]
        
        # Open the task details window
        self.open_task_details_window(task_id)
    
    def open_task_details_window(self, task_id):
        """Open a task details window for the given task ID"""
        if self.task_details_window is None or not tk.Toplevel.winfo_exists(self.task_details_window):
            self.task_details_window = CompletedTaskDetailsWindow(task_id=task_id, parent=self)
            self.task_details_window.grab_set()  # Make window modal
        else:
            # If window already exists, try to close it and open a new one
            try:
                self.task_details_window.destroy()
                self.task_details_window = CompletedTaskDetailsWindow(task_id=task_id, parent=self)
                self.task_details_window.grab_set()
            except:
                messagebox.showinfo("Info", "Please close the existing details window first.")
                self.task_details_window.lift()
                self.task_details_window.focus_force()

    def delete_selected_task(self):
        """Archive the selected task from the completed tasks list"""
        selected_items = self.completed_list.selection()
        
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a task to archive.")
            return

        # Get the task details for confirmation
        task_name = self.completed_list.item(selected_items[0])['values'][0]
        task_id = self.completed_list.item(selected_items[0])['values'][3]

        # Confirm archiving
        if not messagebox.askyesno("Confirm Archive", f"Are you sure you want to archive the task '{task_name}'?"):
            return

        # Move to archive database
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # Begin transaction
            c.execute("BEGIN")
            
            # Get the task data
            c.execute("SELECT * FROM CompletedTasks WHERE task_id = ?", (task_id,))
            task_data = c.fetchone()
            
            if task_data:
                # Add to ArchivedTasks with current timestamp as archive_date
                archive_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Insert into ArchivedTasks
                c.execute("""
                    INSERT INTO ArchivedTasks
                    (task_name, task_time, task_weight, task_id, completion_date, 
                    total_duration, archive_date, task_tags, task_weight_type, task_description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task_data[0],  # task_name
                    task_data[1],  # task_time
                    task_data[2],  # task_weight
                    task_data[3],  # task_id
                    task_data[4],  # completion_date
                    task_data[5],  # total_duration
                    archive_date,  # archive_date (new)
                    task_data[7] if len(task_data) > 7 else None,  # task_tags
                    task_data[8] if len(task_data) > 8 else None,  # task_weight_type
                    task_data[9] if len(task_data) > 9 else None   # task_description
                ))
                
                # Delete from CompletedTasks
                c.execute("DELETE FROM CompletedTasks WHERE task_id = ?", (task_id,))
                
                # Commit changes
                conn.commit()
                
                # Remove from treeview
                self.completed_list.delete(selected_items[0])
                
                # Recolor rows
                for i, item in enumerate(self.completed_list.get_children()):
                    self.completed_list.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))
                
                messagebox.showinfo("Success", "Task archived successfully!")
            else:
                messagebox.showerror("Error", "Task not found in database.")
                conn.rollback()
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error archiving task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def delete_all_tasks(self):
        """Archive all tasks from the completed tasks list"""
        if not self.completed_list.get_children():
            messagebox.showinfo("No Tasks", "There are no completed tasks to archive.")
            return

        # Confirm archiving
        if not messagebox.askyesno("Confirm Archive All", 
                                "Are you sure you want to archive ALL completed tasks?"):
            return

        # Move to archive database
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # Begin transaction
            c.execute("BEGIN")
            
            # Get all completed tasks
            c.execute("SELECT * FROM CompletedTasks")
            tasks = c.fetchall()
            
            archive_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Archive each task
            for task in tasks:
                c.execute("""
                    INSERT INTO ArchivedTasks
                    (task_name, task_time, task_weight, task_id, completion_date, 
                    total_duration, archive_date, task_tags, task_weight_type, task_description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task[0],  # task_name
                    task[1],  # task_time
                    task[2],  # task_weight
                    task[3],  # task_id
                    task[4],  # completion_date
                    task[5],  # total_duration
                    archive_date,  # archive_date (new)
                    task[7] if len(task) > 7 else None,  # task_tags
                    task[8] if len(task) > 8 else None,  # task_weight_type
                    task[9] if len(task) > 9 else None   # task_description
                ))
            
            # Delete all from CompletedTasks
            c.execute("DELETE FROM CompletedTasks")
            
            # Commit changes
            conn.commit()
            
            # Clear treeview
            for item in self.completed_list.get_children():
                self.completed_list.delete(item)
            
            messagebox.showinfo("Success", "All completed tasks archived successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error archiving tasks: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def undo_task_completion(self):
        """Move selected task from CompletedTasks back to TaskList"""
        selected_items = self.completed_list.selection()
        
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a task to undo.")
            return

        # Get the task details from the selected item
        values = self.completed_list.item(selected_items[0])['values']
        task_name = values[0]
        task_time = values[1]
        task_weight = values[2]
        task_id = values[3]

        # Confirm undo
        if not messagebox.askyesno("Confirm Undo", f"Move '{task_name}' back to tasks list?"):
            return

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # Begin transaction
            c.execute("BEGIN")

            # Get ALL columns from CompletedTasks for this task to ensure we have the description
            c.execute("SELECT * FROM CompletedTasks WHERE task_id = ?", (task_id,))
            completed_task_data = c.fetchone()
            
            if not completed_task_data:
                messagebox.showerror("Error", "Task data not found in database.")
                conn.rollback()
                conn.close()
                return
            
            # Get the highest list_place value
            c.execute("SELECT COALESCE(MAX(list_place), 0) FROM TaskList")
            max_list_place = c.fetchone()[0] or 0
            next_list_place = max_list_place + 1
            
            # Get the structure of the CompletedTasks table to find description column index
            c.execute("PRAGMA table_info(CompletedTasks)")
            completed_columns = c.fetchall()
            description_index = None
            
            # Find the index of the task_description column
            for i, col in enumerate(completed_columns):
                if col[1] == 'task_description':
                    description_index = i
                    break
            
            # Prepare data for TaskList based on CompletedTasks columns
            # Get task description, using a default empty string if not found
            task_description = ""
            if description_index is not None and description_index < len(completed_task_data):
                task_description = completed_task_data[description_index] or ""
                
            # Insert the task back to TaskList with all available data including description
            c.execute("""
                INSERT INTO TaskList 
                (task_name, task_time, task_weight, task_id, task_start_date, 
                task_end_date, task_description, task_weight_type, task_tags, list_place) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                completed_task_data[0],                          # task_name
                completed_task_data[1],                          # task_time
                completed_task_data[2],                          # task_weight
                completed_task_data[3],                          # task_id
                completed_task_data[6] if len(completed_task_data) > 6 else None,  # start_date if available
                None,                                            # end_date
                task_description,                                # task_description with robust handling
                completed_task_data[8] if len(completed_task_data) > 8 else None,  # task_weight_type if available
                completed_task_data[7] if len(completed_task_data) > 7 else None,  # task_tags if available
                next_list_place                                  # list_place at the end
            ))

            # Remove from CompletedTasks
            c.execute("DELETE FROM CompletedTasks WHERE task_id = ?", (task_id,))

            # Record this change in task history
            if hasattr(self, 'history_db'):
                self.history_db.record_change(
                    task_id, 
                    "status",
                    "completed",
                    "in_progress",
                    existing_conn=conn
                )

            # Commit transaction
            conn.commit()

            # Remove from treeview
            self.completed_list.delete(selected_items[0])

            # Recolor remaining rows
            for i, item in enumerate(self.completed_list.get_children()):
                self.completed_list.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

            # Refresh main page task list if controller exists
            if self.controller and hasattr(self.controller, 'query_database'):
                self.controller.query_database()
                
            # Also refresh main app if it's available
            if self.main_app and hasattr(self.main_app, 'query_database'):
                self.main_app.query_database()

            messagebox.showinfo("Success", "Task moved back to tasks list successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error undoing task completion: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def load_completed_tasks(self):
        """Load completed tasks from database into the treeview"""
        try:
            # Connect to the database
            conn = sqlite3.connect(path)
            c = conn.cursor()
            
            # Check if CompletedTasks table exists before querying
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CompletedTasks'")
            if not c.fetchone():
                print("CompletedTasks table does not exist yet. It will be created when needed.")
                return  # Exit early if table doesn't exist
            
            # Clear existing data in Treeview
            for item in self.completed_list.get_children():
                self.completed_list.delete(item)
            
            # Fetch data from CompletedTasks table
            c.execute("SELECT * FROM CompletedTasks ORDER BY completion_date DESC")
            completed_data = c.fetchall()
            
            # Insert data into Treeview
            for count, record in enumerate(completed_data):
                tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                # Make sure we only access valid indices
                values = (
                    record[0],                             # task_name
                    record[1],                             # task_time
                    record[2],                             # task_weight
                    record[3],                             # task_id
                    record[4] if len(record) > 4 else "",  # completion_date
                    record[5] if len(record) > 5 else "",  # total_duration
                )
                self.completed_list.insert('', 'end', iid=count, values=values, tags=tags)
                
        except sqlite3.Error as e:
            print(f"Database error in load_completed_tasks: {e}")
        except Exception as e:
            print(f"Unexpected error in load_completed_tasks: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def export_tasks(self):
        """Export completed tasks to CSV file"""
        # Check if there are tasks to export
        if not self.completed_list.get_children():
            messagebox.showinfo("No Tasks", "There are no completed tasks to export.")
            return

        try:
            # Get user's home directory for exports
            export_dir = pathlib.Path.home() / ".timetracker" / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)

            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = export_dir / f"completed_tasks_{timestamp}.csv"

            # Get all tasks from the treeview
            tasks = []
            headers = self.completed_list['columns']
            tasks.append(headers)  # Add headers as first row

            for item in self.completed_list.get_children():
                values = self.completed_list.item(item)['values']
                tasks.append(values)

            # Write to CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(tasks)

            messagebox.showinfo("Success", f"Tasks exported successfully to:\n{filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting tasks: {str(e)}")

    def sort_completed_tasks(self, col):
        """Sort completed tasks by column."""
        try:
            # Retrieve all items from Treeview
            items = [(self.completed_list.set(k, col), k) for k in self.completed_list.get_children("")]

            # Convert to appropriate type (for numeric columns)
            if col in ["Task Time", "Task Weight", "Task ID", "Total Duration"]:
                items.sort(key=lambda x: float(x[0]) if x[0] and x[0].replace('.', '', 1).isdigit() else 0, 
                        reverse=self.current_sort_reverse)
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

    def on_task_select(self, event):
        """Handle task selection and show history"""
        selection = self.completed_list.selection()
        if not selection:
            return

        # Get task details
        task_values = self.completed_list.item(selection[0])['values']
        task_id = task_values[3]  # Assuming task_id is at index 3

        # Clear existing text
        self.prev_text.delete(1.0, tk.END)
        self.new_text.delete(1.0, tk.END)

        # Get task history
        history = self.history_db.get_task_history(task_id)
        
        if history:
            last_change = history[0]  # Get most recent change
            change_date, field, old_val, new_val = last_change

            # Update text widgets
            self.prev_text.insert(tk.END, f"Date: {change_date}\n")
            self.prev_text.insert(tk.END, f"Field Changed: {field}\n")
            self.prev_text.insert(tk.END, f"Previous Value: {old_val}")

            self.new_text.insert(tk.END, f"Date: {change_date}\n")
            self.new_text.insert(tk.END, f"Field Changed: {field}\n")
            self.new_text.insert(tk.END, f"New Value: {new_val}")
        else:
            self.prev_text.insert(tk.END, "No history available")
            self.new_text.insert(tk.END, "No history available")

    def open_CommitHistoryWindow(self):
        """Open commit history window for selected task"""
        selection = self.completed_list.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a task to view commit history.")
            return
            
        task_values = self.completed_list.item(selection[0])['values']
        task = task_values[3]  # Task ID
        
        if self.main_app.commithistory_window is None or not self.main_app.commithistory_window.winfo_exists():
            self.main_app.commit_button.config(state=tk.DISABLED)
            self.commithistory_window = CommitHistoryWindow(main_app=self.main_app, task_id=task, compFlag=True)
        else:
            messagebox.showwarning("Window Already Open", "Please close the existing commit history window before opening a new one.")
            self.main_app.commithistory_window.lift()
            self.main_app.commithistory_window.focus_force()