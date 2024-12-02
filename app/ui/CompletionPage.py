from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from datetime import datetime

from .CommitHistoryPage import CommitHistoryWindow


class CompletedTasksWindow(tk.Tk):
    def __init__(self, task_name, completed_date, time_taken):
        super().__init__()

        self.geometry("600x400")
        self.title("Task Details")
        self.configure(bg="#5DADE2")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Info.TLabel", font=("Arial", 10), background='#5DADE2')
        self.style.configure("Tag.TLabel", font=("Arial", 8), background='#D3D3D3', padding=2, foreground='white')

        # Main container - using tk.Frame instead of ttk.Frame
        self.main_container = tk.Frame(self, bg='#5DADE2', bd=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top section with header and buttons - using tk.Frame
        self.top_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.top_frame.pack(fill=tk.X, pady=(0, 10))

        # Header
        self.header_label = tk.Label(
            self.top_frame,
            text=task_name,
            font=("Arial", 16, "bold"),
            bg='#5DADE2',
            bd=0
        )
        self.header_label.pack(side=tk.LEFT)

        # Content area
        self.content_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel (70% width)
        self.left_panel = tk.Frame(self.content_frame, bg='#5DADE2', bd=0)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Description section
        self.create_collapsible_section(self.left_panel, "Description:", "Enter description here...", width=150)

        # Commit History section
        self.create_collapsible_section(self.left_panel, "Commit History:", "Enter commit history...", width=150)

        # Right panel (30% width)
        self.right_panel = tk.Frame(self.content_frame, bg='#5DADE2', bd=0)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Tags
        self.tags_frame = tk.Frame(self.right_panel, bg='#5DADE2', bd=0)
        self.tags_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(self.tags_frame, text="Tags:", font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)

        # Create tag labels
        self.create_tag("Blue")
        self.create_tag("Small")
        self.create_tag("Tech")

        # Time information
        self.create_info_field("Time of Completion:", time_taken)
        self.create_info_field("Time Complexity:", "5")
        self.create_info_field("Date Completed:", completed_date)

        # Buttons frame
        self.button_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.button_frame.pack(side=tk.BOTTOM, pady=1, anchor='e')

        # Cancel and Complete buttons
        self.cancel_btn = tk.Button(
            self.button_frame,
            text="Cancel",
            command=self.open_commit_history_page,
            bg='#F08080',
            fg='black',
            relief='flat',
            padx=10,
            pady=5
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=1)

        self.complete_btn = tk.Button(
            self.button_frame,
            text="Complete",
            command=self.destroy,
            bg='#90EE90',
            fg='black',
            relief='flat',
            padx=10,
            pady=5
        )
        self.complete_btn.pack(side=tk.LEFT)

    def create_collapsible_section(self, parent, title, placeholder, width=1):
        frame = tk.Frame(parent, bg='#5DADE2', bd=0)
        frame.pack(fill=tk.X, pady=(0, 10))

        header_frame = tk.Frame(frame, bg='#5DADE2')
        header_frame.pack(fill=tk.X, anchor=tk.W)

        tk.Label(header_frame, text=title, font=("Arial", 10), bg='#5DADE2').pack(side=tk.LEFT, padx=5, pady=5)

        # Create container frame for content and scrollbar
        container_frame = tk.Frame(frame, bg='#D3D3D3')
        container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 5))

        if title == "Commit History:":
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview",
                            background="#D3D3D3",
                            fieldbackground="#D3D3D3",
                            borderwidth=0,
                            relief='flat',
                            rowheight=25)

            # Configure alternating row colors
            style.configure("Treeview.oddrow", background="#D3D3D3")
            style.configure("Treeview.evenrow", background="#A9A9A9")

            # Create frame for treeview and scrollbar
            tree_frame = tk.Frame(container_frame, bg='#D3D3D3')
            tree_frame.pack(fill=tk.BOTH, expand=True)

            # Create treeview
            tree = ttk.Treeview(tree_frame, columns=("Date",), show="tree", height=4)
            tree.pack(side='left', fill='both', expand=True)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)

            # Insert sample data with alternating colors
            dates = ["12/4/24", "12/6/24", "12/8/24", "12/10/24"]
            for i, date in enumerate(dates):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                tree.insert("", "end", values=(date,), tags=(tag,))

            # Configure row tags
            tree.tag_configure("oddrow", background="#D3D3D3")
            tree.tag_configure("evenrow", background="#A9A9A9")
            tree.tag_configure('selected', background='#b3b3b3')

            def on_commit_click(event):
                selected_item = tree.selection()[0]
                for item in tree.get_children():
                    tree.item(item, tags=(tree.item(item)['tags'][0],))
                tree.item(selected_item, tags=('selected',))
                date = tree.item(selected_item)['values'][0]
                self.open_commit_history_page()

            tree.bind("<Button-1>", on_commit_click)

        else:
            # Create frame for text widget and scrollbar
            text_frame = tk.Frame(container_frame, bg='#D3D3D3')
            text_frame.pack(fill=tk.BOTH, expand=True)

            # Create text widget
            text = tk.Text(text_frame, height=10, wrap=tk.WORD, width=1, bg='#D3D3D3', borderwidth=0)
            text.pack(side='left', fill='both', expand=True)
            text.insert("1.0", placeholder)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text.yview)
            scrollbar.pack(side='right', fill='y')
            text.configure(yscrollcommand=scrollbar.set)

    def create_tag(self, text):
        tag_label = tk.Label(
            self.tags_frame,
            text=text,
            font=("Arial", 8),
            bg='#5DADE2',
            fg='black',
            padx=5,
            pady=2
        )
        tag_label.pack(side=tk.LEFT, padx=(0, 5))

    def create_info_field(self, label_text, value_text):
        frame = tk.Frame(self.right_panel, bg='#5DADE2', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text=label_text, font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)
        tk.Label(frame, text=value_text, font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)

    def open_commit_history_page(self):
        self.task_window = CommitHistoryWindow()
        self.task_window.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = CompletedTasksWindow("Sample Task", "12/4/24", "03:23:56")
    root.mainloop()