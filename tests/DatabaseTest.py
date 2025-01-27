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


#Global Variables
blue_background_color = "#5DADE2"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "E0E0E0"





class App:
    def __init__(self, root):
      self.root = root
      self.root.title("Task Manager")
      self.root.geometry("800x600")
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

      self.setup_full_page()
      self.setup_completedtasks_page()
      self.setup_smalloverlay_page()

    def show_menu(self):
        try:
            self.popup_menu.tk_popup(
                self.menu_button.winfo_rootx(),
                self.menu_button.winfo_rooty() + self.menu_button.winfo_height()
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

    def setup_full_page(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
        background = blue_background_color,
        foreground = blue_background_color,
        rowheight = 25,
        fieldbackground = grey_button_color)

        #Current Task Frame
        currenttask_frame = tk.Frame(self.full_page)
        currenttask_frame.pack(pady=10, side = TOP)

        label = ttk.Label(currenttask_frame, text = "Task Name", font = ['Title_tuple'])
        label.pack(anchor = W)

        #Change color when a item is selected
        style.map("Treeview",
        background = [('selected', "347083")])

        #Put the task list inside a frame
        tasklist_frame = ttk.Frame(self.full_page, style = "Treeview")
        tasklist_frame.pack(pady=10, side = BOTTOM)

        #Create scrollbar
        tasklist_scroll = Scrollbar(tasklist_frame)
        tasklist_scroll.pack(side = RIGHT, fill = Y)

        #Set scrollbar
        task_list = ttk.Treeview(tasklist_frame, yscrollcommand=tasklist_scroll.set, selectmode = "extended")
        task_list.pack()

        #Task List is vertical scroll
        tasklist_scroll.config(command = task_list.yview)

        #Format columns
        task_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID")
        task_list.column("#0", width = 0, stretch=NO)
        task_list.column('Task Name', anchor = W, width = 250)
        task_list.column('Task Time', anchor = CENTER, width = 100)
        task_list.column('Task Weight', anchor = CENTER, width =100)
        task_list.column('Task ID',anchor = CENTER, width = 100)


        task_list.heading("#0", text = "", anchor = W)
        task_list.heading("Task Name", text = "Task Name", anchor = W)
        task_list.heading("Task Time", text = "Time", anchor = CENTER)
        task_list.heading("Task Weight", text = "Weight", anchor = CENTER)
        task_list.heading("Task ID", text = "ID", anchor = CENTER)

        data = [
            ["Collect money", "00:14:35", "5", "1"],
            ["Print paper", "00:30:21", "3", "2"]
        ]

        task_list.tag_configure('oddrow', background=  "white")
        task_list.tag_configure('evenrow', background=  grey_button_color)

        #Add data to screen
        global count
        count = 0

        for record in data:
            if count % 2 == 0:
                task_list.insert(parent = '', index = 'end', iid = count, text = '', values = (record[0],record[1],record[2],record[3]), tags = ('evenrow', ""))
            else:
                task_list.insert(parent = '', index = 'end', iid = count, text = '', values = (record[0],record[1],record[2],record[3]), tags = ('oddrow', ""))
            #Increment count
            count += 1

        data_frame = LabelFrame(root, text = "Input")
        data_frame.pack(fill = "x", expand = YES, padx = 20)

        tn_label = Label(data_frame, text = "Task Name")
        tn_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        tn_entry = Entry(data_frame)
        tn_entry.grid(row = 1, column = 0)

        tt_label = Label(data_frame, text = "Task Time")
        tt_label.grid(row = 0, column = 1, padx = 10, pady = 10)
        tt_entry = Entry(data_frame)
        tt_entry.grid(row = 1, column = 1)

        tw_label = Label(data_frame, text = "Task Weight")
        tw_label.grid(row = 0, column = 2, padx = 10, pady = 10)
        tw_entry = Entry(data_frame)
        tw_entry.grid(row = 1, column = 2)

        ti_label = Label(data_frame, text = "Task ID")
        ti_label.grid(row = 0, column = 3, padx = 10, pady = 10)
        ti_entry = Entry(data_frame)
        ti_entry.grid(row = 1, column = 3)

        button_frame = LabelFrame(root, text = "Commands")
        button_frame.pack(fill = "x", expand = YES, padx = 20,side = BOTTOM)


        update_button = Button(button_frame, text = "Update Record")
        update_button.grid(row = 0, column = 0, padx = 6, pady = 10)

        add_button = Button(button_frame, text = "Add Task")
        add_button.grid(row = 0, column = 1, padx = 6, pady = 10)

        remove_button = Button(button_frame, text = "Remove Task")
        remove_button.grid(row = 0, column = 2, padx = 6, pady = 10)

        remove_all_button = Button(button_frame, text = "Remove All")
        remove_all_button.grid(row = 0, column = 3, padx = 6, pady = 10)

        moveup_button = Button(button_frame, text = "Move Up")
        moveup_button.grid(row = 0, column = 4, padx = 6, pady = 10)

        movedown_button = Button(button_frame, text = "Move Down")
        movedown_button.grid(row = 0, column = 5, padx = 6, pady = 10)

        tags_button = Button(button_frame, text = "Tags")
        tags_button.grid(row = 0, column = 6, padx = 6, pady = 10)

        select_record_button = Button(button_frame, text = "Select Record")
        select_record_button.grid(row = 0, column = 7, padx = 6, pady = 10)



       
    #def insert_task(self, task_id):
       
    def setup_completedtasks_page(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
        background = grey_button_color,
        foreground = blue_background_color,
        rowheight = 25,
        fieldbackground = grey_button_color)

        #Change color when a item is selected
        style.map("Treeview",
        background = [('selected', "347083")])

        #Put the task list inside a frame
        completedlist_frame = Frame(self.completedtasks_page)
        completedlist_frame.pack(pady=10)

        #Create scrollbar
        completedlist_scroll = Scrollbar(completedlist_frame)
        completedlist_scroll.pack(side = RIGHT, fill = Y)

        #Set scrollbar
        completed_list = ttk.Treeview(completedlist_frame, yscrollcommand=completedlist_scroll.set, selectmode = "extended")
        completed_list.pack()

        #Task List is vertical scroll
        completedlist_scroll.config(command = completed_list.yview)

        #Format columns
        completed_list['columns'] = ("Task Name", "Task Time", "Task Weight", "Task ID")
        completed_list.column("#0", width = 0, stretch=NO)
        completed_list.column('Task Name', anchor = W, width = 150)
        completed_list.column('Task Time', anchor = CENTER, width = 50)
        completed_list.column('Task Weight', anchor = CENTER, width =25)
        completed_list.column('Task ID',anchor = CENTER, width = 25)


        completed_list.heading("#0", text = "", anchor = W)
        completed_list.heading("Task Name", text = "Task Name", anchor = W)
        completed_list.heading("Task Time", text = "Time", anchor = CENTER)
        completed_list.heading("Task Weight", text = "Weight", anchor = CENTER)
        completed_list.heading("Task ID", text = "ID", anchor = CENTER)
       
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
        self.task_window = EditTaskWindow()
        self.task_window.grab_set()

    def open_CurrentTaskWindow(self):
        self.task_window = CurrentTaskWindow()
        self.task_window.grab_set()

    def select_record(tn_entry, tt_entry, ti_entry, tw_entry, task_list):
        #Clear entry boxes
        tn_entry.delete(0)
        tt_entry.delete(0)
        ti_entry.delete(0)
        tw_entry.delete(0)

        #Grab record number
        selected = task_list.focus()

        #Grab record values
        values = task_list.item(selected, values)


        return tn_entry, tt_entry, ti_entry, tw_entry

    
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
