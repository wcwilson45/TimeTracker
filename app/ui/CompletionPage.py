from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime

from .CommitHistoryPage import CommitHistoryWindow


class CompletedTasksWindow(tk.Tk):
    def __init__(self, task_name, completed_date, time_taken):
        super().__init__()

        # Font Tuples for Use on pages
        self.fonts = {
            "Title_Tuple": tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            "Body_Tuple": tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            "Description_Tuple": tkfont.Font(family="Sf Pro Text", size=12)
        }

        self.geometry("600x600")  # Reduced height
        self.title("Task Details")
        self.configure(bg="#5DADE2")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Info.TLabel", font=("Arial", 10), background='#5DADE2')
        self.style.configure("Tag.TLabel", font=("Arial", 8), background='#D3D3D3', padding=2, foreground='white')

        # Main container with reduced padding
        self.main_container = tk.Frame(self, bg='#5DADE2', bd=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)  # Reduced pady

        # Top section with header and buttons with reduced padding
        self.top_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.top_frame.pack(fill=tk.X, pady=(0, 5))  # Reduced pady

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

        # Left panel wrapper
        self.left_panel_wrapper = tk.Frame(self.content_frame, bg='#5DADE2', bd=0)
        self.left_panel_wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Left panel (centered, fixed width)
        self.left_panel = tk.Frame(self.left_panel_wrapper, bg='#5DADE2', bd=0, width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        self.left_panel.pack_propagate(False)

        # Right panel
        self.right_panel = tk.Frame(self.content_frame, bg='#5DADE2', bd=0, width=160)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_panel.pack_propagate(False)

        # Tags
        self.tags_frame = tk.Frame(self.right_panel, bg='#5DADE2', bd=0)
        self.tags_frame.pack(fill=tk.X, pady=(0, 5))  # Reduced pady
        tk.Label(self.tags_frame, text="Tags:", font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)

        # Create tag labels
        self.create_tag("Blue")
        self.create_tag("Small")
        self.create_tag("Tech")

        # Time information
        self.create_info_field("Time of Completion:", time_taken)
        self.create_info_field("Time Complexity:", "5")
        self.create_info_field("Date Completed:", completed_date)

        # Create sections with buttons aligned to bottom
        self.sections_frame = tk.Frame(self.left_panel, bg='#5DADE2', bd=0)
        self.sections_frame.pack(fill=tk.BOTH, expand=True)

        # Description section
        self.create_collapsible_section(self.sections_frame, "Description:", "Enter description here...", height=15)

        # Commit History section
        self.create_collapsible_section(self.sections_frame, "Commit History:", "Enter commit history...", height=15)

        # Buttons frame - now packed after commit history
        self.button_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.button_frame.pack(side=tk.RIGHT, pady=(5, 10))

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

    def create_collapsible_section(self, parent, title, placeholder, height=10):
        frame = tk.Frame(parent, bg='#5DADE2', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))  # Reduced pady

        header_frame = tk.Frame(frame, bg='#5DADE2')
        header_frame.pack(fill=tk.X, anchor=tk.W)

        tk.Label(header_frame, text=title, font=("Arial", 10), bg='#5DADE2').pack(side=tk.LEFT, padx=5, pady=2)  # Reduced pady

        if title == "Commit History:":
            # Container frame
            container_frame = tk.Frame(frame, bg='#D3D3D3', bd=1, relief='solid')
            container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 2))  # Reduced pady

            # Create frame for treeview and scrollbar
            tree_frame = tk.Frame(container_frame, bg='#D3D3D3')
            tree_frame.pack(fill=tk.BOTH, expand=True)

            # Create the treeview
            tree = ttk.Treeview(tree_frame, columns=("Date",), show="headings", height=15)
            tree.heading("Date", text="Date", anchor="center")  # Center the header
            tree.column("Date", anchor="center", width=150)  # Center the content

            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # Pack the tree and scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Add the dates
            dates = ["12/4/24", "12/6/24", "12/8/24", "12/10/24", "10/8/24", "11,2,24", "10/8/24", "11,2,24", "10/8/24", "11,2,24", "10/8/24"]
            for i, date in enumerate(dates):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                tree.insert("", "end", values=(date,), tags=(tag,))

            tree.tag_configure("oddrow", background="#D3D3D3")
            tree.tag_configure("evenrow", background="#A9A9A9")
            tree.tag_configure('selected', background='#b3b3b3')

            def on_commit_click(event):
                try:
                    selected_item = tree.selection()[0]
                    for item in tree.get_children():
                        tree.item(item, tags=(tree.item(item)['tags'][0],))
                    tree.item(selected_item, tags=('selected',))
                    self.open_commit_history_page()
                except IndexError:
                    pass

            tree.bind("<Button-1>", on_commit_click)

        else:
            # Container frame for description
            container_frame = tk.Frame(frame, bg='#D3D3D3', bd=1, relief='solid')
            container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 2))  # Reduced pady

            # Create a scrollbar first
            scrollbar = tk.Scrollbar(container_frame, orient="vertical")
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Create text widget
            text = tk.Text(container_frame, height=height, wrap=tk.WORD, bg='#D3D3D3', bd=0,
                           yscrollcommand=scrollbar.set)  # Connect text widget to scrollbar
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Configure scrollbar to work with text widget
            scrollbar.config(command=text.yview)

            # Insert placeholder text
            text.insert("1.0", placeholder)

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