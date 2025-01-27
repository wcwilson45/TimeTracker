from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime


class CurrentTask(tk.Toplevel):
    def __init__(self,parent, current_task_name, current_task_time, current_time_comp):
        super().__init__(parent)


        # Font Tuples for Use on pages
        self.fonts = {
            "Title_Tuple": tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            "Body_Tuple": tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            "Description_Tuple": tkfont.Font(family="Sf Pro Text", size=12)
        }

        self.geometry("500x310")
        self.title("Task Details")
        self.configure(bg="#5DADE2")

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("Info.TLabel", font=("Arial", 10), background='#5DADE2')
        self.style.configure("Tag.TLabel", font=("Arial", 8), background='#D3D3D3', padding=2, foreground='white')

        # Main container
        self.main_container = tk.Frame(self, bg='#5DADE2', bd=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Top frame for title
        self.top_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.top_frame.pack(fill=tk.X, pady=(0, 5))

        # Header
        self.header_label = tk.Label(
            self.top_frame,
            text=current_task_name,
            font=("Arial", 16, "bold"),
            bg='#5DADE2',
            bd=0
        )
        self.header_label.pack(side=tk.LEFT)

        # Main content frame using grid
        self.content_frame = tk.Frame(self.main_container, bg='#5DADE2', bd=0)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel (description)
        self.left_panel = tk.Frame(self.content_frame, bg='#5DADE2', bd=0, width=300)
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Right panel (info and buttons)
        self.right_panel = tk.Frame(self.content_frame, bg='#5DADE2', bd=0, width=160)
        self.right_panel.grid(row=0, column=1, sticky='n')
        self.right_panel.grid_propagate(False)

        # Configure grid weights
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Tags
        self.tags_frame = tk.Frame(self.right_panel, bg='#5DADE2', bd=0)
        self.tags_frame.pack(fill=tk.X, pady=(25, 5))
        tk.Label(self.tags_frame, text="Tags:", font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)

        # Create tag labels
        self.create_tag("Blue")
        self.create_tag("Small")
        self.create_tag("Tech")

        # Information being filled in
        self.create_info_field("Time:", current_task_time)
        self.create_info_field("Time Complexity:", current_time_comp)
        self.create_info_field("Date completed", "3/10/21")

        # Creates the Desc box
        self.create_section(self.left_panel, "Description:", "PlaceHolder for Desc", height=12)

        # Button frame
        self.button_frame = tk.Frame(self.right_panel, bg='#5DADE2', bd=0)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))  # Reduced top padding from 20 to 10

        # Cancel and Select buttons
        self.select_btn = tk.Button(
            self.button_frame,
            text="Select",
            command=self.destroy,
            bg='#90EE90',
            fg='black',
            relief='flat',
            padx=10,
            pady=5
        )
        self.select_btn.pack(side=tk.RIGHT, padx=(0, 5))

        self.cancel_btn = tk.Button(
            self.button_frame,
            text="Cancel",
            bg='#F08080',
            fg='black',
            relief='flat',
            padx=10,
            pady=5
        )
        self.cancel_btn.pack(side=tk.RIGHT, padx=5)
        

    def create_info_field(self, label_text, value_text):
        frame = tk.Frame(self.right_panel, bg='#5DADE2', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text=label_text, font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)
        tk.Label(frame, text=value_text, font=("Arial", 10), bg='#5DADE2').pack(anchor=tk.W)


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
        tag_label.pack(side=tk.RIGHT, padx=(0, 5))

    def create_section(self, parent, title, desc, height=7):
        frame = tk.Frame(parent, bg='#5DADE2', bd=0)
        frame.pack(fill=tk.X, pady=(0, 5))

        header_frame = tk.Frame(frame, bg='#5DADE2')
        header_frame.pack(fill=tk.X, anchor=tk.W)

        tk.Label(header_frame, text=title, font=self.fonts["Body_Tuple"], bg='#5DADE2').pack(side=tk.LEFT, padx=5, pady=2)

        container_frame = tk.Frame(frame, bg='#D3D3D3', bd=1, relief='solid')
        container_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=(0, 2))

        scrollbar = tk.Scrollbar(container_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(
            container_frame, 
            height=height, 
            wrap=tk.WORD, 
            bg='#D3D3D3', 
            bd=0,
            yscrollcommand=scrollbar.set,
            font=self.fonts["Description_Tuple"],  
            fg='black',         
            padx=5,            
            pady=5
        )
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=text.yview)
        text.insert("1.0", desc)

        # Disable the text widget to make it read-only
        text.config(state='disabled')
        # Change cursor to default arrow instead of text insertion cursor
        text.config(cursor="arrow")


    

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrentTask()
    root.mainloop()