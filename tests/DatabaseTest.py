from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
from datetime import datetime
from ui import (
    CompletedTasksWindow,
    EditTaskWindow,
    CommitHistoryWindow,
    AddTaskWindow,
    CurrentTaskWindow
)


#MAKE SURE TO EITHER COMMENT OUT VOID CODE OR JUST DELETE IT WHEN APPLICABLE
#DATABASE IS CALLED task_list.db
#We need to create a table for each distinct treeview as well as the current task.
#Switching current task will just involve moving the current task to the task_list,
#  and the task_list item to the current task.

#Global Variables
blue_background_color = "#5DADE2"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "E0E0E0"


"""
data = [
            ["Collect money", "00:14:35", "5", "1"],
            ["Print money", "00:14:35", "5", "2"],
            ["Do things", "00:14:35", "5", "3"],
            ["Stuff", "00:14:35", "5", "4"],
            ["Explain", "00:14:35", "5", "5"],
            ["Data", "00:14:35", "5", "6"],
            ["Print paper", "00:30:21", "3", "7"]
        ]
"""
#Create a database or connect to an existing database
conn = sqlite3.connect('task_list.db')

#Create a cursor instance
c = conn.cursor()

#Table for TaskList database
c.execute("""CREATE TABLE if not exists TaskList (
          task_name text,
          task_time text,
          task_weight text,
          task_id integer)
""")

#Table for Completed database

#Table for Tags

#Add dummy data to database
"""
for task in data:
    c.execute("INSERT INTO TaskList VALUES (:task_name, :task_time, :task_weight, :task_id)",
              {
               "task_name": task[0],
               "task_time": task[1],
               "task_weight": task[2],
               "task_id": task[3]
              }
              )
"""
#Commit Changes
conn.commit()

conn.close()



