from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import re
from datetime import datetime

class AddTaskWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the main window geometry and title
        self.geometry("550x250")
        self.title("Add Task")
        self.configure(bg='#5DADE2')  # Lighter Blue background

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=28, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=8, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }

        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]

        # Style configurations
        self.style = ttk.Style(self)
        self.style.theme_use("alt")
        self.style.configure('MainFrame.TFrame', background='#5DADE2')  # Lighter Blue for frames
        self.style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('Input.TCombobox', fieldbackground='#d3d3d3', background="#5DADE2", font=("SF Pro Text", 10))
        self.style.configure('TLabel', background='#5DADE2', font=("SF Pro Text", 8))  # Lighter Blue for labels
        self.style.configure('TButton', background='#5DADE2', font=("SF Pro Text", 10))  # Default Lighter Blue for buttons

        # Custom button styles
        self.style.configure('ConfirmButton.TButton', background='#90EE90', font=("SF Pro Text", 10))
        self.style.configure('CancelButton.TButton', background='#F08080', font=("SF Pro Text", 10))

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Header frame
        header_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        header_frame.pack(fill='x', pady=(0, 6))

        # Task Name Label
        label = ttk.Label(header_frame, text="Task Name", font=self.fonts['header'], style='TLabel')
        label.pack(side='left', padx=(0, 10))

        # Task Name Entry
        self.task_name_entry = ttk.Entry(header_frame, style='Input.TEntry', width=40)
        self.task_name_entry.pack(side='left', fill='x', expand=True)

        # Content container
        content_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        content_frame.pack(fill='both', expand=True)

        # Left column
        left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))

        # Description
        label = ttk.Label(left_frame, text="Description:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')
        desc_text = tk.Text(left_frame, height=7, width=30, bg='#d3d3d3', relief="solid", bd=1, font=("SF Pro Text", 10))
        desc_text.pack(fill='x', pady=(3, 6))

        # Button frame below the description
        button_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        button_frame.pack(fill='x', pady=(3, 6))

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_action,
                       bg="#F08080", fg="#000000", font=("SF Pro Text", 10),
                       relief="flat", activebackground="#F49797", activeforeground="#000000")
        cancel_btn.pack(side='left', padx=(0, 8))

        # Confirm button
        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirm_action,
                        bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                        relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        confirm_btn.pack(side='left')

        # Right column
        right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        right_frame.pack(side='left', fill='both', expand=True)

        # Tags
        label = ttk.Label(right_frame, text="Tags:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')
        tag_entry = ttk.Entry(right_frame, style='Input.TEntry')
        tag_entry.pack(fill='x', pady=(3, 6))

        # Time Complexity with nested dropdowns
        label = ttk.Label(right_frame, text="Time Complexity:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Complexity type frame
        complexity_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
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

        # Date Completed with format validation
        label = ttk.Label(right_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Date frame to hold entry and validation message
        date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        date_frame.pack(fill='x', pady=(3, 6))

        # Create StringVar for the date entry
        self.date_var = tk.StringVar()
        self.date_var.trace('w', self.validate_date_format)

        # Date entry
        self.date_entry = ttk.Entry(date_frame, style='Input.TEntry', textvariable=self.date_var)
        self.date_entry.pack(fill='x')

        # Validation message label
        self.validation_label = ttk.Label(date_frame, text="", font=self.fonts['body'], foreground='red', style='TLabel')
        self.validation_label.pack(anchor='w')

    def update_values(self, event=None):
        selected_type = self.type_combo.get()
        if selected_type == "T-Shirt Size":
            self.value_combo['values'] = self.tshirt_sizes
        elif selected_type == "Fibonacci":
            self.value_combo['values'] = self.fibonacci
        else:
            self.value_combo['values'] = []
        self.value_combo.set("Select Value")

    def validate_date_format(self, *args):
        date_str = self.date_var.get()
        if not date_str:
            self.validation_label.config(text="")
            return
        if not re.match(r'^\d{0,2}-?\d{0,2}-?\d{0,4}$', date_str):
            self.validation_label.config(text="Use format: MM-DD-YYYY")
            return
        if re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
            try:
                datetime.strptime(date_str, '%m-%d-%Y')
                self.validation_label.config(text="")
            except ValueError:
                self.validation_label.config(text="Invalid date")
        else:
            if len(date_str) in [2, 5] and not date_str.endswith('-'):
                self.date_var.set(date_str + '-')

    def cancel_action(self):
        # Implement the cancel action (e.g., close the window)
        self.destroy()

    def confirm_action(self):
        # Implement the confirm action (e.g., save the task data)
        pass
