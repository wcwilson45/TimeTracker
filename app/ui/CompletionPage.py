from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from datetime import datetime


# from .CommitHistoryPage import CommitHistoryWindow


class CompletedTasksWindow(tk.Tk):
    def __init__(self, task_name, completed_date, time_taken):
        super().__init__()

        self.geometry("600x350")
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
        self.create_collapsible_section(self.left_panel, "Description:", "Enter description here...", width=40)

        # Commit History section
        self.create_collapsible_section(self.left_panel, "Commit History:", "Enter commit history...", width=40)

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
            bg='#F08080',  # Background color
            fg='black',  # Text color
            relief='flat',  # Makes it look more modern
            padx=10,  # Horizontal padding
            pady=5  # Vertical padding
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=1)

        self.complete_btn = tk.Button(
            self.button_frame,
            text="Complete",
            command=self.destroy,
            bg='#90EE90',  # Background color
            fg='black',  # Text color
            relief='flat',  # Makes it look more modern
            padx=10,  # Horizontal padding
            pady=5  # Vertical padding
        )

        self.complete_btn.pack(side=tk.LEFT)

    def create_collapsible_section(self, parent, title, placeholder, width=None):
        frame = tk.Frame(parent, bg='#D3D3D3', bd=0)
        frame.pack(fill=tk.X, pady=(0, 10))

        header_frame = tk.Frame(frame, bg='#D3D3D3')
        header_frame.pack(fill=tk.X, anchor=tk.W)

        tk.Label(header_frame, text=title, font=("Arial", 10), bg='#D3D3D3').pack(side=tk.LEFT, padx=5, pady=5)

        outer_frame = tk.Frame(frame, bg='#D3D3D3')
        outer_frame.pack(fill=tk.X, anchor=tk.W)

        # Create toggle button with larger font
        toggle_btn = tk.Button(
            header_frame,
            text="⊖",
            font=("Arial", 12),
            width=2,
            relief='flat',
            bg='#D3D3D3',
            bd=0,
            cursor="hand2"
        )
        toggle_btn.pack(side=tk.RIGHT, padx=5)

        # Function to toggle visibility
        def toggle_collapse():
            if outer_frame.winfo_viewable():
                outer_frame.pack_forget()
                toggle_btn.configure(text="⊕")
            else:
                outer_frame.pack(fill=tk.X, anchor=tk.W)
                toggle_btn.configure(text="⊖")

        toggle_btn.configure(command=toggle_collapse)

        if title == "Commit History:":
            style = ttk.Style(self)
            style.theme_use("clam")
            style.configure("Treeview", background="#D3D3D3", fieldbackground="#D3D3D3")

            tree = ttk.Treeview(
                outer_frame,
                columns=("Date",),
                show="tree",
                height=4
            )
            tree.heading("Date", text="Date")
            tree.insert("", "end", values=("12/4/24",))
            tree.insert("", "end", values=("12/6/24",))
            tree.pack(padx=5, pady=(0, 5), fill=tk.X)

            def on_commit_click(event):
                selected_item = tree.selection()[0]
                date = tree.item(selected_item)['values'][0]
                print(f"Clicked on commit from {date}")

            tree.bind("<Double-1>", on_commit_click)
        else:
            # Original text widget for Description
            text = tk.Text(outer_frame, height=4, wrap=tk.WORD, width=width, bg='#D3D3D3', borderwidth=0)
            text.pack(padx=5, pady=(0, 5))
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
    app = CompletedTasksWindow("bullshit", "never", "a lot")
    root.mainloop()