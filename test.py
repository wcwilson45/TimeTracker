import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x400")

        # Data storage
        self.tasks = []
        self.completed_tasks = []

        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(expand=True, fill='both')

        # Create menu button frame
        self.menu_frame = ttk.Frame(self.main_container)
        self.menu_frame.pack(fill='x', padx=5, pady=5)

        # Create three-dot menu button
        self.menu_button = ttk.Button(
            self.menu_frame,
            text="⋮",  # Three vertical dots
            width=3,
            command=self.show_menu
        )
        self.menu_button.pack(side='left', padx=5)

        # Create page title label
        self.page_title = ttk.Label(
            self.menu_frame,
            text="Main",
            font=('Helvetica', 12, 'bold')
        )
        self.page_title.pack(side='left', padx=10)

        # Create pages
        self.main_page = ttk.Frame(self.main_container)
        self.task_page = ttk.Frame(self.main_container)
        self.completion_page = ttk.Frame(self.main_container)

        # Initially show main page
        self.current_page = self.main_page
        self.main_page.pack(expand=True, fill='both', padx=10, pady=5)

        # Create popup menu
        self.popup_menu = tk.Menu(root, tearoff=0)
        self.popup_menu.add_command(label="Main", command=lambda: self.switch_page("Main"))
        self.popup_menu.add_command(label="Tasks", command=lambda: self.switch_page("Tasks"))
        self.popup_menu.add_command(label="Completed", command=lambda: self.switch_page("Completed"))

        self.setup_main_page()
        self.setup_task_page()
        self.setup_completion_page()

    def show_menu(self):
        # Display popup menu below the menu button
        try:
            self.popup_menu.tk_popup(
                self.menu_button.winfo_rootx(),
                self.menu_button.winfo_rooty() + self.menu_button.winfo_height()
            )
        finally:
            self.popup_menu.grab_release()

    def switch_page(self, page_name):
        # Hide current page
        self.current_page.pack_forget()

        # Show selected page
        if page_name == "Main":
            self.current_page = self.main_page
            self.page_title.config(text="Main")
        elif page_name == "Tasks":
            self.current_page = self.task_page
            self.page_title.config(text="Tasks")
        else:  # Completed
            self.current_page = self.completion_page
            self.page_title.config(text="Completed")

        self.current_page.pack(expand=True, fill='both', padx=10, pady=5)

    def setup_main_page(self):
        # Welcome message
        welcome_label = ttk.Label(
            self.main_page,
            text="Welcome to Task Manager",
            font=('Helvetica', 16, 'bold')
        )
        welcome_label.pack(pady=20)

        # Statistics
        self.stats_frame = ttk.LabelFrame(self.main_page, text="Statistics")
        self.stats_frame.pack(padx=10, pady=10, fill='x')

        self.total_tasks_label = ttk.Label(self.stats_frame, text="Total Tasks: 0")
        self.total_tasks_label.pack(pady=5)

        self.completed_tasks_label = ttk.Label(self.stats_frame, text="Completed Tasks: 0")
        self.completed_tasks_label.pack(pady=5)

        self.pending_tasks_label = ttk.Label(self.stats_frame, text="Pending Tasks: 0")
        self.pending_tasks_label.pack(pady=5)

        # Quick Add Task
        quick_add_frame = ttk.LabelFrame(self.main_page, text="Quick Add Task")
        quick_add_frame.pack(padx=10, pady=10, fill='x')

        self.quick_task_entry = ttk.Entry(quick_add_frame)
        self.quick_task_entry.pack(side='left', padx=5, pady=5, expand=True, fill='x')

        quick_add_button = ttk.Button(
            quick_add_frame,
            text="Add Task",
            command=self.quick_add_task
        )
        quick_add_button.pack(side='right', padx=5, pady=5)

    def setup_task_page(self):
        # Task input area
        input_frame = ttk.Frame(self.task_page)
        input_frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Due Date:").grid(row=1, column=0, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(input_frame, width=40)
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.due_date_entry.insert(0, "YYYY-MM-DD")

        add_button = ttk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task
        )
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Task list
        self.task_tree = ttk.Treeview(
            self.task_page,
            columns=("Task", "Due Date", "Status"),
            show="headings"
        )

        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Status", text="Status")

        self.task_tree.pack(padx=10, pady=5, fill='both', expand=True)

        # Buttons frame
        button_frame = ttk.Frame(self.task_page)
        button_frame.pack(padx=10, pady=5, fill='x')

        complete_button = ttk.Button(
            button_frame,
            text="Mark Complete",
            command=self.mark_complete
        )
        complete_button.pack(side='left', padx=5)

        delete_button = ttk.Button(
            button_frame,
            text="Delete Task",
            command=self.delete_task
        )
        delete_button.pack(side='right', padx=5)

    def setup_completion_page(self):
        # Completed tasks list
        self.completed_tree = ttk.Treeview(
            self.completion_page,
            columns=("Task", "Completed Date"),
            show="headings"
        )

        self.completed_tree.heading("Task", text="Task")
        self.completed_tree.heading("Completed Date", text="Completed Date")

        self.completed_tree.pack(padx=10, pady=5, fill='both', expand=True)

        # Clear button
        clear_button = ttk.Button(
            self.completion_page,
            text="Clear Completed",
            command=self.clear_completed
        )
        clear_button.pack(pady=5)

    def quick_add_task(self):
        task = self.quick_task_entry.get()
        if task:
            self.tasks.append({
                'task': task,
                'due_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'Pending'
            })
            self.update_task_list()
            self.quick_task_entry.delete(0, tk.END)
            self.update_statistics()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()

        if task and due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
                self.tasks.append({
                    'task': task,
                    'due_date': due_date,
                    'status': 'Pending'
                })
                self.update_task_list()
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.due_date_entry.insert(0, "YYYY-MM-DD")
                self.update_statistics()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
        else:
            messagebox.showwarning("Warning", "Please fill all fields!")

    def mark_complete(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            item = selected_item[0]
            task_data = self.task_tree.item(item)['values']

            # Move to completed tasks
            self.completed_tasks.append({
                'task': task_data[0],
                'completed_date': datetime.now().strftime('%Y-%m-%d')
            })

            # Remove from pending tasks
            self.tasks = [task for task in self.tasks if task['task'] != task_data[0]]

            self.update_task_list()
            self.update_completed_list()
            self.update_statistics()
        else:
            messagebox.showwarning("Warning", "Please select a task!")

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            item = selected_item[0]
            task_data = self.task_tree.item(item)['values']
            self.tasks = [task for task in self.tasks if task['task'] != task_data[0]]
            self.update_task_list()
            self.update_statistics()
        else:
            messagebox.showwarning("Warning", "Please select a task!")

    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Clear all completed tasks?"):
            self.completed_tasks = []
            self.update_completed_list()
            self.update_statistics()

    def update_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        for task in self.tasks:
            self.task_tree.insert(
                '',
                'end',
                values=(task['task'], task['due_date'], task['status'])
            )

    def update_completed_list(self):
        for item in self.completed_tree.get_children():
            self.completed_tree.delete(item)

        for task in self.completed_tasks:
            self.completed_tree.insert(
                '',
                'end',
                values=(task['task'], task['completed_date'])
            )

    def update_statistics(self):
        total = len(self.tasks) + len(self.completed_tasks)
        completed = len(self.completed_tasks)
        pending = len(self.tasks)

        self.total_tasks_label.config(text=f"Total Tasks: {total}")
        self.completed_tasks_label.config(text=f"Completed Tasks: {completed}")
        self.pending_tasks_label.config(text=f"Pending Tasks: {pending}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()