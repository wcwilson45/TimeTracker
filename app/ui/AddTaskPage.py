

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
        self.main_app.addtask_window = self

        # Define path
        self.path = pathlib.Path(__file__).parent
        self.path = str(self.path).replace("AddTaskPage.py", '') + '\\Databases' + '\\task_list.db'

        self.tags_path = pathlib.Path(__file__).parent
        self.tags_path = str(self.tags_path).replace('AddTaskPage.py','') + '\\Databases' + '\\tags.db'

        # Create or Connect to the database
        conn = sqlite3.connect(self.tags_path)

        # Create a cursor instance
        c = conn.cursor()

        c.execute("SELECT tag_name FROM tags")  # Fetch tag_names from tag database
        tags = c.fetchall()
        global values
        values = []

        # Add data to the list
        for tag in tags:
            values.append(tag[0])

        # Commit changes
        conn.commit()

        # Close connection to the database
        conn.close()


        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set the main window properties
        self.geometry("390x370")
        self.title("Add Task")
        self.configure(bg=background_color)

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=24, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=12, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=12)
        }

        # Complexity options
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]

        # Style configurations
        self.style = ttk.Style(self)
        self.style.theme_use("alt")
        self.style.configure('MainFrame.TFrame', background=background_color) 
        self.style.configure('Input.TEntry', background='d3d3d3', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('TLabel', background=background_color, font=("SF Pro Text", 8)) 

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        # Header frame
        header_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 6), sticky='ew')

        # Task Name
        label = ttk.Label(header_frame, text="Task Name:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, padx=(0, 10), sticky='w')
        self.task_name_entry = ttk.Entry(header_frame, style='Input.TEntry', width=40)
        self.task_name_entry.grid(row=0, column=1, sticky='ew')

        # Content container
        content_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        content_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        # Left column
        left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        left_frame.grid(row=0, column=0, padx=(0, 8), sticky='nsew')

        # Description
        label = ttk.Label(left_frame, text="Description:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w')

        desc_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        desc_frame.grid(row=1, column=0, pady=(3, 6), sticky='nsew')

        desc_scrollbar = ttk.Scrollbar(desc_frame, orient='vertical')
        desc_scrollbar.grid(row=0, column=1, sticky='ns')

        self.desc_text = tk.Text(
            desc_frame, height=7, width=30, bg='#d3d3d3', relief="solid", bd=1, font=("SF Pro Text", 10),
            yscrollcommand=desc_scrollbar.set
        )
        self.desc_text.grid(row=0, column=0, sticky='nsew')
        desc_scrollbar.config(command=self.desc_text.yview)

        button_width = 9

        # Button frame
        button_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        button_frame.grid(row=7, column=0, pady=(8, 6), sticky='ew')

        cancel_btn = tk.Button(button_frame, font=("SF Pro Text", 10),text="Cancel", command=self.cancel_action, bg=org_btn_color)
        cancel_btn.grid(row=0, column=1)

        confirm_btn = tk.Button(button_frame, text="Confirm", font=("SF Pro Text", 10),command=self.confirm_action, bg=green_btn_color)
        confirm_btn.grid(row=0, column=0, padx=(0,6))



        # Right column
        right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        right_frame.grid(row=0, column=1, sticky='nsew')

        # Tags
        label = ttk.Label(right_frame, text="Tags:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w')
        
        # Create the tag text frame
        tag_frame = ttk.Frame(right_frame)
        tag_frame.grid(row=1, column=0, pady=(3, 4), sticky='w')

        # Add a scrollbar for tag_text
        tag_scrollbar = ttk.Scrollbar(tag_frame, orient='vertical')
        tag_scrollbar.grid(row=0, column=1, sticky='ns')

        # Create the Text widget for tags
        self.tag_text = tk.Text(tag_frame, height=7, width=12, bg='#d3d3d3', relief="solid", bd=1, font=("SF Pro Text", 10),
                                yscrollcommand=tag_scrollbar.set)  # Link scrollbar to the Text widget
        self.tag_text.grid(row=0, column=0)

        # Configure the scrollbar to control tag_text
        tag_scrollbar.config(command=self.tag_text.yview)
        

        # New frame specifically for Listbox and Scrollbar
        listbox_frame = ttk.Frame(right_frame, style='MainFrame.TFrame')
        listbox_frame.grid(row=2, column=0, pady=(0, 6), sticky='w')

        # Add a vertical scrollbar for the Listbox
        list_scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical')
        list_scrollbar.grid(row=0, column=1, sticky='ns')  # Scrollbar placed next to the Listbox

        # Create the Listbox and link it to the scrollbar
        self.tag_listbox = tk.Listbox(listbox_frame, selectmode="multiple", exportselection=0, width=14,height=8, bg="#d3d3d3", relief='solid', yscrollcommand=tag_scrollbar.set)
        self.tag_listbox.grid(row=0, column=0, pady=(0, 6), sticky='w')

        # Configure the scrollbar to control the Listbox
        list_scrollbar.config(command=self.tag_listbox.yview)

        # Bind the Listbox selection to update the tag_text
        self.tag_listbox.bind("<<ListboxSelect>>", lambda _: self.update_tag_entry())

        # Adds the tags loaded from the tags table into the listbox
        for value in values:
            self.tag_listbox.insert(tk.END, value)

        # Time Complexity
        label = ttk.Label(left_frame, text="Time Complexity:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=3, column=0, sticky='w')

        #Autofill today's date button
        autofill_date_btn = tk.Button(button_frame, text="Autofill date", command=self.autofill_date,
                                bg="#E39ff6", fg="#000000", font=("SF Pro Text", 10), activebackground="#800080", activeforeground="#000000", width=button_width)
        autofill_date_btn.grid(row=0, column=2, padx=(10, 0))

        complexity_frame = ttk.Frame(left_frame, style='MainFrame.TFrame')
        complexity_frame.grid(row=4, column=0, pady=(3, 6), sticky='ew')


        self.type_combo = ttk.Combobox(complexity_frame, values=self.complexity_types, style='TCombobox', state='readonly')
        self.type_combo.grid(row=0, column=0, sticky='ew', pady=(0, 3))
        self.type_combo.set("Select Type")

        self.value_combo = ttk.Combobox(complexity_frame, state='readonly')
        self.value_combo.grid(row=1, column=0, sticky='ew')
        self.value_combo.set("Select Value")

        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)

        # Date Completed
        label = ttk.Label(left_frame, text="Start Date (MM-DD-YYYY):", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=5, column=0, sticky='w')

        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(left_frame, textvariable=self.date_var,style='Input.TEntry')
        self.date_entry.grid(row=6, column=0, sticky='ew')

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
        self.on_close()

    def update_tag_entry(self):
        # Get selected values from the Listbox widget
        selected_values = [self.tag_listbox.get(idx) for idx in self.tag_listbox.curselection()]

        # Update with the selected values
        self.tag_text.delete(1.0, "end")  # Clear the Text widget
        self.tag_text.insert("1.0", "\n".join(selected_values))  # Insert the selected tags

        

    def confirm_action(self):
        task_name = self.task_name_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        tags = self.tag_text.get("1.0", tk.END).strip()
        complexity_type = self.type_combo.get()
        complexity_value = self.value_combo.get()
        start_date = self.date_entry.get()
        task_time = "00:00:00" 
        end_date = "01-02-2025"

        # Store required fields in a dictionary or list
        required_fields = {
            "Task Name": task_name,
            "Description": description,
            "Tags": tags,
            "Start Date": start_date,
            "Complexity Type": complexity_type,
            "Complexity Value": complexity_value
        }

        # Check if any required field is empty and show a warning if so
        missing_fields = [field for field, value in required_fields.items() if not value or value == "Select Value" or value == "Select Type"]
        
        if missing_fields:
            missing_fields_str = ", ".join(missing_fields)
            messagebox.showwarning("Warning", f"Please fill in the following required fields: {missing_fields_str}")
            
            return  # Stop further action if any field is missing
        
        res = tags.split('\n') # Splits the string to check tags

        if not all(tag in values for tag in res): #Checks to see if tags are in the accepted tags
          
            messagebox.showwarning("Warning", f"The Tags you have selected are invaild")

            return  # Stop further action if any field is missing
        else:
            
            confirm = messagebox.askyesno("Confirm Add", "Are you sure you want to add this task?") #Askes if sure to add task
            
        #Adds task
        if confirm:

            # Connect to the database
            conn = sqlite3.connect(self.path)
            c = conn.cursor()

            c.execute("SELECT MAX(task_id) FROM TaskList")
            max_tasklist_id = c.fetchone()[0]
            max_tasklist_id = max_tasklist_id if max_tasklist_id is not None else 0  # Default to 0 if None

            c.execute("SELECT MAX(task_id) FROM CompletedTasks")
            max_completed_id = c.fetchone()[0]
            max_completed_id = max_completed_id if max_completed_id is not None else 0  # Default to 0 if None

            c.execute("SELECT MAX(task_id) FROM CurrentTask")
            current_task_id = c.fetchone()[0]
            current_task_id = current_task_id if current_task_id is not None else 0  # Default to 0 if None

            # Find the next task_id (1 + max of both task lists)
            task_id = max(max_tasklist_id, max_completed_id)
            task_id = max(task_id, current_task_id) + 1

            list_place = task_id

            # Insert data
            c.execute(
                "INSERT INTO TaskList VALUES(:task_name, :task_time, :task_weight, :task_id, :task_start_date, :task_end_date, :task_description, :task_weight_type, :task_tags, :list_place)",
                {
                    "task_name": task_name,
                    "task_time": task_time,
                    "task_weight": complexity_value,
                    "task_id": task_id,
                    "task_start_date": start_date,
                    "task_end_date": end_date,
                    "task_description": description,
                    "task_weight_type": complexity_type,
                    "task_tags": tags,
                    "list_place": list_place
                }
            )


            conn.commit()
            conn.close()
            
            if hasattr(self.main_app, 'query_database'):
                self.main_app.query_database()

            self.destroy()
            self.on_close()
           
        else:
            return

    def autofill_date(self):
        CurrentDate = date.today()
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, CurrentDate.strftime("%m-%d-%Y"))

    def on_close(self):
        self.main_app.addtask_window = None  # Reset reference to allow reopening
        self.main_app.add_button.config(state=tk.NORMAL)
        self.destroy()

if __name__ == "__main__":
    app = AddTaskWindow()
    app.mainloop()
