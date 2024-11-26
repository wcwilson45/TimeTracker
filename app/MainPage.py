from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from ui import (
    SmallOverlayWindow,
    CompletedTasksWindow,
    EditTaskWindow,
    CommitHistoryWindow,
    AddTaskWindow
)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x600")
        root.resizable(width = 0, height = 0)

        # Background color hex code
        self.root.configure(bg="#5DADE2")

        # Font Tuples for Use on pages
        self.fonts = {
            "Title_Tuple": tkfont.Font(family ="SF Pro Display", size =24, weight ="bold"),
            "Body_Tuple": tkfont.Font(family = "SF Pro Text", size = 12, weight = "bold"),
            "Description_Tuple": tkfont.Font(family = "Sf Pro Text", size = 12)
        }

        # Main Container
        self.main_container = tk.Frame(root, background="#5DADE2")
        self.main_container.pack(expand=False, fill="both")

        # Menu Button Frame
        self.menu_frame = tk.Frame(self.main_container, background="#5DADE2")
        self.menu_frame.pack(fill="x", padx=5, pady=5)

        # DropDown Menu
        self.menu_button = ttk.Button(self.menu_frame, text="⋮", width=3, command=self.show_menu)
        self.menu_button.pack(side="left", padx=5)

        # Page Title Label
        self.page_title = ttk.Label(self.menu_frame, text="Full", font=self.fonts['Body_Tuple'], background="#5DADE2")
        self.page_title.pack(side="left", padx=10)

        self.time_box_full = None
        self.time_box_overlay = None

        # Create pages
        self.full_page = tk.Frame(self.main_container)
        self.completedtasks_page = tk.Frame(self.main_container)
        self.smalloverlay_page = tk.Frame(self.main_container)

        # Show main page at initialization
        self.current_page = self.full_page
        self.full_page.pack(expand=True, fill="both", padx=10, pady=5)

        # Create the popup menu
        self.popup_menu = tk.Menu(root, tearoff=0)
        self.popup_menu.add_command(label="Full Page", command=lambda: self.switch_page("Full"))
        self.popup_menu.add_command(label="Completed Tasks", command=lambda: self.switch_page("Completed Tasks"))
        self.popup_menu.add_command(label="Small Overlay", command=lambda: self.switch_page("Small Overlay"))

        self.setup_full_page()
        self.setup_completedtasks_page()
        self.setup_smalloverlay_page()

    def show_menu(self):
        try:
            self.popup_menu.tk_popup(
                self.menu_button.winfo_rootx(),
                self.menu_button.winfo_rooty() + self.menu_button.winfo_height()
            )
        finally:
            self.popup_menu.grab_release()

    def switch_page(self, page_name):
        self.current_page.pack_forget()

        if page_name == "Full":
            self.current_page = self.full_page
            self.page_title.config(text="Full", background="#5DADE2")
            self.root.geometry("600x600")
        elif page_name == "Completed Tasks":
            self.current_page = self.completedtasks_page
            self.page_title.config(text="Completed Tasks", background="#5DADE2")
            self.root.geometry("700x300")
        elif page_name == "Small Overlay":
            self.current_page = self.smalloverlay_page
            self.page_title.config(text="Small Overlay", background="#5DADE2")
            self.root.geometry("230x160")


        self.current_page.pack(expand=True, fill="both", padx=10, pady=5)

    def setup_smalloverlay_page(self):
        self.smalloverlay_page.configure(bg='#5DADE2')
        Label(self.smalloverlay_page, text="Task Name:", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=0,
                                                                                                           column=0,
                                                                                                           sticky=W,
                                                                                                           pady=2)
        Label(self.smalloverlay_page, text="Time:", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=1, column=0,
                                                                                                      sticky=W, pady=2)

        # Timer section
        self.time_box_overlay = Text(self.smalloverlay_page, height=1, width=10, font=self.fonts['Body_Tuple'], background = "#d3d3d3")
        self.time_box_overlay.grid(row=1, column=0, padx=50, pady=5, sticky=E)
        self.time_box_overlay.insert("1.0", "00:00:00")  # Initial timer text
        self.time_box_overlay.config(state=DISABLED)  # Make it read-only
        
        print(f"Initialized time_box_overlay: {self.time_box_overlay}")

        self.small_overlay_start_button = tk.Button(self.smalloverlay_page, text="Start",relief = "flat", background="#77DD77", command=self.start_timer)
        self.small_overlay_start_button.grid(row=2, column=0, sticky=W,padx = 0, pady=5)

        self.small_overlay_stop_button = tk.Button(self.smalloverlay_page, text="Stop",relief = "flat", background="#FF7276", command=self.stop_timer)
        self.small_overlay_stop_button.grid(row=2, column=0, sticky=W,padx = 45, pady=5)


        self.reset_timer_values()

    def update_timer_boxes(self, time_text):
        """Update the timer display in both timer boxes."""
        # Update the timer on the Full page
        if self.time_box_full:
            self.time_box_full.config(state=NORMAL)
            self.time_box_full.delete("1.0", tk.END)
            self.time_box_full.insert("1.0", time_text)
            self.time_box_full.config(state=DISABLED)

        # Update the timer on the Small Overlay page
        if self.time_box_overlay:
            self.time_box_overlay.config(state=NORMAL)
            self.time_box_overlay.delete("1.0", tk.END)
            self.time_box_overlay.insert("1.0", time_text)
            self.time_box_overlay.config(state=DISABLED)

    def setup_full_page(self):
        self.full_page.configure(bg='#5DADE2')
        Label(self.full_page, text="Task Name:", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=0, column=0,
                                                                                                   sticky=W, pady=2)
        Label(self.full_page, text="Time: ", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=1, column=0, sticky=W,
                                                                                              pady=2)                                                                                     
        Label(self.full_page, text="Description:", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=4, column=0,
                                                                                                    sticky=W, pady=2)

        self.description_box = Text(self.full_page, height=5, width=44, font=self.fonts['Description_Tuple'],
                                    background="#d3d3d3")
        self.description_box.grid(row=6, column=0, pady = 5,sticky=W)

        # Example pre-filled description (can be replaced dynamically)
        self.description_box.insert("1.0", "This is where the task description will appear.")
        self.description_box.config(state=DISABLED)  # Make it read-only

        add_task_button = tk.Button(self.full_page, text="Add Task",relief = "flat", background="#d3d3d3",
                                    command=self.open_AddTaskWindow)
        add_task_button.grid(row=3, column=0, sticky=W,padx = 90, pady=5)

        edit_task_button = tk.Button(self.full_page, text = "Edit Task",relief = "flat", background = "#d3d3d3",
                                      command = self.open_EditTaskWindow)
        edit_task_button.grid(row = 3, column = 0, sticky = W, padx = 160, pady = 5)

        self.full_page_start_button = tk.Button(self.full_page, text="Start",relief = "flat", background="#77DD77", command=self.start_timer)
        self.full_page_start_button.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.full_page_stop_button = tk.Button(self.full_page, text="Stop",relief = "flat", background="#FF7276", command=self.stop_timer)
        self.full_page_stop_button.grid(row=3, column=0, sticky=tk.W, padx=45, pady=5)

        # Create Treeview with headings
        self.task_list = ttk.Treeview(
            self.full_page, columns=("Task", "Time", "Complexity"), show="headings", style="Treeview"
        )
        self.task_list.bind("<<TreeviewSelect>>", self.on_item_click)
        self.task_list.heading("Task", text="Task")
        self.task_list.heading("Time", text="Time")
        self.task_list.heading("Complexity", text="Complexity")
        self.task_list.grid(row=8, column=0, sticky=W+E)
        self.task_list.column('Task', width=200, anchor='w')  # Left-aligned
        self.task_list.column('Time', width=100, anchor='center')  # Centered
        self.task_list.column('Complexity', width=100, anchor='center')  # Right-aligned

        # Configure Treeview style to show lines between columns
        style = ttk.Style()
        style.theme_use("clam")  # Use a theme that supports detailed styling (e.g., "clam")
        style.configure(
            "self.Treeview",
            rowheight=25,  # Adjust row height for better visibility (optional)
            bordercolor="black",
            borderwidth=1,
            relief = "flat"
        )
        style.configure(
            "self.Treeview.Heading",
            background="#d3d3d3",  # Header background color
            bordercolor="black",  # Header border color
            borderwidth = 1, #Border size
            relief="flat",  # Header border style
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#c0c0c0")],  # Change background on hover
        )

        style.layout(
            "Treeview",
            [
                (
                    "Treeview.field",
                    {"sticky": "nswe", "children": [("Treeview.padding", {"children": [("Treeview.treearea", {"sticky": "nswe"})]})]},
                )
            ],
        )

        # Example Tasks
        self.task_list.insert("", "end", values=("Debug Code", "01:48:36", "7"))
        self.task_list.insert("", "end", values=("Create Report", "00:32:27", "2"))

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.full_page, orient="vertical", command=self.task_list.yview)
        self.task_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=8, column=1, sticky="ns")


        self.reset_timer_values()

    def setup_completedtasks_page(self):
        self.completedtasks_page.configure(bg = '#5DADE2')
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("Treeview", background = "#d3d3d3", fieldbackground = "d3d3d3", activebackground = "#d3d3d3")

        self.completed_tree = ttk.Treeview(
            self.completedtasks_page,
            columns=("Task", "Completed Date", "Time Taken"),
            show="headings"
        )
        self.completed_tree.bind("<<TreeviewSelect>>", self.on_item_click)
        self.completed_tree.insert("", "end", values =("Create Table", "12/4/24", "03:23:56"))
        self.completed_tree.insert("","end", values =("Finalize Document", "12/6/24", "02:48:12"))
        self.completed_tree.heading("Task", text="Task")
        self.completed_tree.heading("Completed Date", text="Completed Date")
        self.completed_tree.heading("Time Taken", text="Time Taken")

        self.completed_tree.pack(padx=10, pady=5, fill="both", expand=True)


    def on_item_click(self, event):
        selected_item = self.completed_tree.selection()[0]
        if selected_item:
            item_values = self.completed_tree.item(selected_item, "values")
            task_name, completed_date, time_taken = item_values

        self.open_AddCompleteTaskWindow(task_name, completed_date, time_taken)

    def open_AddTaskWindow(self):
        self.task_window = AddTaskWindow()
        self.task_window.grab_set()

    def open_AddCompleteTaskWindow(self, task_name, completed_date, time_taken):
        self.task_window = CompletedTasksWindow(
            task_name = task_name,
            completed_date = completed_date,
            time_taken = time_taken
        )
        self.task_window.grab_set()
    
    def open_EditTaskWindow(self):
        self.task_window = EditTaskWindow()
        self.task_window.grab_set()

    def reset_timer_values(self):
        """Reset the timer values."""
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.timer_running = False

        # Update both timer boxes
        self.update_timer_boxes("00:00:00")
    

    def update_timer(self):
        """Update the timer and display in both timer boxes."""
        if self.timer_running:
            self.seconds += 1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1

            # Format time as HH:MM:SS
            timer_text = f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"

            # Update both timer displays
            self.update_timer_boxes(timer_text)

            # Schedule the next update
            self.root.after(1000, self.update_timer)

    def start_timer(self):
        """Start the timer."""
        if not self.timer_running:  # Prevent multiple instances of the timer
            self.timer_running = True
            self.update_timer()

            # Disable Start button and enable Stop button
            self.disable_buttons(start_disabled=True)

    def stop_timer(self):
        """Stop the timer."""
        if self.timer_running:
            self.timer_running = False

            # Enable Start button and disable Stop button
            self.disable_buttons(start_disabled=False)

    def disable_buttons(self, start_disabled):
        """Enable or disable Start and Stop buttons."""
        # Full page buttons
        self.full_page_start_button.config(state=DISABLED if start_disabled else NORMAL)
        self.full_page_stop_button.config(state=NORMAL if start_disabled else DISABLED)

        # Small Overlay buttons
        self.small_overlay_start_button.config(state=DISABLED if start_disabled else NORMAL)
        self.small_overlay_stop_button.config(state=NORMAL if start_disabled else DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
