from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
from datetime import datetime
import pathlib
import csv
import threading
import os
import threading
import time
import sys
import shutil
from ui import (
    CompletedTasksWindow,
    EditTaskWindow,
    AddTaskWindow,
    CurrentTaskWindow,
    TagsDB,
    CompletedTasksList,
    AnalyticsPage,
    ArchiveTasksList, 
    SettingsPage,
    HelpPage
)
from ui.CommitHistoryPage import CommitHistoryWindow
#MAKE SURE TO EITHER COMMENT OUT VOID CODE OR JUST DELETE IT WHEN APPLICABLE
#DATABASE IS CALLED task_list.db
#IF YOU GET ERRORS MAKE SURE TO DELETE THE DATABASE FILES AND RERUN PROGRAM

#Global Variables
background_color = "#A9A9A9"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "#E0E0E0"

main_btn_color = "#b2fba5"
del_btn_color = "#e99e56"

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("MainPage.py", '') + '\\ui' + '\\Databases' + '\\task_list.db'
      

#Create a database or connect to an existing database
conn = sqlite3.connect(path)

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
          task_tags text, 
          list_place integer
          )
""")
#Table for Current Task
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
          start_date text,
          task_tags text,
          task_weight_type text,
          task_description text,
          PRIMARY KEY (task_id)
)""")

