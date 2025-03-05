from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import pathlib
import sqlite3
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)

background_color = "#A9A9A9"
green_btn_color = "#b2fba5"

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

        conn.commit()
        conn.close()

        # Create a database or connect to an existing database
        conn = sqlite3.connect(path)

        # Create a cursor instance
        c = conn.cursor()

        c.execute("SELECT task_weight FROM CompletedTasks ")  # Fetch task_time from completed tasks database
        comps = c.fetchall()
        global complexity
        complexity = []

        # Add data to the list
        for comp in comps:
            complexity.append(comp[0])

        conn.commit()
        conn.close()


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
        content_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Left column
        self.left_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        self.left_frame.grid(row=0, column=0, padx=(0, 0), sticky='nsew')
        # Right column
        self.right_frame = ttk.Frame(content_frame, style='MainFrame.TFrame')
        self.right_frame.grid(row=0, column=1, padx=(0, 0), sticky='nsew')

        # Label for total task time
        label = ttk.Label(self.left_frame, text="Total Task Time:", font=self.fonts['subheader'], style='TLabel')
        label.grid(row=0, column=0, sticky='w')

        label_total = ttk.Label(self.left_frame, font=self.fonts['subheader'], style='TLabel')
        label_total.grid(row=1, column=0, sticky='w')
        total = self.total_Time(values)
        label_total.configure(text=total)

        # Complexity types and values
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]
        self.graphs = ["Time vs Weight"]

        # Label for complexity type selection
        self.label = ttk.Label(self.left_frame, text="Choose a Time Complexity Type:", font=self.fonts['subheader'], style='TLabel')
        self.label.grid(row=3, column=0, sticky='w')

        self.type_combo = ttk.Combobox(self.left_frame, values=self.complexity_types, style='TCombobox', state='readonly')
        self.type_combo.grid(row=4, column=0, sticky='ew', pady=(0, 3))
        self.type_combo.set("Select Type")

        # Label for complexity value selection
        self.label = ttk.Label(self.left_frame, text="Choose a Time Complexity Value:", font=self.fonts['subheader'], style='TLabel')
        self.label.grid(row=5, column=0, sticky='w')

        self.value_combo = ttk.Combobox(self.left_frame, state='readonly')
        self.value_combo.grid(row=6, column=0, sticky='ew')
        self.value_combo.set("Select Value")

        # Update the values in the second combobox based on the first one
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)
        
        # Label that shows the time spent for the selected value
        self.label_time_spent = ttk.Label(self.left_frame, text="Total Time Spent on:", font=self.fonts['subheader'], style='TLabel')
        self.label_time_spent.grid(row=7, column=0, sticky='w')

        # Label that shows the time spent for the selected value
        self.label_time_com = ttk.Label(self.left_frame, text="", font=self.fonts['subheader'], style='TLabel')
        self.label_time_com.grid(row=8, column=0, sticky='w')

        self.label_time_maxS = ttk.Label(self.left_frame, text="Max Time Spent on:", font=self.fonts['subheader'], style='TLabel')
        self.label_time_maxS.grid(row=9, column=0, sticky='w')

        self.label_time_max = ttk.Label(self.left_frame, text="", font=self.fonts['subheader'], style='TLabel')
        self.label_time_max.grid(row=10, column=0, sticky='w')

        self.label_time_minS = ttk.Label(self.left_frame, text="Min Time Spent on:", font=self.fonts['subheader'], style='TLabel')
        self.label_time_minS.grid(row=11, column=0, sticky='w')

        self.label_time_min = ttk.Label(self.left_frame, text="", font=self.fonts['subheader'], style='TLabel')
        self.label_time_min.grid(row=12, column=0, sticky='w')

        self.label_time_avgS = ttk.Label(self.left_frame, text="Average Time Spent on:", font=self.fonts['subheader'], style='TLabel')
        self.label_time_avgS.grid(row=13, column=0, sticky='w')

        self.label_time_avg = ttk.Label(self.left_frame, text="", font=self.fonts['subheader'], style='TLabel')
        self.label_time_avg.grid(row=14, column=0, sticky='w')

        self.graph_combo = ttk.Combobox(self.left_frame, state='readonly',values=self.graphs)
        self.graph_combo.grid(row=15, column=0, sticky='ew')
        self.graph_combo.set("Select Graph")

        self.graphs_btn = tk.Button(self.left_frame, font=("SF Pro Text", 10),text="Plot Graph", command=self.plot_graph, bg=green_btn_color)
        self.graphs_btn.grid(row=16, column=0,padx=(0,0),pady=(0,0),sticky='w')

        # Bind the value_combo to update the label text when a value is selected
        self.value_combo.bind('<<ComboboxSelected>>', self.update_time_spent_label)

    def plot_graph(self):
        selected_graph = self.graph_combo.get()
        if selected_graph == "Time vs Weight":
            # the figure that will contain the plot 
            fig = Figure(figsize = (5, 5), 
                        dpi = 100) 
        
            # list of squares 
            y = [i**2 for i in range(101)] 
        
            # adding the subplot 
            plot1 = fig.add_subplot(111) 
        
            # plotting the graph 
            plot1.plot(y) 
        
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig, 
                                    master = self.right_frame)   
            canvas.draw() 
        
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().grid(row=0, column=0, sticky='ew',padx=(25,0)) 
        
            # creating the Matplotlib toolbar 
            toolbar = NavigationToolbar2Tk(canvas, 
                                        self.right_frame) 
            toolbar.update() 
        
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().grid(row=0, column=0, sticky='ew',padx=(25,0))

    def total_Time(self,times):

        if not times or times == []:
            return "00:00:00"
        value = times
        total_h = 0
        total_m = 0
        total_s = 0
        for time in value:
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
        selected_comp = self.type_combo.get()
        
        if selected_value != "Select Value":  # Ensure a valid value is selected
            # Update the labels to reflect the selected value
            self.label_time_spent.configure(text=f"Total Time Spent on {selected_comp}({selected_value}):")
            self.label_time_maxS.configure(text=f"Max Time Spent on {selected_comp}({selected_value}):")
            self.label_time_minS.configure(text=f"Min Time Spent on {selected_comp}({selected_value}):")
            self.label_time_avgS.configure(text=f"Average Time Spent on {selected_comp}({selected_value}):")

            # Call update_time_comp() and update the corresponding labels with the results
            time_total,max,min,avg  = self.update_time_comp()
            
            # Update labels with the computed values
            self.label_time_com.configure(text=time_total)
            self.label_time_max.configure(text=max)
            self.label_time_min.configure(text=min)
            self.label_time_avg.configure(text=avg)

        else:
            # Reset the labels if no value is selected
            self.label_time_spent.configure(text="Total Time Spent on:")
            self.label_time_maxS.configure(text="Max Time Spent on:")
            self.label_time_minS.configure(text="Min Time Spent on:")
            self.label_time_avgS.configure(text="Average Time Spent on:")
            
            # Clear the label contents
            self.label_time_com.configure(text="")
            self.label_time_max.configure(text="")
            self.label_time_min.configure(text="")
            self.label_time_avg.configure(text="")

    def max_time(self, arr):
        # Convert each time string (hh:mm:ss) into total seconds

        if not arr or arr == []:
            return "00:00:00"
        max_time_in_seconds = 0
        max_index = 0
        
        for i in range(len(arr)):
            # Split the time string into hours, minutes, and seconds
            h, m, s = map(int, arr[i].split(':'))
            
            # Convert the time into total seconds
            total_seconds = h * 3600 + m * 60 + s
            
            # Find the maximum time by comparing the total seconds
            if total_seconds > max_time_in_seconds:
                max_time_in_seconds = total_seconds
                max_index = i
                
        # Return the index of the maximum time
        return arr[max_index]
    
    def min_time(self,arr):

        if not arr or arr == []:
            return "00:00:00"
        # Convert each time string (hh:mm:ss) into total seconds
        min_time_in_seconds = float('inf') 
        min_index = 0
        
        for i in range(len(arr)):
            # Split the time string into hours, minutes, and seconds
            h, m, s = map(int, arr[i].split(':'))
            
            # Convert the time into total seconds
            total_seconds = h * 3600 + m * 60 + s
            
            # Find the minimum time by comparing the total seconds
            if total_seconds < min_time_in_seconds:
                min_time_in_seconds = total_seconds
                min_index = i
            
        # Return the index of the minimum time
        return arr[min_index]
    
    def avg_time(self,arr):
        if not arr or arr == []:
            return "00:00:00" 
        
        total_seconds = 0
        for time in arr:
            # Split the time string into hours, minutes, and seconds
            h, m, s = map(int, time.split(':'))
            
            # Convert the time into total seconds
            total_seconds += h * 3600 + m * 60 + s
        
        # Calculate the average in seconds
        avg_seconds = total_seconds / len(arr)
        
        # Convert the average seconds back to hh:mm:ss
        avg_h = int(avg_seconds / 3600)
        avg_m = int((avg_seconds % 3600) / 60)
        avg_s = int(avg_seconds % 60)
        
        # Format the result into hh:mm:ss
        if avg_h == 0 or avg_h < 9:
            avg_h = "0" + str(avg_h)
        if avg_m == 0 or avg_m < 9:
            avg_m = "0" + str(avg_m)
        if avg_s == 0 or avg_s < 9:
            avg_s = "0" + str(avg_s)

        avg_time_str = str(avg_h) + ":" + str(avg_m) + ":" + str(avg_s)
        return avg_time_str

    def update_time_comp(self):
        newTime = []
        newComp = []
        for i in range(len(complexity)):
            if complexity[i] == self.value_combo.get():
                newComp.append(complexity[i])
                newTime.append(values[i])

        total = self.total_Time(newTime)
        max = self.max_time(newTime)
        min = self.min_time(newTime)
        avg = self.avg_time(newTime)

        return total,max,min,avg

            