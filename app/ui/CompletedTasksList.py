

from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
import csv
from tkinter import messagebox
import pathlib
import os
from datetime import datetime
from .TaskHistory import TaskHistoryDB
from .CommitHistoryPage import CommitHistoryWindow
from .CompletedTaskDetailsPage import CompletedTaskDetailsWindow
from .utils import resource_path
from .utils import get_writable_db_path

# Define the path to the task list database - use writable path
path = get_writable_db_path('app/ui/Databases/task_list.db')

background_color = "#A9A9A9"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "#E0E0E0"

main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"

class CompletedTasksList(tk.Frame):
    def __init__(self, parent, main_app, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.current_sort_reverse = False
        self.history_db = TaskHistoryDB()
        self.commithistory_window = None
        self.task_details_window = None
        self.configure(background="#A9A9A9")
        self.main_app = main_app

        # Create main container
        self.main_container = tk.Frame(self, bg="#A9A9A9")
        self.main_container.pack(fill="both", expand=True)

        # Left side - Tasks list
        self.tasks_frame = tk.Frame(self.main_container, bg="#A9A9A9")
        self.tasks_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                    background="#d3d3d3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#d3d3d3")
        style.map("Treeview", background=[('selected', "#347083")])

        # Create Treeview for completed tasks
        completedlist_frame = tk.Frame(self.tasks_frame, bg="#A9A9A9")
        completedlist_frame.pack(fill="both", expand=True)

        completedlist_scroll = ttk.Scrollbar(completedlist_frame)
        completedlist_scroll.pack(side=tk.RIGHT, fill=tk.Y)

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
        self.completed_list.column('Task Name', anchor=tk.W, width=200)
        self.completed_list.column('Task Time', anchor=tk.CENTER, width=120)
        self.completed_list.column('Task Weight', anchor=tk.CENTER, width=90)
        self.completed_list.column('Task ID', anchor=tk.CENTER, width=0,stretch=tk.NO)
        self.completed_list.column('Completion Date', anchor=tk.CENTER, width=160)
        self.completed_list.column('Total Duration', anchor=tk.CENTER, width=120)

        # Configure headings
        for col in self.completed_list['columns']:
            self.completed_list.heading(col, text=col, anchor=tk.CENTER,
                                    command=lambda c=col: self.sort_completed_tasks(c))

        self.completed_list.tag_configure('oddrow', background="#A9A9A9")
        self.completed_list.tag_configure('evenrow', background="#dcdcdc")

        # Bind double-click to open task details
        self.completed_list.bind("<Double-1>", self.open_task_details)

        # Button frame
        button_frame = tk.Frame(self.tasks_frame, bg="#A9A9A9")
        button_frame.pack(fill='x', side='bottom', pady=5)

        delete_all_button = tk.Button(button_frame, text="Delete All",
                                    bg="#e99e56", command=self.delete_all_tasks)
        delete_all_button.pack(side='right')

        delete_button = tk.Button(button_frame, text="Delete",
                                bg="#e99e56", command=self.delete_selected_task)
        delete_button.pack(side='right')

        export_button = tk.Button(button_frame, text="Export",
                                bg="#b2fba5", command=self.export_tasks)
        export_button.pack(side="left")

        self.commit_button = tk.Button(button_frame, text="Commit History",
                                  bg="#b2fba5", command=self.open_selected_task_details)
        self.commit_button.pack(side="left")

        undo_button = tk.Button(button_frame, text="Undo Commit",
                            bg="#b2fba5", command=self.undo_task_completion)
        undo_button.pack(side="left")

        # View details button
        details_button = tk.Button(button_frame, text="View Details",
                                bg="#b2fba5", command=self.open_selected_task_details)
        details_button.pack(side="left")

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
            # Added the missing compFlag parameter with value True since we're in the CompletedTasksList
            self.task_details_window = CompletedTaskDetailsWindow(compFlag=0, task_id=task_id, parent=self)
            self.task_details_window.grab_set()  # Make window modal
        else:
            # If window already exists, try to close it and open a new one
            try:
                self.task_details_window.destroy()
                # Also added compFlag=True here
                self.task_details_window = CompletedTaskDetailsWindow(compFlag=0, task_id=task_id, parent=self)
                self.task_details_window.grab_set()
            except:
                messagebox.showinfo("Info", "Please close the existing details window first.")
                self.task_details_window.lift()
                self.task_details_window.focus_force()

    def delete_selected_task(self):
        #Archive the selected task from the completed tasks list"""
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
        # Archive all tasks from the completed tasks list"""
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
        #"""Move selected task from CompletedTasks back to TaskList"""
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

        # Get a fresh writable path
        from .utils import get_writable_db_path
        writable_path = get_writable_db_path('app/ui/Databases/task_list.db')
        
        conn = sqlite3.connect(writable_path)
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
            max_list_place = c.fetchone()[0]
            
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
                max_list_place + 1                               # list_place at the end
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

            messagebox.showinfo("Success", "Task moved back to tasks list successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error undoing task completion: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def load_completed_tasks(self):
        """Loads completed tasks from SQLite database into Treeview."""
        for item in self.completed_list.get_children():
            self.completed_list.delete(item)

        # Get a fresh writable path - this ensures we're using the latest copy
        from .utils import get_writable_db_path
        writable_path = get_writable_db_path('app/ui/Databases/task_list.db')
        
        conn = sqlite3.connect(writable_path)
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

    def export_tasks(self):
        """Export completed tasks to CSV file and optionally commit history to a separate file"""
        # Check if there are tasks to export
        if not self.completed_list.get_children():
            messagebox.showinfo("No Tasks", "There are no completed tasks to export.")
            return

        try:
            # Ask user for file name and location for completed tasks
            tasks_file_path = tk.filedialog.asksaveasfilename(
                title="Save Completed Tasks As",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile="completed_tasks.csv"
            )
            
            if not tasks_file_path:  # User canceled
                return
                
            # Get all tasks from the treeview
            tasks = []
            headers = list(self.completed_list['columns'])  # Convert to list to be safe
            tasks.append(headers)  # Add headers as first row

            # Keep track of all task IDs for potential history export
            task_ids = []

            for item in self.completed_list.get_children():
                values = self.completed_list.item(item)['values']
                tasks.append(values)
                # Get the task ID (at index 3)
                task_ids.append(values[3])

            # Write tasks to CSV
            with open(tasks_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(tasks)
                
            # Show success message for tasks export
            messagebox.showinfo("Success", f"Tasks exported successfully to:\n{tasks_file_path}")
            
            # Ask if user wants to export commit history as well
            export_history = messagebox.askyesno("Export History", 
                                                "Would you like to export the task commit history as well?")
            
            if export_history:
                # Ask user for file name and location for history
                history_file_path = tk.filedialog.asksaveasfilename(
                    title="Save Task History As",
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    initialfile="tasks_commit_history.csv"
                )
                
                if not history_file_path:  # User canceled
                    return
                    
                # Get and write commit history for all tasks
                history_rows = []
                # Create headers for history file
                history_headers = ["Task ID", "Task Name", "Change Date", "Field Changed", "Old Value", "New Value"]
                history_rows.append(history_headers)

                # Get task information to include with history
                conn = sqlite3.connect(path)
                c = conn.cursor()
                
                try:
                    for task_id in task_ids:
                        # Get task name for reference
                        c.execute("SELECT task_name FROM CompletedTasks WHERE task_id = ?", (task_id,))
                        result = c.fetchone()
                        task_name = result[0] if result else "Unknown Task"
                        
                        # Get task history
                        history_entries = self.history_db.get_task_history(task_id)
                        
                        # Add each history entry to the rows
                        for entry in history_entries:
                            change_date, field_changed, old_value, new_value = entry
                            history_rows.append([
                                task_id,
                                task_name,
                                change_date,
                                field_changed,
                                old_value,
                                new_value
                            ])
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error retrieving task history: {str(e)}")
                finally:
                    conn.close()

                # Write history to CSV
                with open(history_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(history_rows)

                messagebox.showinfo("Success", f"Task history exported successfully to:\n{history_file_path}")

        except PermissionError:
            messagebox.showerror("Permission Error", 
                            "Unable to write to the selected location. Please check folder permissions.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")
            # Print the error for debugging
            import traceback
            traceback.print_exc()
    
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
        selection = self.completed_list.selection()
        task_values = self.completed_list.item(selection[0])['values']
        task = task_values[3]
        if not task:
            messagebox.showwarning("Selection Required", "Please select a task to complete.")
        elif self.main_app.commithistory_window is None or not self.main_app.commithistory_window.winfo_exists():
            self.commithistory_window = CommitHistoryWindow(main_app=self, task_id=task, compFlag=0)
        else:
            messagebox.showwarning("A commit history window is already open", "Please close it before reopening.")
