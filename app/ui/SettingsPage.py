from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
    
class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A9A9A9")
        self.controller = controller
        
        # Create a notebook for tabbed help content
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a tab for general help
        general_frame = tk.Frame(self.notebook, bg="#d3d3d3")
        self.notebook.add(general_frame, text="General Help")
        
        # Create a scrollable text widget for general help
        general_scroll = tk.Scrollbar(general_frame)
        general_scroll.pack(side="right", fill="y")
        
        general_text = tk.Text(general_frame, yscrollcommand=general_scroll.set, bg="#d3d3d3", wrap="word")
        general_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        general_scroll.config(command=general_text.yview)
        
        # Add general help information
        general_text.tag_configure("heading", font=("SF Pro Display", 12, "bold"))
        general_text.tag_configure("subheading", font=("SF Pro Display", 10, "bold"))
        
        general_text.insert(tk.END, "Task Manager Help\n\n", "heading")
        
        general_text.insert(tk.END, "Time Tracker\n", "subheading")
        general_text.insert(tk.END, "This is the main view where you can manage your tasks. You can add, edit, and delete tasks, as well as start and stop the timer for the current task.\n\n")
        
        general_text.insert(tk.END, "Completed Tasks\n", "subheading")
        general_text.insert(tk.END, "View and manage your completed tasks. You can restore tasks back to the active list or archive them.\n\n")
        
        general_text.insert(tk.END, "Small Overlay\n", "subheading")
        general_text.insert(tk.END, "A minimal view that shows just the current task and timer controls. Useful when you want to keep the timer visible while working on other things.\n\n")
        
        general_text.insert(tk.END, "Tags Database\n", "subheading")
        general_text.insert(tk.END, "Manage the tags used to categorize your tasks. You can add, edit, and delete tags here.\n\n")
        
        general_text.insert(tk.END, "Analytics\n", "subheading")
        general_text.insert(tk.END, "View statistics and visualizations of your task data. See how you're spending your time and identify trends.\n\n")
        
        general_text.insert(tk.END, "Archive\n", "subheading")
        general_text.insert(tk.END, "Access archived tasks that are no longer needed in the completed tasks list. You can restore tasks from here if needed.\n\n")
        
        general_text.insert(tk.END, "Data Management\n", "subheading")
        general_text.insert(tk.END, "The application automatically backs up your database regularly. You can also manually create backups and restore from previous backups using the options in the menu.\n\n")
        
        # Make the text widget read-only
        general_text.config(state="disabled")
        
        # About tab
        about_frame = tk.Frame(self.notebook, bg="#d3d3d3")
        self.notebook.add(about_frame, text="About")
        
        # About content
        about_label = tk.Label(
            about_frame,
            text="Task Manager\nVersion 1.0\n\nA simple task management application with time tracking capabilities.",
            font=("SF Pro Display", 10),
            bg="#d3d3d3",
            justify="center"
        )
        about_label.pack(pady=20)
        
        # Header
        header_frame = tk.Frame(self, bg="#A9A9A9")
        header_frame.pack(fill="x", pady=(10, 0))
        
        title_label = tk.Label(
            header_frame,
            text="Help & Documentation",
            font=("SF Pro Display", 14, "bold"),
            bg="#A9A9A9"
        )
        title_label.pack(pady=5)