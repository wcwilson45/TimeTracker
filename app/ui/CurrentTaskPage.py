import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import messagebox


class CurrentTaskWindow(tk.Tk):
    _instance = None  # Class variable to track the active instance

    def __new__(cls):
        # If there's already an instance, bring it to front instead of creating a new one
        if cls._instance is not None:
            cls._instance.lift()  # Brings existing window to front
            cls._instance.focus_force()  # Forces focus on existing window
            return cls._instance
        return super().__new__(cls)

    def __init__(self):
        # Only initialize if this is a new instance
        if not CurrentTaskWindow._instance:
            super().__init__()
            CurrentTaskWindow._instance = self

            # Bind the window closing event
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Set the main window geometry and title
            self.geometry("620x350")  # Increased height to accommodate additional fields
            self.title("Current Task")
            self.configure(bg='#5DADE2')  # Lighter Blue background
            self.resizable(False, False)  # Prevent window resizing
            #self.attributes('-toolwindow', True)  # Remove maximize button (Windows only)

            # Create fonts
            self.fonts = {
                'header': tkfont.Font(family="SF Pro Display", size=14, weight="bold"),
                'subheader': tkfont.Font(family="SF Pro Display", size=10, weight="bold"),
                'body': tkfont.Font(family="SF Pro Text", size=10)
            }

            # Style configurations
            self.style = ttk.Style(self)
            self.style.theme_use("alt")  # Using "alt" theme for better customization
            self.style.configure('MainFrame.TFrame', background='#5DADE2')  # Lighter Blue for frames
            self.style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
            self.style.configure('TLabel', background='#5DADE2', font=("SF Pro Text", 10))  # Lighter Blue for labels
            self.style.configure('TButton', background='#5DADE2',
                                 font=("SF Pro Text", 10))  # Default Lighter Blue for buttons

            # Custom button styles
            self.style.configure('ConfirmButton.TButton', background='#90EE90', font=("SF Pro Text", 10))
            self.style.configure('CancelButton.TButton', background='#F08080', font=("SF Pro Text", 10))

            # Scrollbar style
            self.style.configure('Vertical.TScrollbar', troughcolor="#E0E0E0", background="#AED6F1",
                                 bordercolor="#5DADE2", arrowcolor="#5DADE2")

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
            scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=desc_text.yview,
                                      style='Vertical.TScrollbar')
            scrollbar.pack(side='right', fill='y')

            # Link the scrollbar with the text widget
            desc_text.configure(yscrollcommand=scrollbar.set)

            # Time Complexity with text entries instead of dropdowns
            label = ttk.Label(left_frame, text="Time Complexity:", font=self.fonts['subheader'], style='TLabel')
            label.pack(anchor='w')

            # Complexity type frame
            complexity_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
            complexity_frame.pack(fill='x', pady=(3, 6))

            # Type entry (replacing type_combo)
            self.type_entry = ttk.Entry(complexity_frame, style='Input.TEntry')
            self.type_entry.pack(fill='x', pady=(0, 3))

            # Value entry (replacing value_combo)
            self.value_entry = ttk.Entry(complexity_frame, style='Input.TEntry')
            self.value_entry.pack(fill='x')

            # Button frame below Time Complexity
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

            # Edit Start Date
            label = ttk.Label(right_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'],
                              style='TLabel')
            label.pack(anchor='w')

            # Start Date frame
            start_date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
            start_date_frame.pack(fill='x', pady=(3, 6))

            self.start_date_var = tk.StringVar()
            self.start_date_entry = ttk.Entry(start_date_frame, style='Input.TEntry', textvariable=self.start_date_var)
            self.start_date_entry.pack(fill='x')

            # Edit End Date
            label = ttk.Label(right_frame, text="End Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
            label.pack(anchor='w')

            # End Date frame
            end_date_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
            end_date_frame.pack(fill='x', pady=(3, 6))

            self.end_date_var = tk.StringVar()
            self.end_date_entry = ttk.Entry(end_date_frame, style='Input.TEntry', textvariable=self.end_date_var)
            self.end_date_entry.pack(fill='x')

            # Edit Timer
            label = ttk.Label(right_frame, text="Timer (HH:MM:SS):", font=self.fonts['subheader'], style='TLabel')
            label.pack(anchor='w')

            # Timer frame
            timer_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
            timer_frame.pack(fill='x', pady=(8, 6))

            self.timer_var = tk.StringVar()
            self.timer_entry = ttk.Entry(timer_frame, style='Input.TEntry', textvariable=self.timer_var)
            self.timer_entry.pack(fill='x')

    def on_closing(self):
        # Reset the instance reference and destroy the window
        CurrentTaskWindow._instance = None
        self.destroy()

    def cancel_action(self):
        # Reset instance reference and destroy the window
        CurrentTaskWindow._instance = None
        self.destroy()

    def confirm_action(self):
        confirm = messagebox.askyesno(
            "Confirm Task:",
            "Are you sure you want to complete this task?",
            icon='question'
        )

        if confirm:
            # Reset instance reference and destroy the window
            CurrentTaskWindow._instance = None
            self.destroy()