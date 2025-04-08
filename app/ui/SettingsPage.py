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
        
        # Create a tab for keyboard shortcuts
        shortcuts_frame = tk.Frame(self.notebook, bg="#d3d3d3")
        
        # Create a scrollable text widget for the shortcuts
        shortcut_scroll = tk.Scrollbar(shortcuts_frame)
        shortcut_scroll.pack(side="right", fill="y")
        
        shortcut_text = tk.Text(shortcuts_frame, yscrollcommand=shortcut_scroll.set, bg="#d3d3d3", wrap="word")
        shortcut_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        shortcut_scroll.config(command=shortcut_text.yview)
        
        # Add shortcut information
        shortcut_text.tag_configure("heading", font=("SF Pro Display", 12, "bold"))
        shortcut_text.tag_configure("subheading", font=("SF Pro Display", 10, "bold"))
        shortcut_text.tag_configure("shortcut", font=("SF Pro Text", 9, "bold"))
        
        shortcut_text.insert(tk.END, "Keyboard Shortcuts\n\n", "heading")
        
        shortcut_text.insert(tk.END, "Global Shortcuts\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+Q: ", "shortcut")
        shortcut_text.insert(tk.END, "Exit application\n")
        shortcut_text.insert(tk.END, "F1: ", "shortcut")
        shortcut_text.insert(tk.END, "Show this help\n")
        shortcut_text.insert(tk.END, "Ctrl+P: ", "shortcut")
        shortcut_text.insert(tk.END, "Preferences\n\n")
        
        shortcut_text.insert(tk.END, "Navigation\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+1: ", "shortcut")
        shortcut_text.insert(tk.END, "Time Tracker\n")
        shortcut_text.insert(tk.END, "Ctrl+2: ", "shortcut")
        shortcut_text.insert(tk.END, "Completed Tasks\n")
        shortcut_text.insert(tk.END, "Ctrl+3: ", "shortcut")
        shortcut_text.insert(tk.END, "Small Overlay\n")
        shortcut_text.insert(tk.END, "Ctrl+4: ", "shortcut")
        shortcut_text.insert(tk.END, "Tags Database\n")
        shortcut_text.insert(tk.END, "Ctrl+5: ", "shortcut")
        shortcut_text.insert(tk.END, "Analytics\n")
        shortcut_text.insert(tk.END, "Ctrl+6: ", "shortcut")
        shortcut_text.insert(tk.END, "Archive\n\n")
        
        shortcut_text.insert(tk.END, "Task Management\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+N: ", "shortcut")
        shortcut_text.insert(tk.END, "Add new task\n")
        shortcut_text.insert(tk.END, "Ctrl+E: ", "shortcut")
        shortcut_text.insert(tk.END, "Edit selected task\n")
        shortcut_text.insert(tk.END, "Ctrl+H: ", "shortcut")
        shortcut_text.insert(tk.END, "View task history\n")
        shortcut_text.insert(tk.END, "Ctrl+Delete: ", "shortcut")
        shortcut_text.insert(tk.END, "Delete selected task\n\n")
        
        shortcut_text.insert(tk.END, "Timer Controls\n", "subheading")
        shortcut_text.insert(tk.END, "F5: ", "shortcut")
        shortcut_text.insert(tk.END, "Start timer\n")
        shortcut_text.insert(tk.END, "F6: ", "shortcut")
        shortcut_text.insert(tk.END, "Stop timer\n\n")
        
        shortcut_text.insert(tk.END, "List Operations\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+A: ", "shortcut")
        shortcut_text.insert(tk.END, "Select all items\n")
        shortcut_text.insert(tk.END, "Ctrl+F: ", "shortcut")
        shortcut_text.insert(tk.END, "Search\n")
        shortcut_text.insert(tk.END, "Escape: ", "shortcut")
        shortcut_text.insert(tk.END, "Deselect all items\n\n")
        
        shortcut_text.insert(tk.END, "Data Management\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+B: ", "shortcut")
        shortcut_text.insert(tk.END, "Backup database\n")
        shortcut_text.insert(tk.END, "Ctrl+R: ", "shortcut")
        shortcut_text.insert(tk.END, "Restore database\n")
        
        # Make the text widget read-only
        shortcut_text.config(state="disabled")
        
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
        
