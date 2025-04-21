from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import pathlib
import sqlite3
from datetime import date
from .TaskHistory import TaskHistoryDB
from .utils import show_messagebox

main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"
background_color = "#A9A9A9"

class EditTaskWindow(tk.Tk):
    def __init__(self, task_id, main_app):
        super().__init__()
        self.task_id = task_id
        self.main_app = main_app
        self.history_db = TaskHistoryDB()
        self.main_app.edittask_window = self
        self.is_current_task = False  # Flag to track if editing current task
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Define paths using pathlib properly
        # For task_list.db
        self.path = pathlib.Path(__file__).parent
        self.path = self.path / 'Databases' / 'task_list.db'
        self.path = str(self.path)  # Convert to string for sqlite3.connect()

        # For tags.db
        self.tags_path = pathlib.Path(__file__).parent
        self.tags_path = self.tags_path / 'Databases' / 'tags.db'
        self.tags_path = str(self.tags_path)

        # Initialize task data
        self.edit_task = None
        
        # Set grab for this window
        try:
            self.grab_set()
        except Exception as e:
            print(f"Error setting grab: {e}")
            
        # Load available tags
        self.load_tags()
        
        # Set up the UI elements
        self.configure_ui()
        
        # Load the task data
        self.load_task()
        
        # If task was found, insert data into the UI
        if self.edit_task:
            self.insert_task()
        else:
            show_messagebox(self, messagebox.showerror, "Error", f"Task with ID {task_id} not found!")
            self.destroy()

    # Separate method to load tags
    def load_tags(self):
        # Create or Connect to the database
        conn = sqlite3.connect(self.tags_path)
        c = conn.cursor()

        try:
            c.execute("SELECT tag_name FROM tags")  # Fetch tag_names from tag database
            tags = c.fetchall()
            global values
            values = []

            # Add data to the list
            for tag in tags:
                values.append(tag[0])
        except sqlite3.Error as e:
            print(f"Error loading tags: {e}")
        finally:
            conn.commit()
            conn.close()

    def load_task(self):
        """Load task data from either TaskList or CurrentTask"""
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        
        try:
            # First check in CurrentTask table
            c.execute("SELECT * FROM CurrentTask WHERE task_id = ?", (int(self.task_id),))
            self.edit_task = c.fetchone()
            
            # If not found in CurrentTask, check in TaskList
            if not self.edit_task:
                c.execute("SELECT * FROM TaskList WHERE task_id = ?", (int(self.task_id),))
                self.edit_task = c.fetchone()
                self.is_current_task = False
            else:
                self.is_current_task = True
        except sqlite3.Error as e:
            print(f"Database error when loading task: {e}")
            self.edit_task = None
        finally:
            conn.close()

    def insert_task(self):
        """Insert task data into UI fields"""
        try:
            # Task Name
            if self.edit_task[0]:
                self.task_name_entry.insert(0, self.edit_task[0])
            
            # Task Time
            if self.edit_task[1]:
                self.task_time_entry.insert(0, self.edit_task[1])
            
            # Task Weight type and value
            if self.edit_task[7]:
                self.type_combo.set(self.edit_task[7])
                self.update_values()  # Update the values dropdown based on the type
            
            if self.edit_task[2]:
                self.value_combo.set(self.edit_task[2])
            
            # Start Date
            if self.edit_task[4]:
                self.start_date_entry.insert(0, self.edit_task[4])
            
            # End Date
            if self.edit_task[5]:
                self.end_date_entry.insert(0, self.edit_task[5])
            
            # Description
            if self.edit_task[6]:
                self.desc_text_entry.insert("1.0", self.edit_task[6])
            
            # Tags
            if self.edit_task[8]:
                self.task_tags_entry.delete("1.0", "end")
                self.task_tags_entry.insert("1.0", self.edit_task[8])
                
                # Select the corresponding tags in the listbox
                tag_list = self.edit_task[8].strip().split('\n')
                
                for i in range(self.tag_listbox.size()):
                    item_text = self.tag_listbox.get(i)
                    if item_text in tag_list:
                        self.tag_listbox.selection_set(i)
        except (IndexError, AttributeError) as e:
            # Handle potential issues with missing fields in the task data
            print(f"Error inserting task data: {e}")
            show_messagebox(self, messagebox.showwarning, "Data Warning", "Some task data could not be loaded correctly.")

    def update_values(self, event=None):
        selected_type = self.type_combo.get()
        if selected_type == "T-Shirt Size":
            self.value_combo['values'] = self.tshirt_sizes
        elif selected_type == "Fibonacci":
            self.value_combo['values'] = self.fibonacci
        else:
            self.value_combo['values'] = []
        self.value_combo.set("Select Value")
    
    def update_tag_entry(self):
        """Updated tag entry function to handle tag selection properly"""
        # Get selected values from the Listbox widget
        selected_values = [self.tag_listbox.get(idx) for idx in self.tag_listbox.curselection()]

        # Update with the selected values - clear first
        self.task_tags_entry.delete("1.0", "end")
        
        # Insert as newline-separated
        if selected_values:
            self.task_tags_entry.insert("1.0", "\n".join(selected_values))

    def cancel_action(self):
        # Implement the cancel action (e.g., close the window)
        self.on_close()

    def confirm_action(self):
        confirm = show_messagebox(self, messagebox.askyesno, "Confirm Edit", "Are you sure you want to edit this task?")
        if confirm:
            # Connect to database
            conn = sqlite3.connect(self.path)
            c = conn.cursor()
            
            try:
                # Begin transaction
                c.execute("BEGIN")
                
                # Get old values before update
                table_name = "CurrentTask" if self.is_current_task else "TaskList"
                c.execute(f"SELECT task_name, task_time, task_weight, task_start_date, task_end_date, task_description, task_weight_type, task_tags FROM {table_name} WHERE task_id = ?", (self.task_id,))
                old_values = c.fetchone()
                
                # Get new values
                new_values = {
                    'task_name': self.task_name_entry.get(),
                    'task_time': self.task_time_entry.get(),
                    'task_weight': self.value_combo.get(),
                    'task_start_date': self.start_date_entry.get(),
                    'task_end_date': self.end_date_var.get(),
                    'task_description': self.desc_text_entry.get("1.0", "end-1c"),
                    'task_weight_type': self.type_combo.get(),
                    'task_tags': self.task_tags_entry.get("1.0","end-1c")
                }

                # Record changes for each field that has changed
                field_map = {
                    0: 'task_name',
                    1: 'task_time',
                    2: 'task_weight',
                    3: 'task_start_date',
                    4: 'task_end_date',
                    5: 'task_description',
                    6: 'task_weight_type',
                    7: 'task_tags'
                }

                for i, (old, new) in enumerate(zip(old_values, new_values.values())):
                    if old != new:
                        self.history_db.record_change(
                            self.task_id,
                            field_map[i],
                            str(old),
                            str(new),
                            existing_conn=conn  # Pass the existing connection
                        )

                # Perform the update on the appropriate table
                update_query = f"""UPDATE {table_name} SET 
                    task_name = ?, 
                    task_time = ?, 
                    task_weight = ?, 
                    task_start_date = ?, 
                    task_end_date = ?, 
                    task_description = ?, 
                    task_weight_type = ?, 
                    task_tags = ? 
                    WHERE task_id = ?"""
                    
                c.execute(update_query,
                    (new_values['task_name'], new_values['task_time'], new_values['task_weight'],
                    new_values['task_start_date'], new_values['task_end_date'], new_values['task_description'],
                    new_values['task_weight_type'], new_values['task_tags'], self.task_id))
                
                conn.commit()
                
                # Refresh the main app's UI
                if hasattr(self.main_app, 'query_database'):
                    self.main_app.query_database()
                    
                # If we edited a current task, refresh the current task display
                if self.is_current_task and hasattr(self.main_app, 'set_current_task'):
                    self.main_app.set_current_task()

                self.destroy()
                self.on_close()
            
            except sqlite3.Error as e:
                show_messagebox(self, messagebox.showerror, "Database Error", f"Error editing task: {str(e)}")
                conn.rollback()
            finally:
                conn.close()

    def delete_action(self):
        delete = show_messagebox(self, messagebox.askyesno, "Confirm Delete", "Are you sure you want to delete this task?")
        if delete:
            # Connect to database
            conn = sqlite3.connect(self.path)
            c = conn.cursor()
            
            try:
                # Determine which table to delete from
                table_name = "CurrentTask" if self.is_current_task else "TaskList"
                
                # Execute the correct DELETE statement
                c.execute(f"DELETE FROM {table_name} WHERE task_id = ?", (int(self.task_id),))
                
                # Commit changes to database
                conn.commit()
                
                show_messagebox(self, messagebox.showinfo, "Success", "Task deleted successfully!")
                
                # Refresh the main app's task list
                if hasattr(self.main_app, 'query_database'):
                    self.main_app.query_database()
                
                # If we deleted a current task, refresh the current task display
                if self.is_current_task and hasattr(self.main_app, 'set_current_task'):
                    self.main_app.set_current_task()
                
                # Close the window
                self.destroy()
                self.on_close()
                
            except sqlite3.Error as e:
                show_messagebox(self, messagebox.showerror, "Database Error", f"Error deleting task: {str(e)}")
                conn.rollback()
            finally:
                conn.close()


    #Configure the ui
    def configure_ui(self):
         # Set the main window geometry and title
        self.geometry("500x430")  # Increased height to accommodate additional fields
        self.title("Edit Task")
        self.configure(bg=background_color)  # Lighter Blue background
        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=14, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=10, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }
        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]

        # Style configurations
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Using "alt" theme for better customization
        self.style.configure('MainFrame.TFrame', background=background_color)  # Lighter Blue for frames
        self.style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('Input.TCombobox', fieldbackground='#d3d3d3', background=background_color, font=("SF Pro Text", 10))
        self.style.configure('TLabel', background=background_color, font=("SF Pro Text", 10))  # Lighter Blue for labels
        self.style.configure('TButton', background=background_color, font=("SF Pro Text", 10))  # Default Lighter Blue for buttons

        # Custom button styles
        self.style.configure('ConfirmButton.TButton', background=main_btn_color, font=("SF Pro Text", 10))
        self.style.configure('CancelButton.TButton', background=del_btn_color, font=("SF Pro Text", 10))

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.grid(row=0, column=0, padx=10, pady=0, sticky='nsew')

        
        # Content container
        content_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        content_frame.grid(row=1, column=0, padx=10, pady=0, sticky='nsew')

        # Left column
        left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        left_frame.grid(row=0, column=0, padx=(0, 8), sticky='nsew')

        # Task Name Label
        label = ttk.Label(left_frame, text="Task Name:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w')

        # Task Name Entry
        self.task_name_entry = ttk.Entry(left_frame, style='Input.TEntry', width=37)
        self.task_name_entry.grid(row=1, column=0, pady=(3, 0), sticky='ew')


        # Description
        label = ttk.Label(left_frame, text="Description:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=2, column=0, sticky='w')

        # Create a frame for the text and scrollbar
        desc_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        desc_frame.grid(row=3, column=0, pady=(3, 0), sticky='ew')

        # Text widget with scrollbar
        self.desc_text_entry = tk.Text(desc_frame, height=7, width=30, bg='#d3d3d3', relief="solid", bd=1,
                                        font=("SF Pro Text", 10))
        self.desc_text_entry.grid(row=0, column=0, sticky='nsew')

        # Add a vertical scrollbar and apply the custom style
        scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=self.desc_text_entry.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Link the scrollbar with the text widget
        self.desc_text_entry.configure(yscrollcommand=scrollbar.set)

        # Time Complexity with nested dropdowns (Moved below Description)
        label = ttk.Label(left_frame, text="Time Complexity:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=4, column=0, sticky='w')

        # Complexity type frame
        complexity_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        complexity_frame.grid(row=5, column=0, pady=(3, 0), sticky='w')

        # Type selector
        self.type_combo = ttk.Combobox(complexity_frame, values=self.complexity_types, style='Input.TCombobox', state='readonly')
        self.type_combo.grid(row=0, column=0, pady=(3, 0), sticky='w')
        self.type_combo.set("Select Type")

        # Value selector
        self.value_combo = ttk.Combobox(complexity_frame, style='Input.TCombobox', state='readonly')
        self.value_combo.grid(row=1, column=0, sticky='w')
        self.value_combo.set("Select Value")

        # Bind the type selection to update value options
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)

        # Edit Start Date
        label = ttk.Label(left_frame, text="Start Date:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=6, column=0, sticky='w')

        # Start Date frame
        start_date_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        start_date_frame.grid(row=7, column=0, pady=(3, 0), sticky='w')

        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(start_date_frame, style='Input.TEntry', textvariable=self.start_date_var)
        self.start_date_entry.grid(row=0, column=0, sticky='w')

        # Edit End Date
        label = ttk.Label(left_frame, text="End Date:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=8, column=0, sticky='w')

        # End Date frame
        end_date_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        end_date_frame.grid(row=9, column=0, pady=(2, 0), sticky='w')

        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(end_date_frame, style='Input.TEntry', textvariable=self.end_date_var)
        self.end_date_entry.grid(row=0, column=0, sticky='w')


        # Button frame below Time Complexity
        button_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        button_frame.grid(row=2, column=0, pady=(8, 0), sticky='w')

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_action,
                               bg="#F08080", fg="#000000", font=("SF Pro Text", 10),
                               activebackground="#F49797", activeforeground="#000000")
        cancel_btn.grid(row=0, column=0, padx=(0, 8))

        # Confirm button
        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirm_action,
                                bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                                activebackground="#A8F0A8", activeforeground="#000000")
        confirm_btn.grid(row=0, column=1,padx=(0,8))

        # Delete button
        delete_btn = tk.Button(button_frame, text="Delete", command=self.delete_action,
                              bg="#FFA500", fg="#000000", font=("SF Pro Text", 10),
                              activebackground="#FFB347", activeforeground="#000000")
        delete_btn.grid(row=0, column=2)

        # Right column
        right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        right_frame.grid(row=0, column=1, padx=(8, 0), sticky='nsew')

        # Tags
        label = ttk.Label(right_frame, text="Task Tags:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w',pady=(2,0))
        
        # Create the tag text frame
        tag_frame = ttk.Frame(right_frame,style='MainFrame.TFrame')
        tag_frame.grid(row=1, column=0, pady=(0, 0), sticky='w')

        # Add a scrollbar for tags
        tag_scrollbar = ttk.Scrollbar(tag_frame, orient='vertical')
        tag_scrollbar.grid(row=1, column=1, sticky='ns')

        # Create the Text widget for tags
        self.task_tags_entry = tk.Text(tag_frame, height=7, width=12, bg='#d3d3d3', relief="solid", bd=1, font=("SF Pro Text", 10),
                                yscrollcommand=tag_scrollbar.set)  # Link scrollbar to the Text widget
        self.task_tags_entry.grid(row=1, column=0)

        # Configure the scrollbar to control tag_text
        tag_scrollbar.config(command=self.task_tags_entry.yview)
        
        # New frame specifically for Listbox and Scrollbar
        listLabel_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        listLabel_frame.grid(row=2, column=0, pady=(0, 0), sticky='w')

        listbox_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        listbox_frame.grid(row=3, column=0, pady=(0, 0), sticky='w')

        label = ttk.Label(listLabel_frame, text="Choose Tags:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w')
        
        # Add a vertical scrollbar for the Listbox
        list_scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical')
        list_scrollbar.grid(row=0, column=1, sticky='ns')  # Scrollbar placed next to the Listbox

        # Create the Listbox and link it to the scrollbar
        self.tag_listbox = tk.Listbox(listbox_frame, selectmode="multiple", exportselection=0, width=12,height=8,
                                      font=("SF Pro Text", 10), bg="#d3d3d3", relief='solid', yscrollcommand=tag_scrollbar.set)
        self.tag_listbox.grid(row=0, column=0, pady=(0, 0), sticky='w')

        # Configure the scrollbar to control the Listbox
        list_scrollbar.config(command=self.tag_listbox.yview)

        # Bind the Listbox selection to update the tag_text
        self.tag_listbox.bind("<<ListboxSelect>>", lambda _: self.update_tag_entry())

        # Timer frame
        timer_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        timer_frame.grid(row=4, column=0, pady=(8 ,0), sticky='nswe')

        # Edit Timer
        label = ttk.Label(timer_frame, text="Timer:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w',pady=(3,0))

        self.timer_var = tk.StringVar()
        self.task_time_entry = ttk.Entry(timer_frame, style='Input.TEntry', width=16,textvariable=self.timer_var)
        self.task_time_entry.grid(row=1, column=0, sticky='w',pady=(0,0))

        # Adds the tags loaded from the tags table into the listbox
        for value in values:
            self.tag_listbox.insert(tk.END, value)

    def on_close(self):
        try:
            self.grab_release()
        except Exception as e:
            print(f"Error releasing grab on close: {e}")
            
        self.main_app.edittask_window = None  # Reset when closed
        self.main_app.update_button.config(state=tk.NORMAL)
        self.destroy()
