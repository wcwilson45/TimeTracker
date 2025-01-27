from tkinter import ttk as ttk
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
from datetime import date

class AddTaskWindow(tk.Tk):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the "X" button to a custom method
         # Make window not maximizable
        self.resizable(False, False)

        # Set the main window geometry and title
        self.geometry("520x275")  # Increased height to accommodate additional fields
        self.title("Add Task")
        self.configure(bg='#5DADE2')  # Lighter Blue background

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
        self.style.theme_use("alt")  # Using "alt" theme for better customization
        self.style.configure('MainFrame.TFrame', background='#5DADE2')  # Lighter Blue for frames
        self.style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('Input.TCombobox', fieldbackground='#d3d3d3', background="#5DADE2", font=("SF Pro Text", 10))
        self.style.configure('TLabel', background='#5DADE2', font=("SF Pro Text", 10))  # Lighter Blue for labels
        self.style.configure('TButton', background='#5DADE2', font=("SF Pro Text", 10))  # Default Lighter Blue for buttons

        # Custom button styles
        self.style.configure('ConfirmButton.TButton', background='#90EE90', font=("SF Pro Text", 10))
        self.style.configure('CancelButton.TButton', background='#F08080', font=("SF Pro Text", 10))

        # Scrollbar style
        self.style.configure('Vertical.TScrollbar', troughcolor="#E0E0E0", background="#AED6F1", bordercolor="#5DADE2", arrowcolor="#5DADE2")

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Header frame
        header_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        header_frame.pack(fill='x', pady=(0, 6))

        # Task Name Label
        label = ttk.Label(header_frame, text="Task Name:", font=self.fonts['subheader'], style='TLabel')
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
        label = ttk.Label(left_frame, text="Description:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Create a frame for the text and scrollbar
        desc_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        desc_frame.pack(fill='x', pady=(3, 6))

        # Text widget with scrollbar
        desc_text = tk.Text(desc_frame, height=7, width=30, bg='#d3d3d3', relief="solid", bd=1,
                            font=("SF Pro Text", 10))
        desc_text.pack(side='left', fill='both', expand=True)

        # Add a vertical scrollbar and apply the custom style
        scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=desc_text.yview, style='Vertical.TScrollbar')
        scrollbar.pack(side='right', fill='y')

        # Link the scrollbar with the text widget
        desc_text.configure(yscrollcommand=scrollbar.set)

        # Button frame below Description
        button_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        button_frame.pack(fill='x', pady=(10, 5))

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_action,
                               bg="#F08080", fg="#000000", font=("SF Pro Text", 10),
                               relief="flat", activebackground="#F49797", activeforeground="#000000")
        cancel_btn.pack(side='left', padx=(10, 5))

        # Confirm button
        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirm_action,
                                bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                                relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        confirm_btn.pack(side='left')

        #Autofill today's date button
        autofill_date_btn = tk.Button(button_frame, text="Autofill date", command=self.autofill_date,
                                bg="#A020F0", fg="#000000", font=("SF Pro Text", 10),
                                relief="flat", activebackground="#800080", activeforeground="#000000")
        autofill_date_btn.pack(side='right')

        # Right column
        right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        right_frame.pack(side='left', fill='both', expand=True)

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

        # Tags
        label = ttk.Label(right_frame, text="Tags:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')
        tag_entry = ttk.Entry(right_frame, style='Input.TEntry')
        tag_entry.pack(fill='x', pady=(3, 6))

        # Start Date
        label = ttk.Label(right_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Start Date frame
        start_date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        start_date_frame.pack(fill='x', pady=(3, 6))

        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(start_date_frame, style='Input.TEntry', textvariable=self.start_date_var)
        self.start_date_entry.pack(fill='x')

    def on_close(self):
        # Reset the reference in the parent App class
        if self.parent:
            self.parent.add_task_window = None
        # Destroy the window
        self.destroy()

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
        self.destroy()

        #Reset the refernece in the parent app
        if self.parent:
            self.parent.add_task_window = None

    def confirm_action(self):
        confirm = messagebox.askyesno("Confirm Add", "Are you sure you want to add this task?")
        if confirm:
            # Logic to save the task
            pass
        else:
            return
    def autofill_date(self):
        CurrentDate = date.today()
        self.start_date_entry.delete(0, "end")
        self.start_date_entry.insert(0, CurrentDate.strftime("%m-%d-%Y"))
