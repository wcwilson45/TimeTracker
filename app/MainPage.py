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
    CurrentTaskWindow,
    TagsDB,
    CompletedTasksList
)


#MAKE SURE TO EITHER COMMENT OUT VOID CODE OR JUST DELETE IT WHEN APPLICABLE
#DATABASE IS CALLED task_list.db
#We need to create a table for each distinct treeview as well as the current task.
#Switching current task will just involve moving the current task to the task_list,
#  and the task_list item to the current task.

#Global Variables
background_color = "#A9A9A9"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "#E0E0E0"

main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"


"""data = [
            ["Collect money", "00:14:35", "1.1", "1", "12-01-10", "12-02-01", "Description for Collect Money Task", "Fibonacci"],
            ["Print money", "00:14:35", "2.1", "2", "12-01-10", "12-02-02", "Description for Print Money Task", "Fibonacci"],
            ["Do things", "00:14:35", "3.1", "3", "12-01-10", "12-02-03", "Description for Do Things Task", "Fibonacci"],
            ["Stuff", "00:14:35", "4.1", "4", "12-01-10", "12-02-04", "Description for Stuff Task", "Fibonacci"],
            ["Explain", "00:14:35", "5.1", "5", "12-01-10", "12-02-05", "Description for Explain Task", "Fibonacci"],
            ["Data", "00:14:35", "5", "6.1", "12-01-10", "12-02-06", "Description for Data Task", "Fibonacci"],
            ["Print paper", "00:30:21", "7.1", "7", "12-01-10", "12-02-07", "Description for Print Paper Task", "Fibonacci"]
        ]
"""
"""
completed_data = [
    ["Write Documentation", "01:30:00", "5", "101", "2024-01-28 15:30:00", "01:45:23"],
    ["Debug Login", "02:00:00", "7", "102", "2024-01-27 14:20:00", "02:15:45"],
    ["Team Meeting", "01:00:00", "3", "103", "2024-01-27 10:00:00", "00:55:30"],
    ["Code Review", "00:45:00", "4", "104", "2024-01-26 16:45:00", "00:50:15"],
    ["Test Features", "03:00:00", "8", "105", "2024-01-26 11:30:00", "03:30:00"]
]
"""
#Create a database or connect to an existing database
conn = sqlite3.connect('task_list.db')

#Create a cursor instance
c = conn.cursor()

#Table for TaskList database
c.execute("""CREATE TABLE if not exists TaskList (
          task_name text,
          task_time text DEFAULT '00:00:00',
          task_weight text,
          task_id integer PRIMARY KEY AUTOINCREMENT,
          task_start_date text,
          task_end_date text,
          task_description text,
          task_weight_type text,
          task_tags text
          )
""")

c.execute("""CREATE TABLE if not exists CurrentTask(
          task_name text,
          task_time text,
          task_weight text,
          task_id integer,
          task_start_date text,
          task_end_date text,
          task_description text,
          task_weight_type text,
          task_tags text)
""")

#Table for Completed database
c.execute("""CREATE TABLE if not exists CompletedTasks (
          task_name text,
          task_time text,
          task_weight text,
          task_id integer,
          completion_date text,
          total_duration text,
          PRIMARY KEY (task_id)
)""")

#Table for Tags

#Add dummy data to database

