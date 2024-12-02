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
    AddTaskWindow,
    CurrentTaskWindow
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
            "Body_Tuple": tkfont.Font(family = "SF Pro Display", size = 12, weight = "bold"),
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
        self.page_title = ttk.Label(self.menu_frame, text="NAVSEA Time Tracker", font=self.fonts['Body_Tuple'], background="#5DADE2")
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
        self.popup_menu.add_command(label="NAVSEA Time Tracker", command=lambda: self.switch_page("NAVSEA Time Tracker"))
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

        if page_name == "NAVSEA Time Tracker":
            self.current_page = self.full_page
            self.page_title.config(text="NAVSEA Time Tracker", background="#5DADE2")
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
        current_task_name = "Clean Stove"
        Label(self.full_page, text=current_task_name, font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=0, column=0,
                                                                                                   sticky=W, pady=2)
        Label(self.full_page, text="Time: ", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=1, column=0, sticky=W,
                                                                                              pady=2)                                                                                     
        Label(self.full_page, text="Description:", font=self.fonts['Body_Tuple'], background="#5DADE2").grid(row=4, column=0,
                                                                                                    sticky=W, pady=2)

        self.description_box = Text(self.full_page, height=5, width=62, font=self.fonts['Description_Tuple'],
                                    background="#d3d3d3")
        self.description_box.grid(row=6, column=0, pady = 5,sticky=W)

        description_scrollbar = tk.Scrollbar(self.full_page, orient="vertical",command=self.description_box.yview)
        self.description_box.configure(yscrollcommand= description_scrollbar.set)
        description_scrollbar.grid(row=6, column=1, sticky="ns")

        # Example pre-filled description (can be replaced dynamically)
        self.description_box.insert("1.0", "This is where the task description will appear.")
        self.description_box.config(state=DISABLED)  # Make it read-only

        add_task_button = tk.Button(self.full_page, text="Add Task",relief = "flat", background="#d3d3d3",
                                    command=self.open_AddTaskWindow)
        add_task_button.grid(row=3, column=0, sticky=W,padx = 90, pady=5)

        edit_task_button = tk.Button(self.full_page, text = "Edit Task",relief = "flat", background = "#d3d3d3",
                                      command = self.open_EditTaskWindow)
        edit_task_button.grid(row = 3, column = 0, sticky = W, padx = 160, pady = 5)

        complete_task_button = tk.Button(self.full_page, text = "Complete Task", relief = "flat", background = "#d3d3d3", command = self.open_CurrentTaskWindow)
        complete_task_button.grid(row = 3, column = 0 ,sticky = W, padx = 230, pady = 5)
        self.full_page_start_button = tk.Button(self.full_page, text="Start",relief = "flat", background="#77DD77", command=self.start_timer)
        self.full_page_start_button.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.full_page_stop_button = tk.Button(self.full_page, text="Stop",relief = "flat", background="#FF7276", command=self.stop_timer)
        self.full_page_stop_button.grid(row=3, column=0, sticky=tk.W, padx=45, pady=5)

        self.time_box_full = Text(self.full_page, height=1, width=10, font=self.fonts['Body_Tuple'], background = "#d3d3d3")
        self.time_box_full.grid(row = 1, column = 0, padx = 50, pady = 5, sticky = W)

        # Create Treeview with headings
        self.task_list = ttk.Treeview(
            self.full_page, columns=("Task", "Time", "Complexity"), show="headings", style="Treeview"
        )
        self.task_list.bind("<<TreeviewSelect>>", self.on_item_click)
        self.task_list.heading("Task", text="Task")
        self.task_list.heading("Time", text="Time")
        self.task_list.heading("Complexity", text="Complexity")
        self.task_list.grid(row=8, column=0, sticky=W+E, pady = 25)
        self.task_list.column('Task', width=200, anchor='w')  # Left-aligned
        self.task_list.column('Time', width=100, anchor='center')  # Centered
        self.task_list.column('Complexity', width=100, anchor='center')  # Right-aligned

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, bordercolor="black", borderwidth=1, relief="flat")
        style.configure("Treeview.Heading", background="#A9A9A9", bordercolor="black", borderwidth=1, relief="flat")
        style.map("Treeview.Heading", background=[("active", "#c0c0c0")])

        # Configure alternating row colors
        style.configure("Treeview.oddrow", background="#d3d3d3")  # Light gray for odd rows
        style.configure("Treeview.evenrow", background="#A9A9A9")  # Slightly lighter grey for even rows

        self.task_list.tag_configure("oddrow", background="#d3d3d3")  # Apply light gray background
        self.task_list.tag_configure("evenrow", background="#A9A9A9")  # Apply slightly lighter grey background

        # Insert tasks with tags for alternating colors
        self.insert_task("Debug Code", "01:48:36", "7")
        self.insert_task("Create Report", "00:32:27", "2")
        self.insert_task("Design Database Schema", "02:15:40", "8")
        self.insert_task("Write Unit Tests", "01:00:00", "5")
        self.insert_task("Optimize Query Performance", "00:45:12", "6")
        self.insert_task("Refactor Code", "03:23:55", "9")
        self.insert_task("Update Documentation", "00:50:45", "4")
        self.insert_task("Review Pull Request", "00:20:30", "3")
        self.insert_task("Research New Feature", "01:30:10", "6")
        self.insert_task("Fix Bugs", "01:10:05", "7")
        self.insert_task("Fix Bugs", "01:10:05", "7")
        self.insert_task("Fix Bugs", "01:10:05", "7")
        self.insert_task("Fix Bugs", "01:10:05", "7")
        self.insert_task("Fix Bugs", "01:10:05", "7")
        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar( self.full_page,orient = "vertical", command=self.task_list.yview)
        self.task_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=8, column=1, sticky="ns", pady = 25)


        self.reset_timer_values()

    def insert_task(self, task_name, time, complexity):
        # Determine whether to use odd or even row color
        row_tag = "oddrow" if len(self.task_list.get_children()) % 2 == 0 else "evenrow"
        self.task_list.insert("", "end", values=(task_name, time, complexity), tags=(row_tag,))

    def setup_completedtasks_page(self):
        self.completedtasks_page.configure(bg = '#5DADE2')

        self.completed_tree = ttk.Treeview(
            self.completedtasks_page,
            columns=("Task", "Completed Date", "Time Taken"),
            show="headings", style = "Treeview"
        )
        self.completed_tree.bind("<<TreeviewSelect>>", self.on_item_click)
        self.completed_tree.insert("", "end", values =("Create Table", "12/4/24", "03:23:56"))
        self.completed_tree.insert("","end", values =("Finalize Document", "12/6/24", "02:48:12"))
        self.completed_tree.heading("Task", text="Task")
        self.completed_tree.heading("Completed Date", text="Completed Date")
        self.completed_tree.heading("Time Taken", text="Time Taken")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, bordercolor="black", borderwidth=1, relief="flat")
        style.configure("Treeview.Heading", background="#A9A9A9", bordercolor="black", borderwidth=1, relief="flat")
        style.map("Treeview.Heading", background=[("active", "#c0c0c0")])

        # Configure alternating row colors
        style.configure("Treeview.oddrow", background="#d3d3d3")  # Light gray for odd rows
        style.configure("Treeview.evenrow", background="#A9A9A9")  # Slightly lighter grey for even rows

        self.completed_tree.tag_configure("oddrow", background="#d3d3d3")  # Apply light gray background
        self.completed_tree.tag_configure("evenrow", background="#A9A9A9")  # Apply slightly lighter grey background

        self.completed_tree.pack(padx=10, pady=5, fill="both", expand=True)


    def on_item_click(self, event):
        selected_item = self.completed_tree.selection()[0]
        if selected_item:
            item_values = self.completed_tree.item(selected_item, "values")
            task_name, completed_date, time_taken = item_values

        self.open_AddCompleteTaskWindow(task_name, completed_date, time_taken)
    
    def current_item_click(self, event):
        selected_item= self.task_list.selection()[0]
        if selected_item:
            item_values = self.task_list.item(selected_item, "values")
            current_task_name, current_task_time, current_time_complexity = item_values

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

    def open_CurrentTaskWindow(self, current_task_name, current_task_time, current_time_complexity):
        self.task_window = CurrentTaskWindow()
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
