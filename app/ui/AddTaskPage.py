from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import pathlib
import sqlite3
from datetime import date

background_color = "#A9A9A9"

green_btn_color = "#b2fba5"
org_btn_color = "#e99e56"



class AddTaskWindow(tk.Tk):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.main_app.task_window = self

        # Define path
        self.path = pathlib.Path(__file__).parent
        self.path = str(self.path).replace("ui", '') + 'task_list.db'

        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set the main window properties
        self.geometry("700x250")
        self.title("Add Task")
        self.configure(bg=background_color)

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=8, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }

        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]

        # Style configurations
        self.style = ttk.Style(self)
        self.style.theme_use("alt")
        self.style.configure('MainFrame.TFrame', background=background_color)  # Light Blue for frames
        self.style.configure('Input.TEntry', background='d3d3d3', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('TLabel', background=background_color, font=("SF Pro Text", 8))  # Light Blue for labels

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Header frame
        header_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        header_frame.pack(fill='x', pady=(0, 6))

        # Task Name
        label = ttk.Label(header_frame, text="Task Name", font=self.fonts['header'], style='TLabel')
        label.pack(side='left', padx=(0, 10))
        self.task_name_entry = ttk.Entry(header_frame, style='Input.TEntry', width=40)
        self.task_name_entry.pack(side='left', fill='x', expand=True)

        # Content container
        content_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        content_frame.pack(fill='both', expand=True)

        # Left column
        left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))

        # Description
        label = ttk.Label(left_frame, text="Description:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        desc_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        desc_frame.pack(fill='x', pady=(3, 6))

        desc_scrollbar = ttk.Scrollbar(desc_frame, orient='vertical')
        desc_scrollbar.pack(side='right', fill='y')

        self.desc_text = tk.Text(
            desc_frame, height=7, width=30, bg='#d3d3d3', relief="solid", bd=1, font=("SF Pro Text", 10),
            yscrollcommand=desc_scrollbar.set
        )
        self.desc_text.pack(side='left', fill='both', expand=True)
        desc_scrollbar.config(command=self.desc_text.yview)

        button_width = 9

        # Button frame
        button_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        button_frame.pack(fill='x', pady=(3, 6))

        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_action, bg=org_btn_color, width=button_width)
        cancel_btn.pack(side='left', padx=(0, 8))

        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirm_action, bg=green_btn_color, width=button_width)
        confirm_btn.pack(side='left')


        # Right column
        right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        right_frame.pack(side='left', fill='both', expand=True)

        # Tags
        label = ttk.Label(right_frame, text="Tags:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')
        self.tag_entry = ttk.Entry(right_frame, style='Input.TEntry')
        self.tag_entry.pack(fill='x', pady=(3, 6))

        # Time Complexity
        label = ttk.Label(right_frame, text="Time Complexity:", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        #Autofill today's date button
        autofill_date_btn = tk.Button(button_frame, text="Autofill date", command=self.autofill_date,
                                bg="#E39ff6", fg="#000000", font=("SF Pro Text", 10), activebackground="#800080", activeforeground="#000000", width=button_width)
        autofill_date_btn.pack(side='right')

        complexity_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        complexity_frame.pack(fill='x', pady=(3, 6))

        self.type_combo = ttk.Combobox(complexity_frame, values=self.complexity_types, state='readonly')
        self.type_combo.pack(fill='x', pady=(0, 3))
        self.type_combo.set("Select Type")

        self.value_combo = ttk.Combobox(complexity_frame, state='readonly')
        self.value_combo.pack(fill='x')
        self.value_combo.set("Select Value")

        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)

        # Date
        label = ttk.Label(right_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.pack(anchor='w')

        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(right_frame, textvariable=self.date_var, style='Input.TEntry')
        self.date_entry.pack(fill='x')

    def update_values(self, event=None):
        selected_type = self.type_combo.get()
        if selected_type == "T-Shirt Size":
            self.value_combo['values'] = self.tshirt_sizes
        elif selected_type == "Fibonacci":
            self.value_combo['values'] = self.fibonacci
        else:
            self.value_combo['values'] = []
        self.value_combo.set("Select Value")

    def cancel_action(self):
        self.main_app.add_button.config(state=tk.NORMAL)
        self.destroy()
        self.main_app.task_window = None
        

    def confirm_action(self):
        confirm = messagebox.askyesno("Confirm Add", "Are you sure you want to add this task?")
        task_name = self.task_name_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        tags = self.tag_entry.get()
        complexity_type = self.type_combo.get()
        complexity_value = self.value_combo.get()
        start_date = self.date_var.get()
        task_time = "00:00:00" 
        end_date = "01-02-2025"

        if confirm:
            # Connect to the database
            conn = sqlite3.connect(self.path)
            c = conn.cursor()

            c.execute("SELECT MAX(task_id) FROM TaskList")
            last_id = c.fetchone()[0]
            task_id = (last_id + 1) if last_id else 1



            # Insert data
            c.execute(
            "INSERT INTO TaskList VALUES(:task_name, :task_time, :task_weight, :task_id, :task_start_date, :task_end_date, :task_description, :task_weight_type, :task_tags)",
            {
                "task_name": task_name,
                "task_time": task_time,
                "task_weight": complexity_value,
                "task_id": task_id,
                "task_start_date": start_date,
                "task_end_date": end_date,
                "task_description": description,
                "task_weight_type": complexity_type,
                "task_tags": tags
            }
        )


            conn.commit()
            conn.close()

            self.main_app.add_button.config(state=tk.NORMAL)
            self.destroy()
            self.main_app.task_window = None

        else:
            self.lift()
            self.focus_force()
            return

    def autofill_date(self):
        CurrentDate = date.today()
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, CurrentDate.strftime("%m-%d-%Y"))

    def on_close(self):
        self.main_app.add_button.config(state=tk.NORMAL)
        self.destroy()
        self.main_app.task_window = None  # Reset reference to allow reopening

if __name__ == "__main__":
    app = AddTaskWindow()
    app.mainloop()
