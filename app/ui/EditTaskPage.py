
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import pathlib
import sqlite3
from datetime import date

main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"
background_color = "#A9A9A9"

class EditTaskWindow(tk.Tk):
    def __init__(self, task_id, main_app):
        super().__init__()
        self.task_id = task_id
        self.main_app = main_app
        self.main_app = main_app
        self.main_app.edittask_window = self
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Define path
        self.path = pathlib.Path(__file__).parent
        self.path = str(self.path).replace("EditTaskPage.py", '') + '\\Databases' + '\\task_list.db'
        self.configure_ui()
        self.load_task()



        conn = sqlite3.connect(self.path)
        c = conn.cursor()

        c.execute("SELECT * FROM TaskList WHERE task_id = ?", (int(task_id),))
        edit_task = c.fetchone()

        conn.close()

        print(self.edit_task)
        if self.edit_task:
            self.task_name_var = edit_task[0]
            self.task_time_var = edit_task[1]
            self.task_weight_var = edit_task[2]
            self.task_start_date_var = edit_task[4]
            self.task_end_date_var = edit_task[5]
            self.task_desc_var = edit_task[6]
            self.task_weight_type_var = edit_task[7]
            self.task_tags_var = edit_task[8]

        else:
            messagebox.showerror("Error", "Task not found!")
            self.destroy()

        self.insert_task()




    def load_task(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT * FROM TaskList WHERE task_id = ?", (int(self.task_id),))
        self.edit_task = c.fetchone()
        conn.close()


    def insert_task(self):
        self.task_name_entry.insert(0, self.edit_task[0])
        self.task_time_entry.insert(0, self.edit_task[1])
        self.value_combo.set(self.edit_task[2])
        self.start_date_entry.insert(0, self.edit_task[4])
        self.end_date_entry.insert(0, self.edit_task[5])
        self.type_combo.set(self.edit_task[7])
        self.desc_text_entry.insert("1.0", self.edit_task[6])
        self.task_tags_entry.insert(0, self.edit_task[8])

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
        # Implement the cancel action (e.g., close the window)
        self.on_close()

    def confirm_action(self):
        confirm = messagebox.askyesno("Confirm Edit", "Are you sure you want to edit this task?")
        if confirm:
            # Implement the confirm action (e.g., save the task data)
            conn = sqlite3.connect(self.path)
            c = conn.cursor()

            c.execute("""UPDATE TaskList SET task_name = ?, task_time = ?, task_weight = ?, task_start_date = ?, task_end_date = ?, task_description = ?, task_weight_type = ?, task_tags = ? WHERE task_id = ?
                    """, (self.task_name_entry.get(), self.task_time_entry.get(), self.value_combo.get(),
                            self.start_date_entry.get(), self.end_date_var.get(), self.desc_text_entry.get("1.0", "end-1c"),
                            self.type_combo.get(), self.task_tags_entry.get(), self.task_id))
            
            conn.commit()
            conn.close()

            if hasattr(self.main_app, 'query_database'):
                self.main_app.query_database()

            self.on_close()
        else:
            self.lift()
            self.focus_force()
            return

    def delete_action(self):
        pass


    #Configure the ui
    def configure_ui(self):
        # Set the main window geometry and title
        self.geometry("620x350")  # Increased height to accommodate additional fields
        self.title("Edit Task")
        self.configure(bg=background_color)  # Lighter Blue background
        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Text", size=14, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Text", size=10, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }
        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]

        # Style configurations
        self.style = ttk.Style(self)
        self.style.theme_use("alt")  # Using "alt" theme for better customization
        self.style.configure('MainFrame.TFrame', background=background_color)  # Lighter Blue for frames
        self.style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('Input.TCombobox', fieldbackground='#d3d3d3', background=background_color, font=("SF Pro Text", 10))
        self.style.configure('TLabel', background=background_color, font=("SF Pro Text", 10))  # Lighter Blue for labels
        self.style.configure('TButton', background=background_color, font=("SF Pro Text", 10))  # Default Lighter Blue for buttons

        # Custom button styles
        self.style.configure('ConfirmButton.TButton', background=main_btn_color, font=("SF Pro Text", 10))
        self.style.configure('CancelButton.TButton', background=del_btn_color, font=("SF Pro Text", 10))

        # Scrollbar style
        self.style.configure('Vertical.TScrollbar', troughcolor="#E0E0E0", background="#AED6F1", bordercolor=background_color, arrowcolor=background_color)

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Header frame
        header_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        header_frame.pack(fill='x', pady=(0, 6))

        # Task Name Label
        label = ttk.Label(header_frame, text="Edit Task Name:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Task Name Entry
        self.task_name_entry = ttk.Entry(header_frame, style='Input.TEntry', width=40)
        self.task_name_entry.pack(fill='x', pady=(3, 6))

        # Content container
        content_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        content_frame.pack(fill='both', expand=True)

        # Left column
        left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))

        # Description
        label = ttk.Label(left_frame, text="Edit Description:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Create a frame for the text and scrollbar
        desc_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        desc_frame.pack(fill='x', pady=(3, 6))

        # Text widget with scrollbar
        self.desc_text_entry = tk.Text(desc_frame, height=7, width=30, bg='#d3d3d3', relief="solid", bd=1,
                            font=("SF Pro Text", 10))
        self.desc_text_entry.pack(side='left', fill='both', expand=True)

        # Add a vertical scrollbar and apply the custom style
        scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=self.desc_text_entry.yview, style='Vertical.TScrollbar')
        scrollbar.pack(side='right', fill='y')

        # Link the scrollbar with the text widget
        self.desc_text_entry.configure(yscrollcommand=scrollbar.set)

        # Time Complexity with nested dropdowns (Moved below Description)
        label = ttk.Label(left_frame, text="Edit Time Complexity:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Complexity type frame
        complexity_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        complexity_frame.pack(fill='x', pady=(3, 6))

        # Type selector
        self.type_combo = ttk.Combobox(complexity_frame, values=self.complexity_types, style='Input.TCombobox', state='readonly')
        self.type_combo.pack(fill='x', pady=(0, 3))
        self.type_combo.set("Select Type")

        # Value selector
        self.value_combo = ttk.Combobox(complexity_frame, style='Input.TCombobox', state='readonly')
        self.value_combo.pack(fill='x')
        self.value_combo.set("Select Value")

        # Bind the type selection to update value options
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)

        # Button frame below Time Complexity
        button_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        button_frame.pack(fill='x', pady=(3, 6))

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_action,
                               bg="#F08080", fg="#000000", font=("SF Pro Text", 10),
                               activebackground="#F49797", activeforeground="#000000")
        cancel_btn.pack(side='left', padx=(0, 8))

        # Confirm button
        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirm_action,
                                bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                                activebackground="#A8F0A8", activeforeground="#000000")
        confirm_btn.pack(side='left')

        # Delete button
        delete_btn = tk.Button(button_frame, text="Delete", command=self.delete_action,
                              bg="#FFA500", fg="#000000", font=("SF Pro Text", 10),
                              activebackground="#FFB347", activeforeground="#000000")
        delete_btn.pack(side='right')
        
        # Right column
        right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        right_frame.pack(side='left', fill='both', expand=True)

        # Tags
        label = ttk.Label(right_frame, text="Edit Tags:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')
        self.task_tags_entry = ttk.Entry(right_frame, style='Input.TEntry')
        self.task_tags_entry.pack(fill='x', pady=(3, 6))

        # Edit Start Date
        label = ttk.Label(right_frame, text="Edit Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Start Date frame
        start_date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        start_date_frame.pack(fill='x', pady=(3, 6))

        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(start_date_frame, style='Input.TEntry', textvariable=self.start_date_var)
        self.start_date_entry.pack(fill='x')

        # Edit End Date
        label = ttk.Label(right_frame, text="Edit End Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # End Date frame
        end_date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        end_date_frame.pack(fill='x', pady=(3, 6))

        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(end_date_frame, style='Input.TEntry', textvariable=self.end_date_var)
        self.end_date_entry.pack(fill='x')

        # Edit Timer
        label = ttk.Label(right_frame, text="Edit Timer (HH:MM:SS):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Timer frame
        timer_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        timer_frame.pack(fill='x', pady=(8, 6))

        self.timer_var = tk.StringVar()
        self.task_time_entry = ttk.Entry(timer_frame, style='Input.TEntry', textvariable=self.timer_var)
        self.task_time_entry.pack(fill='x')

    def on_close(self):
        self.main_app.edittask_window = None  # Reset when closed
        self.main_app.update_button.config(state=tk.NORMAL)
        self.destroy()