"""for task in data:
    c.execute(INSERT INTO TaskList (task_name, task_time, task_weight, task_id, task_start_date, task_end_date, task_description, task_weight_type)
              VALUES (:task_name, :task_time, :task_weight, :task_id, :task_start_date, :task_end_date, :task_description, :task_weight_type),
              {
               "task_name": task[0],
               "task_time": task[1],
               "task_weight": task[2],
               "task_id": task[3],
               "task_start_date": task[4],
               "task_end_date": task[5],
               "task_description": task[6],
               "task_weight_type": task[7]
              }
              )
"""
"""
# Add completed tasks dummy data
for task in completed_data:
    c.execute(INSERT OR REPLACE INTO CompletedTasks VALUES 
              (:task_name, :task_time, :task_weight, :task_id, :completion_date, :total_duration),
              {
                  "task_name": task[0],
                  "task_time": task[1],
                  "task_weight": task[2],
                  "task_id": task[3],
                  "completion_date": task[4],
                  "total_duration": task[5]
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
      self.root.geometry("488x650")
      root.resizable(width = 0, height = 0)

      self.addtask_window = None
      self.edittask_window = None

      self.root.protocol("WM_DELETE_WINDOW", self.on_close)

      # Font Tuples for Use on pages
      self.fonts = {
            "Title_Tuple": tkfont.Font(family ="SF Pro Display", size =24, weight ="bold"),
            "Body_Tuple": tkfont.Font(family = "SF Pro Display", size = 12, weight = "bold"),
            "Description_Tuple": tkfont.Font(family = "Sf Pro Text", size = 12)
        }

      #Set Background color
      self.root.configure(bg = background_color)

      #Main Container
      self.main_container = tk.Frame(root, background= background_color)
      self.main_container.pack(expand = False, fill = "both")
      
      #Menu Button Dropdown
      self.menu_frame = tk.Frame(self.main_container, background= background_color)
      self.menu_frame.pack(fill = "x", padx = 5, pady = 5)

      #Dropdown Menu
      self.menu_btn = ttk.Button(self.menu_frame, text = "⋮", width = 3, command = self.show_menu)
      self.menu_btn.pack(side = "left", padx = 5)

      #Page Title Label
      self.page_title = ttk.Label(self.menu_frame, text="NAVSEA Time Tracker", font=self.fonts['Body_Tuple'], background= background_color)
      self.page_title.pack(side="left", padx=10)

      #get_current_time()
      current_task_time = 0
      self.time_box_full = current_task_time
      self.time_box_overlay = current_task_time

      #Create pages
      self.full_page = tk.Frame(self.main_container)
      self.completedtasks_page = CompletedTasksList(self.main_container, self)
      self.smalloverlay_page = tk.Frame(self.main_container)
      self.tags_database_page = TagsDB(self.main_container)

      #Show main page at start-up
      self.current_page = self.full_page
      self.full_page.pack(expand=True, fill="both", padx=10, pady=5)

      #Create the popup menu
      self.popup_menu = tk.Menu(root, tearoff=0)
      self.popup_menu.add_command(label="NAVSEA Time Tracker", command=lambda: self.switch_page("NAVSEA Time Tracker"))
      self.popup_menu.add_command(label="Completed Tasks", command=lambda: self.switch_page("Completed Tasks"))
      self.popup_menu.add_command(label="Small Overlay", command=lambda: self.switch_page("Small Overlay"))
      self.popup_menu.add_command(label="Tags Database", command=lambda: self.switch_page("Tags Database"))
      self.popup_menu.configure(bg= background_color)

      self.setup_full_page()
      self.completedtasks_page.pack_forget()
      self.setup_smalloverlay_page()

      #Query the database for all information inside
      self.query_database()

    def on_close(self):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit the program?")

        if confirm:
            if self.addtask_window:
                self.addtask_window.destroy()
            if self.edittask_window:
                self.edittask_window.destroy()
            self.root.destroy()
        else:
            self.root.lift()
            self.root.focus_force()
            return

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
            self.page_title.config(text="NAVSEA Time Tracker", background= background_color)
            self.root.geometry("488x650")
            self.query_database()
        elif page_name == "Completed Tasks":
            self.current_page = self.completedtasks_page
            self.page_title.config(text="Completed Tasks", background= background_color)
            self.root.geometry("600x400")
            self.completedtasks_page.load_completed_tasks()
        elif page_name == "Small Overlay":
            self.current_page = self.smalloverlay_page
            self.page_title.config(text="Small Overlay", background=background_color)
            self.root.geometry("230x160")
        elif page_name == "Tags Database":
            self.current_page = self.tags_database_page  
            self.page_title.config(text="Tags Database", background=background_color) #CHANGED REMEMBER <<<<<<<<<<
            self.root.geometry("530x600")  


        self.current_page.pack(expand=True, fill="both", padx=10, pady=5)



    def setup_smalloverlay_page(self):
      self.smalloverlay_page.configure(bg = background_color)
      Label(self.smalloverlay_page, text = "Task Name:", 
             font = self.fonts['Body_Tuple'],
             background= background_color
       ).grid(row = 0, column= 0, sticky = W, pady = 2)

      Label(self.smalloverlay_page, text = "Time: ",
             font=self.fonts['Body_Tuple'],
             background= background_color
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


    def setup_full_page(self):
        self.full_page.configure(background= background_color)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
        background = "black",
        foreground = "black",
        rowheight = 20,
        fieldbackground = grey_button_color,
        bd = "black")



        #Current Task Frame
        self.currenttask_frame = LabelFrame(self.full_page, text = f"Current Task" )
        self.currenttask_frame.pack(pady=0, side = TOP, fill = 'x')

        #Set Labels for Name, Time, and Description
        self.display_task_name = ttk.Label(self.currenttask_frame, text = f"Task Name:",
               font=self.fonts['Body_Tuple']).grid(row=0, column=0, sticky=W,pady=2)
        self.task_name_entry = Entry(self.currenttask_frame, width = 50)
        self.task_name_entry.grid(row = 0 , column = 1)
        self.display_task_id =ttk.Label(self.currenttask_frame, text = f"Task ID:",
              font = self.fonts['Body_Tuple']).grid(row = 1, column = 0, sticky = W, pady = 2)
        self.current_id_entry = Entry(self.currenttask_frame, width = 10)
        self.current_id_entry.grid(row = 1, column = 1, sticky = W)

        
        Label(self.currenttask_frame, text = "Time: ",
               font=self.fonts['Body_Tuple']).grid(row=2, column=0, sticky=W,pady=2)
        
        #Set Description Frame and Box inside the Frame
        description_frame = tk.Frame(self.full_page, bg = background_color)
        description_frame.pack(pady = 5, fill = "x")

        Label(description_frame, text="Description:",
               font=self.fonts['Body_Tuple'],background = background_color).grid(row=0, column=0,sticky=W, pady=2)

        #Description Scrollbar
        description_scroll = Scrollbar(description_frame)
        description_scroll.grid(row = 1, column = 1, sticky = "ns")
        self.description_box = Text(description_frame, yscrollcommand= description_scroll.set,
                                height=5,
                                    width=50,border = 1, font=self.fonts['Description_Tuple'],
                                    background="#d3d3d3")
        self.description_box.grid(row = 1, column = 0)

        #Insert Current Task Description
        description_scroll.config(command = self.description_box.yview)



        #Change color when a item is selected
        style.map("Treeview",
        background = [('selected', "#4169E1")], 
        foreground=[('selected', '#000000')])

        #Top Button Frame
        top_btn_frame = LabelFrame(self.full_page, text = "TaskList")
        top_btn_frame.pack( pady = 5, fill = "x")

        #Put the task list inside a frame
        tasklist_frame = tk.Frame(self.full_page, bg = background_color)
        tasklist_frame.pack(pady=0, fill = "x")

        #Buttons for Underneath Description Box + Above TaskList

        moveup_button = tk.Button(top_btn_frame, text = "Move Up",bg = main_btn_color, command = self.move_up)
        moveup_button.grid(row = 0, column = 1, padx = 4, pady =6)

        movedown_button = tk.Button(top_btn_frame, text = "Move Down",bg = main_btn_color, command = self.move_down)
        movedown_button.grid(row = 0, column = 2, padx = 4, pady = 6)


        reload_button = tk.Button(top_btn_frame, text = "Reload TaskList",bg = main_btn_color, command = self.query_database)
        reload_button.grid(row = 0, column = 0, padx = 4, pady = 6)

        complete_task_btn = tk.Button(top_btn_frame, text = "Complete Task", bg = main_btn_color, command = self.open_CompletionPage)
        complete_task_btn.grid(row = 0, column = 3, padx = 4, pady = 6)



        #Create scrollbar
        tasklist_scroll = Scrollbar(tasklist_frame)
        tasklist_scroll.grid(row = 1, column = 1, sticky = "ns")

        #Set scrollbar
        self.task_list = ttk.Treeview(tasklist_frame, yscrollcommand=tasklist_scroll.set, selectmode = "extended", style  = "Treeview", height = 8)
        self.task_list.grid(row = 1, column = 0)

        #Task List is vertical scroll
        tasklist_scroll.config(command = self.task_list.yview)

        #Format columns
        self.task_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID", "Start Date", "End Date", "Description")
        self.task_list.column("#0", width = 0, stretch=NO)
        self.task_list.column('Task Name', anchor = W, width = 250)
        self.task_list.column('Task Time', anchor = CENTER, width = 100)
        self.task_list.column('Task Weight', anchor = CENTER, width =100)
        self.task_list.column('Task ID',anchor = CENTER, width = 0, stretch = NO)
        self.task_list.column('Start Date', anchor = CENTER, width = 0, stretch = NO)
        self.task_list.column('End Date', anchor = CENTER, width = 0, stretch = NO)
        self.task_list.column('Description', anchor = CENTER, width = 0, stretch = NO)

        #Format headings
        self.task_list.heading("#0", text = "", anchor = W)
        self.task_list.heading("Task Name", text = "Task Name", anchor = W)
        self.task_list.heading("Task Time", text = "Time", anchor = CENTER)
        self.task_list.heading("Task Weight", text = "Weight", anchor = CENTER)
        self.task_list.heading("Task ID", text = "ID", anchor = CENTER)
        self.task_list.heading("Start Date", text = "Start Date", anchor = CENTER)
        self.task_list.heading("End Date", text = "End Date", anchor = CENTER)
        self.task_list.heading("Description", text = "Description", anchor = CENTER)

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

        sd_label = Label(data_frame, text = "Start Date")
        sd_label.grid(row = 0, column = 4, padx = 10, pady = 0)
        self.sd_entry = Entry(data_frame)
        self.sd_entry.grid(row = 1, column = 4)

        td_label = Label(data_frame, text = "Start Date")
        td_label.grid(row = 0, column = 5, padx = 10, pady = 0)
        self.td_entry = Entry(data_frame)
        self.td_entry.grid(row = 1, column = 5)

        data_frame.pack_forget()

        button_frame = LabelFrame(self.full_page, text = "Commands")
        button_frame.pack(fill = "x",pady = 10,side = BOTTOM)


        #Buttons
        self.update_button = tk.Button(button_frame, text = "Edit Task",bg = main_btn_color, command = self.open_EditTaskWindow)
        self.update_button.grid(row = 0, column = 0, padx = 6, pady = 10)

        self.add_button = tk.Button(button_frame, text = "Add Task",bg = main_btn_color, command = self.open_AddTaskWindow)
        self.add_button.grid(row = 0, column = 1, padx = 6, pady = 10)

        remove_button = tk.Button(button_frame, text = "Remove Task",bg = del_btn_color, command = self.remove_current_task)
        remove_button.grid(row = 0, column = 3, padx = 6, pady = 10)

        remove_all_button = tk.Button(button_frame, text = "Remove All",bg = del_btn_color, command = self.remove_all)
        remove_all_button.grid(row = 0, column = 4, padx = 6, pady = 10)


        select_record_button = tk.Button(button_frame, text = "Select Record",bg = main_btn_color, command = self.select_current_task)
        select_record_button.grid(row = 0, column = 2, padx = 6, pady = 10)

        #Uses select button on single click. Takes value from TreeView, not the database
        self.task_list.bind("<ButtonRelease-1>", self.select_record)

        self.set_current_task()


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
        self.sd_entry.delete(0, END)
        self.td_entry.delete(0, END)

        #Grab record number
        selected = self.task_list.focus()

        #Grab record values
        values = self.task_list.item(selected, "values")

        #Insert into current task
        if values:
            self.tn_entry.insert(0, values[0])
            self.tt_entry.insert(0, values[1])
            self.ti_entry.insert(0, values[3])
            self.tw_entry.insert(0, values[2])
            self.sd_entry.insert(0, values[4])

        #Send values from TaskList Table to CurrentTaskList Table
    

    def select_current_task(self):
        task_id = self.ti_entry.get()

        conn = sqlite3.connect('task_list.db')
        c = conn.cursor()

        try:
            # Get the current task if it exists
            c.execute("SELECT * FROM CurrentTask LIMIT 1")
            current_task = c.fetchone()

            # Get the selected task
            c.execute("SELECT * FROM TaskList WHERE task_id = ?", (task_id,))
            selected_task = c.fetchone()

            if selected_task:
                # Remove old current task and insert new one
                c.execute("DELETE FROM CurrentTask")
                c.execute("""
                    INSERT INTO CurrentTask (task_id, task_name, task_time, task_weight, task_start_date, task_end_date, task_description, task_weight_type, task_tags) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (selected_task[3], selected_task[0], selected_task[1], selected_task[2], selected_task[4], selected_task[5], selected_task[6], selected_task[7], selected_task[8]))

                # Remove the selected task from TaskList
                c.execute("DELETE FROM TaskList WHERE task_id = ?", (task_id,))

            # If there was a previous current task, move it back to TaskList
            if current_task:
                c.execute("""
                    INSERT INTO TaskList (task_id, task_name, task_time, task_weight, task_start_date, task_end_date, task_description, task_weight_type, task_tags) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (current_task[3], current_task[0], current_task[1], current_task[2], current_task[4], current_task[5], current_task[6], current_task[7], current_task[8]))
            conn.commit()
            print("Task swapped successfully!")

        except sqlite3.Error as e:
            print("Database error:", e)
            conn.rollback()

        finally:
            conn.close()

        self.set_current_task()

    def set_current_task(self):
        conn = sqlite3.connect('task_list.db')
        c = conn.cursor()

        c.execute("SELECT * FROM CurrentTask")
        cur_task = c.fetchone()

        if cur_task:  # Prevent error if CurrentTask is empty
            #Enable entry boxes to change information
            self.task_name_entry.configure(state = NORMAL,foreground= "black")
            self.current_id_entry.configure(state = NORMAL,foreground= "black")
            self.description_box.configure(state = NORMAL,foreground= "black")

            #Switch out entry boxes for all information
            self.task_name_entry.delete(0, END)
            self.current_id_entry.delete(0, END)
            self.task_name_entry.insert(0 , cur_task[0])
            self.current_id_entry.insert(0, cur_task[3])
            self.description_box.delete("1.0", END)
            self.description_box.insert("1.0", cur_task[6])  # Assuming description is at index 6
            #Disable entry boxes                             
            self.task_name_entry.configure(state = DISABLED)
            self.current_id_entry.configure(state = DISABLED)
            self.description_box.configure(state = DISABLED)
            
        else:
            self.task_name_entry.configure(state = NORMAL,foreground= "black")
            self.current_id_entry.configure(state = NORMAL,foreground= "black")
            self.description_box.configure(state = NORMAL,foreground= "black")
            self.task_name_entry.insert(0 , "No Current Task")
            self.description_box.delete("1.0", "end")
            self.task_name_entry.configure(state = DISABLED)
            self.current_id_entry.configure(state = DISABLED)
            self.description_box.configure(state = DISABLED)


        self.query_database()

        conn.close()
      

        
    def query_database(self):
        for record in self.task_list.get_children():
            self.task_list.delete(record)

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
                self.task_list.insert(parent = '', index = 'end', iid = count, text = '', values = (record[1],record[2],record[3],record[4], record[5],record[6],record[7]), tags = ('evenrow', ""))
            else:
                self.task_list.insert(parent = '', index = 'end', iid = count, text = '', values = (record[1],record[2],record[3],record[4], record[5],record[6],record[7]), tags = ('oddrow', ""))
                #Increment count
            count += 1
        
        #Commit Changes
        conn.commit()

        conn.close()
       
    #def insert_task(self, task_id):

    

    def remove_current_task(self):
        x = self.task_list.selection()[0]
        self.task_list.delete(x)

    def remove_all(self):
        response = messagebox.askyesno("Are you sure you want to delete everything from the tasklist? This is irreversible.")

        if response == 1:
            for record in self.task_list.get_children():
                self.task_list.delete(record)

                conn = sqlite3.connect('task_list.db')
                c = conn.cursor()

                c.execute("DROP TABLE TaskList")

                conn.commit()

                conn.close()

                self.create_tasklist_again()

    def create_tasklist_again(self):
        # Create a database or connect to one that exists
        conn = sqlite3.connect('task_list.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists TaskList (
          task_name text,
          task_time text DEFAULT '00:00:00',
          task_weight text,
          task_id integer PRIMARY KEY AUTOINCREMENT,
          task_start_date text,
          task_end_date text,
          task_description text,
          task_weight_type text,
          task_tags
          )
        """)
        
        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()
       
    def open_AddTaskWindow(self):
        if self.addtask_window is None or not self.addtask_window.winfo_exists():
            self.add_button.config(state=tk.DISABLED)  # Disable the button
            self.addtask_window = AddTaskWindow(self)  # Pass self to allow callback
        else:
            self.addtask_window.deiconify()
            self.addtask_window.lift()


    

    def open_AddCompleteTaskWindow(self, task_id):
        self.task_window = CompletedTasksWindow(
            task_id = task_id
        )
        self.task_window.grab_set()
    
    def open_EditTaskWindow(self):
        task_id = self.ti_entry.get()
        if task_id:
            if self.edittask_window is None or not self.edit_task_window.winfo_exists():
                self.update_button.config(state=tk.DISABLED)  # Disable the button
                self.edittask_window = EditTaskWindow(task_id = task_id, main_app=self)
                self.edittask_window.grab_set()
            else:
                self.edittask_window.deiconify()
                self.edittask_window.lift()
        else:
            messagebox.showwarning("Selection Required", "Please select a task to complete.")

    def open_CurrentTaskWindow(self):
        self.task_window = CurrentTaskWindow()
        self.task_window.grab_set()
    
    def open_CompletionPage(self):
        selected = self.task_list.selection()
        if selected:
            values = self.task_list.item(selected[0], "values")
            task_name = values[0]
            task_time = values[1]
            task_weight = values[2]
            task_id = values[3]

            self.task_window = CompletedTasksWindow(
                task_name=task_name,
                task_time=task_time,
                task_weight=task_weight,
                task_id=task_id,
                refresh_callback=self.query_database
            )
            self.task_window.grab_set()
        else:
            messagebox.showwarning("Selection Required", "Please select a task to complete.")

    
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