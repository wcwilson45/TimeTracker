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
frame_bg_color = "#dcdcdc"

global path 
path = pathlib.Path(__file__).parent
path = str(path).replace("Analytics.py", '') + '\\Databases' + '\\task_list.db'

class AnalyticsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.load_data()

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
        style.configure('TLabel', background=frame_bg_color, font=("SF Pro Text", 10))  
        style.configure('TButton', background=background_color, font=("SF Pro Text", 10))
        style.configure('MainFrame.TFrame', background=background_color)
        style.configure('TLabelframe', background=frame_bg_color)
        style.configure('TLabelframe.Label', background=frame_bg_color, font=("SF Pro Display", 10, "bold"))

        # Main container
        main_frame = tk.Frame(self, bg=background_color)
        main_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        # Content container
        content_frame = tk.Frame(main_frame, bg=background_color)
        content_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Configure grid weights to ensure proper expansion
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left column
        self.left_frame = tk.Frame(content_frame, bg=background_color)
        self.left_frame.grid(row=0, column=0, padx=(0, 10), sticky='n')
        
        # Right column
        self.right_frame = tk.Frame(content_frame, bg=background_color)
        self.right_frame.grid(row=0, column=1, padx=(0, 0), sticky='n')

        # Complexity types and values
        self.complexity_types = ["T-Shirt Size", "Fibonacci"]
        self.tshirt_sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.fibonacci = ["1", "2", "3", "5", "7", "11", "13"]
        self.graphs = ["Time vs Fibonacci", "Time vs T-Shirt Size", "BoxPlot(Fib)", "BoxPlot(T-Shirt)", "Pie Chart - Fibonacci", "Pie Chart - T-Shirt Size"]
        self.models = ["WIP"]

        # ================ FRAME 1: General Information ================
        general_frame = ttk.LabelFrame(self.left_frame, text="General Information")
        general_frame.grid(row=0, column=0, sticky='new', pady=(5, 10), padx=5)
        general_frame.configure(style='TLabelframe')

        # Label for total task time
        total_time_label = ttk.Label(general_frame, text="Total Task Time:", font=self.fonts['subheader'])
        total_time_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.total_time_value = ttk.Label(general_frame, font=self.fonts['subheader'])
        self.total_time_value.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.update_total_time()

        # Label for complexity type selection
        type_label = ttk.Label(general_frame, text="Choose a Time Complexity Type:", font=self.fonts['subheader'])
        type_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.type_combo = ttk.Combobox(general_frame, values=self.complexity_types, state='readonly')
        self.type_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.type_combo.set("Select Type")

        # Label for complexity value selection
        value_label = ttk.Label(general_frame, text="Choose a Time Complexity Value:", font=self.fonts['subheader'])
        value_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)

        self.value_combo = ttk.Combobox(general_frame, state='readonly')
        self.value_combo.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        self.value_combo.set("Select Value")

        # Update the values in the second combobox based on the first one
        self.type_combo.bind('<<ComboboxSelected>>', self.update_values)
        
        # ================ FRAME 2: Time Analysis ================
        analysis_frame = ttk.LabelFrame(self.left_frame, text="Time Analysis")
        analysis_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10), padx=5)
        analysis_frame.configure(style='TLabelframe')

        # Label that shows the time spent for the selected value
        self.label_time_spent = ttk.Label(analysis_frame, text="Total Time Spent on:", font=self.fonts['subheader'])
        self.label_time_spent.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.label_time_com = ttk.Label(analysis_frame, text="", font=self.fonts['subheader'])
        self.label_time_com.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        self.label_time_maxS = ttk.Label(analysis_frame, text="Max Time Spent on:", font=self.fonts['subheader'])
        self.label_time_maxS.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.label_time_max = ttk.Label(analysis_frame, text="", font=self.fonts['subheader'])
        self.label_time_max.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        self.label_time_minS = ttk.Label(analysis_frame, text="Min Time Spent on:", font=self.fonts['subheader'])
        self.label_time_minS.grid(row=2, column=0, sticky='w', padx=5, pady=5)

        self.label_time_min = ttk.Label(analysis_frame, text="", font=self.fonts['subheader'])
        self.label_time_min.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        self.label_time_avgS = ttk.Label(analysis_frame, text="Average Time Spent on:", font=self.fonts['subheader'])
        self.label_time_avgS.grid(row=3, column=0, sticky='w', padx=5, pady=5)

        self.label_time_avg = ttk.Label(analysis_frame, text="", font=self.fonts['subheader'])
        self.label_time_avg.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        # ================ FRAME 3: Graph Options ================
        graph_frame = ttk.LabelFrame(self.left_frame, text="Graph Options")
        graph_frame.grid(row=2, column=0, sticky='ew', pady=(0, 10), padx=5)
        graph_frame.configure(style='TLabelframe')

        # Graph selection
        graph_label = ttk.Label(graph_frame, text="Select Graph Type:", font=self.fonts['subheader'])
        graph_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.graph_combo = ttk.Combobox(graph_frame, state='readonly', values=self.graphs)
        self.graph_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.graph_combo.set("Select Graph")

        # Plot button
        self.graphs_btn = tk.Button(graph_frame, font=("SF Pro Text", 10), text="Plot Graph", 
                                    command=self.plot_graph, bg=green_btn_color)
        self.graphs_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Bind the value_combo to update the label text when a value is selected
        self.value_combo.bind('<<ComboboxSelected>>', self.update_time_spent_label)

        # ================ FRAME 3: Model Options ================
        model_frame = ttk.LabelFrame(self.left_frame, text="Model Options")
        model_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10), padx=5)
        model_frame.configure(style='TLabelframe')

        # Graph selection
        graph_label = ttk.Label(model_frame, text="Select Model:", font=self.fonts['subheader'])
        graph_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.model_combo = ttk.Combobox(model_frame, state='readonly', values=self.models)
        self.model_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.model_combo.set("Select Model")

        # Plot button
        self.model_btn = tk.Button(model_frame, font=("SF Pro Text", 10), text="Plot Model", 
                                    bg=green_btn_color)
        self.model_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        
    def plot_graph(self):
        # Reload data 
        self.load_data()

        # Grabs the graph the user selected
        selected_graph = self.graph_combo.get()
        
        # Clear any existing widgets in the right frame (common to all graph types)
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        # Create a frame to contain the graph (common to all graph types)
        graph_container = ttk.LabelFrame(self.right_frame, text="Graphs")
        graph_container.grid(row=0, column=0, sticky='new', padx=(0, 10), pady=5)
        graph_container.configure(style='TLabelframe')
        
        # Checks to see what Graph it is with chain of if Statements
        if selected_graph == "Time vs Fibonacci":
            # Collect time data for each Fibonacci weight
            time_arrays = {
                "1": [], "2": [], "3": [], "5": [], "7": [], "11": [], "13": []
            }
            
            # Uses Empty Arrays to find all the times for that complexity group
            for i in range(len(complexity)):
                weight = complexity[i]
                if weight in time_arrays:
                    time_arrays[weight].append(values[i])
            
            # Gets there average times
            avgTime = [self.avg_time(time_arrays[w]) for w in ["1", "2", "3", "5", "7", "11", "13"]]
            
            # Makes it into total seconds
            avgTimeSec = []
            for time in avgTime:
                # Split the time string into hours, minutes, and seconds
                h, m, s = map(int, time.split(':'))
                # Convert the time into total seconds
                avgTimeSec.append(h * 3600 + m * 60 + s)
            
            # Create the figure
            fig = Figure(figsize=(5, 4), dpi=100, facecolor='none')
            
            # Adding the subplot
            plot1 = fig.add_subplot(111)
            
            # Set labels and title
            plot1.set_xlabel('Task Weight')
            plot1.set_ylabel('Time (seconds)')
            plot1.set_title('Task Time vs Weight')
                
            # Plot the data
            plot1.bar(self.fibonacci, avgTimeSec)

        elif selected_graph == "Time vs T-Shirt Size":
            # Collect time data for each T-shirt size
            time_arrays = {
                "XXS": [], "XS": [], "S": [], "M": [], "L": [], "XL": [], "XXL": []
            }
            
            # Uses Empty Arrays to find all the times for that complexity group
            for i in range(len(complexity)):
                size = complexity[i]
                if size in time_arrays:
                    time_arrays[size].append(values[i])
            
            # Gets average time for all time values
            avgTime = [self.avg_time(time_arrays[s]) for s in ["XXS", "XS", "S", "M", "L", "XL", "XXL"]]
            
            # Makes it total seconds
            avgTimeSec = []
            for time in avgTime:
                # Split the time string into hours, minutes, and seconds
                h, m, s = map(int, time.split(':'))
                # Convert the time into total seconds
                avgTimeSec.append(h * 3600 + m * 60 + s)
            
            # Create the figure
            fig = Figure(figsize=(5, 4), dpi=100, facecolor='none')
            
            # Adding the subplot
            plot1 = fig.add_subplot(111)
            
            # Set labels and title
            plot1.set_xlabel('Task Weight')
            plot1.set_ylabel('Time (seconds)')
            plot1.set_title('Task Time vs Weight')
            
            # Plot the data
            plot1.bar(self.tshirt_sizes, avgTimeSec)

        elif selected_graph == "BoxPlot(Fib)":
            # Collect time data for each Fibonacci weight
            time_arrays = {
                "1": [], "2": [], "3": [], "5": [], "7": [], "11": [], "13": []
            }
            
            # Uses Empty Arrays to find all the times for that complexity group
            for i in range(len(complexity)):
                weight = complexity[i]
                if weight in time_arrays:
                    time_arrays[weight].append(values[i])
            
            # Convert the string times to seconds for each complexity level
            time_data = []
            for weight in ["1", "2", "3", "5", "7", "11", "13"]:
                time_data.append([self.time_to_seconds(t) for t in time_arrays[weight]])
            
            # Create the figure
            fig = Figure(figsize=(5, 4), dpi=100, facecolor='none')
            
            # Adding the subplot
            plot1 = fig.add_subplot(111)

            # Set labels and title
            plot1.set_title('BoxPlot(Fib)')
            plot1.set_xlabel('Task Weight')
            plot1.set_ylabel('Time (seconds)')
            
            # Plot the data
            plot1.boxplot(time_data, labels=self.fibonacci)

        elif selected_graph == "BoxPlot(T-Shirt)":
            # Collect time data for each T-shirt size
            time_arrays = {
                "XXS": [], "XS": [], "S": [], "M": [], "L": [], "XL": [], "XXL": []
            }
            
            # Uses Empty Arrays to find all the times for that complexity group
            for i in range(len(complexity)):
                size = complexity[i]
                if size in time_arrays:
                    time_arrays[size].append(values[i])
            
            # Convert the string times to seconds for each complexity level
            time_data = []
            for size in ["XXS", "XS", "S", "M", "L", "XL", "XXL"]:
                time_data.append([self.time_to_seconds(t) for t in time_arrays[size]])
            
            # Create the figure
            fig = Figure(figsize=(6, 4), dpi=100, facecolor='none')
            
            # Adding the subplot
            plot1 = fig.add_subplot(111)

            # Set labels and title
            plot1.set_title('BoxPlot(T-Shirt)')
            plot1.set_xlabel('Task Weight')
            plot1.set_ylabel('Time (seconds)')
            
            # Plot the data
            plot1.boxplot(time_data, labels=self.tshirt_sizes)

        elif selected_graph == "Pie Chart - Fibonacci":
            # Create the figure
            fig = Figure(figsize=(5, 4), dpi=100, facecolor='none')
            
            # New pie chart for Fibonacci weights
            total_times = self.get_total_time_by_fibonacci()
            labels = []
            sizes = []
            
            for weight, time_seconds in total_times.items():
                # Only include weights that have data
                if time_seconds > 0:
                    labels.append(weight)
                    sizes.append(time_seconds)
            
            # Adding the subplot
            plot1 = fig.add_subplot(111)
            plot1.set_facecolor('none')
            
            # Set title
            plot1.set_title('Time Distribution by Fibonacci Weight')
            
            # Create an explode array of the same length as labels
            explode = [0.05] * len(labels)
            
            # Plot the data
            wedges, texts, autotexts = plot1.pie(
                sizes, 
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                shadow=False,
                explode=explode
            )
            
            # Set font size for better readability using the Figure methods
            for autotext in autotexts:
                autotext.set_size(8)
                autotext.set_weight('bold')
            
            for text in texts:
                text.set_size(9)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            plot1.axis('equal')
            fig.tight_layout()

        elif selected_graph == "Pie Chart - T-Shirt Size":
            # Create the figure
            fig = Figure(figsize=(5, 4), dpi=100, facecolor='none')
            
            # New pie chart for T-shirt size weights
            total_times = self.get_total_time_by_tshirt()
            labels = []
            sizes = []
            
            for weight, time_seconds in total_times.items():
                # Only include weights that have data
                if time_seconds > 0:
                    labels.append(weight)
                    sizes.append(time_seconds)
            
            # Adding the subplot
            plot1 = fig.add_subplot(111)
            
            # Set title
            plot1.set_title('Time Distribution by T-Shirt Size')
            
            # Create an explode array of the same length as labels
            explode = [0.05] * len(labels)
            
            # Plot the data
            wedges, texts, autotexts = plot1.pie(
                sizes, 
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                shadow=False,
                explode=explode
            )
            
            # Set font size for better readability using the Figure methods
            for autotext in autotexts:
                autotext.set_size(8)
                autotext.set_weight('bold')
            
            for text in texts:
                text.set_size(9)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            plot1.axis('equal')
        
        # Common code for all graph types to display the figure
        # Create the Tkinter canvas containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=graph_container)
        canvas.draw()
        
        # Place the canvas in the frame with proper padding
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.get_tk_widget().configure(bg='#dcdcdc')
        
        # Add the Matplotlib toolbar
        toolbar_frame = tk.Frame(graph_container)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
    
    def get_fibonacci_time_data(self):
        """Helper method to get time data for each Fibonacci weight"""
        new1T = []
        new2T = []
        new3T = []
        new5T = []
        new7T = []
        new11T = []
        new13T = []
        
        for i in range(len(complexity)):
            if complexity[i] == "1":
                new1T.append(values[i])
            if complexity[i] == "2":
                new2T.append(values[i])
            if complexity[i] == "3":
                new3T.append(values[i])
            if complexity[i] == "5":
                new5T.append(values[i])
            if complexity[i] == "7":
                new7T.append(values[i])
            if complexity[i] == "11":
                new11T.append(values[i])
            if complexity[i] == "13":
                new13T.append(values[i])
                
        return new1T, new2T, new3T, new5T, new7T, new11T, new13T
        
    def get_total_time_by_fibonacci(self):
        """Calculate total time in seconds for each Fibonacci weight"""
        time_by_weight = {weight: 0 for weight in self.fibonacci}
        
        for i in range(len(complexity)):
            if complexity[i] in self.fibonacci:
                # Convert time string to seconds
                h, m, s = map(int, values[i].split(':'))
                seconds = h * 3600 + m * 60 + s
                time_by_weight[complexity[i]] += seconds
                
        return time_by_weight
        
    def get_total_time_by_tshirt(self):
        """Calculate total time in seconds for each T-shirt size weight"""
        time_by_weight = {size: 0 for size in self.tshirt_sizes}
        
        for i in range(len(complexity)):
            if complexity[i] in self.tshirt_sizes:
                # Convert time string to seconds
                h, m, s = map(int, values[i].split(':'))
                seconds = h * 3600 + m * 60 + s
                time_by_weight[complexity[i]] += seconds
                
        return time_by_weight

    # Convert time strings into total seconds
    def time_to_seconds(self,time_str):
        if not time_str or time_str == []:
            return 0
        else:
            h, m, s = map(int, time_str.split(':'))
            return h * 3600 + m * 60 + s


    def total_Time(self, times):
    
        if not times or times == []:
            return "00:00:00"
        
        total_h = 0
        total_m = 0
        total_s = 0
        
        for time in times:
            h, m, s = map(int, time.split(':'))
            total_h += h
            total_m += m
            total_s += s
        
        # Convert seconds to minutes and hours
        total_m += total_s // 60
        total_s %= 60
        
        # Convert minutes to hours
        total_h += total_m // 60
        total_m %= 60
        
        # Format with leading zeros
        total = f"{total_h:02d}:{total_m:02d}:{total_s:02d}"
        return total
    
    def update_total_time(self):
        self.load_data()
        total = self.total_Time(values)
        self.total_time_value.configure(text=total)


    def update_values(self, event=None):
        # Reload data 
        self.load_data()
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
            time_total,max,min,avg = self.update_time_comp()
            
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
        if avg_h == 0 or avg_h <= 9:
            avg_h = "0" + str(avg_h)
        if avg_m == 0 or avg_m <= 9:
            avg_m = "0" + str(avg_m)
        if avg_s == 0 or avg_s <= 9:
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

    def load_data(self):
        # DATABASE SECTION ####################################################
        conn = sqlite3.connect(path)
        c = conn.cursor()

        try:
            # --- Fetch task_time values ---
            c.execute("SELECT task_time FROM CompletedTasks")
            times = c.fetchall()
            global values
            values = [time[0] for time in times]

            # --- Fetch task_weight values ---
            c.execute("SELECT task_weight FROM CompletedTasks")
            comps = c.fetchall()
            global complexity
            complexity = [comp[0] for comp in comps]

            # --- Update the completed_tasks_list Treeview ---
            if hasattr(self, 'completed_tasks_list'):
                # Clear existing data in Treeview
                for record in self.completed_tasks_list.get_children():
                    self.completed_tasks_list.delete(record)

                # Fetch full data from CompletedTasks table
                c.execute("SELECT * FROM CompletedTasks ORDER BY completion_date DESC")
                completed_data = c.fetchall()

                # Insert data into Treeview
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
                        record[8],  # task_weight_type
                        record[9],  # task_description
                    ), tags=tags)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", "Failed to load data from CompletedTasks.")
        finally:
            conn.commit()
            conn.close()
        # END OF DATABASE SECTION ##############################################


            