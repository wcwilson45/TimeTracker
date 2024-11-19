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

        ttk.Label(self, text="Task Name:").pack(pady=10)
        self.task_name_entry = ttk.Entry(self, width=50)
        self.task_name_entry.pack(pady=5)

        ttk.Label(self, text="Description:").pack(pady=10)
        self.description_entry = ttk.Entry(self, width=50)
        self.description_entry.pack(pady=5)

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
        self.root.geometry("600x400")

        # Main Container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(expand=False, fill="both")

        # Menu Button Frame
        self.menu_frame = ttk.Frame(self.main_container)
        self.menu_frame.pack(fill="x", padx=5, pady=5)

        # DropDown Menu
        self.menu_button = ttk.Button(self.menu_frame, text="⋮", width=3, command=self.show_menu)
        self.menu_button.pack(side="left", padx=5)

        # Page Title Label
        self.page_title = ttk.Label(self.menu_frame, text="Full", font=("Arial", 12, "bold"))
        self.page_title.pack(side="left", padx=10)

        # Create pages
        self.full_page = ttk.Frame(self.main_container)
        self.completedtasks_page = ttk.Frame(self.main_container)
        self.smalloverlay_page = ttk.Frame(self.main_container)

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
            self.page_title.config(text="Full")
        elif page_name == "Completed Tasks":
            self.current_page = self.completedtasks_page
            self.page_title.config(text="Completed Tasks")
        elif page_name == "Small Overlay":
            self.current_page = self.smalloverlay_page
            self.page_title.config(text="Small Overlay")

        self.current_page.pack(expand=True, fill="both", padx=10, pady=5)

    def setup_full_page(self):
        Label(self.full_page, text="Task Name").grid(row=0, column=0, sticky=W, pady=2)
        Label(self.full_page, text="Description").grid(row=1, column=0, sticky=W, pady=2)

        add_task_button = ttk.Button(self.full_page, text="Add Task", command=self.open_AddTaskWindow)
        add_task_button.grid(row=3, column=0, sticky=W, pady=10)

    def setup_completedtasks_page(self):
        self.completed_tree = ttk.Treeview(
            self.completedtasks_page,
            columns=("Task", "Completed Date", "Time Taken"),
            show="headings"
        )

        self.completed_tree.heading("Task", text="Task")
        self.completed_tree.heading("Completed Date", text="Completed Date")
        self.completed_tree.heading("Time Taken", text="Time Taken")

        self.completed_tree.pack(padx=10, pady=5, fill="both", expand=True)

    def setup_smalloverlay_page(self):
        Label(self.smalloverlay_page, text="Task Name", font = ("Arial", 24, "bold")).grid(row=0, column=0, sticky=W, pady=2)
        Label(self.smalloverlay_page, text="Description", font = ("Arial", 12, "bold")).grid(row=2, column=0, sticky=W, pady=2)
        Label(self.smalloverlay_page, text="Time: ", font = ("Arial", 12, "bold")).grid(row = 1, column = 0, sticky = W, pady = 2)
        Label(self.smalloverlay_page, text= "Tags", font = ("Arial", 12, "bold")).grid(row = 2, column = 4, sticky = W, pady = 2)

        # Text box to show the description
        self.description_box = Text(self.smalloverlay_page, height=5, width=50)
        self.description_box.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky=W)

        # Example pre-filled description (can be replaced dynamically)
        self.description_box.insert("1.0", "This is where the task description will appear.")
        self.description_box.config(state=DISABLED)  # Make it read-only

        self.tag_box = Text(self.smalloverlay_page, height = 5, width = 15)
        self.tag_box.grid(row=3, column=4, columnspan=2, pady=5, padx=5, sticky=W)


    def open_AddTaskWindow(self):
        window = AddTaskWindow(self.root)
        window.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
