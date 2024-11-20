from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime




class AddTaskWindow(tk.Toplevel):
    """A separate window to add a task."""
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("560x280")
        self.title("Add Task")

        ttk.Label(self, text="Task Name:").grid(row = 0, column= 0, sticky = W, pady = 2)
        self.task_name_entry = tk.Entry(self).grid(row = 0, column = 1, sticky = W, pady = 2)

        ttk.Label(self, text="Description:").grid(row = 1, column = 0, sticky = NW, pady = 2)
        self.description_entry = tk.Text(self, height = 5, width = 25).grid(row = 1, column = 1, sticky = W, pady = 2)

        ttk.Button(self, text="Save", command=self.save_task).pack(side="left", padx=20, pady=20)
        ttk.Button(self, text="Cancel", command=self.destroy).pack(side="right", padx=20, pady=20)

    def save_task(self):
        """Save task details (placeholder functionality)."""
        task_name = self.task_name_entry.get()
        description = self.description_entry.get()

        if task_name and description:
            messagebox.showinfo("Task Saved", f"Task '{task_name}' saved successfully!")
        else:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        self.destroy()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("540x1080")

        #Background color hex code
        self.root.configure(bg = "#add8e6")

        #Font Tuples for Use on pages
        self.Title_tuple = ("SF Pro Display", 24, "bold")
        self.Body_tuple = ("SF Pro Text", 12, "bold")
        self.Description_tuple =("SF Pro Text", 12)

        # Main Container
        self.main_container = tk.Frame(root, background= "#add8e6")
        self.main_container.pack(expand=False, fill="both")

        # Menu Button Frame
        self.menu_frame = tk.Frame(self.main_container, background= "#add8e6")
        self.menu_frame.pack(fill="x", padx=5, pady=5)

        # DropDown Menu
        self.menu_button = ttk.Button(self.menu_frame, text="⋮", width=3, command=self.show_menu)
        self.menu_button.pack(side="left", padx=5)

        # Page Title Label
        self.page_title = ttk.Label(self.menu_frame, text="Full", font=self.Body_tuple, background= "#add8e6")
        self.page_title.pack(side="left", padx=10)

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
            self.page_title.config(text="Full", background = "#add8e6")
        elif page_name == "Completed Tasks":
            self.current_page = self.completedtasks_page
            self.page_title.config(text="Completed Tasks", background= "#add8e6")
        elif page_name == "Small Overlay":
            self.current_page = self.smalloverlay_page
            self.page_title.config(text="Small Overlay", background= "#add8e6")

        self.current_page.pack(expand=True, fill="both", padx=10, pady=5)

    def setup_full_page(self):
        self.full_page.configure(bg = '#add8e6')
        Label(self.full_page, text="Task Name:", font = self.Title_tuple, background = "#add8e6").grid(row=0, column=0, sticky=W, pady=2)
        Label(self.full_page, text="Time: ", font = self.Body_tuple, background = "#add8e6").grid(row = 1, column = 0, sticky = W, pady = 2)
        Label(self.full_page, text="Description:", font = self.Body_tuple, background = "#add8e6").grid(row=2, column=0, sticky=W, pady=2)

        self.description_box = Text(self.full_page, height=5, width=50, font = self.Description_tuple, background = "#d3d3d3")
        self.description_box.grid(row=3, column=0, rowspan = 2, columnspan=2, pady=5, padx=5, sticky=W)

        # Example pre-filled description (can be replaced dynamically)
        self.description_box.insert("1.0", "This is where the task description will appear.")
        self.description_box.config(state=DISABLED)  # Make it read-only

        add_task_button = tk.Button(self.full_page, text="Add Task", background= "#d3d3d3",  command=self.open_AddTaskWindow)
        add_task_button.grid(row=11, column=0, sticky=W, pady=10)

        self.task_list = ttk.Treeview(self.full_page, columns= ("Task", "Time","Complexity"), show = "headings")
        self.task_list.heading("Task", text = "Task")
        self.task_list.heading("Time", text = "Time")
        self.task_list.heading("Complexity", text = "Complexity")
        self.task_list.grid(row = 6, column = 0)


    def on_item_click(self, event):
        selected_item = self.completed_tree.selection()[0]

        item_values = self.completed_tree.item(selected_item, "values")

        print(f"Item Clicked")

    def setup_completedtasks_page(self):
        self.completedtasks_page.configure(bg = '#add8e6')
        self.completed_tree = ttk.Treeview(
            self.completedtasks_page,
            columns=("Task", "Completed Date", "Time Taken"),
            show="headings"
        )
        self.completed_tree.bind("<<TreeviewSelect>>", self.on_item_click)

        self.completed_tree.insert("", "end", values =("1", "1", "1"))
        self.completed_tree.heading("Task", text="Task")
        self.completed_tree.heading("Completed Date", text="Completed Date")
        self.completed_tree.heading("Time Taken", text="Time Taken")

        self.completed_tree.pack(padx=10, pady=5, fill="both", expand=True)

    def setup_smalloverlay_page(self):
        self.smalloverlay_page.configure(bg = '#add8e6')
        Label(self.smalloverlay_page, text= "Task Name:", font = self.Title_tuple, background = "#add8e6").grid(row=0, column=0, sticky=W, pady=2)
        Label(self.smalloverlay_page, text= "Description:", font = self.Body_tuple, background = "#add8e6").grid(row=3, column=0, sticky=W, pady=2)
        Label(self.smalloverlay_page, text= "Time:", font = self.Title_tuple, background = "#add8e6").grid(row = 1, column = 0, sticky = W, pady = 2)
        Label(self.smalloverlay_page, text= "Tags", font = self.Body_tuple, background = "#add8e6").grid(row = 3, column = 8, sticky = W, pady = 2)

        # Timer section
        self.time_box = Text(self.smalloverlay_page, height=1, width=10, font = self.Body_tuple)
        self.time_box.grid(row=1, column=0, padx=5, pady=5,sticky = E)
        self.time_box.insert("1.0", "00:00:00")  # Initial timer text
        self.time_box.config(state=DISABLED)  # Make it read-only

        start_button = tk.Button(self.smalloverlay_page, text="Start", background= "#77DD77", command=self.start_timer)
        start_button.grid(row=2, column=0,sticky = W, pady=5)

        stop_button = tk.Button(self.smalloverlay_page, text="Stop", background= "#FF7276", command=self.stop_timer)
        stop_button.grid(row=2, column=1,sticky = W, pady=5)
        # Text box to show the description
        self.description_box = Text(self.smalloverlay_page, height=5, width=35, font = self.Description_tuple, background = "#d3d3d3")
        self.description_box.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky=W)

        # Example pre-filled description (can be replaced dynamically)
        self.description_box.insert("1.0", "This is where the task description will appear.")
        self.description_box.config(state=DISABLED)  # Make it read-only

        self.tag_box = Text(self.smalloverlay_page, height = 5, width = 15, font = self.Description_tuple, background= "#d3d3d3")
        self.tag_box.grid(row=4, column=8, columnspan=1, pady=5, padx=5, sticky=W)

        self.tag_box.insert("1.0", "This is where the task tags will appear.")
        self.tag_box.config(state=DISABLED)  # Make it read-only

        self.reset_timer_values()


    def open_AddTaskWindow(self):
        window = AddTaskWindow(self.root)
        window.grab_set()
    

    def reset_timer_values(self):
        """Reset the timer values."""
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.timer_running = False

    def update_timer(self):
        """Update the timer and display in the `time_box`."""
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

            # Update the `time_box` content
            self.time_box.config(state=NORMAL)  # Make it editable to update text
            self.time_box.delete("1.0", tk.END)  # Clear previous content
            self.time_box.insert("1.0", timer_text)  # Insert updated timer value
            self.time_box.config(state=DISABLED)  # Make it read-only again

            # Schedule next update
            self.root.after(1000, self.update_timer)

    def start_timer(self):
        """Start the timer."""
        if not self.timer_running:  # Prevent multiple instances of the timer
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        """Stop the timer."""
        self.timer_running = False



