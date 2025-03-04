from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
import csv
from tkinter import messagebox
import pathlib

background_color = "#A9A9A9"
green_btn_color = "#b2fba5"
org_btn_color = "#e99e56"

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("Analytics.py", '') + '\\Databases' + '\\task_list.db'

class AnalyticsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # DATABASE SECTION ####################################################

        # Create a database or connect to an existing database
        conn = sqlite3.connect(path)

        # Create a cursor instance
        c = conn.cursor()

        c.execute("SELECT task_time FROM CompletedTasks ")  # Fetch task_time from completed tasks database
        times = c.fetchall()
        global values
        values = []

        # Add data to the list
        for time in times:
            values.append(time[0])

        # END OF DATABASE SECTION ##############################################

        # Set the main window 
        self.configure(bg=background_color)

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=14, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=10, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }

        # Style configurations
        style = ttk.Style(self)
        style.theme_use("alt")  
        style.configure('Input.TEntry', fieldbackground=background_color, font=("SF Pro Text", 10))
        style.configure('TLabel', background=background_color, font=("SF Pro Text", 10))  
        style.configure('TButton', background=background_color, font=("SF Pro Text", 10))
        style.configure('MainFrame.TFrame', background=background_color)

        # Main container
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        # Content container
        content_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        content_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        # Left column
        left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        left_frame.grid(row=0, column=0, padx=(0, 8), sticky='nsew')

        # Label for total task time
        label = ttk.Label(left_frame, text="Total Task Time:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w')

        label_total = ttk.Label(left_frame, font=self.fonts['subheader'], style='TLabel')
        label_total.grid(row=1, column=0, sticky='w')
        total = self.total_Time()
        label_total.configure(text=total)

        # Complexity types and values
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]

        # Label for complexity type selection
        label = ttk.Label(left_frame, text="Choose a Time Complexity Type:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=3, column=0, sticky='w')

        self.type_combo = ttk.Combobox(left_frame, values=self.complexity_types, style='TCombobox', state='readonly')
        self.type_combo.grid(row=4, column=0, sticky='ew', pady=(0, 3))
        self.type_combo.set("Select Type")

        # Label for complexity value selection
        label = ttk.Label(left_frame, text="Choose a Time Complexity Value:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=5, column=0, sticky='w')

        self.value_combo = ttk.Combobox(left_frame, state='readonly')
        self.value_combo.grid(row=6, column=0, sticky='ew')
        self.value_combo.set("Select Value")

        # Update the values in the second combobox based on the first one
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)

        # Label that shows the time spent for the selected value
        self.label_time_spent = ttk.Label(left_frame, text="Total Time Spent on:", font=self.fonts['subheader'], style='TLabel')
        self.label_time_spent.grid(row=7, column=0, sticky='w')

        # Label that shows the time spent for the selected value
        self.label_time_com = ttk.Label(left_frame, text="Placeholder", font=self.fonts['subheader'], style='TLabel')
        self.label_time_com.grid(row=8, column=0, sticky='w')

        # Bind the value_combo to update the label text when a value is selected
        self.value_combo.bind('<<ComboboxSelected>>', self.update_time_spent_label)

    def total_Time(self):
        total_h = 0
        total_m = 0
        total_s = 0
        for time in values:
            h, m, s = map(int, time.split(':'))
            total_h += h
            total_m += m
            total_s += s
            if total_s >= 60:
                total_m += int(total_s / 60)
                total_s = total_s % 60
            if total_m >= 60:
                total_h += int(total_m / 60)
                total_m = total_m % 60
        if total_h == 0 or total_h < 9:
            total_h = "0" + str(total_h)
        if total_m == 0 or total_m < 9:
            total_m = "0" + str(total_m)
        if total_s == 0 or total_s < 9:
            total_s = "0" + str(total_s)

        total = str(total_h) + ":" + str(total_m) + ":" + str(total_s)
        return total

    def update_values(self, event=None):
        """This function updates the values in the second combobox based on the first one"""
        selected_type = self.type_combo.get()
        if selected_type == "T-Shirt Size":
            self.value_combo['values'] = self.tshirt_sizes
        elif selected_type == "Fibonacci":
            self.value_combo['values'] = self.fibonacci
        else:
            self.value_combo['values'] = []
        self.value_combo.set("Select Value")

    def update_time_spent_label(self, event=None):
        """This function updates the label with the selected value from value_combo"""
        selected_value = self.value_combo.get()
        if selected_value != "Select Value":
            self.label_time_spent.configure(text=f"Total Time Spent on {selected_value}:")
        else:
            self.label_time_spent.configure(text="Total Time Spent on:")