from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from ui import (
    SmallOverlayWindow,
    CompletedTasksWindow,
    EditTaskWindow,
    CommitHistoryWindow,
    AddTaskWindow,
    CurrentTaskWindow
)
import sqlite3

#Global Variables
blue_background_color = "#5DADE2"
grey_button_color = "#d3d3d3"
green_button_color = "#77DD77"
red_button_color = "#FF7276"
scroll_trough_color = "E0E0E0"


# Database Functions
def create_connection():
    conn = sqlite3.connect('task_manager.db')
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

#Create the tasklist table
    cursor.execute("""CREATE TABLE TaskList
          task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
          task_name TEXT NOT NULL,
          task_description TEXT,
          completion_date TEXT,
          task_tags TEXT,
          task_weight INTEGER NOT NULL DEFAULT 1,
          current_time INTEGER NOT NULL DEFAULT 0,
          task_status TEXT NOT NULL DEFAULT 'Incomplete'
"""
)

    cursor.execute("""CREATE TABLE CompletedTasks
          task_id INTEGER PRIMARY KEY, 
          task_name TEXT NOT NULL,
          task_description TEXT,
          completion_date TEXT,
          current_time INTEGER NOT NULL DEFAULT 0,
          task_status TEXT NOT NULL DEFAULT 'Completed'
"""
)
    
    cursor.execute("""CREATE TABLE CurrentTask
          task_id INTEGER PRIMARY KEY,
          task_name TEXT NOT NULL,
          task_description TEXT,
          completion_date TEXT,
          task_tags TEXT,
          task_weight INTEGER NOT NULL DEFAULT 1,
          current_time INTEGER NOT NULL DEFAULT 0,
          task_status TEXT NOT NULL DEFAULT 'Incomplete'
"""
)
    conn.commit()
    conn.close()


def add_task_to_db(title, description, tags):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO TaskList (title, description, tags) VALUES (?, ?, ?)' (title, description, tags))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Task added successfully.")

def list_tasks_from_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TaskList')
    TaskList = cursor.fetchall()
    conn.close
    return TaskList

def complete_task_in_db(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TaskList WHERE task_id = ?', (task_id))
    task = cursor.fetchone()
    if task:
      cursor.execute('INSERT INTO CompletedTasks (title, description, completion_date, time_spent, task_weight) VALUES (?, ?, datetime("now"),?)', (task[1], task[2], task[4]))
      cursor.execute('DELETE FROM TaskList WHERE id = ?', (task_id))
      conn.commit()
      messagebox.showinfo("Success", "Task completed and moved to CompletedTasks.")
    else:
      messagebox.showerror("Error", "Task not found.")
    conn.close()
def get_current_time():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT current_time FROM CurrentTask', (current_task_time))
    current_task_time = cursor.fetchone()
    return current_task_time


#GUI Functions

def add_task():
    title = title_entry.get()
    description = description_entry.get()
    weight = weight_entry.get()
    if title:
      add_task_db(title, description)
      title_entry.delete(0, tk.END)
      description_entry.delete(0, tk.END)
      update_task_list()
    else:
      messagebox.showwarning("Input Error", "Please enter a task title.")

def update_task_list():
    task_list.delete(0, tk.END)
    TaskList = list_tasks_from_db
    for task in TaskList:
      task_list.insert(tk.END, f"ID: {task[0]}, Title: {task[1]}, Status: {task[3]}, Time Spent: {task[4]}")

def complete_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
      task_id = int(selected_task.split(',')[0].split(': ')[1])
      complete_task_in_db(task_id)
      update_task_list()
    else:
      messagebox.showwarning("Selection Error", "Please select a task to complete.")

class App:
    def __init__(self,root):
      self.root = root
      self.root.title("Task Manager")
      self.root.geometry("600x600")
      root.resizable(width = 0, height = 0)

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

      get_current_time()
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


    def setup_smalloverlay_page(self, current_task_time):
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
      self.time_box.grid(row = 1, columd = 0, padx = 50, pady = 5, sticky = E)
      #Set the timer text to the current time
      self.time_box_overlay.insert("1.0", current_task_time)
      #Make the time box Read-Only
      self.time_box.config(state = DISABLED)
   
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
    #def setup_full_page(self):
       
    #def insert_task(self, task_id):
       
    #def setup_completedtasks_page(self):
       
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