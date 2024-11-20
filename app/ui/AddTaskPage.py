from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.font as tkfont
import re
from datetime import datetime

class AddTaskWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("550x300")
        self.title("Add Task")
        self.configure(bg='#f0f0f0')

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=32, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=11, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }
        
        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]
        
        # Style configurations
        style = Style()
        style.configure('MainFrame.TFrame', background='#f0f0f0')
        style.configure('Input.TFrame', background='#f0f0f0')
        style.configure('Input.TEntry', fieldbackground='white', font=("SF Pro Text", 10))
        style.configure('Input.TCombobox', fieldbackground='white', font=("SF Pro Text", 10))
        style.configure('TLabel', background='#f0f0f0', font=("SF Pro Text", 10))
        
        # Main container
        main_frame = Frame(self, style='MainFrame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Header frame
        header_frame = Frame(main_frame, style='MainFrame.TFrame')
        header_frame.pack(fill='x', pady=(0,6))
        
        # Task Name Label
        Label(header_frame, text="Task Name", font=self.fonts['header'],
              style='TLabel').pack(side='left')

        # Content container
        content_frame = Frame(main_frame, style='MainFrame.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        # Left column
        left_frame = Frame(content_frame, style='MainFrame.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0,8))
        
        # Description
        Label(left_frame, text="Description:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        desc_text = tk.Text(left_frame, height=7, width=30, bg='white',
                           relief="solid", bd=1, font=self.fonts['body'])
        desc_text.pack(fill='x', pady=(3,6))
        
        # Right column
        right_frame = Frame(content_frame, style='MainFrame.TFrame')
        right_frame.pack(side='left', fill='both', expand=True)
        
        # Tags
        Label(right_frame, text="Tags:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        Entry(right_frame, style='Input.TEntry').pack(fill='x', pady=(3,6))
        
        # Time Complexity with nested dropdowns
        Label(right_frame, text="Time Complexity:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        
        # Complexity type frame
        complexity_frame = Frame(right_frame, style='MainFrame.TFrame')
        complexity_frame.pack(fill='x', pady=(3,6))
        
        # Type selector
        self.type_combo = Combobox(complexity_frame, 
                                 values=self.complexity_types,
                                 style='Input.TCombobox',
                                 state='readonly')
        self.type_combo.pack(fill='x', pady=(0,3))
        self.type_combo.set("Select Type")
        
        # Value selector
        self.value_combo = Combobox(complexity_frame,
                                  style='Input.TCombobox',
                                  state='readonly')
        self.value_combo.pack(fill='x')
        self.value_combo.set("Select Value")
        
        # Bind the type selection to update value options
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)
        
        # Date Completed with format validation
        Label(right_frame, text="Date Completed (MM-DD-YYYY):", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        
        # Date frame to hold entry and validation message
        date_frame = Frame(right_frame, style='MainFrame.TFrame')
        date_frame.pack(fill='x', pady=(3,6))
        
        # Create StringVar for the date entry
        self.date_var = StringVar()
        self.date_var.trace('w', self.validate_date_format)
        
        # Date entry
        self.date_entry = Entry(date_frame, 
                              style='Input.TEntry',
                              textvariable=self.date_var)
        self.date_entry.pack(fill='x')
        
        # Validation message label
        self.validation_label = Label(date_frame, 
                                    text="", 
                                    font=self.fonts['body'],
                                    foreground='red',
                                    style='TLabel')
        self.validation_label.pack(anchor='w')

        # Bottom buttons frame
        buttons_frame = Frame(main_frame, style='MainFrame.TFrame')
        buttons_frame.pack(fill='x', pady=(3,0))
        
        # Container for left-aligned buttons
        left_buttons = Frame(buttons_frame, style='MainFrame.TFrame')
        left_buttons.pack(side='left')
        
        # Cancel button (light red with black text)
        cancel_btn = tk.Label(left_buttons, 
                            text="Cancel", 
                            bg="#F08080",
                            fg="black",
                            font=self.fonts['body'],
                            padx=15,
                            pady=5)
        cancel_btn.pack(side='left', padx=(0,8))
        
        # Confirm button (light green with black text)
        confirm_btn = tk.Label(left_buttons, 
                             text="Confirm", 
                             bg="#90EE90",
                             fg="black",
                             font=self.fonts['body'],
                             padx=15,
                             pady=5)
        confirm_btn.pack(side='left')

    def update_values(self, event=None):
        """Update the values dropdown based on the selected type"""
        selected_type = self.type_combo.get()
        
        if selected_type == "T-Shirt Size":
            self.value_combo['values'] = self.tshirt_sizes
        elif selected_type == "Fibonacci":
            self.value_combo['values'] = self.fibonacci
        else:
            self.value_combo['values'] = []
            
        self.value_combo.set("Select Value")

    def validate_date_format(self, *args):
        """Validate the date format as MM-DD-YYYY"""
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

