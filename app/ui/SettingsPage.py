from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

background_color = "#A9A9A9"
grey_button_color = "#d3d3d3"
main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"

class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_color)
        self.controller = controller
        
        # Configure style to match ArchiveTasksList
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#d3d3d3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#d3d3d3")

        style.map("Treeview", background=[('selected', "347083")])
        
        # Create a notebook for tabbed help content
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # General help tab
        general_frame = tk.Frame(self.notebook, bg=grey_button_color)
        self.notebook.add(general_frame, text="General Help")
        
        # Make the general frame expand to fill the notebook tab
        general_frame.pack_propagate(False)
        
        # Set a minimum height for the general frame
        general_frame.config(height=500)  # Set the frame height to 500 pixels
        
        # Create a frame for scrollable content - explicitly fill all available space
        general_content_frame = tk.Frame(general_frame, bg=grey_button_color)
        general_content_frame.pack(fill="both", expand=True, pady=5, padx=0)
        
        # Create a scrollable text widget with matching style
        general_scroll = Scrollbar(general_content_frame)
        general_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        general_text = tk.Text(general_content_frame, 
                             yscrollcommand=general_scroll.set, 
                             bg=grey_button_color, 
                             wrap="word",
                             bd=0,
                             highlightthickness=0,
                             height=30)  # Set a tall height for the text widget
        general_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        general_scroll.config(command=general_text.yview)
        
        # Add general help information
        general_text.tag_configure("heading", font=("SF Pro Display", 12, "bold"))
        general_text.tag_configure("subheading", font=("SF Pro Display", 10, "bold"))
        
        general_text.insert(tk.END, "Task Manager Help\n\n", "heading")
        
        general_text.insert(tk.END, "Time Tracker\n", "subheading")
        general_text.insert(tk.END, "This is the main view where you can manage your tasks. You can add, edit, and delete tasks, as well as start and stop the timer for the current task.\n\n")
        general_text.insert(tk.END, "Start and Stop: When a current task is selected press these buttons to start and stop teh timer.\n\n")
        general_text.insert(tk.END, "Current Task Complete Button: Used to complete teh current task.\n\n")
        general_text.insert(tk.END, "Current Task Commit History: Get the commit history of the current task\n\n")
        general_text.insert(tk.END, "Current Task Edit Button: Used to edit the current task\n\n")
        general_text.insert(tk.END, "Move Up and Down: When a task is selected in the task list clikc these buttons to move the task up or down.\n\n")
        general_text.insert(tk.END, "Complete Task: Used to complete the selected task in the task list\n\n")
        general_text.insert(tk.END, "Import Button: Used to import an excel file to the task list (Duplicates will not be added).\n\n")
        general_text.insert(tk.END, "Edit Task: Edits the selected task in the task list.\n\n")
        general_text.insert(tk.END, "Add Task: Used to manually add a new task into the task list.\n\n")
        general_text.insert(tk.END, "Select Task: Is used to move a selected task in the task list into the current task.\n\n")
        general_text.insert(tk.END, "Remove All: Removes all tasks from the task list\n\n\n")
        
        general_text.insert(tk.END, "Completed Tasks\n", "subheading")
        general_text.insert(tk.END, "View and manage your completed tasks. You can restore tasks back to the active list or archive them.\n\n")
        general_text.insert(tk.END, "Export: Used to export the completed tasks list inot an excel file.\n\n")
        general_text.insert(tk.END, "Commit History: When a task is selected in the completed task list this shows that tasks commit history.\n\n")
        general_text.insert(tk.END, "Undo Commit: Moves the selected completed task back into the task list.\n\n")
        general_text.insert(tk.END, "Delete: Moves the selected completed task into the archive task list.\n\n")
        general_text.insert(tk.END, "Delete All: Moves all completed tasks into the archive task list.\n\n\n")
        
        general_text.insert(tk.END, "Small Overlay\n", "subheading")
        general_text.insert(tk.END, "A minimal view that shows just the current task and timer controls. Useful when you want to keep the timer visible while working on other things.\n\n")
        
        general_text.insert(tk.END, "Tags Database\n", "subheading")
        general_text.insert(tk.END, "Manage the tags used to categorize your tasks. You can add, edit, and delete tags here.\n\n")
        general_text.insert(tk.END, "Import: Import an excel file into the tags list.\n\n")
        general_text.insert(tk.END, "Export: Download an excel file of the current tags list.\n\n")
        general_text.insert(tk.END, "Add Tag: In the tag name and description entry box input your tag data then click the button to add a tag to the tag list.\n\n")
        general_text.insert(tk.END, "Update Tag: Click to update the tag list if it is not auto updating.\n\n")
        general_text.insert(tk.END, "Clear Tag: Removes the selected tag from the entry boxes.\n\n")
        general_text.insert(tk.END, "Delete Tag: Deletes the selected tag\n\n")
        general_text.insert(tk.END, "Remove All: Deletes all tags\n\n\n")

        
        general_text.insert(tk.END, "Analytics\n", "subheading")
        general_text.insert(tk.END, "View statistics and visualizations of your task data. See how you're spending your time and identify trends.\n\n")
        
        general_text.insert(tk.END, "Archive\n", "subheading")
        general_text.insert(tk.END, "Access archived tasks that are no longer needed in the completed tasks list. You can restore tasks from here if needed.\n\n")
        general_text.insert(tk.END, "Export: Exports the archive task list to an excel file.\n\n")
        general_text.insert(tk.END, "Restore Task: Moves the selcted archived task back into the task list\n\n")
        general_text.insert(tk.END, "Delete: Completely remove the selected task.\n\n")
        general_text.insert(tk.END, "Delete All: Completely remove the entire archive task list.\n\n\n")
        
        general_text.insert(tk.END, "Data Management\n", "subheading")
        general_text.insert(tk.END, "The application automatically backs up your database regularly. You can also manually create backups and restore from previous backups using the options in the menu.\n\n")
        
        # Make the text widget read-only
        general_text.config(state="disabled")
        
        # About tab
        about_frame = tk.Frame(self.notebook, bg=grey_button_color)
        self.notebook.add(about_frame, text="About")
        
        # Set a minimum height for the about frame too
        about_frame.config(height=500)  # Set the frame height to 500 pixels
        about_frame.pack_propagate(False)  # Prevent the frame from shrinking
        
        # About content with matching style
        about_label = tk.Label(
            about_frame,
            text="Task Manager\nVersion 1.0\n\nA simple task management application with time tracking capabilities.",
            font=("SF Pro Display", 10),
            bg=grey_button_color,
            justify="center"
        )
        about_label.pack(pady=20)