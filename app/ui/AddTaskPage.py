from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class AddTaskWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        # Set the main window geometry and title
        self.geometry("550x250")
        self.title("Add Task")
        self.configure(bg='#5DADE2')  # Lighter Blue background

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
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
        self.style.configure('Vertical.TScrollbar', troughcolor="#E0E0E0", background="#AED6F1", bordercolor="#5DADE2", arrowcolor="#5DADE2")

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

        # Frame to hold the description text and scrollbar
        desc_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        desc_frame.pack(fill='x', pady=(3, 6))

        # Scrollbar for the description
        desc_scrollbar = ttk.Scrollbar(desc_frame, orient='vertical', style="Vertical.TScrollbar")
        desc_scrollbar.pack(side='right', fill='y')

        # Text widget for description
        desc_text = tk.Text(
            desc_frame,
            height=7,
            width=30,
            bg='#d3d3d3',
            relief="solid",
            bd=1,
            font=("SF Pro Text", 10),
            yscrollcommand=desc_scrollbar.set
        )
        desc_text.pack(side='left', fill='both', expand=True)

        # Link scrollbar to text widget
        desc_scrollbar.config(command=desc_text.yview)

        # Button frame below the description
        button_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        button_frame.pack(fill='x', pady=(3, 6))

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_action,
                       bg="#F08080", fg="#000000", font=("SF Pro Text", 10),
                       relief="flat", activebackground="#F49797", activeforeground="#000000")
        cancel_btn.pack(side='left', padx=(0, 8))

        # Confirm button
        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirm_press,
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

        # Date Completed without validation
        label = ttk.Label(right_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        # Date frame to hold entry and potential validation message
        date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        date_frame.pack(fill='x', pady=(3, 6))

        # Date entry (text box)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(date_frame, style='Input.TEntry', textvariable=self.date_var)
        self.date_entry.pack(fill='x')

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

    def confirm_save(self):
        # Implement the confirm action (e.g., save the task data)
        self.destroy()  # Corrected line to close the Toplevel window

    def confirm_press(self):
        result = tk.messagebox.askyesno("Confirmation", "Are you sure you want to continue?",icon="question")
        if result:
            self.confirm_save()
        else:
            pass

# Run the application
if __name__ == "__main__":
    app = AddTaskWindow()
    app.mainloop()
