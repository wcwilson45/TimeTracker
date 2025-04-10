

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
    TagsDB,
    CompletedTasksList,
    AnalyticsPage,
    ArchiveTasksList, 
    SettingsPage,
    HelpPage
)
from ui.CommitHistoryPage import CommitHistoryWindow
from ui.CompletedTaskDetailsPage import CompletedTaskDetailsWindow as CTDW
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
      # self.settings_page = SettingsPage(self.main_container, self)

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
      self.popup_menu.add_command(label="Help and Documentation", command=lambda: self.switch_page("Help and Documentation"))
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
            self.root.geometry("640x580")
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
        elif page_name == "Help and Documentation":
            self.current_page = self.help_page
            self.page_title.config(text = "Help and Documentation", background=background_color)
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

        self.full_page_commit_history_button = tk.Button(time_controls_frame, text = "Commit History", background= main_btn_color, command= self.commit_history_current)
        self.full_page_commit_history_button.pack(side = LEFT, padx = (5,0))

        self.full_page_edit_button = tk.Button(time_controls_frame, text = "Edit", background= main_btn_color, command = self.edit_current_task)
        self.full_page_edit_button.pack(side = LEFT, padx = (5,0))
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
        response = messagebox.askyesno("Remove Everything?",
                                       "Warning!! This will remove everything from the TaskList, Current Task, and all of the Task History for all tasks.")

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
                self.set_current_task()

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
                # self.commit_button.config(state=tk.DISABLED)  # Disable the button
                # self.commithistory_window = CommitHistoryWindow(main_app=self, task_id=task, compFlag=False)  # Pass self to allow callback
                self.commithistory_window = CTDW(task_id=task, compFlag=1)
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

    def edit_current_task(self):
        """Open edit window for the current task"""
        # Check if there is a current task
        if not self.task_id_label.cget("text") or self.task_id_label.cget("text") == "-":
            messagebox.showwarning("No Current Task", "Please select a task first.")
            return
            
        task_id = self.task_id_label.cget("text")
        
        # Open the edit window
        if self.edittask_window is None or not self.edittask_window.winfo_exists():
            self.edittask_window = EditTaskWindow(task_id=task_id, main_app=self)
            self.edittask_window.grab_set()
        else:
            self.edittask_window.deiconify()
            self.edittask_window.lift()
            self.edittask_window.focus_force()

    def commit_history_current(self):
        """Open commit history window for the current task"""
        # Get the task ID from the current task label
        task_id = self.task_id_label.cget("text")
        
        # Check if there is a current task
        if not task_id or task_id == "-":
            messagebox.showwarning("No Current Task", "There is no current task selected.")
            return
        
        # Open the commit history window for the current task
        try:
            if self.commithistory_window is None or not self.commithistory_window.winfo_exists():
                # self.commit_button.config(state=tk.DISABLED)  # Disable the button
                # self.commithistory_window = CommitHistoryWindow(main_app=self, task_id=task_id, compFlag=False)
                self.commithistory_window = CTDW(task_id=task_id, compFlag=2)
            else:
                self.commithistory_window.deiconify()
                self.commithistory_window.lift()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening history window: {str(e)}")
            print(f"Exception details: {e}")
            # Re-enable the button if there was an error
            self.commit_button.config(state=tk.NORMAL)

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

            tags_path = str(path).replace('task_list.db', 'tags.db')
            
            # First extract all unique tags from the CSV
            all_tags = set()
            
            # First pass: extract all tags from the CSV
            for task_row in data:
                if len(task_row) >= 6:  # Ensure we have a task tags column
                    tag_text = task_row[5].strip()
                    
                    # Process tags with multiple possible separators
                    tag_list = []
                    # Check for pipe separator
                    if '|' in tag_text:
                        tag_list = [t.strip() for t in tag_text.split('|') if t.strip()]
                    # Check for comma separator as fallback
                    elif ',' in tag_text:
                        tag_list = [t.strip() for t in tag_text.split(',') if t.strip()]
                    # Use whitespace as last resort if no other separators found
                    elif tag_text and not any(sep in tag_text for sep in ['|', ',']):
                        tag_list = [t.strip() for t in tag_text.split() if t.strip()]
                    # If there are no separators but text exists, it's a single tag
                    elif tag_text:
                        tag_list = [tag_text]
                    
                    # Add individual tags to our set of all tags
                    all_tags.update(tag_list)
            
            # Fetch existing tag names from the database
            conn = sqlite3.connect(tags_path)
            c = conn.cursor()
            c.execute("SELECT tag_name FROM tags")
            existing_tags = [tag[0].lower() for tag in c.fetchall()]  # List of lowercase tag names for comparison
            existing_tags_original = {tag[0].lower(): tag[0] for tag in c.execute("SELECT tag_name FROM tags").fetchall()}  # Map lowercase to original case
            conn.close()

            # Insert new unique tags into the database
            conn = sqlite3.connect(tags_path)
            c = conn.cursor()

            # Add each new tag to the database
            for new_tag in all_tags:
                if new_tag and new_tag.lower() not in existing_tags:
                    try:
                        # Insert the new tag into the 'tags' table
                        c.execute("INSERT INTO tags (tag_name) VALUES (?)", (new_tag,))
                        # Update our tracking of existing tags
                        existing_tags.append(new_tag.lower())
                        existing_tags_original[new_tag.lower()] = new_tag
                    except sqlite3.Error as e:
                        print(f"Error inserting tag '{new_tag}': {str(e)}")

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            
            # Connect to the SQLite database for tasks
            conn = sqlite3.connect(path)
            c = conn.cursor()

            # Get existing task names from all three tables
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

            # Refresh valid tags list from the database
            tags_conn = sqlite3.connect(tags_path)
            tags_c = tags_conn.cursor()
            
            # Get all valid tag names (including newly added ones)
            tags_c.execute("SELECT tag_name FROM tags")
            valid_tags = [row[0] for row in tags_c.fetchall()]
            
            # Create a case-insensitive lookup dictionary
            valid_tags_lookup = {tag.lower(): tag for tag in valid_tags}
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
                    
                    # Process tags with multiple possible separators
                    tag_list = []
                    # Check for pipe separator
                    if '|' in tag_text:
                        tag_list = [t.strip() for t in tag_text.split('|') if t.strip()]
                    # Check for comma separator as fallback
                    elif ',' in tag_text:
                        tag_list = [t.strip() for t in tag_text.split(',') if t.strip()]
                    # Use whitespace as last resort if no other separators found
                    elif tag_text and not any(sep in tag_text for sep in ['|', ',']):
                        tag_list = [t.strip() for t in tag_text.split() if t.strip()]
                    # If there are no separators but text exists, it's a single tag
                    elif tag_text:
                        tag_list = [tag_text]
                    
                    # Filter and standardize tags
                    valid_task_tags = []
                    for tag in tag_list:
                        # Check if the tag exists (case-insensitive)
                        if tag.lower() in valid_tags_lookup:
                            # Use the version from the database to maintain consistent casing
                            valid_task_tags.append(valid_tags_lookup[tag.lower()])
                    
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


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
