from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
import csv
from tkinter import messagebox

background_color = "#A9A9A9"
green_btn_color = "#b2fba5"
org_btn_color = "#e99e56"

class TagsDB(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #DATABASE SECTION ############################################

        # Create or Connect to database
        
        conn = sqlite3.connect("tags.db")

        # Create a cursor instnace
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT,
            description TEXT
            )
        """)

        # Commit changes
        conn.commit()

        # Close connection to database
        conn.close()

        def query_database():
            # Create or Connect to the database
            conn = sqlite3.connect('tags.db')

            # Create a cursor instance
            c = conn.cursor()

            c.execute("SELECT rowid, * FROM tags")  # Fetch rowid as the first column
            tags = c.fetchall()

            # Add data to the screen
            global count
            count = 0

            for tag in tags:
                if count % 2 == 0:
                    # For even rows (0, 2, 4, ...) apply 'evenrow' tag
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('evenrow',""))
                else:
                    # For odd rows (1, 3, 5, ...) apply 'oddrow' tag
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('oddrow',""))
                
                # Increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close connection to the database
            conn.close()

        #END OF DATABASE SECTION #################################################


        # Set the main window 
        self.configure(bg= background_color)

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=14, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=10, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }

        # Style configurations
        style = ttk.Style(self)
        style.theme_use("alt")  
        style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        style.configure('TLabel', background='#d3d3d3', font=("SF Pro Text", 10))  
        style.configure('TButton', background= background_color, font=("SF Pro Text", 10))

        # Create a Treeview Frame
        tree_frame = tk.Frame(self, bg= background_color)
        tree_frame.grid(row=1, column=0, sticky="nsew")

        # Change color when a item is selected
        style.map("Treeview",
        background = [('selected', "347083")])

        style.configure("Treeview",
        background = "black",
        foreground = "black",
        rowheight = 25,
        fieldbackground = "#d3d3d3",
        bd = "black")


        # Ensure that tree_frame grid is configured properly
        tree_frame.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        tree_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.grid(row = 1, column = 1, sticky = "ns")

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",style="Treeview")
        my_tree.grid(row=1, column=0, sticky="nsew")

        # Configure the different rows for color
        my_tree.tag_configure('oddrow', background=  "#A9A9A9", foreground= "black")
        my_tree.tag_configure('evenrow', background= "#d3d3d3", foreground= "black")

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Name", "Description")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Name", anchor=W, width=80)
        my_tree.column("Description", anchor=W, width=240)
        my_tree.column("ID", anchor=W, width=20)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Name", text="Name", anchor=W)
        my_tree.heading("Description", text="Description", anchor=W)
        
        
        data_frame = tk.Frame(self,background=background_color)
        data_frame.grid(row=2, column=0, sticky="w")

     
        # ID Label
        id_label = ttk.Label(data_frame, text="ID: ", font=("SF Pro Text", 10, "bold"), background=background_color)
        id_label.grid(row=0, column=0, pady=1, sticky="w")

        # Change the ID entry to a Label to hold the ID (non-editable)
        id_display = ttk.Label(data_frame, font=("SF Pro Text", 10, "bold"), background=background_color)
        id_display.grid(row=0, column=0, padx=20, pady=3, sticky="w")

        # Tag Name Label & Entry
        n_label = ttk.Label(data_frame, text="Tag Name", font=("SF Pro Text", 10, "bold"),background=background_color)
        n_label.grid(row=3, column=0, padx=1, pady=5, sticky="w")
        n_entry = tk.Entry(data_frame, font=("SF Pro Text", 10), bg="#d3d3d3")
        n_entry.grid(row=4, column=0, padx=1, pady=1, sticky="w")

        # Description Label & Textbox
        desc_label = Label(data_frame, text="Description", font=("SF Pro Text", 10, "bold"),background=background_color)
        desc_label.grid(row=5, column=0, padx=1, pady=5, sticky="w")
        desc_text = Text(data_frame, font=("SF Pro Text", 12), height=5, width=40, background="#d3d3d3")
        desc_text.grid(row=6, column=0, padx=1, pady=1, sticky="w")

        # START OF FUNCTION SECTION ##############################################

        # Clear entry boxes
        def clear_Tag():
            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
        
        # Select Record
        def select_tag(event):
            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
            id_display.configure(text="")

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')

            # Populate entry boxes
            id_display.configure(text=values[0])  # Insert ID
            n_entry.insert(0, values[1])  # Insert name
            desc_text.insert("1.0", values[2])  # Insert description



        # Remove Tag
        def del_Tag():
            # Get the selected item from the Treeview
            selected = my_tree.selection()[0]
            my_tree.delete(selected)

            # Get the ID from the label (this will hold the ID for the selected tag)
            tag_id = id_display.cget("text")

            if tag_id:  # Ensure that the ID exists
                # Connecting to the database and creating a cursor
                conn = sqlite3.connect('tags.db')
                c = conn.cursor()

                # Delete the tag from the database using a parameterized query
                c.execute("DELETE FROM tags WHERE rowid = ?", (tag_id,))

                conn.commit()
                conn.close()

                # Clear entry boxes
                n_entry.delete(0, END)
                desc_text.delete("1.0", END)
                id_display.configure(text="")
            

        # Remove all Tags
        def remove_all_Tags():
            # Add a little message box for fun
            response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")

            #Add logic for message box
            if response == 1:
                # Clear the Treeview
                for tag in my_tree.get_children():
                    my_tree.delete(tag)

                # Create a database or connect to one that exists
                conn = sqlite3.connect('tags.db')

                # Create a cursor instance
                c = conn.cursor()

                # Delete Everything From The Table
                c.execute("DROP TABLE tags")

                c.execute("""
                    CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_name TEXT,
                    description TEXT
                    )
                """)
                            


                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes if filled
                n_entry.delete(0, END)
                desc_text.delete("1.0", END)
                id_display.configure(text="")



                

        # Add Tag to db
        def add_Tag():
            #Create db connection
            conn = sqlite3.connect('tags.db')

            # Create cursor
            c = conn.cursor()

            c.execute("INSERT INTO tags (tag_name, description) VALUES (:name, :desc)",
              {
                'name': n_entry.get(),
                'desc': desc_text.get("1.0", "end-1c")
              })

            conn.commit()
            conn.close()

            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
            id_display.configure(text="")

            # Clear Treeview table
            my_tree.delete(*my_tree.get_children())

            # Query Data base to add data
            query_database()


        # Update Tag
        def update_Tag():
            # Grab the tag number
            selected = my_tree.focus()

            # Update tag in treeview
            my_tree.item(selected, text="", values=(id_display.cget("text"), n_entry.get(), desc_text.get("1.0", "end-1c")))

            # Update the database
            conn = sqlite3.connect('tags.db')
            c = conn.cursor()

            c.execute("""UPDATE tags SET
                tag_name = :name,
                description = :desc
                WHERE rowid = :id""",
                {
                    'name': n_entry.get(),
                    'desc': desc_text.get("1.0", "end-1c"),
                    'id': id_display.cget("text"),
                }
            )

            conn.commit()
            conn.close()

            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
            id_display.configure(text="")


        def search_Tag(event):

            #Getting the name they entered
            lookup = search_entry.get()

            # Create or Connect to the database
            conn = sqlite3.connect('tags.db')

            # Create a cursor instance
            c = conn.cursor()

            # Clear the Treeview
            for tag in my_tree.get_children():
                my_tree.delete(tag)

            if lookup == "":

                c.execute("SELECT rowid, * FROM tags")  # Fetch all rows
            else:
                c.execute("SELECT rowid, * FROM tags WHERE tag_name like ?", (f"%{lookup}%",)) 
                
            tags = c.fetchall()
            

            # Add data to the screen
            global count
            count = 0

            for tag in tags:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('evenrow',""))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('oddrow',""))

                # Increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close connection to the database
            conn.close()
            



        def import_Tags():
            global data
            # Ask user for the file
            file_path = tk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

            # If file has been selected cont
            if file_path:
                # Open file and read from file
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    csv_reader = csv.reader(file)
                    data = list(csv_reader)

                    # Check if the first row is a header (by comparing column names)
                    if data:
                        header = data[0]
                        expected_header = ["Tag Name", "Description"]

                        # If the first row matches the header, remove it
                        if header == expected_header:
                            data = data[1:]
            
            # Connect to the SQLite database
            conn = sqlite3.connect('tags.db')
            c = conn.cursor()

            # Insert data into the table
            c.executemany("INSERT INTO tags (tag_name, description) VALUES (?, ?)", data)

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            query_database()


        def export_Tags():
            # Connect to the database
            conn = sqlite3.connect('tags.db')
            c = conn.cursor()

            # Fetch all tags
            c.execute("SELECT tag_name, description FROM tags")
            tags = c.fetchall()

            # Ask user where to save the file
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

            if file_path:  # Only proceed if the user selected a file path
                # Open the CSV file for writing
                with open(file_path, "w", newline='', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)

                    # Write the header
                    csv_writer.writerow(["Tag Name", "Description"])

                    # Write data rows
                    for tag in tags:
                        csv_writer.writerow(tag)

                # Close the database connection
                conn.close()
            


                    
        #END OF FUNCTION SECTION ########################################

        # Search Bar

        # Frame for search bar
        search_frame = tk.Frame(self, bg= background_color)
        search_frame.grid(row=0, column=0, padx=1, pady=1, sticky="ew")
        
        # Search bar label
        search_label = Label(search_frame, text="Search by Tag Name:", font=("SF Pro Text", 10, "bold"), background=background_color)
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Entry for search bar for user to input search
        search_entry = tk.Entry(search_frame, font=("SF Pro Text", 10), bg="#d3d3d3")
        search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        search_entry.bind("<KeyRelease>", search_Tag)


        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_tag)

       # Frame for the buttons
        button_frame = tk.Frame(self, background=background_color)
        button_frame.grid(row=7, column=0, pady=1, padx=1, sticky="w")

        # Configure columns of the button_frame to distribute the space evenly
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)
        button_frame.grid_columnconfigure(4, weight=1)
        button_frame.grid_columnconfigure(5, weight=1)
        button_frame.grid_columnconfigure(6, weight=1)

        # Add Tag Button
        add_btn = tk.Button(button_frame, text=" Add Tag ",  
                            bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10), command=add_Tag,
                            activebackground="#A8F0A8", activeforeground="#000000")
        add_btn.grid(row=0, column=0, pady=2, padx=(0, 3), sticky="w")

        # Update Button
        update_btn = tk.Button(button_frame, text="Update Tag", command=update_Tag,
                            bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                            activebackground="#A8F0A8", activeforeground="#000000")
        update_btn.grid(row=0, column=1, pady=2, padx=3, sticky="ew")

        # Clear Task Button
        clc_btn = tk.Button(button_frame, text="Clear Task", command=clear_Tag,
                            bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                            activebackground="#A8F0A8", activeforeground="#000000")
        clc_btn.grid(row=0, column=2, pady=2, padx=3, sticky="ew")


        # Delete Tag Button
        del_btn = tk.Button(button_frame, text="Delete Tag", command=del_Tag,
                            bg=org_btn_color, fg="#000000", font=("SF Pro Text", 10),
                            activebackground="#FFB347", activeforeground="#000000")
        del_btn.grid(row=0, column=5, pady=2, padx=(100, 3), sticky="ew")

        # Remove All Button
        remove_all_btn = tk.Button(button_frame, text="Remove All", command=remove_all_Tags,
                                    bg=org_btn_color, fg="#000000", font=("SF Pro Text", 10),
                                    activebackground="#FFB347", activeforeground="#000000")
        remove_all_btn.grid(row=0, column=6, pady=2, padx=3, sticky="ew")


        # Import Button
        import_btn = tk.Button(search_frame, text=" Import ", command=import_Tags,
                                    bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                                    activebackground="#A8F0A8", activeforeground="#000000")
        import_btn.grid(row=0, column=2, pady=3, padx=(85,3), sticky="w")

        # Import Button
        export_btn = tk.Button(search_frame, text=" Export ", command=export_Tags,
                                    bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                                    activebackground="#A8F0A8", activeforeground="#000000")
        export_btn.grid(row=0, column=2, pady=3, padx=(145,3), sticky="e")

        # Run to pull data from database on start
        query_database()
        
