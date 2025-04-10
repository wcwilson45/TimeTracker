
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

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("ArchiveTasksList.py", '') + '\\Databases' + '\\task_list.db'

background_color = "#A9A9A9"
grey_button_color = "#d3d3d3"
main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"

class ArchiveTasksList(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.current_sort_reverse = False

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
        archivelist_frame = tk.Frame(self, bg="#A9A9A9")
        archivelist_frame.pack(pady=5, padx=10)

        archivelist_scroll = ttk.Scrollbar(archivelist_frame)
        archivelist_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.archive_list = ttk.Treeview(archivelist_frame,
                                           yscrollcommand=archivelist_scroll.set,
                                           selectmode="extended",
                                           height=20)
        self.archive_list.pack()

        archivelist_scroll.config(command=self.archive_list.yview)

        # Column configuration
        self.archive_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID", 
                                         "Completion Date", "Total Duration", "Archive Date")

        self.archive_list.column("#0", width=0, stretch=tk.NO)
        self.archive_list.column('Task Name', anchor=tk.CENTER, width=100)
        self.archive_list.column('Task Time', anchor=tk.CENTER, width=75)
        self.archive_list.column('Task Weight', anchor=tk.CENTER, width=50)
        self.archive_list.column('Task ID', anchor=tk.CENTER, width=0, stretch=tk.NO)  # Hidden but available
        self.archive_list.column('Completion Date', anchor=tk.CENTER, width=100)
        self.archive_list.column('Total Duration', anchor=tk.CENTER, width=100)
        self.archive_list.column('Archive Date', anchor=tk.CENTER, width=155)

        # Headings
        self.archive_list.heading("#0", text="", anchor=tk.W)
        self.archive_list.heading("Task Name", text="Task Name", anchor=tk.W,
                                   command=lambda: self.sort_archive_tasks("Task Name"))
        self.archive_list.heading("Task Time", text="Time", anchor=tk.CENTER,
                                   command=lambda: self.sort_archive_tasks("Task Time"))
        self.archive_list.heading("Task Weight", text="Weight", anchor=tk.CENTER,
                                   command=lambda: self.sort_archive_tasks("Task Weight"))
        self.archive_list.heading("Task ID", text="", anchor=tk.CENTER)  # Empty header for hidden column
        self.archive_list.heading("Completion Date", text="Completed On", anchor=tk.CENTER,
                                   command=lambda: self.sort_archive_tasks("Completion Date"))
        self.archive_list.heading("Total Duration", text="Total Time", anchor=tk.CENTER,
                                   command=lambda: self.sort_archive_tasks("Total Duration"))
        self.archive_list.heading("Archive Date", text="Archived On", anchor=tk.CENTER,
                                   command=lambda: self.sort_archive_tasks("Archive Date"))

        self.archive_list.tag_configure('oddrow', background="white")
        self.archive_list.tag_configure('evenrow', background="#d3d3d3")

        # Button frame
        bottom_frame = tk.Frame(self, bg=background_color)
        bottom_frame.pack(fill='x', side='bottom', pady=5, padx=10)

        delete_all_button = tk.Button(bottom_frame, text="Delete All", bg=del_btn_color, 
                                     command=self.delete_all_tasks)
        delete_all_button.pack(side='right')

        delete_button = tk.Button(bottom_frame, text="Delete", bg=del_btn_color, 
                                 command=self.delete_selected_task)
        delete_button.pack(side='right', padx=(0, 5))

        export_button = tk.Button(bottom_frame, text="Export", bg=main_btn_color, 
                                 command=self.export_tasks)
        export_button.pack(side="left")

        restore_button = tk.Button(bottom_frame, text="Restore Task", bg=main_btn_color, 
                                  command=self.restore_task)
        restore_button.pack(side="left", padx=6)

        self.load_archive_tasks()

    def delete_selected_task(self):
        """Delete the selected task from the archive list"""
        selected_items = self.archive_list.selection()
        
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a task to delete.")
            return

        # Get the task details for confirmation
        task_name = self.archive_list.item(selected_items[0])['values'][0]
        task_id = self.archive_list.item(selected_items[0])['values'][3]

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete '{task_name}'?"):
            return

        # Delete from database
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            c.execute("DELETE FROM ArchivedTasks WHERE task_id = ?", (task_id,))
            conn.commit()
            
            # Remove from treeview
            self.archive_list.delete(selected_items[0])
            
            # Recolor rows
            for i, item in enumerate(self.archive_list.get_children()):
                self.archive_list.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))
            
            messagebox.showinfo("Success", "Task deleted successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def delete_all_tasks(self):
        """Delete all tasks from the archive list"""
        if not self.archive_list.get_children():
            messagebox.showinfo("No Tasks", "There are no archived tasks to delete.")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete All", 
                                  "Are you sure you want to permanently delete ALL archived tasks? This cannot be undone."):
            return

        # Delete from database
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            c.execute("DELETE FROM ArchivedTasks")
            conn.commit()
            
            # Clear treeview
            for item in self.archive_list.get_children():
                self.archive_list.delete(item)
            
            messagebox.showinfo("Success", "All archived tasks deleted successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting tasks: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def restore_task(self):
        # Move selected task from ArchivedTasks back to TaskList"""
        selected_items = self.archive_list.selection()
        
        if not selected_items:
            messagebox.showwarning("Selection Required", "Please select a task to restore.")
            return

        # Get the task details
        values = self.archive_list.item(selected_items[0])['values']
        task_name = values[0]
        task_id = values[3]

        # Confirm restore
        if not messagebox.askyesno("Confirm Restore", f"Move '{task_name}' back to task list?"):
            return

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # Begin transaction
            c.execute("BEGIN")

            # Get ALL columns from ArchivedTasks for this task
            c.execute("SELECT * FROM ArchivedTasks WHERE task_id = ?", (task_id,))
            task_data = c.fetchone()
            
            if not task_data:
                messagebox.showerror("Error", "Task data not found in database.")
                conn.rollback()
                conn.close()
                return
            
            # Get the highest list_place value for proper positioning
            c.execute("SELECT COALESCE(MAX(list_place), 0) FROM TaskList")
            max_list_place = c.fetchone()[0] or 0
            
            # Insert task back to TaskList with appropriate columns
            c.execute("""
                INSERT INTO TaskList 
                (task_name, task_time, task_weight, task_id, task_start_date, 
                task_end_date, task_description, task_weight_type, task_tags, list_place) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_data[0],                          # task_name
                task_data[1],                          # task_time
                task_data[2],                          # task_weight
                task_data[3],                          # task_id
                datetime.now().strftime("%Y-%m-%d"),   # task_start_date (current date)
                None,                                  # task_end_date
                task_data[9] if len(task_data) > 9 else None,  # task_description
                task_data[8] if len(task_data) > 8 else None,  # task_weight_type
                task_data[7] if len(task_data) > 7 else None,  # task_tags
                max_list_place + 1                     # list_place (at the end)
            ))

            # Remove from ArchivedTasks
            c.execute("DELETE FROM ArchivedTasks WHERE task_id = ?", (task_id,))

            # Commit transaction
            conn.commit()

            # Remove from treeview
            self.archive_list.delete(selected_items[0])

            # Recolor remaining rows
            for i, item in enumerate(self.archive_list.get_children()):
                self.archive_list.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

            # Refresh main task list if controller exists
            if self.controller and hasattr(self.controller, 'query_database'):
                self.controller.query_database()

            messagebox.showinfo("Success", "Task restored to task list successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error restoring task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def load_archive_tasks(self):
        """Loads archived tasks from SQLite database into Treeview."""
        for item in self.archive_list.get_children():
            self.archive_list.delete(item)

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM ArchivedTasks ORDER BY archive_date DESC")
            tasks = c.fetchall()

            for i, task in enumerate(tasks):
                tag = ('evenrow' if i % 2 == 0 else 'oddrow')
                self.archive_list.insert('', 'end', values=task, tags=tag)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading archived tasks: {str(e)}")
        finally:
            conn.close()

    def export_tasks(self):
        """Export archived tasks to CSV file"""
        # Check if there are tasks to export
        if not self.archive_list.get_children():
            messagebox.showinfo("No Tasks", "There are no archived tasks to export.")
            return

        try:
            # Create Archives directory if it doesn't exist
            export_dir = pathlib.Path(__file__).parent / "Archives"
            export_dir.mkdir(exist_ok=True)
            
            # Get all tasks from the treeview
            tasks = []
            headers = self.archive_list['columns']
            tasks.append(headers)  # Add headers as first row
            
            # Variables to track earliest completion date and latest archive date
            earliest_completion = None
            latest_archive = None
            
            # Collect data and find date range
            for item in self.archive_list.get_children():
                values = self.archive_list.item(item)['values']
                tasks.append(values)
                
                # Get completion date and archive date from the row
                # Based on column positions: Completion Date at index 4, Archive Date at index 6
                completion_date = values[4]
                archive_date = values[6]
                
                try:
                    # Parse dates to datetime objects
                    if completion_date:
                        completion_dt = datetime.strptime(completion_date, "%Y-%m-%d %H:%M:%S")
                        if earliest_completion is None or completion_dt < earliest_completion:
                            earliest_completion = completion_dt
                    
                    if archive_date:
                        archive_dt = datetime.strptime(archive_date, "%Y-%m-%d %H:%M:%S")
                        if latest_archive is None or archive_dt > latest_archive:
                            latest_archive = archive_dt
                except ValueError:
                    # Handle case where date format is different
                    pass
            
            # Format dates for filename - using dashes instead of slashes to avoid filename errors
            start_date_str = earliest_completion.strftime("%m-%d-%y") if earliest_completion else "unknown"
            end_date_str = latest_archive.strftime("%m-%d-%y") if latest_archive else "unknown"
            
            # Create filename with date range
            filename = export_dir / f"archive_list_{start_date_str}_to_{end_date_str}.csv"
            
            # Write to CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(tasks)

            messagebox.showinfo("Success", f"Tasks exported successfully to:\n{filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting tasks: {str(e)}")

    def sort_archive_tasks(self, col):
        """Sort archived tasks by column."""
        try:
            # Retrieve all items from Treeview
            items = [(self.archive_list.set(k, col), k) for k in self.archive_list.get_children("")]
            
            # Helper function to convert time string to seconds for sorting
            def time_to_seconds(time_str):
                if not time_str:
                    return 0
                try:
                    # Handle time format "HH:MM:SS"
                    parts = time_str.split(":")
                    if len(parts) == 3:
                        hours, minutes, seconds = parts
                        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                    # Handle other potential time formats
                    return 0
                except (ValueError, IndexError):
                    return 0

            # Convert to appropriate type (for numeric columns)
            if col in ["Task Time", "Total Time"]:
                # Use the helper function for time columns
                items.sort(key=lambda x: time_to_seconds(x[0]), reverse=self.current_sort_reverse)
            elif col in ["Task Weight", "Task ID"]:
                # These are still numeric columns
                items.sort(key=lambda x: float(x[0]) if x[0] and x[0].replace('.', '', 1).isdigit() else 0, 
                        reverse=self.current_sort_reverse)
            elif col in ["Completed On", "Archive Date", "Archived On"]:
                # Date columns
                items.sort(key=lambda x: x[0] if x[0] else "", reverse=self.current_sort_reverse)
            else:
                # Text columns
                items.sort(reverse=self.current_sort_reverse)

            # Rearrange items in sorted order
            for index, (_, k) in enumerate(items):
                self.archive_list.move(k, "", index)

                # Reapply row colors
                self.archive_list.item(k, tags=('evenrow' if index % 2 == 0 else 'oddrow'))

            # Toggle sort direction for next click
            self.current_sort_reverse = not self.current_sort_reverse

        except Exception as e:
            messagebox.showerror("Sorting Error", f"An error occurred while sorting: {str(e)}")