# Table for Archive database
c.execute("""CREATE TABLE if not exists ArchivedTasks (
          task_name text,
          task_time text,
          task_weight text,
          task_id integer,
          completion_date text,
          total_duration text,
          archive_date text,
          task_tags text,
          task_weight_type text,
          task_description text,
          PRIMARY KEY (task_id)
)""")


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
      self.commithistory_window = None
      self.root.protocol("WM_DELETE_WINDOW", self.on_close)

     # Initialize activity tracking
      self.inactivity_timer = None
      self.inactivity_limit = 2 * 60 * 60
      self.bind_activity_events()

     # Set initial inactivity timer
      self.reset_inactivity_timer()

      base_dir = os.path.dirname(os.path.abspath(__file__))
      image_path = os.path.join(base_dir, "image.png")
      icon = tk.PhotoImage(file=image_path)
      self.root.iconphoto(True, icon)

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
      self.page_title = ttk.Label(self.menu_frame, text="Time Tracker", font=self.fonts['Body_Tuple'], background= background_color)
      self.page_title.pack(side="left", padx=10)

      #Create pages
      self.full_page = tk.Frame(self.main_container)
      self.completedtasks_page = CompletedTasksList(self.main_container, self)
      self.smalloverlay_page = tk.Frame(self.main_container)
      self.tags_database_page = TagsDB(self.main_container)
      self.analytics_page = AnalyticsPage(self.main_container)
      self.archive_page = ArchiveTasksList(self.main_container, self)
      self.help_page = HelpPage(self.main_container, self)
      self.settings_page = SettingsPage(self.main_container, self)

      #Show main page at start-up
      self.current_page = self.full_page
      self.full_page.pack(expand=True, fill="both", padx=10, pady=5)

      #Create the popup menu
      self.popup_menu = tk.Menu(root, tearoff=0)
      self.popup_menu.add_command(label="Time Tracker", command=lambda: self.switch_page("Time Tracker"))
      self.popup_menu.add_command(label="Completed Tasks", command=lambda: self.switch_page("Completed Tasks"))
      self.popup_menu.add_command(label="Small Overlay", command=lambda: self.switch_page("Small Overlay"))
      self.popup_menu.add_command(label="Tags Database", command=lambda: self.switch_page("Tags Database"))
      self.popup_menu.add_command(label="Analytics", command=lambda: self.switch_page("Analytics"))
      self.popup_menu.add_command(label="Archive", command=lambda: self.switch_page("Archive"))
      self.popup_menu.add_command(label="Help", command=lambda: self.switch_page("Help"))
      self.popup_menu.add_command(label="Settings", command=lambda: self.switch_page("Settings"))
      # self.popup_menu.add_command(label="Commit History", command=lambda: self.switch_page("Commit History"))
      self.popup_menu.configure(bg= background_color)

      self.setup_smalloverlay_page()
      self.setup_full_page()
      self.completedtasks_page.pack_forget()

      #self.initialize_ui_enhancements()
      

      #Query the database for all information inside
      self.query_database()

    def on_close(self):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit the program?")
        if self.inactivity_timer:
            self.inactivity_timer.cancel()

        if confirm:
            if self.addtask_window:
                self.addtask_window.destroy()
            if self.edittask_window:
                self.edittask_window.destroy()
            if self.commithistory_window:
                self.commithistory_window.destroy()
            root.destroy()
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

        if page_name == "Time Tracker":
            self.current_page = self.full_page
            self.page_title.config(text="Time Tracker", background= background_color)
            self.root.geometry("488x650")
            self.query_database()
        elif page_name == "Completed Tasks":
            self.current_page = self.completedtasks_page
            self.page_title.config(text="Completed Tasks", background= background_color)
            self.root.geometry("600x400")
            self.query_database()
            self.completedtasks_page.load_completed_tasks()
        elif page_name == "Small Overlay":
            self.current_page = self.smalloverlay_page
            self.page_title.config(text="Small Overlay", background=background_color)
            self.root.geometry("230x160")
            self.query_database()
        elif page_name == "Tags Database":
            self.current_page = self.tags_database_page  
            self.page_title.config(text="Tags Database", background=background_color) #CHANGED REMEMBER <<<<<<<<<<
            self.root.geometry("530x610")
            self.query_database()
        elif page_name == "Analytics":
            self.current_page = self.analytics_page  
            self.page_title.config(text="Analytics", background=background_color) #CHANGED REMEMBER <<<<<<<<<<
            self.root.geometry("1000x1000")
            self.query_database()
            self.analytics_page.update_total_time()  
        elif page_name == "Archive":  
            self.current_page = self.archive_page
            self.page_title.config(text="Archived Tasks", background=background_color)
            self.root.geometry("650x515")
            self.archive_page.load_archive_tasks()
        elif page_name == "Help":
            self.current_page = self.help_page
            self.page_title.config(text = "Help", background=background_color)
            self.root.geometry("650x600")
            self.query_database()
        elif page_name == "Settings":
            self.current_page = self.settings_page
            self.page_title.config(text = "Settings", background=background_color)
            self.root.geometry("650x600")
            self.query_database()
            

        self.current_page.pack(expand=True, fill="both", padx=10, pady=5)



    def setup_smalloverlay_page(self):
        # Button not flat
        # Entry box grey
        self.smalloverlay_page.configure(bg=background_color)
        style = ttk.Style()
        style.configure('TLabel', background="#dcdcdc")
        self.so_task_name_label = ttk.Label(self.smalloverlay_page, text="No Current Task", font=self.fonts['Body_Tuple'], background=background_color)
        self.so_task_name_label.grid(row = 0, column = 0, pady = 2, sticky = W)
        # Time label and box
        Label(self.smalloverlay_page, text="Time: ",
            font=self.fonts['Body_Tuple'],
            background=background_color
        ).grid(row=1, column=0, sticky=W, pady=2)
        self.time_box_overlay = Text(self.smalloverlay_page, height=1, width=10,
                                    font=self.fonts['Description_Tuple'],
                                    background=grey_button_color)
        self.time_box_overlay.grid(row=1, column=0, padx=50, pady=5, sticky=E)
        # Timer control buttons
        self.small_overlay_start_button = tk.Button(self.smalloverlay_page, 
                                                text="Start",
                                                # relief="flat",
                                                background="#77DD77",
                                                command=self.start_timer)
        self.small_overlay_start_button.grid(row=2, column=0, sticky=W, padx=0, pady=5)
        self.small_overlay_stop_button = tk.Button(self.smalloverlay_page, 
                                                text="Stop",
                                                # relief="flat",
                                                background="#FF7276",
                                                command=self.stop_timer)
        self.small_overlay_stop_button.grid(row=2, column=0, sticky=W, padx=45, pady=5)
        self.small_overlay_stop_button.config(state=DISABLED)

        self.small_overlay_complete_button = tk.Button(self.smalloverlay_page,
                                          text="Complete",
                                          background="#4682B4",
                                          command=self.complete_current_task)
        self.small_overlay_complete_button.grid(row=2, column=0, sticky=W, padx=90, pady=5)
   
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
        style.configure('TLabel', background= "#dcdcdc")
        style.theme_use('alt')
        style.configure("Treeview",
        background = "black",
        foreground = "black",
        rowheight = 20,
        fieldbackground = "#dcdcdc")

        #Current Task Frame
        self.currenttask_frame = tk.LabelFrame(self.full_page, text = f"Current Task", bg="#dcdcdc" )
        self.currenttask_frame.pack(pady=0, side = TOP, fill = 'x')

        #Task Name row
        task_name_frame = tk.Frame(self.currenttask_frame, bg="#dcdcdc")
        task_name_frame.grid(row=0, column=0, sticky=W)

        ttk.Label(task_name_frame, text=f"Task Name:", font=self.fonts['Body_Tuple'], style='TLabel').grid(row=0, column=0, sticky=W)
        self.task_name_label = ttk.Label(task_name_frame, text="No Current Task", font=self.fonts['Description_Tuple'])
        self.task_name_label.grid(row=0, column=1, sticky=W, padx=(0, 0))

        # Create a frame for Task ID
        task_id_frame = tk.Frame(self.currenttask_frame, bg="#dcdcdc")
        task_id_frame.grid(row=1, column=0, pady=5, sticky=W)

        # Task ID Label and Task ID Display inside the frame
        ttk.Label(task_id_frame, text="Task ID:", font=self.fonts['Body_Tuple']).grid(row=0, column=0, sticky=W, padx=0)
        self.task_id_label = ttk.Label(task_id_frame, text="-", font=self.fonts['Description_Tuple'])
        self.task_id_label.grid(row=0, column=1, sticky=W)

        # Create a frame to hold the time label, box and buttons - all on same row
        time_controls_frame = tk.Frame(self.currenttask_frame, bg="#dcdcdc")
        time_controls_frame.grid(row=2, column=0, columnspan=2, sticky=W, pady=2)

        # Time label
        Label(time_controls_frame, text="Time:", font=self.fonts['Body_Tuple']).pack(side=LEFT)

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
                                    background="#dcdcdc")
        self.description_box.grid(row = 1, column = 0)

        #Insert Current Task Description
        description_scroll.config(command = self.description_box.yview)

        # Add timer-related instance variables
        self.timer_running = False
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.total_seconds = 0
        
        # Create time box right next to the label
        self.time_box_full = Text(time_controls_frame, height=1, width=10,
                                font=self.fonts['Description_Tuple'],
                                background=grey_button_color)
        self.time_box_full.pack(side=LEFT, padx=(5, 5))
        self.time_box_full.config(state=DISABLED)
        
        # Add timer control buttons right next to the time box
        self.full_page_start_button = tk.Button(time_controls_frame, text="Start", background="#77DD77", command=self.start_timer)
        self.full_page_start_button.pack(side=LEFT, padx=(0, 5))

        self.full_page_stop_button = tk.Button(time_controls_frame, text="Stop", background="#FF7276", command=self.stop_timer)
        self.full_page_stop_button.pack(side=LEFT)
        self.full_page_stop_button.config(state=DISABLED)

        self.full_page_complete_button = tk.Button(time_controls_frame, text="Complete", background="#4682B4", command=self.complete_current_task)
        self.full_page_complete_button.pack(side=LEFT, padx=(5, 0))

        #Change color when a item is selected
        style.map("Treeview",
        background = [('selected', "#4169E1")], 
        foreground=[('selected', '#000000')])

        #Top Button Frame
        top_btn_frame = tk.LabelFrame(self.full_page, text = "TaskList", bg="#dcdcdc")
        top_btn_frame.pack( pady = 5, fill = "x")

        #Put the task list inside a frame
        tasklist_frame = tk.Frame(self.full_page, bg = background_color)
        tasklist_frame.pack(pady=0, fill = "x")

        #Buttons for Underneath Description Box + Above TaskList

        moveup_button = tk.Button(top_btn_frame, text = "Move Up",bg = main_btn_color, command = self.move_up)
        moveup_button.grid(row = 0, column = 0, padx = 4, pady =6)

        movedown_button = tk.Button(top_btn_frame, text = "Move Down",bg = main_btn_color, command = self.move_down)
        movedown_button.grid(row = 0, column = 1, padx = 4, pady = 6)

        complete_task_btn = tk.Button(top_btn_frame, text = "Complete Task", bg = main_btn_color, command = self.open_CompletionPage)
        complete_task_btn.grid(row = 0, column = 2, padx = 4, pady = 6)

        import_btn = tk.Button(top_btn_frame, text = "Import", bg = main_btn_color, command = self.import_Tasks)
        import_btn.grid(row = 0, column= 3, padx = 4, pady = 6)

        Label(top_btn_frame, text = "Search:").grid(row = 0, column = 4)

        self.search_entry = tk.Entry(top_btn_frame, bg="#dcdcdc", width = 15)
        self.search_entry.grid(row = 0, column= 5, padx = 4, pady= 6)
        self.search_entry.bind("<KeyRelease>", self.search_Task)

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
        self.task_list.tag_configure('evenrow', background=  "#dcdcdc", foreground= "black")

        #This is the select thing. Will become void after current task table is implemented
        #So Full page will become smaller and when using select button it should put task information at the top.
        data_frame = tk.LabelFrame(self.full_page, text = "Input", bg="#dcdcdc")
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

        button_frame = tk.LabelFrame(self.full_page, text = "Commands", bg="#dcdcdc")
        button_frame.pack(fill = "x",pady = 10,side = BOTTOM)


        #Buttons
        self.update_button = tk.Button(button_frame, text = "Edit Task",bg = main_btn_color, command = self.open_EditTaskWindow)
        self.update_button.grid(row = 0, column = 0, padx = 6, pady = 10)

        self.commit_button = tk.Button(button_frame, text="Commit History", bg=main_btn_color, command=self.open_CommitHistoryWindow)
        self.commit_button.grid(row=0, column=3, padx=6, pady=10)

        self.add_button = tk.Button(button_frame, text = "Add Task",bg = main_btn_color, command = self.open_AddTaskWindow)
        self.add_button.grid(row = 0, column = 1, padx = 6, pady = 10)

        remove_all_button = tk.Button(button_frame, text = "Remove All",bg = del_btn_color, command = self.remove_all)
        remove_all_button.grid(row = 0, column = 4, padx = 6, pady = 10)


        select_record_button = tk.Button(button_frame, text = "Select Task",bg = main_btn_color, command = self.select_current_task)
        select_record_button.grid(row = 0, column = 2, padx = 6, pady = 10)

        #Uses select button on single click. Takes value from TreeView, not the database
        self.task_list.bind("<ButtonRelease-1>", self.select_record)

        self.set_current_task()


    #Move a task up in the task list
    def move_up(self):
        selected = self.task_list.selection()
        if not selected:
            return

        current_index = self.task_list.index(selected[0])
        if current_index == 0:  # Already at top
            return

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            task_id = self.task_list.item(selected[0])['values'][3]  # Get selected task ID

            # Fetch ordered tasks
            c.execute("SELECT task_id, list_place FROM TaskList ORDER BY list_place")
            tasks = c.fetchall()

            for i, (tid, place) in enumerate(tasks):
                if tid == int(task_id) and i > 0:  # Ensure it's not already at the top
                    above_task_id, above_place = tasks[i - 1]

                    # Swap positions in the database
                    c.execute("UPDATE TaskList SET list_place = ? WHERE task_id = ?", (above_place, task_id))
                    c.execute("UPDATE TaskList SET list_place = ? WHERE task_id = ?", (place, above_task_id))
                    conn.commit()

                    # Refresh treeview
                    self.query_database()

                    # Move selection UP to follow the moved task
                    new_index = current_index - 1
                    new_item = self.task_list.get_children()[new_index]
                    self.task_list.selection_set(new_item)
                    self.task_list.focus(new_item)

                    break

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()
            
        # Refresh the display to show correct alternating colors
        self.query_database()
        
        # Reselect the moved item after refresh
        self.reselect_task_by_id(task_id)
    
    def move_down(self):
        selected = self.task_list.selection()
        if not selected:
            return

        current_index = self.task_list.index(selected[0])
        last_index = len(self.task_list.get_children()) - 1
        if current_index == last_index:  # Already at bottom
            return

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            task_id = self.task_list.item(selected[0])['values'][3]  # Get selected task ID

            # Fetch ordered tasks
            c.execute("SELECT task_id, list_place FROM TaskList ORDER BY list_place")
            tasks = c.fetchall()

            for i, (tid, place) in enumerate(tasks):
                if tid == int(task_id) and i < len(tasks) - 1:  # Ensure it's not already at the bottom
                    below_task_id, below_place = tasks[i + 1]

                    # Swap positions in the database
                    c.execute("UPDATE TaskList SET list_place = ? WHERE task_id = ?", (below_place, task_id))
                    c.execute("UPDATE TaskList SET list_place = ? WHERE task_id = ?", (place, below_task_id))
                    conn.commit()

                    # Refresh treeview
                    self.query_database()

                    # Move selection DOWN to follow the moved task
                    new_index = current_index + 1
                    new_item = self.task_list.get_children()[new_index]
                    self.task_list.selection_set(new_item)
                    self.task_list.focus(new_item)

                    break

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()
            
        # Refresh the display to show correct alternating colors
        self.query_database()
        
        # Reselect the moved item after refresh
        self.reselect_task_by_id(task_id)

    # Add this new helper method to reselect a task by its ID
    def reselect_task_by_id(self, task_id):
        """Reselect a task in the treeview by its task_id"""
        # Look through all items in the treeview to find matching task_id
        for item_id in self.task_list.get_children():
            item_values = self.task_list.item(item_id, 'values')
            if item_values and str(item_values[3]) == str(task_id):
                # Select the found item
                self.task_list.selection_set(item_id)
                # Make sure the item is visible
                self.task_list.see(item_id)
                # Optionally focus on the item
                self.task_list.focus(item_id)
                break


    def select_record(self, e):
        # Clear entry boxes
        self.tn_entry.delete(0, END)
        self.tt_entry.delete(0, END)
        self.ti_entry.delete(0, END)
        self.tw_entry.delete(0, END)
        self.sd_entry.delete(0, END)
        self.td_entry.delete(0, END)

        # Grab record number
        selected = self.task_list.focus()

        # Grab record values
        values = self.task_list.item(selected, "values")

        # Only proceed if we have values
        if values:
            task_id = values[3]  # Task ID is at index 3
            
            # Insert values from TreeView into entries
            self.tn_entry.insert(0, values[0])  # Task Name
            self.tt_entry.insert(0, values[1])  # Task Time
            self.ti_entry.insert(0, task_id)    # Task ID
            self.tw_entry.insert(0, values[2])  # Task Weight
            self.sd_entry.insert(0, values[4] if len(values) > 4 else "")  # Start Date
            
            # Connect to database to get the full task details including description
            conn = sqlite3.connect(path)
            c = conn.cursor()
            
            try:
                # Get task description directly from database
                c.execute("SELECT task_description FROM TaskList WHERE task_id = ?", (task_id,))
                result = c.fetchone()
                
                
            except sqlite3.Error as e:
                print(f"Database error when getting description: {e}")
            finally:
                conn.close()
                
        #Send values from TaskList Table to CurrentTaskList Table
    

    def select_current_task(self):
        """Move selected task to current task and return previous current task to task list"""
        # Check if there's actually a task selected
        if not self.ti_entry.get():
            messagebox.showwarning("No Task Selected", "Please select a task from the list first.")
            return

        # Stop the timer if it's running
        if self.timer_running:
            self.stop_timer()
            
        task_id = self.ti_entry.get()

        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # Get the current task if it exists
            c.execute("SELECT * FROM CurrentTask LIMIT 1")
            current_task = c.fetchone()

            # Get the selected task
            c.execute("SELECT * FROM TaskList WHERE task_id = ?", (task_id,))
            selected_task = c.fetchone()

            if selected_task:
                # If there was a previous current task, move it back to TaskList
                if current_task:
                    # Only move current task back if it's different from the selected task
                    if str(current_task[3]) != str(task_id):
                        c.execute("""
                            INSERT INTO TaskList (task_id, task_name, task_time, task_weight, task_start_date, 
                            task_end_date, task_description, task_weight_type, task_tags) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (current_task[3], current_task[0], current_task[1], current_task[2], 
                            current_task[4], current_task[5], current_task[6], current_task[7], 
                            current_task[8]))
                    
                # Remove old current task and insert new one
                c.execute("DELETE FROM CurrentTask")
                c.execute("""
                    INSERT INTO CurrentTask (task_id, task_name, task_time, task_weight, task_start_date, 
                    task_end_date, task_description, task_weight_type, task_tags) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (selected_task[3], selected_task[0], selected_task[1], selected_task[2], 
                    selected_task[4], selected_task[5], selected_task[6], selected_task[7], 
                    selected_task[8]))

                # Remove the selected task from TaskList
                c.execute("DELETE FROM TaskList WHERE task_id = ?", (task_id,))
                
                conn.commit()
            else:
                messagebox.showwarning("Task Not Found", "The selected task could not be found in the database.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            conn.close()

        self.set_current_task()
        self.query_database()

    def set_current_task(self):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM CurrentTask")
        cur_task = c.fetchone()

        if cur_task:
            self.enable_boxes()
            self.task_name_label.config(text=cur_task[0])  # Assuming Task Name is at index 0
            self.so_task_name_label.config(text = cur_task[0])
            self.task_id_label.config(text=cur_task[3])  # Assuming Task ID is at index 3
            self.time_box_full.delete("1.0", END)
            self.time_box_full.insert("1.0", cur_task[1])  # Assuming Task Time is at index 1
            self.time_box_overlay.delete("1.0", END)
            self.time_box_overlay.insert("1.0", cur_task[1])
            self.description_box.delete("1.0", END)
            self.description_box.insert("1.0", cur_task[6])  # Assuming description is at index 6
            self.disable_boxes()
        else:
            self.enable_boxes()
            self.task_name_label.config(text="No Current Task")
            self.so_task_name_label.config(text="No Current Task")
            self.task_id_label.config(text="-")
            self.time_box_full.delete("1.0", END)
            self.time_box_overlay.delete("1.0", END)
            self.description_box.delete("1.0", "end")
            self.disable_boxes()
        
        self.query_database()
        conn.close()
    
    def disable_boxes(self):
        self.description_box.configure(state = DISABLED)
        self.time_box_full.configure(state = DISABLED)
        self.time_box_overlay.configure(state = DISABLED)
    
    def enable_boxes(self):
        self.time_box_full.configure(state = NORMAL,foreground= "black")
        self.time_box_overlay.configure(state = NORMAL, foreground= "black")
        self.description_box.configure(state = NORMAL,foreground= "black") 

    def reset_inactivity_timer(self):
        """Reset the inactivity timer to log out after inactivity limit"""
        if self.inactivity_timer:
            self.inactivity_timer.cancel()  # Cancel the existing timer if any
        self.inactivity_timer = threading.Timer(self.inactivity_limit, self.timerlog)  # Create a new timer
        self.inactivity_timer.start()  # Start the timer

    def bind_activity_events(self):
        """Bind all activity events that reset the timer"""
        self.root.bind("<KeyPress>", lambda event: self.reset_inactivity_timer())  # Any key press
        self.root.bind("<Motion>", lambda event: self.reset_inactivity_timer())  # Mouse movement
        self.root.bind("<ButtonPress>", lambda event: self.reset_inactivity_timer())  # Mouse button click

    def timerlog(self):
        self.stop_timer()
        messagebox.showinfo("Timed Out", "Your Timer has stopped due to inactivity.")
        

        
    def query_database(self):
        """Refresh all task-related tables in the GUI with the latest database data."""
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            # Ensure all tables exist
            c.execute("""CREATE TABLE IF NOT EXISTS TaskList (
                task_name text,
                task_time text DEFAULT '00:00:00',
                task_weight text,
                task_id integer PRIMARY KEY AUTOINCREMENT,
                task_start_date text,
                task_end_date text,
                task_description text,
                task_weight_type text,
                task_tags text, 
                list_place integer
            )""")
            
            c.execute("""CREATE TABLE IF NOT EXISTS CurrentTask(
                task_name text,
                task_time text,
                task_weight text,
                task_id integer,
                task_start_date text,
                task_end_date text,
                task_description text,
                task_weight_type text,
                task_tags text
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS CompletedTasks (
                task_name text,
                task_time text,
                task_weight text,
                task_id integer PRIMARY KEY,
                completion_date text,
                total_duration text,
                start_date text,
                task_tags text,
                task_weight_type text,
                task_description text
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS ArchivedTasks (
                task_name text,
                task_time text,
                task_weight text,
                task_id integer PRIMARY KEY,
                completion_date text,
                total_duration text,
                archive_date text,
                task_tags text,
                task_weight_type text,
                task_description text
            )""")

            # --- Update TaskList (Main Task Table) ---
            # Ensure all tasks have a list_place
            c.execute("SELECT task_id FROM TaskList WHERE list_place IS NULL")
            null_place_tasks = c.fetchall()
            if null_place_tasks:
                c.execute("SELECT COALESCE(MAX(list_place), 0) FROM TaskList")
                max_place = c.fetchone()[0]
                for i, (task_id,) in enumerate(null_place_tasks):
                    c.execute("UPDATE TaskList SET list_place = ? WHERE task_id = ?", (max_place + i + 1, task_id))
                conn.commit()

            # Clear and populate TaskList
            for record in self.task_list.get_children():
                self.task_list.delete(record)

            c.execute("SELECT * FROM TaskList ORDER BY list_place")
            tasklist_data = c.fetchall()
            for count, record in enumerate(tasklist_data):
                tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                self.task_list.insert('', 'end', iid=count, values=(
                    record[0],  # task_name
                    record[1],  # task_time
                    record[2],  # task_weight
                    record[3],  # task_id
                    record[4],  # task_start_date
                    record[5],  # task_end_date
                    record[6],  # task_description
                ), tags=tags)

            # --- Update CompletedTasks ---
            if hasattr(self, 'completed_tasks_list'):
                for record in self.completed_tasks_list.get_children():
                    self.completed_tasks_list.delete(record)

                c.execute("SELECT * FROM CompletedTasks ORDER BY completion_date DESC")
                completed_data = c.fetchall()
                for count, record in enumerate(completed_data):
                    tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                    self.completed_tasks_list.insert('', 'end', iid=count, values=(
                        record[0],  # task_name
                        record[1],  # task_time
                        record[2],  # task_weight
                        record[3],  # task_id
                        record[4],  # completion_date
                        record[5],  # total_duration
                        record[6],  # start_date
                        record[7],  # task_tags
                    ), tags=tags)

            # --- Update ArchivedTasks ---
            if hasattr(self, 'archived_tasks_list'):
                for record in self.archived_tasks_list.get_children():
                    self.archived_tasks_list.delete(record)

                c.execute("SELECT * FROM ArchivedTasks ORDER BY archive_date DESC")
                archived_data = c.fetchall()
                for count, record in enumerate(archived_data):
                    tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                    self.archived_tasks_list.insert('', 'end', iid=count, values=(
                        record[0],  # task_name
                        record[1],  # task_time
                        record[2],  # task_weight
                        record[3],  # task_id
                        record[4],  # completion_date
                        record[5],  # total_duration
                        record[6],  # archive_date
                        record[7],  # task_tags
                    ), tags=tags)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", "Failed to load tasks from database.")
        finally:
            conn.commit()
            conn.close()


    def remove_all(self):
        response = messagebox.askyesno("Are you sure you want to delete everything?              ")

        if response == 1:
            for record in self.task_list.get_children():
                self.task_list.delete(record)

                conn = sqlite3.connect(path)
                c = conn.cursor()

                c.execute("DROP TABLE TaskList")
                c.execute("DROP TABLE CurrentTask")
                c.execute("DROP TABLE task_history")
                
                

                conn.commit()

                conn.close()

                self.create_tasklist_again()
                self.create_currenttask_again()
                self.create_task_history_again()
                #self.create_completed_tasks_again()
                self.set_current_task()

    """def create_completed_tasks_again():
        # Create a database or connect to one that exists
        conn = sqlite3.connect(path)

        # Create a cursor instance
        c = conn.cursor()
        c.execute(CREATE TABLE if not exists CompletedTasks (
          task_name text,
          task_time text,
          task_weight text,
          task_id integer,
          completion_date text,
          total_duration text,
          start_date text,
          task tags text,
          task_weight_type text,
          task_description text,
          PRIMARY KEY (task_id)
            ))
        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()
        """
    def create_tasklist_again(self):
        # Create a database or connect to one that exists
        conn = sqlite3.connect(path)

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
          task_tags text, 
          list_place integer
          )
        """)
        
        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

    def create_currenttask_again(self):
        # Create a database or connect to one that exists
        conn = sqlite3.connect(path)

        # Create a cursor instance
        c = conn.cursor()

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

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

    def create_task_history_again(self):
        # Create the history table
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        c.execute("""CREATE TABLE IF NOT EXISTS task_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            change_date TEXT,
            field_changed TEXT,
            old_value TEXT,
            new_value TEXT,
            FOREIGN KEY (task_id) REFERENCES TaskList(task_id)
        )""")
        
        conn.commit()
        conn.close()
       
    def open_AddTaskWindow(self):
        if self.addtask_window is None or not self.addtask_window.winfo_exists():
            self.add_button.config(state=tk.DISABLED)  # Disable the button
            self.addtask_window = AddTaskWindow(self)  # Pass self to allow callback
        else:
            self.addtask_window.deiconify()
            self.addtask_window.lift()

    def open_CommitHistoryWindow(self):
        task = self.ti_entry.get()
        if task:
            if self.commithistory_window is None or not self.commithistory_window.winfo_exists():
                self.commit_button.config(state=tk.DISABLED)  # Disable the button
                self.commithistory_window = CommitHistoryWindow(main_app=self, task_id=task, compFlag=False)  # Pass self to allow callback
            else:
                self.commithistory_window.deiconify()
                self.commithistory_window.lift()
        else:
            messagebox.showwarning("Selection Required", "Please select a task to complete.")

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
            task_description = values[6]

            self.task_window = CompletedTasksWindow(
                task_name=task_name,
                task_time=task_time,
                task_weight=task_weight,
                task_id=task_id,
                task_description = task_description,
                refresh_callback=self.query_database
            )
            self.task_window.grab_set()
        else:
            messagebox.showwarning("Selection Required", "Please select a task to complete.")

    def format_time(self, total_seconds):
        """Convert total seconds to HH:MM:SS format"""
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    
    def update_timer(self):
        """Update the timer display and database"""
        if self.timer_running:
            self.total_seconds += 1
            timer_text = self.format_time(self.total_seconds)
            
            # Update both timer displays
            self.update_timer_boxes(timer_text)
            
            # Update the time in the database for current task
            conn = sqlite3.connect(path)
            c = conn.cursor()
            
            try:
                c.execute("""
                    UPDATE CurrentTask 
                    SET task_time = ? 
                    WHERE task_id = ?
                """, (timer_text, self.task_id_label.cget("text")))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            finally:
                conn.close()
            
            # Schedule the next update
            self.root.after(1000, self.update_timer)

    def start_timer(self):
        """Start the timer for current task"""
        # Check if there is a current task
        if not self.task_id_label.cget("text") or self.task_id_label.cget("text") == "No Current Task":
            messagebox.showwarning("No Task Selected", 
                                "Please select a task before starting the timer.")
            return
        
        if not self.timer_running:
            # Get existing time from database
            conn = sqlite3.connect(path)
            c = conn.cursor()
            
            try:
                c.execute("SELECT task_time FROM CurrentTask WHERE task_id = ?", 
                        (self.task_id_label.cget("text"),))
                current_time = c.fetchone()[0]
                
                # Convert HH:MM:SS to total seconds
                if current_time:
                    h, m, s = map(int, current_time.split(':'))
                    self.total_seconds = h * 3600 + m * 60 + s
                else:
                    self.total_seconds = 0
                    
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                self.total_seconds = 0
            finally:
                conn.close()
            
            self.timer_running = True
            self.update_timer()
            
            # Update button states
            self.disable_buttons(start_disabled=True)

    def stop_timer(self):
        """Stop the timer and save current time"""
        if self.timer_running:
            self.timer_running = False
            
            # Get final time
            final_time = self.format_time(self.total_seconds)
            
            # Update database with final time
            conn = sqlite3.connect(path)
            c = conn.cursor()
            try:
                c.execute("""
                    UPDATE CurrentTask 
                    SET task_time = ? 
                    WHERE task_id = ?
                """, (final_time, self.task_id_label.cget("text")))
                conn.commit()
                
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                messagebox.showerror("Error", 
                                "Failed to save time to database. Please try again.")
            finally:
                conn.close()
            
            # Reset timer variables
            self.total_seconds = 0
            
            # Update button states
            self.disable_buttons(start_disabled=False)
    
    def complete_current_task(self):
        """Complete the current active task"""
        # Stop the timer if it's running
        if self.timer_running:
            self.stop_timer()
        
        # Check if there is a current task
        if not self.task_id_label.cget("text") or self.task_id_label.cget("text") == "-":
            messagebox.showwarning("No Task", "There is no current task to complete.")
            return
        
        # Get current task details from labels and text boxes
        task_id = self.task_id_label.cget("text")
        task_name = self.task_name_label.cget("text")
        
        # Get task time from the time box
        self.time_box_full.config(state=NORMAL)
        task_time = self.time_box_full.get("1.0", tk.END).strip()
        self.time_box_full.config(state=DISABLED)
        
        # Get description from the description box
        self.description_box.config(state=NORMAL)
        task_description = self.description_box.get("1.0", tk.END).strip()
        self.description_box.config(state=DISABLED)
        
        # Fetch additional task details from the database
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            c.execute("SELECT task_weight, task_start_date, task_tags, task_weight_type FROM CurrentTask WHERE task_id = ?", (task_id,))
            result = c.fetchone()
            
            if result:
                task_weight, start_date, task_tags, task_weight_type = result
                
                # Open CompletedTasksWindow with all the data
                self.task_window = CompletedTasksWindow(
                    task_name=task_name,
                    task_time=task_time,
                    task_weight=task_weight,
                    task_id=task_id,
                    task_description=task_description,
                    start_date=start_date,
                    refresh_callback=self.set_current_task
                )
                self.task_window.grab_set()
            else:
                messagebox.showerror("Error", "Could not find current task details in the database.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error retrieving task details: {str(e)}")
        finally:
            conn.close()

    def disable_buttons(self, start_disabled):
        """Enable/disable timer control buttons"""
        start_state = DISABLED if start_disabled else NORMAL
        stop_state = NORMAL if start_disabled else DISABLED
        
        # Full page buttons
        self.full_page_start_button.config(state=start_state)
        self.full_page_stop_button.config(state=stop_state)
        
        # Small overlay buttons
        self.small_overlay_start_button.config(state=start_state)
        self.small_overlay_stop_button.config(state=stop_state)

    def import_Tasks(self):
        """Import tasks from a CSV file with proper tag handling"""
        global data
        # Ask user for the file
        file_path = tk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        # If file has been selected continue
        if file_path:
            # Open file and read from file
            with open(file_path, "r", encoding="utf-8-sig") as file:
                csv_reader = csv.reader(file)
                data = list(csv_reader)

                # Check if the first row is a header (by comparing column names)
                if data:
                    header = data[0]
                    expected_header = ["Task Name", "Task Weight", "Start Date", "Description", "Task Weight Type", "Task Tags"]

                    # If the first row matches the header, remove it
                    if header == expected_header:
                        data = data[1:]
        
            # Connect to the SQLite database
            conn = sqlite3.connect(path)
            c = conn.cursor()

            # Get existing task names from all three tables: TaskList, CurrentTask, and CompletedTasks
            c.execute("SELECT task_name FROM TaskList")
            tasklist_names = {row[0] for row in c.fetchall()}
            
            c.execute("SELECT task_name FROM CurrentTask")
            currenttask_names = {row[0] for row in c.fetchall()}
            
            c.execute("SELECT task_name FROM CompletedTasks")
            completedtasks_names = {row[0] for row in c.fetchall()}
            
            # Combine all task names into one set
            existing_tasks = tasklist_names.union(currenttask_names).union(completedtasks_names)

            # Track statistics for user feedback
            tasks_imported = 0
            tasks_skipped = 0
            skipped_tasks = []

            # Get the tags database path
            tags_path = str(path).replace('task_list.db', 'tags.db')
            
            # Connect to tags database to get valid tags
            tags_conn = sqlite3.connect(tags_path)
            tags_c = tags_conn.cursor()
            
            # Get all valid tag names
            tags_c.execute("SELECT tag_name FROM tags")
            valid_tags = [row[0] for row in tags_c.fetchall()]
            tags_conn.close()

            # Filter out tasks with names that already exist in the database
            filtered_data = []
            for task in data:
                if len(task) < 6:
                    # Skip tasks with incomplete data
                    tasks_skipped += 1
                    if task and len(task) > 0:
                        skipped_tasks.append(task[0])
                    continue
                    
                if task[0] not in existing_tasks:  # task[0] is the task name
                    # Process the task tags (index 5) to ensure they're in the correct format
                    tag_text = task[5].strip()
                    
                    # Split tags if they're comma-separated
                    if ',' in tag_text:
                        tag_list = [t.strip() for t in tag_text.split(',')]
                    else:
                        tag_list = [t.strip() for t in tag_text.split() if t.strip()]  # Split by whitespace if no commas
                    
                    # Only keep valid tags that exist in the tags database
                    valid_task_tags = [tag for tag in tag_list if tag in valid_tags]
                    
                    # Format tags as newline-separated list (the format used by the app)
                    formatted_tags = '\n'.join(valid_task_tags)
                    
                    # Update the task data with formatted tags
                    task_with_formatted_tags = list(task)
                    task_with_formatted_tags[5] = formatted_tags
                    
                    filtered_data.append(task_with_formatted_tags)
                    tasks_imported += 1
                else:
                    tasks_skipped += 1
                    skipped_tasks.append(task[0])

            # Get the max list_place value
            c.execute("SELECT COALESCE(MAX(list_place), 0) FROM TaskList")
            max_list_place = c.fetchone()[0] or 0
            
            # Insert filtered data into the table with proper list_place values
            if filtered_data:
                for i, task_data in enumerate(filtered_data):
                    # Add a default task time
                    task_time = "00:00:00"
                    
                    # Set end date to None (can be updated later)
                    task_end_date = None
                    
                    # Use prepared statement
                    c.execute("""
                        INSERT INTO TaskList (
                            task_name, task_weight, task_start_date, task_description,
                            task_weight_type, task_tags, task_time, task_end_date, list_place
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        task_data[0],  # task_name
                        task_data[1],  # task_weight
                        task_data[2],  # task_start_date
                        task_data[3],  # task_description
                        task_data[4],  # task_weight_type
                        task_data[5],  # task_tags (properly formatted)
                        task_time,     # default task_time
                        task_end_date, # default task_end_date (None)
                        max_list_place + i + 1  # increment list_place for each task
                    ))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Provide feedback to the user
            if tasks_imported > 0 and tasks_skipped > 0:
                messagebox.showinfo("Import Results", 
                                f"Successfully imported {tasks_imported} tasks.\n"
                                f"Skipped {tasks_skipped} tasks with duplicate names or missing data.")
                
                # If there are many skipped tasks, offer to show them in a separate dialog
                if tasks_skipped > 5:
                    show_details = messagebox.askyesno("Show Details", 
                                                    f"Would you like to see the list of skipped tasks?")
                    if show_details:
                        skipped_list = "\n".join(skipped_tasks[:20])
                        if len(skipped_tasks) > 20:
                            skipped_list += f"\n... and {len(skipped_tasks) - 20} more"
                        
                        messagebox.showinfo("Skipped Tasks", skipped_list)
            elif tasks_imported > 0:
                messagebox.showinfo("Import Complete", f"Successfully imported {tasks_imported} tasks.")
            elif tasks_skipped > 0:
                messagebox.showwarning("Import Failed", 
                                    f"All {tasks_skipped} tasks could not be imported due to duplicates or missing data.")
            else:
                messagebox.showinfo("Import Notice", "No tasks were found to import.")

            self.query_database()

    def search_Task(self, event):

            #Getting the name they entered
            lookup = self.search_entry.get()

            # Create or Connect to the database
            conn = sqlite3.connect(path)

            # Create a cursor instance
            c = conn.cursor()

            # Clear the Treeview
            for task in self.task_list.get_children():
                self.task_list.delete(task)

            if lookup == "":

                c.execute("""
                SELECT rowid, * FROM TaskList 
                ORDER BY list_place
            """)
            tasks = c.fetchall()
            for count, record in enumerate(tasks):
                tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                self.task_list.insert(
                    parent='',
                    index='end',
                    iid=count,
                    text='',
                    values=(
                        record[1],   # task_name
                        record[2],   # task_time
                        record[3],   # task_weight
                        record[4],   # task_id
                        record[5],   # start_date
                        record[6],   # end_date
                        record[7]    # description
                    ),
                    tags=tags
                )
            else:
                c.execute("SELECT * FROM TaskList WHERE task_name like ? OR task_tags LIKE ?", (f"%{lookup}%", f"%{lookup}%")) 
                
                tasks = c.fetchall()
            

                # Add data to screen
                for count, record in enumerate(tasks):
                    tags = ('evenrow',) if count % 2 == 0 else ('oddrow',)
                    self.task_list.insert(
                        parent='',
                        index='end',
                        iid=count,
                        text='',
                        values=(
                            record[0],   # task_name
                            record[1],   # task_time
                            record[2],   # task_weight
                            record[3],   # task_id
                            record[4],   # start_date
                            record[5],   # end_date
                            record[6]    # description
                        ),
                        tags=tags
                    )

            # Commit changes
            conn.commit()

            # Close connection to the database
            conn.close()
 
 


    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common operations"""
        # Global application shortcuts
        self.root.bind("<Control-q>", lambda event: self.on_close())  # Ctrl+Q to close the application
        self.root.bind("<F1>", lambda event: self.show_help())  # F1 for help
        self.root.bind("<Control-p>", lambda event: self.show_preferences())  # Ctrl+P for preferences
        
        # Page-specific shortcuts need to be bound to each page
        # Add Task shortcuts
        self.root.bind("<Control-n>", lambda event: self.open_AddTaskWindow())  # Ctrl+N for new task
        
        # Task management shortcuts
        self.root.bind("<Control-e>", lambda event: self.open_EditTaskWindow())  # Ctrl+E to edit selected task
        self.root.bind("<Control-h>", lambda event: self.open_CommitHistoryWindow())  # Ctrl+H to view history
        self.root.bind("<Control-Delete>", lambda event: self.delete_task())  # Ctrl+Delete to delete task
        
        # Timer control shortcuts
        self.root.bind("<F5>", lambda event: self.start_timer())  # F5 to start timer
        self.root.bind("<F6>", lambda event: self.stop_timer())  # F6 to stop timer
        
        # Navigation shortcuts
        self.root.bind("<Control-1>", lambda event: self.switch_page("Time Tracker"))  # Ctrl+1 for Time Tracker
        self.root.bind("<Control-2>", lambda event: self.switch_page("Completed Tasks"))  # Ctrl+2 for Completed Tasks
        self.root.bind("<Control-3>", lambda event: self.switch_page("Small Overlay"))  # Ctrl+3 for Small Overlay
        self.root.bind("<Control-4>", lambda event: self.switch_page("Tags Database"))  # Ctrl+4 for Tags Database
        self.root.bind("<Control-5>", lambda event: self.switch_page("Analytics"))  # Ctrl+5 for Analytics
        self.root.bind("<Control-6>", lambda event: self.switch_page("Archive"))  # Ctrl+6 for Archive
        
        # Data management shortcuts
        self.root.bind("<Control-b>", lambda event: self.backup_database(manual=True))  # Ctrl+B for backup
        self.root.bind("<Control-r>", lambda event: self.restore_database())  # Ctrl+R for restore

    def show_help(self):
        """Display help dialog with keyboard shortcuts"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Task Manager Help")
        help_window.geometry("500x500")
        help_window.configure(bg="#A9A9A9")
        help_window.transient(self.root)  # Make this window a child of the main window
        
        # Create a notebook for tabbed help content
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a tab for keyboard shortcuts
        shortcuts_frame = tk.Frame(notebook, bg="#d3d3d3")
        notebook.add(shortcuts_frame, text="Keyboard Shortcuts")
        
        # Create a scrollable text widget for the shortcuts
        shortcut_scroll = tk.Scrollbar(shortcuts_frame)
        shortcut_scroll.pack(side="right", fill="y")
        
        shortcut_text = tk.Text(shortcuts_frame, yscrollcommand=shortcut_scroll.set, bg="#d3d3d3", wrap="word")
        shortcut_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        shortcut_scroll.config(command=shortcut_text.yview)
        
        # Add shortcut information
        shortcut_text.tag_configure("heading", font=("SF Pro Display", 12, "bold"))
        shortcut_text.tag_configure("subheading", font=("SF Pro Display", 10, "bold"))
        shortcut_text.tag_configure("shortcut", font=("SF Pro Text", 9, "bold"))
        
        shortcut_text.insert(tk.END, "Keyboard Shortcuts\n\n", "heading")
        
        shortcut_text.insert(tk.END, "Global Shortcuts\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+Q: ", "shortcut")
        shortcut_text.insert(tk.END, "Exit application\n")
        shortcut_text.insert(tk.END, "F1: ", "shortcut")
        shortcut_text.insert(tk.END, "Show this help\n")
        shortcut_text.insert(tk.END, "Ctrl+P: ", "shortcut")
        shortcut_text.insert(tk.END, "Preferences\n\n")
        
        shortcut_text.insert(tk.END, "Navigation\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+1: ", "shortcut")
        shortcut_text.insert(tk.END, "Time Tracker\n")
        shortcut_text.insert(tk.END, "Ctrl+2: ", "shortcut")
        shortcut_text.insert(tk.END, "Completed Tasks\n")
        shortcut_text.insert(tk.END, "Ctrl+3: ", "shortcut")
        shortcut_text.insert(tk.END, "Small Overlay\n")
        shortcut_text.insert(tk.END, "Ctrl+4: ", "shortcut")
        shortcut_text.insert(tk.END, "Tags Database\n")
        shortcut_text.insert(tk.END, "Ctrl+5: ", "shortcut")
        shortcut_text.insert(tk.END, "Analytics\n")
        shortcut_text.insert(tk.END, "Ctrl+6: ", "shortcut")
        shortcut_text.insert(tk.END, "Archive\n\n")
        
        shortcut_text.insert(tk.END, "Task Management\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+N: ", "shortcut")
        shortcut_text.insert(tk.END, "Add new task\n")
        shortcut_text.insert(tk.END, "Ctrl+E: ", "shortcut")
        shortcut_text.insert(tk.END, "Edit selected task\n")
        shortcut_text.insert(tk.END, "Ctrl+H: ", "shortcut")
        shortcut_text.insert(tk.END, "View task history\n")
        shortcut_text.insert(tk.END, "Ctrl+Delete: ", "shortcut")
        shortcut_text.insert(tk.END, "Delete selected task\n\n")
        
        shortcut_text.insert(tk.END, "Timer Controls\n", "subheading")
        shortcut_text.insert(tk.END, "F5: ", "shortcut")
        shortcut_text.insert(tk.END, "Start timer\n")
        shortcut_text.insert(tk.END, "F6: ", "shortcut")
        shortcut_text.insert(tk.END, "Stop timer\n\n")
        
        shortcut_text.insert(tk.END, "List Operations\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+A: ", "shortcut")
        shortcut_text.insert(tk.END, "Select all items\n")
        shortcut_text.insert(tk.END, "Ctrl+F: ", "shortcut")
        shortcut_text.insert(tk.END, "Search\n")
        shortcut_text.insert(tk.END, "Escape: ", "shortcut")
        shortcut_text.insert(tk.END, "Deselect all items\n\n")
        
        shortcut_text.insert(tk.END, "Data Management\n", "subheading")
        shortcut_text.insert(tk.END, "Ctrl+B: ", "shortcut")
        shortcut_text.insert(tk.END, "Backup database\n")
        shortcut_text.insert(tk.END, "Ctrl+R: ", "shortcut")
        shortcut_text.insert(tk.END, "Restore database\n")
        
        # Make the text widget read-only
        shortcut_text.config(state="disabled")
        
        # Create a tab for general help
        general_frame = tk.Frame(notebook, bg="#d3d3d3")
        notebook.add(general_frame, text="General Help")
        
        # Create a scrollable text widget for general help
        general_scroll = tk.Scrollbar(general_frame)
        general_scroll.pack(side="right", fill="y")
        
        general_text = tk.Text(general_frame, yscrollcommand=general_scroll.set, bg="#d3d3d3", wrap="word")
        general_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        general_scroll.config(command=general_text.yview)
        
        # Add general help information
        general_text.tag_configure("heading", font=("SF Pro Display", 12, "bold"))
        general_text.tag_configure("subheading", font=("SF Pro Display", 10, "bold"))
        
        general_text.insert(tk.END, "Task Manager Help\n\n", "heading")
        
        general_text.insert(tk.END, "Time Tracker\n", "subheading")
        general_text.insert(tk.END, "This is the main view where you can manage your tasks. You can add, edit, and delete tasks, as well as start and stop the timer for the current task.\n\n")
        
        general_text.insert(tk.END, "Completed Tasks\n", "subheading")
        general_text.insert(tk.END, "View and manage your completed tasks. You can restore tasks back to the active list or archive them.\n\n")
        
        general_text.insert(tk.END, "Small Overlay\n", "subheading")
        general_text.insert(tk.END, "A minimal view that shows just the current task and timer controls. Useful when you want to keep the timer visible while working on other things.\n\n")
        
        general_text.insert(tk.END, "Tags Database\n", "subheading")
        general_text.insert(tk.END, "Manage the tags used to categorize your tasks. You can add, edit, and delete tags here.\n\n")
        
        general_text.insert(tk.END, "Analytics\n", "subheading")
        general_text.insert(tk.END, "View statistics and visualizations of your task data. See how you're spending your time and identify trends.\n\n")
        
        general_text.insert(tk.END, "Archive\n", "subheading")
        general_text.insert(tk.END, "Access archived tasks that are no longer needed in the completed tasks list. You can restore tasks from here if needed.\n\n")
        
        general_text.insert(tk.END, "Data Management\n", "subheading")
        general_text.insert(tk.END, "The application automatically backs up your database regularly. You can also manually create backups and restore from previous backups using the options in the menu.\n\n")
        
        # Make the text widget read-only
        general_text.config(state="disabled")
        
        # About tab
        about_frame = tk.Frame(notebook, bg="#d3d3d3")
        notebook.add(about_frame, text="About")
        
        # About content
        about_label = tk.Label(
            about_frame,
            text="Task Manager\nVersion 1.0\n\nA simple task management application with time tracking capabilities.",
            font=("SF Pro Display", 10),
            bg="#d3d3d3",
            justify="center"
        )
        about_label.pack(pady=20)
        
        # Close button
        close_btn = tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            bg="#e99e56",
            font=("SF Pro Text", 10)
        )
        close_btn.pack(pady=10)
    def show_preferences(self):
        """Show and edit user preferences"""
        prefs_window = tk.Toplevel(self.root)
        prefs_window.title("Preferences")
        prefs_window.geometry("400x300")
        prefs_window.configure(bg="#A9A9A9")
        prefs_window.transient(self.root)  # Make this window a child of the main window
        prefs_window.grab_set()  # Make this window modal
        
        # Load current preferences
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            # Create the preferences table if it doesn't exist
            c.execute("""CREATE TABLE IF NOT EXISTS user_preferences (
                preference_key TEXT PRIMARY KEY,
                preference_value TEXT
            )""")
            
            # Insert default preferences if they don't exist
            c.execute("""INSERT OR IGNORE INTO user_preferences (preference_key, preference_value)
                VALUES 
                    ('theme', 'light'),
                    ('inactivity_timeout', '7200'),
                    ('auto_backup', 'true'),
                    ('backup_interval', '86400')
            """)
            
            # Get current preferences
            c.execute("SELECT preference_key, preference_value FROM user_preferences")
            preferences = dict(c.fetchall())
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            preferences = {
                'theme': 'light',
                'inactivity_timeout': '7200',
                'auto_backup': 'true',
                'backup_interval': '86400'
            }
        finally:
            conn.close()
        
        # Create main frame
        main_frame = tk.Frame(prefs_window, bg="#A9A9A9")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Theme preference
        theme_frame = tk.Frame(main_frame, bg="#A9A9A9")
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = tk.Label(theme_frame, text="Theme:", bg="#A9A9A9", font=("SF Pro Text", 10))
        theme_label.pack(side="left", padx=(0, 10))
        
        theme_var = tk.StringVar(value=preferences.get('theme', 'light'))
        theme_rb_light = tk.Radiobutton(theme_frame, text="Light", variable=theme_var, value="light", bg="#dcdcdc")
        theme_rb_light.pack(side="left", padx=5)
        
        theme_rb_dark = tk.Radiobutton(theme_frame, text="Dark", variable=theme_var, value="dark", bg="#A9A9A9")
        theme_rb_dark.pack(side="left", padx=5)
        
        # Inactivity timeout preference
        timeout_frame = tk.Frame(main_frame, bg="#A9A9A9")
        timeout_frame.pack(fill="x", pady=5)
        
        timeout_label = tk.Label(timeout_frame, text="Inactivity Timeout (seconds):", bg="#A9A9A9", font=("SF Pro Text", 10))
        timeout_label.pack(side="left", padx=(0, 10))
        
        timeout_var = tk.StringVar(value=preferences.get('inactivity_timeout', '7200'))
        timeout_entry = tk.Entry(timeout_frame, textvariable=timeout_var, width=10)
        timeout_entry.pack(side="left")
        
        # Auto backup preference
        backup_frame = tk.Frame(main_frame, bg="#A9A9A9")
        backup_frame.pack(fill="x", pady=5)
        
        backup_var = tk.BooleanVar(value=preferences.get('auto_backup', 'true').lower() == 'true')
        backup_cb = tk.Checkbutton(backup_frame, text="Enable Automatic Backups", variable=backup_var, bg="#A9A9A9")
        backup_cb.pack(side="left")
        
        # Backup interval preference
        interval_frame = tk.Frame(main_frame, bg="#A9A9A9")
        interval_frame.pack(fill="x", pady=5)
        
        interval_label = tk.Label(interval_frame, text="Backup Interval (seconds):", bg="#A9A9A9", font=("SF Pro Text", 10))
        interval_label.pack(side="left", padx=(0, 10))
        
        interval_var = tk.StringVar(value=preferences.get('backup_interval', '86400'))
        interval_entry = tk.Entry(interval_frame, textvariable=interval_var, width=10)
        interval_entry.pack(side="left")
        
        # Buttons frame
        buttons_frame = tk.Frame(prefs_window, bg="#A9A9A9")
        buttons_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        
        # Save function
        def save_preferences():
            # Validate inputs
            try:
                # Convert to ensure they are valid numbers
                inactivity_timeout = int(timeout_var.get())
                backup_interval = int(interval_var.get())
                
                # Enforce minimum values
                if inactivity_timeout < 60:
                    messagebox.showwarning("Invalid Value", "Inactivity timeout must be at least 60 seconds.")
                    return
                    
                if backup_interval < 300:
                    messagebox.showwarning("Invalid Value", "Backup interval must be at least 300 seconds (5 minutes).")
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Timeout and interval must be valid numbers.")
                return
            
            # Save preferences to database
            conn = sqlite3.connect(path)
            c = conn.cursor()
            
            try:
                c.execute("BEGIN")
                
                # Update preferences
                c.execute("UPDATE user_preferences SET preference_value = ? WHERE preference_key = ?", 
                        (theme_var.get(), 'theme'))
                c.execute("UPDATE user_preferences SET preference_value = ? WHERE preference_key = ?", 
                        (timeout_var.get(), 'inactivity_timeout'))
                c.execute("UPDATE user_preferences SET preference_value = ? WHERE preference_key = ?", 
                        (str(backup_var.get()).lower(), 'auto_backup'))
                c.execute("UPDATE user_preferences SET preference_value = ? WHERE preference_key = ?", 
                        (interval_var.get(), 'backup_interval'))
                
                c.execute("COMMIT")
                
                # Apply preferences
                self.apply_preferences()
                
                # Close dialog
                prefs_window.destroy()
                
            except sqlite3.Error as e:
                c.execute("ROLLBACK")
                print(f"Database error: {e}")
                messagebox.showerror("Error", f"Failed to save preferences: {e}")
            finally:
                conn.close()
        
        # Save button
        save_btn = tk.Button(buttons_frame, text="Save", command=save_preferences, bg="#90EE90", font=("SF Pro Text", 10))
        save_btn.pack(side="right", padx=(5, 0))
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame, text="Cancel", command=prefs_window.destroy, bg="#e99e56", font=("SF Pro Text", 10))
        cancel_btn.pack(side="right")

    def apply_preferences(self):
        """Apply user preferences"""
        # Load preferences from database
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            c.execute("SELECT preference_key, preference_value FROM user_preferences")
            preferences = dict(c.fetchall())
            
            # Apply theme
            theme = preferences.get('theme', 'light')
            self.set_theme(theme)
            
            # Apply inactivity timeout
            if hasattr(self, 'inactivity_limit'):
                try:
                    self.inactivity_limit = int(preferences.get('inactivity_timeout', '7200'))
                    # Reset timer
                    self.reset_inactivity_timer()
                except (ValueError, TypeError):
                    print("Invalid inactivity timeout value in preferences")
            
            # Apply auto backup
            auto_backup = preferences.get('auto_backup', 'true').lower() == 'true'
            if hasattr(self, 'auto_backup') and auto_backup != self.auto_backup:
                self.auto_backup = auto_backup
                # Setup backup timer if enabled, otherwise cancel existing timer
                if self.auto_backup:
                    self.setup_auto_backup()
                elif hasattr(self, 'backup_timer') and self.backup_timer:
                    self.backup_timer.cancel()
                    self.backup_timer = None
            
        except sqlite3.Error as e:
            print(f"Database error when applying preferences: {e}")
        finally:
            conn.close()

    def set_theme(self, theme):
        """Set the application theme"""
        if theme == 'light':
            # Set light theme colors
            self.bg_color = "#A9A9A9"
            self.fg_color = "#000000"
            self.frame_color = "#dcdcdc"
            self.entry_bg_color = "#d3d3d3"
            self.button_bg_color = "#b2fba5"
            self.delete_button_bg_color = "#e99e56"
        else:
            # Set dark theme colors
            self.bg_color = "#333333"
            self.fg_color = "#FFFFFF"
            self.entry_bg_color = "#555555"
            self.button_bg_color = "#4A6984"
            self.delete_button_bg_color = "#8B4513"
        
        # Apply theme to root window
        self.root.configure(bg=self.bg_color)
        
        # Apply to all frames - recursively update widgets
        self.update_widget_colors(self.root)

    def update_widget_colors(self, widget):
        """Recursively update widget colors for theme"""
        try:
            # Update this widget's colors if applicable
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.configure(bg=self.bg_color)
            elif isinstance(widget, tk.LabelFrame):
                widget.configure(bg = self.frame_color)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.bg_color, fg=self.fg_color)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=self.entry_bg_color, fg=self.fg_color)
            elif isinstance(widget, tk.Text):
                widget.configure(bg=self.entry_bg_color, fg=self.fg_color)
            elif isinstance(widget, tk.Button):
                # Check if it's a delete button or regular button
                if widget.cget("text") in ("Delete", "Delete All", "Remove All"):
                    widget.configure(bg=self.delete_button_bg_color)
                else:
                    widget.configure(bg=self.button_bg_color)
                    
            # Now recursively update children
            for child in widget.winfo_children():
                self.update_widget_colors(child)
                
        except tk.TclError:
            # Some widgets might not support all operations, just skip those
            pass

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create a toplevel window
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            
        def hide_tooltip(event):
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def setup_auto_backup(self):
        """Setup automatic database backups"""
        # Stop existing backup timer if any
        if hasattr(self, 'backup_timer') and self.backup_timer:
            self.backup_timer.cancel()
        
        # Load backup preferences
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            # Create user_preferences table if it doesn't exist
            c.execute("""CREATE TABLE IF NOT EXISTS user_preferences (
                preference_key TEXT PRIMARY KEY,
                preference_value TEXT
            )""")
            
            # Insert default backup preferences if not exist
            c.execute("""INSERT OR IGNORE INTO user_preferences (preference_key, preference_value)
                VALUES 
                    ('auto_backup', 'true'),
                    ('backup_interval', '86400')
            """)
            
            # Get auto backup setting
            c.execute("SELECT preference_value FROM user_preferences WHERE preference_key = 'auto_backup'")
            auto_backup = c.fetchone()
            if auto_backup and auto_backup[0].lower() == 'true':
                # Get backup interval
                c.execute("SELECT preference_value FROM user_preferences WHERE preference_key = 'backup_interval'")
                interval = c.fetchone()
                if interval:
                    try:
                        interval_seconds = int(interval[0])
                        # Set a minimum interval
                        if interval_seconds < 300:  # 5 minutes minimum
                            interval_seconds = 300
                        
                        # Create backup timer
                        self.backup_timer = threading.Timer(interval_seconds, self.run_auto_backup)
                        self.backup_timer.daemon = True  # Allow the timer to exit when the program exits
                        self.backup_timer.start()
                        
                        print(f"Auto backup scheduled every {interval_seconds} seconds")
                    except (ValueError, TypeError):
                        print("Invalid backup interval in preferences")
                        
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error when setting up auto backup: {e}")
        finally:
            conn.close()

    def run_auto_backup(self):
        """Run automatic database backup"""
        try:
            # Create backup
            self.backup_database()
            
            # Schedule next backup
            self.setup_auto_backup()
        except Exception as e:
            print(f"Error during auto backup: {e}")
            # Try again later even if there was an error
            if hasattr(self, 'backup_timer'):
                self.backup_timer = threading.Timer(3600, self.run_auto_backup)  # Retry after an hour
                self.backup_timer.daemon = True
                self.backup_timer.start()

    def backup_database(self, manual=False):
        """Backup the database files"""
        try:
            # Create backup directory if it doesn't exist
            backup_dir = pathlib.Path(__file__).parent / "Backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create timestamped backup directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_subdir = backup_dir / timestamp
            backup_subdir.mkdir(parents=True, exist_ok=True)
            
            # Get database directory
            db_dir = pathlib.Path(path).parent
            
            # Count backed up files
            backed_up_count = 0
            
            # Copy all database files
            for file in db_dir.glob("*.db"):
                # Create backup file path
                backup_file = backup_subdir / file.name
                
                # Copy file
                shutil.copy2(file, backup_file)
                backed_up_count += 1
            
            # Clean up old backups - keep last 10
            self.cleanup_old_backups(backup_dir, 10)
            
            if manual:
                messagebox.showinfo("Backup Complete", f"Database backup completed successfully.\n{backed_up_count} files backed up to:\n{backup_subdir}")
            else:
                # Update status if available
                if hasattr(self, 'page_title'):
                    old_text = self.page_title.cget("text")
                    self.page_title.config(text=f"Auto backup completed at {datetime.now().strftime('%H:%M:%S')}")
                    # Reset after a moment
                    self.root.after(3000, lambda: self.page_title.config(text=old_text))
            
            return True
        except Exception as e:
            error_message = f"Backup failed: {str(e)}"
            print(error_message)
            if manual:
                messagebox.showerror("Backup Failed", error_message)
            return False

    def cleanup_old_backups(self, backup_dir, keep_count=10):
        """Clean up old backups, keeping only the most recent ones"""
        try:
            # Get all backup directories
            backups = [d for d in backup_dir.iterdir() if d.is_dir()]
            
            # Sort by creation time (oldest first)
            backups.sort(key=lambda d: d.stat().st_ctime)
            
            # Delete oldest backups if we have more than keep_count
            if len(backups) > keep_count:
                for old_backup in backups[:-keep_count]:
                    try:
                        # Remove all files in directory
                        for file in old_backup.iterdir():
                            file.unlink()
                        # Remove directory
                        old_backup.rmdir()
                    except Exception as e:
                        print(f"Error removing old backup {old_backup}: {e}")
        except Exception as e:
            print(f"Error cleaning up old backups: {e}")

    def restore_database(self):
        """Restore the database from a backup"""
        try:
            # Get backup directory
            backup_dir = pathlib.Path(__file__).parent / "Backups"
            if not backup_dir.exists():
                messagebox.showinfo("No Backups", "No backups found to restore.")
                return False
            
            # Get all backup directories
            backups = [d for d in backup_dir.iterdir() if d.is_dir()]
            if not backups:
                messagebox.showinfo("No Backups", "No backups found to restore.")
                return False
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda d: d.stat().st_ctime, reverse=True)
            
            # Create restore dialog
            restore_window = tk.Toplevel(self.root)
            restore_window.title("Restore Database")
            restore_window.geometry("500x400")
            restore_window.configure(bg="#A9A9A9")
            restore_window.transient(self.root)  # Make this window a child of the main window
            restore_window.grab_set()  # Make this window modal
            
            # Create main frame
            main_frame = tk.Frame(restore_window, bg="#A9A9A9")
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Add instruction label
            instruction_label = tk.Label(
                main_frame,
                text="Select a backup to restore:",
                font=("SF Pro Display", 12),
                bg="#A9A9A9"
            )
            instruction_label.pack(pady=(0, 10))
            
            # Create frame for backup list
            list_frame = tk.Frame(main_frame, bg="#d3d3d3")
            list_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Add a scrollbar
            scrollbar = tk.Scrollbar(list_frame)
            scrollbar.pack(side="right", fill="y")
            
            # Create listbox for backups
            backup_listbox = tk.Listbox(
                list_frame,
                yscrollcommand=scrollbar.set,
                font=("SF Pro Text", 10),
                bg="#d3d3d3",
                selectbackground="#347083",
                selectforeground="white",
                height=15
            )
            backup_listbox.pack(side="left", fill="both", expand=True)
            
            # Configure the scrollbar
            scrollbar.config(command=backup_listbox.yview)
            
            # Populate listbox with backup timestamps and file count
            for i, backup in enumerate(backups):
                # Get creation time
                timestamp = datetime.fromtimestamp(backup.stat().st_ctime)
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # Count files
                file_count = len(list(backup.glob("*.db")))
                
                # Add to listbox
                backup_listbox.insert(tk.END, f"{timestamp_str} ({file_count} files)")
                # Store the backup path as an item configuration
                backup_listbox.itemconfig(i, {"backup_path": str(backup)})
            
            # Select the first (most recent) backup
            if backups:
                backup_listbox.select_set(0)
            
            # Create details frame
            details_frame = tk.Frame(main_frame, bg="#A9A9A9")
            details_frame.pack(fill="x", pady=10)
            
            # Add details label
            details_label = tk.Label(
                details_frame,
                text="",
                font=("SF Pro Text", 10),
                bg="#A9A9A9",
                anchor="w",
                justify="left"
            )
            details_label.pack(fill="x")
            
            # Function to update details when selection changes
            def on_select(event):
                selected_indices = backup_listbox.curselection()
                if selected_indices:
                    selected_idx = selected_indices[0]
                    # Get backup path
                    backup_path = pathlib.Path(backup_listbox.itemconfig(selected_idx, "backup_path"))
                    
                    # Get creation time
                    timestamp = datetime.fromtimestamp(backup_path.stat().st_ctime)
                    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # List files
                    files = list(backup_path.glob("*.db"))
                    file_list = "\n".join([f"- {file.name}" for file in files])
                    
                    # Update details label
                    details_label.config(text=f"Backup Date: {timestamp_str}\nFiles:\n{file_list}")
            
            # Bind selection event
            backup_listbox.bind("<<ListboxSelect>>", on_select)
            
            # Trigger initial selection
            if backups:
                on_select(None)
            
            # Button frame
            button_frame = tk.Frame(restore_window, bg="#A9A9A9")
            button_frame.pack(fill="x", pady=10)
            
            # Function to perform database restore
            def do_restore():
                selected_indices = backup_listbox.curselection()
                if not selected_indices:
                    messagebox.showwarning("Selection Required", "Please select a backup to restore.")
                    return
                        
                selected_idx = selected_indices[0]
                # Get backup path
                backup_path = pathlib.Path(backup_listbox.itemconfig(selected_idx, "backup_path"))
                        
                # Confirm restore
                if not messagebox.askyesno("Confirm Restore", 
                                           "Are you sure you want to restore from this backup?\n\n"
                                           "This will replace your current database files. Any changes made "
                                           "since this backup will be lost."):
                    return
                        
                try:
                    # Create backup of current database first
                    self.backup_database()
                    
                    # Get database directory
                    db_dir = pathlib.Path(self.path).parent
                    
                    # Copy each backup file to database directory
                    restored_count = 0
                    for file in backup_path.glob("*.db"):
                        # Create target file path
                        target_file = db_dir / file.name
                        
                        # Copy file
                        shutil.copy2(file, target_file)
                        restored_count += 1
                    
                    messagebox.showinfo("Restore Complete", 
                                         f"Database restored successfully from backup.\n{restored_count} files restored.")
                    
                    # Close restore dialog
                    restore_window.destroy()
                    
                    # Ask if user wants to restart application
                    if messagebox.askyesno("Restart Required", 
                                           "The application needs to be restarted to apply the restored database.\n\n"
                                           "Do you want to restart now?"):
                        # Restart application
                        self.restart_application()
                    
                except Exception as e:
                    messagebox.showerror("Restore Failed", f"Failed to restore database: {str(e)}")
            
            # Restore button
            restore_btn = tk.Button(
                button_frame,
                text="Restore",
                command=do_restore,
                bg="#90EE90",
                font=("SF Pro Text", 10)
            )
            restore_btn.pack(side="left", padx=10)
            
            # Cancel button
            cancel_btn = tk.Button(
                button_frame,
                text="Cancel",
                command=restore_window.destroy,
                bg="#e99e56",
                font=("SF Pro Text", 10)
            )
            cancel_btn.pack(side="right", padx=10)
            
            return True
        
        except Exception as e:
            messagebox.showerror("Restore Error", f"An error occurred: {str(e)}")
            return False

    def restart_application(self):
        """Restart the application"""
        # Save any pending changes
        if hasattr(self, 'save_pending_changes'):
            self.save_pending_changes()
        
        # Close the application
        self.root.destroy()
        
        # Restart Python script
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Add a manual backup option to the menu
    def add_backup_menu_item(self):
        """Add backup and restore options to the menu"""
        # Check if popup menu exists
        if hasattr(self, 'popup_menu'):
            # Add a separator
            self.popup_menu.add_separator()
            
            # Add backup command
            self.popup_menu.add_command(label="Backup Database", command=lambda: self.backup_database(manual=True))
            
            # Add restore command
            self.popup_menu.add_command(label="Restore Database", command=self.restore_database)

    # Initialize backup timer when application starts
    def initialize_backup_system(self):
        """Initialize the database backup system"""
        # Set default auto backup setting if not exists
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        try:
            # Create user_preferences table if it doesn't exist
            c.execute("""CREATE TABLE IF NOT EXISTS user_preferences (
                preference_key TEXT PRIMARY KEY,
                preference_value TEXT
            )""")
            
            # Insert default values if not exists
            c.execute("""INSERT OR IGNORE INTO user_preferences (preference_key, preference_value)
                VALUES 
                    ('auto_backup', 'true'),
                    ('backup_interval', '86400')
            """)
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error when initializing backup system: {e}")
        finally:
            conn.close()
        
        # Setup auto backup
        self.auto_backup = True  # Default to enabled
        self.setup_auto_backup()
        
        # Add backup menu items
        self.add_backup_menu_item()

    # This function needs to be added to the __init__ method
    def initialize_ui_enhancements(self):
        """Initialize UI enhancements like keyboard shortcuts and tooltips"""
        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Add tooltips to buttons
        self.add_tooltips()
        
        # Initialize backup system
        self.initialize_backup_system()
        
        # Apply user preferences
        self.apply_preferences()

    def add_tooltips(self):
        """Add tooltips to various UI elements"""
        # Add tooltips to main page buttons
        if hasattr(self, 'update_button'):
            self.create_tooltip(self.update_button, "Edit the selected task (Ctrl+E)")
        
        if hasattr(self, 'add_button'):
            self.create_tooltip(self.add_button, "Add a new task (Ctrl+N)")
        
        if hasattr(self, 'commit_button'):
            self.create_tooltip(self.commit_button, "View the task's history (Ctrl+H)")
        
        # Timer control buttons
        if hasattr(self, 'full_page_start_button'):
            self.create_tooltip(self.full_page_start_button, "Start the timer (F5)")
        
        if hasattr(self, 'full_page_stop_button'):
            self.create_tooltip(self.full_page_stop_button, "Stop the timer (F6)")
        
        # Small overlay buttons
        if hasattr(self, 'small_overlay_start_button'):
            self.create_tooltip(self.small_overlay_start_button, "Start the timer (F5)")
        
        if hasattr(self, 'small_overlay_stop_button'):
            self.create_tooltip(self.small_overlay_stop_button, "Stop the timer (F6)")
        
        # Menu button
        if hasattr(self, 'menu_btn'):
            self.create_tooltip(self.menu_btn, "Open the menu to switch between pages")
        
        # Search entry
        if hasattr(self, 'search_entry'):
            self.create_tooltip(self.search_entry, "Search tasks (Ctrl+F)")

    # Define a delete_task method to be called by keyboard shortcut
    def delete_task(self):
        """Delete the selected task (called by keyboard shortcut)"""
        # Check if we are in Completed Tasks view
        if self.current_page == self.completedtasks_page:
            if hasattr(self.completedtasks_page, 'delete_selected_task'):
                self.completedtasks_page.delete_selected_task()
        # Check if we are in Archive view
        elif self.current_page == self.archive_page:
            if hasattr(self.archive_page, 'delete_selected_task'):
                self.archive_page.delete_selected_task()
        # Default to main page task list
        else:
            # This would depend on how tasks are deleted in the main view
            # For example, you might have a remove_task method
            task_id = self.ti_entry.get()
            if task_id:
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                    # Delete from database
                    conn = sqlite3.connect(path)
                    c = conn.cursor()
                    
                    try:
                        c.execute("DELETE FROM TaskList WHERE task_id = ?", (task_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Task deleted successfully.")
                        # Refresh the display
                        self.query_database()
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Failed to delete task: {e}")
                    finally:
                        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