class App:
    def __init__(self, root):
      self.root = root
      self.root.title("Task Manager")
      self.root.geometry("800x1000")
      root.resizable(width = 0, height = 0)

      # Font Tuples for Use on pages
      self.fonts = {
            "Title_Tuple": tkfont.Font(family ="SF Pro Display", size =24, weight ="bold"),
            "Body_Tuple": tkfont.Font(family = "SF Pro Display", size = 12, weight = "bold"),
            "Description_Tuple": tkfont.Font(family = "Sf Pro Text", size = 12)
        }

      #Set Background color
      self.root.configure(bg = blue_background_color)

      #Main Container
      self.main_container = tk.Frame(root, background= blue_background_color)
      self.main_container.pack(expand = False, fill = "both")
      
      #Menu Button Dropdown
      self.menu_frame = tk.Frame(self.main_container, background= blue_background_color)
      self.menu_frame.pack(fill = "x", padx = 5, pady = 5)

      #Dropdown Menu
      self.menu_btn = ttk.Button(self.menu_frame, text = "⋮", width = 3, command = self.show_menu)
      self.menu_btn.pack(side = "left", padx = 5)

      #Page Title Label
      self.page_title = ttk.Label(self.menu_frame, text="NAVSEA Time Tracker", font=self.fonts['Body_Tuple'], background="#5DADE2")
      self.page_title.pack(side="left", padx=10)

      #get_current_time()
      current_task_time = 0
      self.time_box_full = current_task_time
      self.time_box_overlay = current_task_time

      #Create pages
      self.full_page = tk.Frame(self.main_container)
      self.completedtasks_page = tk.Frame(self.main_container)
      self.smalloverlay_page = tk.Frame(self.main_container)

      #Show main page at start-up
      self.current_page = self.full_page
      self.full_page.pack(expand=True, fill="both", padx=10, pady=5)

      #Create the popup menu
      self.popup_menu = tk.Menu(root, tearoff=0)
      self.popup_menu.add_command(label="NAVSEA Time Tracker", command=lambda: self.switch_page("NAVSEA Time Tracker"))
      self.popup_menu.add_command(label="Completed Tasks", command=lambda: self.switch_page("Completed Tasks"))
      self.popup_menu.add_command(label="Small Overlay", command=lambda: self.switch_page("Small Overlay"))
      self.popup_menu.configure(bg="#5DADE2")

      self.setup_full_page(self)
      self.setup_completedtasks_page()
      self.setup_smalloverlay_page()

      #Query the database for all information inside
      self.query_database()

      

    def show_menu(self):
        try:
            self.popup_menu.tk_popup(
                self.menu_btn.winfo_rootx(),
                self.menu_btn.winfo_rooty() + self.menu_btn.winfo_height()
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
      self.smalloverlay_page.configure(bg = blue_background_color)
      Label(self.smalloverlay_page, text = "Task Name:", 
             font = self.fonts['Body_Tuple'],
             background= blue_background_color
       ).grid(row = 0, column= 0, sticky = W, pady = 2)

      Label(self.smalloverlay_page, text = "Time: ",
             font=self.fonts['Body_Tuple'],
             background= blue_background_color
             ).grid(row = 1, column = 0, sticky = W, pady = 2)
      
      self.time_box_overlay = Text(self.smalloverlay_page, height = 1, width = 10,
                    font = self.fonts['Body_Tuple'],
                    background = grey_button_color)
      self.time_box_overlay.grid(row = 1, column = 0, padx = 50, pady = 5, sticky = E)
      #Set the timer text to the current time
      self.time_box_overlay.insert("1.0", "00:00:00")
      #Make the time box Read-Only
      self.time_box_overlay.config(state = DISABLED)
      self.small_overlay_start_button = tk.Button(self.smalloverlay_page, text="Start",relief = "flat", background="#77DD77", command=self.start_timer)
      self.small_overlay_start_button.grid(row=2, column=0, sticky=W,padx = 0, pady=5)

      self.small_overlay_stop_button = tk.Button(self.smalloverlay_page, text="Stop",relief = "flat", background="#FF7276", command=self.stop_timer)
      self.small_overlay_stop_button.grid(row=2, column=0, sticky=W,padx = 45, pady=5)


   
    def update_timer_boxes(self, timer_text):
      """Update the timer display in both timer boxes."""
          # Update the timer on the Full page
      if self.time_box_full:
        self.time_box_full.config(state=NORMAL)
        self.time_box_full.delete("1.0", tk.END)
        self.time_box_full.insert("1.0", timer_text)
        self.time_box_full.config(state=DISABLED)

          # Update the timer on the Small Overlay page
      if self.time_box_overlay:
        self.time_box_overlay.config(state=NORMAL)
        self.time_box_overlay.delete("1.0", tk.END)
        self.time_box_overlay.insert("1.0", timer_text)
        self.time_box_overlay.config(state=DISABLED)


    def setup_full_page(self, task_list):
        self.full_page.configure(background= blue_background_color)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
        background = "black",
        foreground = "black",
        rowheight = 25,
        fieldbackground = grey_button_color,
        bd = "black")
        
        #Dummy info for name and description. Will become void
        currenttask_name = "John"
        currenttask_desc = "This is the description"

        #Current Task Frame
        currenttask_frame = tk.Frame(self.full_page, bg = blue_background_color)
        currenttask_frame.pack(pady=0, side = TOP, fill = 'x')

        #Set Labels for Name, Time, and Description
        Label(currenttask_frame, text = f"Task Name: {currenttask_name}",
               font=self.fonts['Body_Tuple'],
               background="#5DADE2").grid(row=0, column=0, sticky=W,pady=2)

        Label(currenttask_frame, text = "Time: ",
               font=self.fonts['Body_Tuple'],
               background="#5DADE2").grid(row=1, column=0, sticky=W,pady=2)
        Label(currenttask_frame, text="Description:",
               font=self.fonts['Body_Tuple'],
               background="#5DADE2").grid(row=4, column=0,sticky=W, pady=2)
        
        #Set Description Frame and Box inside the Frame
        description_frame = tk.Frame(self.full_page, bg = blue_background_color)
        description_frame.pack(pady = 5, fill = 'x')

        #Description Scrollbar
        description_scroll = Scrollbar(description_frame)
        description_scroll.grid(row = 0, column = 1, sticky = "ns")
        description_box = Text(description_frame, yscrollcommand= description_scroll.set,
                                height=5,
                                    width=62,border = 1, font=self.fonts['Description_Tuple'],
                                    background="#d3d3d3")
        description_box.grid(row = 0, column = 0)

        #Insert Current Task Description
        description_box.insert("1.0", currenttask_desc)
        description_scroll.config(command = description_box.yview)


        #Change color when a item is selected
        style.map("Treeview",
        background = [('selected', "347083")])

        #Put the task list inside a frame
        tasklist_frame = tk.Frame(self.full_page, bg = blue_background_color)
        tasklist_frame.pack(pady=10, fill = "x")

        #Create scrollbar
        tasklist_scroll = Scrollbar(tasklist_frame)
        tasklist_scroll.grid(row = 0, column = 1, sticky = "ns")

        #Set scrollbar
        self.task_list = ttk.Treeview(tasklist_frame, yscrollcommand=tasklist_scroll.set, selectmode = "extended", style  = "Treeview")
        self.task_list.grid(row = 0, column = 0)

        #Task List is vertical scroll
        tasklist_scroll.config(command = self.task_list.yview)

        #Format columns
        self.task_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID")
        self.task_list.column("#0", width = 0, stretch=NO)
        self.task_list.column('Task Name', anchor = W, width = 250)
        self.task_list.column('Task Time', anchor = CENTER, width = 100)
        self.task_list.column('Task Weight', anchor = CENTER, width =100)
        self.task_list.column('Task ID',anchor = CENTER, width = 100)

        #Format headings
        self.task_list.heading("#0", text = "", anchor = W)
        self.task_list.heading("Task Name", text = "Task Name", anchor = W)
        self.task_list.heading("Task Time", text = "Time", anchor = CENTER)
        self.task_list.heading("Task Weight", text = "Weight", anchor = CENTER)
        self.task_list.heading("Task ID", text = "ID", anchor = CENTER)

        #Configure the different rows for color
        self.task_list.tag_configure('oddrow', background=  "#A9A9A9", foreground= "black")
        self.task_list.tag_configure('evenrow', background=  grey_button_color, foreground= "black")

        #This is the select thing. Will become void after current task table is implemented
        #So Full page will become smaller and when using select button it should put task information at the top.
        data_frame = LabelFrame(self.full_page, text = "Input")
        data_frame.pack(fill = "x", padx = 20)

        tn_label = Label(data_frame, text = "Task Name")
        tn_label.grid(row = 0, column = 0, padx = 10, pady = 0)
        self.tn_entry = Entry(data_frame)
        self.tn_entry.grid(row = 1, column = 0)

        tt_label = Label(data_frame, text = "Task Time")
        tt_label.grid(row = 0, column = 1, padx = 10, pady = 0)
        self.tt_entry = Entry(data_frame)
        self.tt_entry.grid(row = 1, column = 1)

        tw_label = Label(data_frame, text = "Task Weight")
        tw_label.grid(row = 0, column = 2, padx = 10, pady = 0)
        self.tw_entry = Entry(data_frame)
        self.tw_entry.grid(row = 1, column = 2)

        ti_label = Label(data_frame, text = "Task ID")
        ti_label.grid(row = 0, column = 3, padx = 10, pady = 0)
        self.ti_entry = Entry(data_frame)
        self.ti_entry.grid(row = 1, column = 3)

        button_frame = LabelFrame(self.full_page, text = "Commands")
        button_frame.pack(fill = "x",pady = 10,padx = 5,side = BOTTOM)


        #Buttons
        update_button = Button(button_frame, text = "Edit Task", command = self.open_EditTaskWindow)
        update_button.grid(row = 0, column = 0, padx = 6, pady = 10)

        add_button = Button(button_frame, text = "Add Task", command = self.open_AddTaskWindow)
        add_button.grid(row = 0, column = 1, padx = 6, pady = 10)

        remove_button = Button(button_frame, text = "Remove Task", command = self.remove_one)
        remove_button.grid(row = 0, column = 2, padx = 6, pady = 10)

        remove_all_button = Button(button_frame, text = "Remove All", command = self.remove_all)
        remove_all_button.grid(row = 0, column = 3, padx = 6, pady = 10)

        moveup_button = Button(button_frame, text = "Move Up", command = self.move_up)
        moveup_button.grid(row = 0, column = 4, padx = 6, pady = 10)

        movedown_button = Button(button_frame, text = "Move Down", command = self.move_down)
        movedown_button.grid(row = 0, column = 5, padx = 6, pady = 10)

        #Need to add command for opening the tags Page
        tags_button = Button(button_frame, text = "Tags")
        tags_button.grid(row = 0, column = 6, padx = 6, pady = 10)

        select_record_button = Button(button_frame, text = "Select Record", command = self.select_record)
        select_record_button.grid(row = 0, column = 7, padx = 6, pady = 10)

        #Uses select button on single click. Takes value from TreeView, not the database
        self.task_list.bind("<ButtonRelease-1>", self.select_record)


    #Move a task up in the task list
    def move_up(self):
        rows = self.task_list.selection()
        for row in rows:
            self.task_list.move(row, self.task_list.parent(row), self.task_list.index(row)-1)
    
    def move_down(self):
        rows = self.task_list.selection()
        for row in reversed(rows):
            self.task_list.move(row, self.task_list.parent(row), self.task_list.index(row)+1)


    def select_record(self, e):
        #Clear entry boxes
        self.tn_entry.delete(0, END)
        self.tt_entry.delete(0, END)
        self.ti_entry.delete(0, END)
        self.tw_entry.delete(0, END)

        #Grab record number
        selected = self.task_list.focus()

        #Grab record values
        values = self.task_list.item(selected, "values")

        #Insert into current task
        if values:
            self.tn_entry.insert(0, values[0])
            self.tt_entry.insert(0, values[1])
            self.ti_entry.insert(0, values[2])
            self.tw_entry.insert(0, values[3])


    def query_database(self):
    #Create a database or connect to an existing database
        conn = sqlite3.connect('task_list.db')

        #Create a cursor instance
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM TaskList")
        tasks = c.fetchall()
        #Add data to screen
        global count
        count = 0

        for record in tasks:
            print(record)
            #Adding the dummy data. Will become void?
        for record in tasks:
            if count % 2 == 0:
                self.task_list.insert(parent = '', index = 'end', iid = count, text = '', values = (record[1],record[2],record[0],record[4]), tags = ('evenrow', ""))
            else:
                self.task_list.insert(parent = '', index = 'end', iid = count, text = '', values = (record[1],record[2],record[0],record[4]), tags = ('oddrow', ""))
                #Increment count
            count += 1
        
        #Commit Changes
        conn.commit()

        conn.close()

       
    #def insert_task(self, task_id):

    def remove_one(self):
        x = self.task_list.selection()[0]
        self.task_list.delete(x)

    def remove_all(self):
        for task in self.task_list.get_children():
            self.task_list.delete(task)

    def setup_completedtasks_page(self):
        self.completedtasks_page.configure(background=blue_background_color)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background=grey_button_color,
                        foreground=blue_background_color,
                        rowheight=25,
                        fieldbackground=grey_button_color)

        # Change color when a item is selected
        style.map("Treeview",
                  background=[('selected', "347083")])

        # Put the task list inside a frame
        completedlist_frame = tk.Frame(self.completedtasks_page, bg=blue_background_color)
        completedlist_frame.pack(pady=10)

        # Create scrollbar
        completedlist_scroll = Scrollbar(completedlist_frame)
        completedlist_scroll.pack(side=RIGHT, fill=Y)

        # Set scrollbar
        completed_list = ttk.Treeview(completedlist_frame, yscrollcommand=completedlist_scroll.set,
                                      selectmode="extended")
        completed_list.pack()

        self.completed_list = completed_list

        # Task List is vertical scroll
        completedlist_scroll.config(command=completed_list.yview)

        # Format columns
        completed_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID", "Completion Date",
                                     "Total Duration")

        completed_list.column("#0", width=0, stretch=NO)
        completed_list.column('Task Name', anchor=W, width=120)
        completed_list.column('Task Time', anchor=CENTER, width=100)
        completed_list.column('Task Weight', anchor=CENTER, width=75)
        completed_list.column('Task ID', anchor=CENTER, width=100)
        completed_list.column('Completion Date', anchor=CENTER, width=150)
        completed_list.column('Total Duration', anchor=CENTER, width=100)

        completed_list.heading("#0", text="", anchor=W)
        completed_list.heading("Task Name", text="Task Name", anchor=W)
        completed_list.heading("Task Time", text="Time", anchor=CENTER)
        completed_list.heading("Task Weight", text="Weight", anchor=CENTER)
        completed_list.heading("Task ID", text="ID", anchor=CENTER)
        completed_list.heading("Completion Date", text="Completed On", anchor=CENTER)
        completed_list.heading("Total Duration", text="Total Time", anchor=CENTER)

        self.completed_list.tag_configure('oddrow', background="white")
        self.completed_list.tag_configure('evenrow', background=grey_button_color)

        # load completed tasks data
        self.load_completed_tasks

    def load_completed_tasks(self):
        # Clear existing items
        for item in self.completed_list.get_children():
            self.completed_list.delete(item)

        conn = sqlite3.connect('task_list.db')
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM CompletedTasks ORDER BY completion_date DESC")
            tasks = c.fetchall()

            for i, task in enumerate(tasks):
                tag = ('evenrow' if i % 2 == 0 else 'oddrow')
                self.completed_list.insert('', 'end', values=task, tags=tag)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading completed tasks: {str(e)}")
        finally:
            conn.close()

    #def insert_completed_task(self, task_id):
       
    #def on_item_click(self, event):
       
    #def current_item_click(self, event):
       
    def open_AddTaskWindow(self):
        self.task_window = AddTaskWindow()
        self.task_window.grab_set()

    def open_AddCompleteTaskWindow(self, task_id):
        self.task_window = CompletedTasksWindow(
            task_id = task_id
        )
        self.task_window.grab_set()
    
    def open_EditTaskWindow(self):
        self.tn_value = self.tn_entry.get()
        self.tt_value = self.tt_entry.get()
        self.tw_value = self.tw_entry.get()
        self.ti_value = self.ti_entry.get()
        self.task_window = EditTaskWindow(self.tn_value, self.tt_value, self.tw_value, self.ti_value)
        self.task_window.grab_set()

    def open_CurrentTaskWindow(self):
        self.task_window = CurrentTaskWindow()
        self.task_window.grab_set()

    
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
