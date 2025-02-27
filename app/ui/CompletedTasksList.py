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

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("CompletedTasksList.py", '') + '\\Databases' + '\\task_list.db'

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
        self.controller = controller
        self.current_sort_reverse = False
        self.history_db = TaskHistoryDB()

        self.configure(background="#A9A9A9")

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
        self.completed_list.column('Task Name', anchor=tk.W, width=135)
        self.completed_list.column('Task Time', anchor=tk.CENTER, width=75)
        self.completed_list.column('Task Weight', anchor=tk.CENTER, width=50)
        self.completed_list.column('Task ID', anchor=tk.CENTER, width=50)
        self.completed_list.column('Completion Date', anchor=tk.CENTER, width=135)
        self.completed_list.column('Total Duration', anchor=tk.CENTER, width=100)

        # Configure headings
        for col in self.completed_list['columns']:
            self.completed_list.heading(col, text=col, anchor=tk.CENTER,
                                    command=lambda c=col: self.sort_completed_tasks(c))

        self.completed_list.tag_configure('oddrow', background="white")
        self.completed_list.tag_configure('evenrow', background="#d3d3d3")

        # Right side - History view
        self.history_frame = tk.Frame(self.main_container, bg="#A9A9A9", width=400)
        self.history_frame.pack(side="right", fill="both", padx=5, pady=5)
        
        # History title
        self.history_title = tk.Label(self.history_frame, 
                                    text="Task History", 
                                    font=("SF Pro Display", 14, "bold"),
                                    bg="#A9A9A9")
        self.history_title.pack(pady=(0, 5))

        # Previous state frame
        self.prev_frame = ttk.LabelFrame(self.history_frame, text="Previous State")
        self.prev_frame.pack(fill="both", expand=True, pady=5)
        
        self.prev_text = tk.Text(self.prev_frame, height=10, wrap="word", bg="#d3d3d3")
        self.prev_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Changed state frame
        self.new_frame = ttk.LabelFrame(self.history_frame, text="Changed State")
        self.new_frame.pack(fill="both", expand=True, pady=5)
        
        self.new_text = tk.Text(self.new_frame, height=10, wrap="word", bg="#d3d3d3")
        self.new_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Button frame
        button_frame = tk.Frame(self.tasks_frame, bg="#A9A9A9")
        button_frame.pack(fill='x', side='bottom', pady=5)

        delete_all_button = tk.Button(button_frame, text="Delete All",
                                    bg="#e99e56", command=self.delete_all_tasks)
        delete_all_button.pack(side='right')

        delete_button = tk.Button(button_frame, text="Delete",
                                bg="#e99e56", command=self.delete_selected_task)
        delete_button.pack(side='right', padx=5)

        export_button = tk.Button(button_frame, text="Export",
                                bg="#b2fba5", command=self.export_tasks)
        export_button.pack(side="left")

        undo_button = tk.Button(button_frame, text="Undo Commit",
                            bg="#b2fba5", command=self.undo_task_completion)
        undo_button.pack(side="left", padx=6)

        # Bind selection event
        self.completed_list.bind('<<TreeviewSelect>>', self.on_task_select)

        self.load_completed_tasks()

    def delete_selected_task(self):
        """Delete the selected task from the completed tasks list"""
        selected_items = self.completed_list.selection()
        
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a task to delete.")
            return

        # Get the task details for confirmation
        task_name = self.completed_list.item(selected_items[0])['values'][0]
        task_id = self.completed_list.item(selected_items[0])['values'][3]

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the task '{task_name}'?"):
            return

        # Delete from database
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            c.execute("DELETE FROM CompletedTasks WHERE task_id = ?", (task_id,))
            conn.commit()
            
            # Remove from treeview
            self.completed_list.delete(selected_items[0])
            
            # Recolor rows
            for i, item in enumerate(self.completed_list.get_children()):
                self.completed_list.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))
            
            messagebox.showinfo("Success", "Task deleted successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def delete_all_tasks(self):
        """Delete all tasks from the completed tasks list"""
        if not self.completed_list.get_children():
            messagebox.showinfo("No Tasks", "There are no completed tasks to delete.")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete All", 
                                  "Are you sure you want to delete ALL completed tasks? This cannot be undone."):
            return

        # Delete from database
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            c.execute("DELETE FROM CompletedTasks")
            conn.commit()
            
            # Clear treeview
            for item in self.completed_list.get_children():
                self.completed_list.delete(item)
            
            messagebox.showinfo("Success", "All completed tasks deleted successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting tasks: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def undo_task_completion(self):
        """Move selected task from CompletedTasks back to TaskList"""
        selected_items = self.completed_list.selection()
        
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a task to undo.")
            return

        # Get the task details
        values = self.completed_list.item(selected_items[0])['values']
        task_name = values[0]
        task_time = values[1]
        task_weight = values[2]
        task_id = values[3]
        completion_date = values[4]
        total_duration = values[5]

        # Confirm undo
        if not messagebox.askyesno("Confirm Undo", f"Move '{task_name}' back to tasks list?"):
            return

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # Begin transaction
            c.execute("BEGIN")

            # Get additional details from CompletedTasks (if available)
            c.execute("""
                SELECT start_date, task_tags, task_weight_type, task_description 
                FROM CompletedTasks 
                WHERE task_id = ?
            """, (task_id,))
            
            extra_details = c.fetchone()
            
            # Set default values for missing fields
            start_date = extra_details[0] if extra_details and extra_details[0] else ""
            task_tags = extra_details[1] if extra_details and extra_details[1] else ""
            task_weight_type = extra_details[2] if extra_details and extra_details[2] else ""
            task_description = extra_details[3] if extra_details and extra_details[3] else ""
            
            # Default end date (1 month from now)
            end_date = "01-02-2025"

            # Get highest list_place value
            c.execute("SELECT COALESCE(MAX(list_place), 0) FROM TaskList")
            max_list_place = c.fetchone()[0]
            list_place = max_list_place + 1 if max_list_place is not None else 1

            # Insert back into TaskList with all required fields
            c.execute("""
                INSERT INTO TaskList 
                (task_name, task_time, task_weight, task_id, task_start_date, 
                task_end_date, task_description, task_weight_type, task_tags, list_place) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_name, task_time, task_weight, task_id, start_date, 
                end_date, task_description, task_weight_type, task_tags, list_place))

            # Remove from CompletedTasks
            c.execute("DELETE FROM CompletedTasks WHERE task_id = ?", (task_id,))

            # Record this change in task history - pass the existing connection
            if hasattr(self, 'history_db'):
                self.history_db.record_change(
                    task_id,
                    "status",
                    "completed",
                    "in_progress",
                    existing_conn=conn  # Pass the existing connection
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

        conn = sqlite3.connect(path)
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
        """Export completed tasks to CSV file"""
        # Check if there are tasks to export
        if not self.completed_list.get_children():
            messagebox.showinfo("No Tasks", "There are no completed tasks to export.")
            return

        try:
            # Create Completed Tasks directory if it doesn't exist
            export_dir = pathlib.Path(__file__).parent / "Completed Tasks"
            export_dir.mkdir(exist_ok=True)

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
